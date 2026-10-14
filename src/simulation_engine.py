"""
simulation_engine.py
====================
The master simulation engine for the Actor Hypothesis in NVIDIA Isaac Sim 5.0.1+:
Integrates the complete 6-stage Transduction Chain:
  1. Actor Field
  2. Conscious Entity
  3. Thought Wave Superposition (|Psi> = sum c_i |phi_i>)
  4. Microtubule Biological Transducer (Orch-OR)
  5. Objective Reduction Threshold & Actor Operator (A_hat) & Projection Tensor (P_hat)
  6. Tangible Physical Action in 4D Spacetime & Thermodynamic Entropy Reduction

Also manages the Thermodynamics of the Unacted (Dissipation & Residue)
and Empirical Falsifiability (Anesthesia Disruption).
"""

import os
import json
import time
import numpy as np
from typing import Dict, Any, Optional

from pxr import Usd, UsdGeom, Gf, Sdf

from src.quantum_engine import QuantumThoughtWave
from src.microtubule_transducer import MicrotubuleTransducer
from src.objective_reduction import ObjectiveReductionSystem
from src.spacetime_geometry import SpacetimeCurvatureGrid
from src.physical_actuator import PhysicalActuatorController
from src.usd_scene_generator import USDSceneBuilder
from src.telemetry_overlay import TelemetryReporter


