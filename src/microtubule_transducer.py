"""
microtubule_transducer.py
=========================
Simulates Stage 4 of the Transduction Chain:
- Brain microtubules as biological quantum transducers (Orch-OR integration).
- 13-protofilament cylindrical tubulin dipole lattice.
- Fröhlich quantum condensation and quantum coherence scaling with focus density.
- Testable Vector 2: The Anesthesia Disruption mechanism severing the bridge.
"""

import math
import numpy as np
from typing import Tuple, List, Dict


class TubulinHeterodimer:
    """Represents an individual tubulin protein subunit in the microtubule lattice."""

    def __init__(self, filament_idx: int, ring_idx: int, position_3d: np.ndarray):
        self.filament_idx = filament_idx
        self.ring_idx = ring_idx
        self.position = position_3d  # [x, y, z] in local transducer coordinates
        self.dipole_moment = 0.0     # Normalized dipole state in [-1.0, 1.0]
        self.phase_offset = (filament_idx * 0.48) + (ring_idx * 0.25)
        self.quantum_coherence = 0.0


class MicrotubuleTransducer:
    """
    Biological Transducer modeling a 13-protofilament cylindrical microtubule lattice.
    Couples dimensionless thought waves to local spacetime geometry.
    """

    def __init__(self, config: dict):
        self.config = config
        cfg_mt = config.get("microtubules", {})
        self.protofilaments = int(cfg_mt.get("protofilaments", 13))
        self.subunits_per_filament = int(cfg_mt.get("subunits_per_filament", 20))
        self.radius = float(cfg_mt.get("cylinder_radius", 0.12))
        self.length = float(cfg_mt.get("cylinder_length", 1.2))
        self.base_position = np.array(cfg_mt.get("position", [-1.0, 0.0, 1.2]), dtype=np.float32)

        self.dipole_freq = float(cfg_mt.get("dipole_oscillation_freq", 12.5))
        self.base_coherence = float(cfg_mt.get("frohlich_coherence_base", 0.025))
        self.coherence_gain = float(cfg_mt.get("coherence_gain_alpha", 2.5))

        # Anesthesia disruption state (Empirical Falsifiability Vector 2)
        self.anesthesia_enabled: bool = bool(cfg_mt.get("anesthesia_enabled", False))
        self.anesthesia_damping: float = float(cfg_mt.get("anesthesia_damping", 0.02))

        # Generate tubulin lattice
        self.subunits: List[TubulinHeterodimer] = []
        self._build_lattice()

        # Telemetry metrics
        self.current_coherence_time: float = self.base_coherence
        self.frohlich_condensation_factor: float = 0.0
        self.spacetime_coupling_strength: float = 0.0
        self.time_elapsed: float = 0.0

    def _build_lattice(self) -> None:
        """Constructs the cylindrical 13-protofilament tubulin coordinate structure."""
        self.subunits.clear()
        d_theta = 2.0 * math.pi / self.protofilaments
        dz = self.length / max(1, self.subunits_per_filament - 1)

        for ring in range(self.subunits_per_filament):
            z = -0.5 * self.length + ring * dz
            # Tubulin lattice has a helical pitch skew of 3 monomers per turn
            skew = (ring * 3.0 / self.protofilaments) * d_theta
            for f in range(self.protofilaments):
                theta = f * d_theta + skew
                x = self.radius * math.cos(theta)
                y = self.radius * math.sin(theta)
                pos = np.array([x, y, z], dtype=np.float32) + self.base_position
                self.subunits.append(TubulinHeterodimer(f, ring, pos))

    def set_anesthesia(self, enabled: bool) -> None:
        """Toggles anesthesia disruption state."""
        self.anesthesia_enabled = enabled

    def update(self, dt: float, focus_density: float) -> None:
        """
        Updates tubulin dipole vibrations, quantum coherence, and spacetime coupling:
        - When conscious focus density increases, dipole vibrations lock phase (Fröhlich condensation).
        - If anesthesia is active, tubulin flickering is disrupted/severed.
        """
        self.time_elapsed += dt

        if self.anesthesia_enabled:
            # Anesthesia physically disrupts quantum flickers in tubulin hydrophobic pockets
            effective_focus = focus_density * self.anesthesia_damping
            anesthesia_factor = self.anesthesia_damping
        else:
            effective_focus = focus_density
            anesthesia_factor = 1.0

        # Quantum coherence time scales directly with focus density (Vector 1: Quantum Biology)
        self.current_coherence_time = self.base_coherence * (1.0 + self.coherence_gain * effective_focus)

        # Fröhlich condensation factor: order parameter of coherent collective dipole resonance
        self.frohlich_condensation_factor = (effective_focus ** 1.5) * anesthesia_factor

        # Transduction coupling to local spacetime
        self.spacetime_coupling_strength = self.frohlich_condensation_factor * 0.85

        # Update individual tubulin dipole oscillations
        for subunit in self.subunits:
            # Individual phase lock under Fröhlich condensation
            phase = self.dipole_freq * self.time_elapsed + (1.0 - self.frohlich_condensation_factor) * subunit.phase_offset
            raw_dipole = math.cos(phase)

            # Dipole alignment with collective field
            subunit.dipole_moment = raw_dipole * anesthesia_factor
            subunit.quantum_coherence = self.frohlich_condensation_factor

    def get_lattice_dipoles(self) -> np.ndarray:
        """Returns array of dipole moments for all tubulin units."""
        return np.array([s.dipole_moment for s in self.subunits], dtype=np.float32)

    def get_subunits_summary(self) -> Dict[str, float]:
        """Provides status summary of the biological transducer."""
        return {
            "num_subunits": len(self.subunits),
            "frohlich_condensation": float(self.frohlich_condensation_factor),
            "coherence_time_s": float(self.current_coherence_time),
            "spacetime_coupling": float(self.spacetime_coupling_strength),
            "anesthesia_active": float(1.0 if self.anesthesia_enabled else 0.0),
        }
