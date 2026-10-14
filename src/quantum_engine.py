"""
quantum_engine.py
=================
Simulates the foundational quantum mechanics of the Actor Hypothesis:
- Stage 1: The Actor Field (Universal background field of conscious potential)
- Stage 2: Conscious Entity (Localized excitation in Hilbert space)
- Stage 3: The Thought Wave (|Psi> = sum c_i |phi_i>) in Hilbert Space
- Thermodynamics of the Unacted (Dissipation & Residue Pathways)
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Optional


class Eigenstate:
    """Represents a potential physical action outcome |phi_i> in Hilbert Space."""

    def __init__(
        self,
        id_num: int,
        name: str,
        description: str,
        base_amplitude: float,
        phase_velocity: float,
        target_cartesian: List[float],
        target_color: List[float],
    ):
        self.id = id_num
        self.name = name
        self.description = description
        self.base_amplitude = float(base_amplitude)
        self.phase_velocity = float(phase_velocity)
        self.target_cartesian = np.array(target_cartesian, dtype=np.float32)
        self.target_color = np.array(target_color, dtype=np.float32)

        # Dynamic quantum amplitude (complex)
        self.amplitude = complex(base_amplitude, 0.0)
        self.phase = 0.0

    @property
    def probability(self) -> float:
        """Born rule probability: P_i = |c_i|^2."""
        return float(abs(self.amplitude) ** 2)


class QuantumThoughtWave:
    """
    Simulates the uncollapsed thought wave:
    |Psi> = sum_{i=1}^N c_i |phi_i>
    
    Exhibits cognitive wave-particle duality:
    - In unacted state: pure superposition, high entropy, zero 3D physical footprint.
    - Focus density D_f concentrates probability amplitudes towards the intended eigenstate.
    """

    def __init__(self, config: dict):
        self.config = config
        cfg_wave = config.get("thought_wave", {})
        self.eigenstates: List[Eigenstate] = []
        for state_cfg in cfg_wave.get("eigenstates", []):
            self.eigenstates.append(
                Eigenstate(
                    id_num=state_cfg["id"],
                    name=state_cfg["name"],
                    description=state_cfg["description"],
                    base_amplitude=state_cfg["base_amplitude"],
                    phase_velocity=state_cfg["phase_velocity"],
                    target_cartesian=state_cfg["target_cartesian"],
                    target_color=state_cfg["target_color"],
                )
            )

        self.num_states = len(self.eigenstates)
        self.focus_density = float(config.get("conscious_entity", {}).get("default_focus_density", 0.85))
        self.target_focus_id: int = 0  # Intended eigenstate under deliberate focus

        # Pathway tracking
        self.dissipation_energy: float = 0.0
        self.spacetime_residue_integral: float = 0.0
        self.is_collapsed: bool = False
        self.collapsed_state_idx: Optional[int] = None

        # Actor Field background metrics
        self.actor_field_potential: float = 1.0
        self.vacuum_energy: float = float(config.get("actor_field", {}).get("vacuum_energy_density", 1.25e-9))
        self.field_fluctuation_phase: float = 0.0

        self.normalize_state()

    def normalize_state(self) -> None:
        """Enforces quantum state normalization: sum |c_i|^2 = 1.0."""
        total_prob = sum(s.probability for s in self.eigenstates)
        if total_prob > 1e-12:
            norm_factor = 1.0 / math.sqrt(total_prob)
            for s in self.eigenstates:
                s.amplitude *= norm_factor

    def set_focus(self, focus_density: float, target_state_id: Optional[int] = None) -> None:
        """
        Updates the focus density D_f in [0.0, 1.0] and optionally the target state.
        Higher focus density concentrates the probability amplitude into target_state_id.
        """
        self.focus_density = float(np.clip(focus_density, 0.0, 1.0))
        if target_state_id is not None and 0 <= target_state_id < self.num_states:
            self.target_focus_id = target_state_id

    def update(self, dt: float) -> None:
        """
        Evolves the quantum thought wave through time dt:
        - Phase rotation: theta_i += omega_i * dt
        - Amplitude steering by deliberate focus density D_f
        - Natural dissipation if focus density is low
        """
        if self.is_collapsed:
            return

        # 1. Background Actor Field fluctuations
        self.field_fluctuation_phase += 2.4 * dt
        self.actor_field_potential = 1.0 + 0.08 * math.sin(self.field_fluctuation_phase)

        # 2. Focus amplitude redistribution
        # Target state receives weight proportional to focus density
        weights = np.zeros(self.num_states, dtype=np.float32)
        for i, state in enumerate(self.eigenstates):
            base_w = state.base_amplitude ** 2
            if i == self.target_focus_id:
                # Strong focus concentrates probability amplitude
                w = base_w + (1.0 - base_w) * (self.focus_density ** 1.8)
            else:
                # Dispersed states are attenuated by high focus density
                w = base_w * (1.0 - 0.9 * self.focus_density)
            weights[i] = max(1e-4, w)

        weights /= np.sum(weights)

        # 3. Phase evolution & complex amplitude assignment
        for i, state in enumerate(self.eigenstates):
            state.phase += state.phase_velocity * dt
            target_mag = math.sqrt(weights[i])
            state.amplitude = target_mag * (math.cos(state.phase) + 1j * math.sin(state.phase))

        self.normalize_state()

        # 4. Pathway 2: Accumulate Spacetime Residue if in unacted superposition
        residue_rate = float(self.config.get("spacetime_geometry", {}).get("residue_accumulation_rate", 0.08))
        self.spacetime_residue_integral += residue_rate * (self.focus_density * (1.0 - self.focus_density)) * dt

    def dissipate_to_actor_field(self, dt: float) -> float:
        """
        Pathway 1: Dissipation.
        For unacted thoughts that never cross the threshold, the energy gently returns
        to the universal Actor Field: <Psi_Actor | Psi_Creator> != 0.
        """
        if self.is_collapsed:
            return 0.0

        decay_rate = 0.65 * (1.0 - self.focus_density + 0.1)
        decay_factor = math.exp(-decay_rate * dt)
        dissipated_amount = (1.0 - decay_factor) * sum(s.probability for s in self.eigenstates)
        self.dissipation_energy += dissipated_amount

        for s in self.eigenstates:
            s.amplitude *= decay_factor

        self.normalize_state()
        return dissipated_amount

    def compute_entropy(self) -> float:
        """
        Computes the Shannon/von Neumann informational entropy:
        S(Psi) = -sum P_i * log2(P_i)
        High entropy in superposition; collapses to 0.0 upon singular eigenstate selection.
        """
        if self.is_collapsed:
            return 0.0
        entropy = 0.0
        for s in self.eigenstates:
            p = s.probability
            if p > 1e-9:
                entropy -= p * math.log2(p)
        return float(entropy)

    def collapse(self, chosen_idx: Optional[int] = None) -> Tuple[int, Eigenstate]:
        """
        Executes the Actor Operator collapse:
        Forces the dimensionless thought wave to collapse into a singular eigenstate of definitive choice.
        Probability of collapsing into state i is |c_i|^2.
        """
        if self.is_collapsed and self.collapsed_state_idx is not None:
            return self.collapsed_state_idx, self.eigenstates[self.collapsed_state_idx]

        probs = [s.probability for s in self.eigenstates]
        total_p = sum(probs)
        probs = [p / total_p for p in probs]

        if chosen_idx is None:
            chosen_idx = int(np.random.choice(len(self.eigenstates), p=probs))

        self.is_collapsed = True
        self.collapsed_state_idx = chosen_idx

        # Project state vector onto singular collapsed eigenstate: |Psi> -> |phi_k>
        for i, s in enumerate(self.eigenstates):
            if i == chosen_idx:
                s.amplitude = complex(1.0, 0.0)
            else:
                s.amplitude = complex(0.0, 0.0)

        return chosen_idx, self.eigenstates[chosen_idx]

    def reset(self) -> None:
        """Resets the quantum state to uncollapsed initial superposition."""
        self.is_collapsed = False
        self.collapsed_state_idx = None
        self.dissipation_energy = 0.0
        self.spacetime_residue_integral = 0.0
        for s in self.eigenstates:
            s.amplitude = complex(s.base_amplitude, 0.0)
            s.phase = 0.0
        self.normalize_state()

    def sample_wave_profile(self, num_points: int = 40, x_span: float = 1.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generates 3D coordinates representing the continuous thought wave packet
        for volumetric or spline visualization in Isaac Sim USD.
        """
        xs = np.linspace(0.0, x_span, num_points, dtype=np.float32)
        ys = np.zeros(num_points, dtype=np.float32)
        zs = np.zeros(num_points, dtype=np.float32)

        for i, state in enumerate(self.eigenstates):
            p = state.probability
            k_wave = 12.0 + i * 3.5
            amp = math.sqrt(p) * 0.12
            ys += amp * np.sin(k_wave * xs + state.phase)
            zs += amp * np.cos(k_wave * xs + state.phase)

        # Apply focus density envelope
        envelope = np.sin(np.pi * xs / x_span)
        ys *= envelope
        zs *= envelope
        return xs, ys, zs
