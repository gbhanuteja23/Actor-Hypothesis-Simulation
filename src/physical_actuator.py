"""
physical_actuator.py
====================
Simulates Stage 6 of the Transduction Chain:
- Tangible Physical Action in 4D Spacetime.
- Robotic manipulator articulation controller in Isaac Sim PhysX.
- Physical mass/energy transfer, contact forces, work done W = \int F . dx.
- Combating local entropic decay: measurable entropy drop Delta S_phys < 0.
"""

import math
import numpy as np
from typing import Dict, Any, Optional, Tuple


class PhysicalActuatorController:
    """
    Translates Projection Tensor outputs into tangible physical robotic motion.
    Computes kinematics, smooth trajectory interpolation, contact physics,
    mechanical work, and physical entropy reduction.
    """

    def __init__(self, config: dict):
        self.config = config
        self.dt = float(config.get("physics", {}).get("physics_dt", 0.01666667))
        self.robot_base = np.array(config.get("physical_world", {}).get("robot_base_position", [0.0, 0.0, 0.0]), dtype=np.float32)

        # 7-DOF joint configuration (current and target)
        self.num_joints = 7
        self.current_joint_positions = np.array([0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785], dtype=np.float32)
        self.target_joint_positions = np.copy(self.current_joint_positions)
        self.joint_velocities = np.zeros(self.num_joints, dtype=np.float32)

        # End effector position and trajectory
        self.current_ee_pos = np.array([0.3, 0.0, 0.5], dtype=np.float32)
        self.target_ee_pos = np.array([0.3, 0.0, 0.5], dtype=np.float32)
        self.home_ee_pos = np.array([0.3, 0.0, 0.5], dtype=np.float32)

        # Motion status
        self.is_moving: bool = False
        self.motion_progress: float = 1.0
        self.motion_duration: float = 1.8
        self.start_ee_pos = np.copy(self.current_ee_pos)

        # Physical metrics
        self.contact_force_magnitude: float = 0.0
        self.cumulative_work_joules: float = 0.0
        self.entropy_reduction_rate: float = 0.0
        self.active_action_id: Optional[int] = None

        # Gripper state (0.0 = open, 1.0 = closed)
        self.gripper_state: float = 0.0
        self.target_gripper_state: float = 0.0

        # Physical objects displaced in the scene
        self.object_displacements = {
            0: 0.0,  # Cylinder lifted/grasped
            1: 0.0,  # Block pushed distance
            2: 0.0,  # Switch depressed
        }

    def command_action(self, action_id: int, projection_data: Dict[str, Any]) -> None:
        """
        Receives the collapsed eigenstate via the Projection Tensor and initiates
        physical movement toward the target coordinate.
        """
        self.active_action_id = action_id
        self.target_ee_pos = np.array(projection_data["target_position_3d"], dtype=np.float32)
        self.start_ee_pos = np.copy(self.current_ee_pos)
        self.motion_progress = 0.0
        self.is_moving = True

        if action_id == 0:
            # Grasp cylinder
            self.target_gripper_state = 1.0
            self.motion_duration = 1.8
        elif action_id == 1:
            # Push block
            self.target_gripper_state = 0.0
            self.motion_duration = 2.2
        elif action_id == 2:
            # Toggle switch
            self.target_gripper_state = 0.5
            self.motion_duration = 1.5
        else:
            # Idle / Daydream
            self.target_gripper_state = 0.0
            self.target_ee_pos = np.copy(self.home_ee_pos)
            self.motion_duration = 1.2

    def update(self, dt: float) -> Dict[str, Any]:
        """
        Advances the robot kinematics and physics integration:
        - Minimum-jerk trajectory interpolation.
        - Computes dynamic torque, mechanical work W = F * dx.
        - Computes entropy drop Delta S_phys < 0.
        """
        if self.is_moving:
            self.motion_progress = min(1.0, self.motion_progress + dt / max(1e-4, self.motion_duration))
            # Smooth minimum-jerk polynomial: s(t) = 10t^3 - 15t^4 + 6t^5
            tau = self.motion_progress
            s = 10.0 * (tau ** 3) - 15.0 * (tau ** 4) + 6.0 * (tau ** 5)

            # Interpolate end effector Cartesian position
            prev_pos = np.copy(self.current_ee_pos)
            self.current_ee_pos = self.start_ee_pos + s * (self.target_ee_pos - self.start_ee_pos)
            delta_dist = float(np.linalg.norm(self.current_ee_pos - prev_pos))

            # Interpolate gripper
            self.gripper_state += (self.target_gripper_state - self.gripper_state) * 0.1

            # Approximate joint angles based on end-effector coordinate
            dx = self.current_ee_pos[0]
            dy = self.current_ee_pos[1]
            dz = self.current_ee_pos[2]
            base_angle = math.atan2(dy, dx)
            reach = math.sqrt(dx * dx + dy * dy)

            self.current_joint_positions[0] = base_angle
            self.current_joint_positions[1] = -0.4 - 0.5 * (reach - 0.3)
            self.current_joint_positions[3] = -1.8 - 0.4 * (0.6 - dz)
            self.current_joint_positions[5] = 1.2 + 0.3 * (reach - 0.3)

            # Compute contact force when reaching near target object
            if self.motion_progress > 0.65 and self.active_action_id is not None:
                if self.active_action_id == 0:
                    # Grasping force
                    self.contact_force_magnitude = 12.5 * math.sin(math.pi * (self.motion_progress - 0.65) / 0.35)
                    self.object_displacements[0] = min(0.08, self.object_displacements[0] + 0.05 * dt)
                elif self.active_action_id == 1:
                    # Pushing force
                    self.contact_force_magnitude = 28.0 * (self.motion_progress - 0.65) / 0.35
                    self.object_displacements[1] = min(0.15, self.object_displacements[1] + 0.08 * dt)
                elif self.active_action_id == 2:
                    # Depressing switch
                    self.contact_force_magnitude = 8.0 * (self.motion_progress - 0.65) / 0.35
                    self.object_displacements[2] = min(0.02, self.object_displacements[2] + 0.02 * dt)

                # Physical mechanical work: W = F * delta_x
                step_work = self.contact_force_magnitude * delta_dist
                self.cumulative_work_joules += step_work

                # Thermodynamic entropy reduction rate: dS/dt = - (d W / dt) / T_room
                t_room = 298.15  # Kelvin
                self.entropy_reduction_rate = (self.contact_force_magnitude * (delta_dist / max(1e-4, dt))) / t_room
            else:
                self.contact_force_magnitude = 0.0
                self.entropy_reduction_rate = 0.0

            if self.motion_progress >= 1.0:
                self.is_moving = False

        return {
            "ee_position": self.current_ee_pos,
            "joint_positions": self.current_joint_positions,
            "gripper_state": self.gripper_state,
            "contact_force_N": float(self.contact_force_magnitude),
            "cumulative_work_J": float(self.cumulative_work_joules),
            "entropy_reduction_rate_W_per_K": float(self.entropy_reduction_rate),
            "object_displacements": self.object_displacements,
            "is_moving": self.is_moving,
        }

    def reset(self) -> None:
        """Resets the actuator to home configuration."""
        self.current_joint_positions = np.array([0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785], dtype=np.float32)
        self.current_ee_pos = np.copy(self.home_ee_pos)
        self.target_ee_pos = np.copy(self.home_ee_pos)
        self.is_moving = False
        self.motion_progress = 1.0
        self.contact_force_magnitude = 0.0
        self.cumulative_work_joules = 0.0
        self.entropy_reduction_rate = 0.0
        self.active_action_id = None
        self.gripper_state = 0.0
        for k in self.object_displacements:
            self.object_displacements[k] = 0.0
