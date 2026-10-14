"""
objective_reduction.py
======================
Simulates Stage 5 of the Transduction Chain:
- The Penrose-Hameroff Objective Reduction Threshold: tau ~ hbar / E_G.
- Gravitational Self-Energy (E_G) calculation driven by conscious Focus Density.
- The Actor Operator (A_hat -> a_k): Forces collapse of dimensionless superposition into singular physical eigenstate.
- The Projection Tensor (P_hat): Shutter mechanism operating near Planck time, projecting into 3D spacetime actuation.
"""

import math
import numpy as np
from typing import Optional, Tuple, Dict, Any


class ObjectiveReductionSystem:
    """
    Evaluates gravitational self-energy E_G, monitors the Objective Reduction
    Threshold tau ~ hbar / E_G, executes the Actor Operator A_hat, and applies
    the Projection Tensor P_hat.
    """

    def __init__(self, config: dict):
        self.config = config
        cfg_or = config.get("objective_reduction", {})
        self.hbar = float(cfg_or.get("hbar_simulation", 1.0))
        self.g_const = float(cfg_or.get("gravitational_constant_g", 6.674e-11))
        self.eg_scale = float(cfg_or.get("eg_scaling_constant", 1.85))
        self.time_scale = float(cfg_or.get("time_to_collapse_scaling", 2.2))
        self.shutter_duration = float(cfg_or.get("optical_shutter_planck_duration_s", 0.08))

        # Dynamic metrics
        self.accumulated_or_integral: float = 0.0
        self.gravitational_self_energy: float = 0.0
        self.time_to_collapse_tau: float = 999.0
        self.threshold_breached: bool = False
        self.collapse_timestamp: Optional[float] = None
        self.shutter_active: bool = False
        self.shutter_timer: float = 0.0

        # Projection Tensor matrices
        cfg_pt = config.get("projection_tensor", {})
        self.cartesian_gain = float(cfg_pt.get("cartesian_projection_gain", 1.0))
        self.torque_gain = float(cfg_pt.get("torque_projection_gain", 120.0))

    def compute_gravitational_self_energy(self, focus_density: float, frohlich_factor: float) -> float:
        """
        Calculates E_G, the mass/energy displacement of the thought wave superposition:
        E_G = G * \iint (\Delta\rho(x) \Delta\rho(x')) / |x - x'| d^3x d^3x'
        Deliberate focus density drives E_G upward until it breaches the threshold.
        """
        # E_G scales quadratically with focus density and coherent biological coupling
        eg = self.eg_scale * (focus_density ** 2.2) * (0.2 + 0.8 * frohlich_factor)
        self.gravitational_self_energy = float(eg)

        if eg > 1e-6:
            # tau ~ hbar / E_G
            self.time_to_collapse_tau = (self.hbar / eg) * self.time_scale
        else:
            self.time_to_collapse_tau = 999.0

        return self.gravitational_self_energy

    def update(
        self,
        dt: float,
        focus_density: float,
        frohlich_factor: float,
        anesthesia_active: bool,
    ) -> bool:
        """
        Evolves the Objective Reduction state through time dt.
        Returns True if Objective Reduction was breached and Actor Operator fired THIS step.
        """
        # If optical shutter is active, advance shutter timer
        if self.shutter_active:
            self.shutter_timer += dt
            if self.shutter_timer >= self.shutter_duration:
                self.shutter_active = False

        if self.threshold_breached:
            return False

        # If anesthesia is active, the Actor Operator is biologically disabled
        if anesthesia_active:
            self.accumulated_or_integral = max(0.0, self.accumulated_or_integral - 0.5 * dt)
            return False

        # Compute current gravitational self-energy
        eg = self.compute_gravitational_self_energy(focus_density, frohlich_factor)

        # Accumulate tension toward Objective Reduction threshold:
        # Rate = 1.0 / tau = E_G / hbar
        collapse_rate = eg / max(1e-6, self.hbar * self.time_scale)

        # Only accumulate if focus density is sufficiently deliberate (> 0.40)
        # Passing daydreams (low focus density) fail to cross the threshold
        if focus_density >= 0.40:
            self.accumulated_or_integral += collapse_rate * dt
        else:
            # Gentle sub-threshold relaxation
            self.accumulated_or_integral = max(0.0, self.accumulated_or_integral - 0.35 * dt)

        # Check threshold condition
        if self.accumulated_or_integral >= 1.0:
            self.threshold_breached = True
            self.shutter_active = True
            self.shutter_timer = 0.0
            return True

        return False

    def project_tensor(self, eigenstate_cartesian: np.ndarray) -> Dict[str, Any]:
        """
        The Projection Tensor (P_hat):
        Converts the collapsed Hilbert space eigenstate into physical 3D coordinates,
        end-effector target orientation, and articulation motor command vectors.
        """
        target_pos = eigenstate_cartesian * self.cartesian_gain

        # Determine target end-effector orientation (quaternion [w, x, y, z] pointing downward)
        target_quat = np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)

        # Compute preliminary joint targets using inverse kinematics approximation
        joint_targets = np.array([
            math.atan2(target_pos[1], target_pos[0]),  # Base rotation
            -0.6,                                       # Shoulder pitch
            0.0,                                        # Elbow roll
            -1.8,                                       # Elbow pitch
            0.0,                                        # Wrist roll
            1.2,                                        # Wrist pitch
            0.785,                                      # Wrist yaw
        ], dtype=np.float32)

        return {
            "target_position_3d": target_pos,
            "target_orientation_quat": target_quat,
            "joint_targets": joint_targets,
            "shutter_state": self.shutter_active,
            "collapse_tension": float(self.accumulated_or_integral),
        }

    def reset(self) -> None:
        """Resets the Objective Reduction accumulator."""
        self.accumulated_or_integral = 0.0
        self.threshold_breached = False
        self.collapse_timestamp = None
        self.shutter_active = False
        self.shutter_timer = 0.0
        self.gravitational_self_energy = 0.0
        self.time_to_collapse_tau = 999.0