class ActorHypothesisSimulation:
    """Master simulation controller orchestrating the entire Actor Hypothesis."""

    def __init__(self, kit_app, config_path: str, mode: str = "COLLAPSE_ACTION"):
        self.kit = kit_app
        self.mode = mode.upper()

        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.dt = float(self.config.get("physics", {}).get("physics_dt", 0.01666667))
        self.sim_time: float = 0.0

        # Retrieve Isaac Sim USD stage
        self.stage = self.kit.context.get_stage()

        # Build complete 3D scene in USD
        print("[ActorSimulation] Building OpenUSD Transduction Scene...")
        self.usd_builder = USDSceneBuilder(self.stage, self.config)
        self.usd_builder.build_all()
        print("[ActorSimulation] OpenUSD Scene built successfully!")

        # Initialize the 6 stages of the Transduction Chain
        self.quantum_wave = QuantumThoughtWave(self.config)
        self.microtubules = MicrotubuleTransducer(self.config)
        self.objective_reduction = ObjectiveReductionSystem(self.config)
        self.spacetime_grid = SpacetimeCurvatureGrid(self.config)
        self.actuator = PhysicalActuatorController(self.config)
        self.telemetry = TelemetryReporter()

        # Configure initial mode parameters
        self._configure_scenario_mode()

    def _configure_scenario_mode(self) -> None:
        """Sets up the initial state depending on the requested scenario mode."""
        print(f"[ActorSimulation] Initializing Scenario Mode: {self.mode}")

        if self.mode == "COLLAPSE_ACTION":
            # High focus density drives E_G upward to breach Objective Reduction
            self.quantum_wave.set_focus(focus_density=0.92, target_state_id=0)
            self.microtubules.set_anesthesia(enabled=False)

        elif self.mode == "DAYDREAM_DISSIPATION":
            # Low focus density: sub-threshold unacted thought returning to Actor Field
            self.quantum_wave.set_focus(focus_density=0.18, target_state_id=3)
            self.microtubules.set_anesthesia(enabled=False)

        elif self.mode == "SPACETIME_RESIDUE":
            # Moderate focus without crossing threshold: leaves cumulative gravitational residue
            self.quantum_wave.set_focus(focus_density=0.48, target_state_id=1)
            self.microtubules.set_anesthesia(enabled=False)

        elif self.mode == "ANESTHESIA_DISRUPTION":
            # High focus density, but Anesthesia is active: halts Actor Operator
            self.quantum_wave.set_focus(focus_density=0.95, target_state_id=0)
            self.microtubules.set_anesthesia(enabled=True)

        elif self.mode == "INTERACTIVE_CYCLE":
            self.quantum_wave.set_focus(focus_density=0.80, target_state_id=0)
            self.microtubules.set_anesthesia(enabled=False)

    def step(self) -> Dict[str, Any]:
        """Advances the entire simulation pipeline by one timestep dt."""
        self.sim_time += self.dt

        # Stage 1 & 2: Conscious Entity and Actor Field updates
        focus = self.quantum_wave.focus_density
        anesthesia_active = self.microtubules.anesthesia_enabled

        # Stage 3: Quantum Thought Wave evolution
        self.quantum_wave.update(self.dt)
        entropy = self.quantum_wave.compute_entropy()

        # Handle unacted pathways
        is_daydream = (self.mode in ["DAYDREAM_DISSIPATION", "SPACETIME_RESIDUE"])
        if is_daydream and not self.quantum_wave.is_collapsed:
            if self.mode == "DAYDREAM_DISSIPATION":
                self.quantum_wave.dissipate_to_actor_field(self.dt)

        # Stage 4: Microtubule Biological Transducer
        self.microtubules.update(self.dt, focus)
        mt_status = self.microtubules.get_subunits_summary()
        frohlich = mt_status["frohlich_condensation"]

        # Stage 5: Objective Reduction & Actor Operator & Projection Tensor
        breached_now = self.objective_reduction.update(
            self.dt,
            focus_density=focus,
            frohlich_factor=frohlich,
            anesthesia_active=anesthesia_active,
        )

        flash_intensity = 0.0
        if breached_now:
            # Objective Reduction Threshold crossed!
            # Actor Operator fires: dimensionless thought collapses into singular physical eigenstate
            chosen_idx, chosen_eigenstate = self.quantum_wave.collapse()
            flash_intensity = 15000.0  # Intense photonic/gravitational collapse flash
            print(f"\n[*** OBJECTIVE REDUCTION TRIGGERED ***] Breach of threshold tau ~ hbar/EG at t = {self.sim_time:.3f} s!")
            print(f"   Actor Operator (A_hat) collapsed state into: '{chosen_eigenstate.name}'")

            # Apply Projection Tensor (P_hat): project collapsed state into 3D spacetime kinematics
            projection = self.objective_reduction.project_tensor(chosen_eigenstate.target_cartesian)
            print(f"   Projection Tensor (P_hat) dispatched target 3D vector: {projection['target_position_3d']}")

            # Stage 6: Command physical actuator
            self.actuator.command_action(chosen_idx, projection)

        elif self.objective_reduction.shutter_active:
            # Fading shutter flash
            flash_intensity = 6000.0 * (1.0 - self.objective_reduction.shutter_timer / self.objective_reduction.shutter_duration)

        # Stage 6: Physical Actuator integration
        actuator_state = self.actuator.update(self.dt)

        # Spacetime Curvature Grid deformation
        current_target = None
        if self.quantum_wave.is_collapsed and self.quantum_wave.collapsed_state_idx is not None:
            current_target = self.quantum_wave.eigenstates[self.quantum_wave.collapsed_state_idx].target_cartesian

        Z_grid = self.spacetime_grid.update(
            self.dt,
            focus_density=focus,
            eg_energy=self.objective_reduction.gravitational_self_energy,
            is_collapsed=self.quantum_wave.is_collapsed,
            target_pos=current_target,
            is_unacted_daydream=(self.mode == "SPACETIME_RESIDUE"),
        )
        grid_pts = self.spacetime_grid.get_grid_points(Z_grid)

        # Update dynamic visual primitives in USD stage
        wave_xs, wave_ys, wave_zs = self.quantum_wave.sample_wave_profile()
        self.usd_builder.update_dynamic_visuals(
            wave_xs=wave_xs,
            wave_ys=wave_ys,
            wave_zs=wave_zs,
            grid_points=grid_pts,
            flash_intensity=flash_intensity,
            tubulin_dipoles=self.microtubules.get_lattice_dipoles(),
        )

        # Step Omniverse Kit application rendering & physics
        self.kit.update()

        # Telemetry package
        action_name = "Superposition (Uncollapsed)"
        if self.quantum_wave.is_collapsed and self.quantum_wave.collapsed_state_idx is not None:
            action_name = self.quantum_wave.eigenstates[self.quantum_wave.collapsed_state_idx].name

        state_summary = {
            "time_s": self.sim_time,
            "focus_density": focus,
            "entropy": entropy,
            "frohlich_condensation": frohlich,
            "coherence_time_s": mt_status["coherence_time_s"],
            "anesthesia_active": anesthesia_active,
            "eg_energy": self.objective_reduction.gravitational_self_energy,
            "tau_collapse_s": self.objective_reduction.time_to_collapse_tau,
            "collapse_tension": self.objective_reduction.accumulated_or_integral,
            "is_collapsed": self.quantum_wave.is_collapsed,
            "collapsed_state_idx": self.quantum_wave.collapsed_state_idx,
            "collapsed_action_name": action_name,
            "spacetime_residue": self.spacetime_grid.get_max_residue(),
            "dissipated_energy": self.quantum_wave.dissipation_energy,
            "contact_force_N": actuator_state["contact_force_N"],
            "work_joules": actuator_state["cumulative_work_J"],
            "entropy_reduction_rate": actuator_state["entropy_reduction_rate_W_per_K"],
        }

        # Periodic status dashboard logging
        self.telemetry.log_step(state_summary, frequency=45)
        return state_summary

    def run(self, max_seconds: float = 8.0) -> Dict[str, Any]:
        """Runs the simulation for max_seconds or until scenario completion."""
        steps = int(max_seconds / self.dt)
        last_state = {}
        for s in range(steps):
            last_state = self.step()
        return last_state
