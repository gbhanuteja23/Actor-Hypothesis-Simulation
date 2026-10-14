"""
spacetime_geometry.py
=====================
Simulates the metric curvature of spacetime underlying cognitive wave-particle duality:
- Real-time 3D grid deformation modeling metric tensor perturbations h_munu.
- Pathway 2: Gravitational Residue left by unacted thoughts.
- Metric concentration during Objective Reduction collapse.
"""

import math
import numpy as np
from typing import Tuple, Dict, Optional


class SpacetimeCurvatureGrid:
    """
    Simulates a 2D/3D deformable spacetime metric grid.
    Visualizes:
    1. Dynamic gravitational ripple during thought wave superposition.
    2. Sharp metric depression at the moment of Objective Reduction.
    3. Persistent subtle residual warping from unacted thoughts (Pathway 2).
    """

    def __init__(self, config: dict):
        self.config = config
        cfg_st = config.get("spacetime_geometry", {})
        self.origin = np.array(cfg_st.get("grid_origin", [-2.5, -1.5, 0.0]), dtype=np.float32)
        self.dims = np.array(cfg_st.get("grid_dimensions", [5.0, 3.0]), dtype=np.float32)
        self.nx = int(cfg_st.get("grid_subdivisions_x", 30))
        self.ny = int(cfg_st.get("grid_subdivisions_y", 20))
        self.coupling = float(cfg_st.get("curvature_coupling", 0.15))
        self.residue_accum_rate = float(cfg_st.get("residue_accumulation_rate", 0.08))
        self.residue_dissip_rate = float(cfg_st.get("residue_dissipation_rate", 0.005))

        # Persistent residual curvature field (Pathway 2)
        self.residual_metric = np.zeros((self.ny, self.nx), dtype=np.float32)

        # Base flat spacetime coordinates
        self.xs = np.linspace(self.origin[0], self.origin[0] + self.dims[0], self.nx, dtype=np.float32)
        self.ys = np.linspace(self.origin[1], self.origin[1] + self.dims[1], self.ny, dtype=np.float32)
        self.X, self.Y = np.meshgrid(self.xs, self.ys)
        self.Z_base = np.zeros_like(self.X)

        self.time: float = 0.0

    def update(
        self,
        dt: float,
        focus_density: float,
        eg_energy: float,
        is_collapsed: bool,
        target_pos: Optional[np.ndarray] = None,
        is_unacted_daydream: bool = False,
    ) -> np.ndarray:
        """
        Updates the vertical deformation Z(x, y) representing metric curvature g_00:
        - Superposition ripple: harmonic oscillation proportional to focus density.
        - Collapse depression: localized Lorentzian curvature well centered at target action.
        - Residue accumulation: persistent warping when daydreaming without action.
        """
        self.time += dt

        # 1. Base thought wave harmonic distortion across the grid
        k_x = 1.8
        k_y = 2.2
        omega = 3.5
        wave_ripple = (
            np.sin(k_x * self.X + omega * self.time)
            * np.cos(k_y * self.Y + 0.5 * omega * self.time)
            * (self.coupling * (0.2 + 0.8 * focus_density))
        )

        # 2. Pathway 2: Accumulate persistent gravitational residue if unacted
        if is_unacted_daydream and not is_collapsed:
            # Subtle imprint concentrated around the conscious entity origin [-1.0, 0.0]
            center_x, center_y = -1.0, 0.0
            dist_sq = (self.X - center_x) ** 2 + (self.Y - center_y) ** 2
            imprint = np.exp(-dist_sq / 1.5) * self.residue_accum_rate * focus_density * dt
            self.residual_metric += imprint
        else:
            # Very slow gradual relaxation of residue
            self.residual_metric *= math.exp(-self.residue_dissip_rate * dt)

        # 3. Collapse depression (Objective Reduction well)
        collapse_well = np.zeros_like(self.X)
        if is_collapsed and target_pos is not None:
            cx, cy = target_pos[0], target_pos[1]
            dist_sq = (self.X - cx) ** 2 + (self.Y - cy) ** 2
            # Deep gravitational well at the physical manifest point
            collapse_well = -0.35 * np.exp(-dist_sq / 0.25)
        elif eg_energy > 0.0:
            # Intermediate well developing as E_G approaches threshold
            cx, cy = 0.5, 0.0
            dist_sq = (self.X - cx) ** 2 + (self.Y - cy) ** 2
            collapse_well = -0.15 * (eg_energy / 2.0) * np.exp(-dist_sq / 0.6)

        # Net metric curvature Z
        Z_net = wave_ripple + (-self.residual_metric * 0.25) + collapse_well
        return Z_net

    def get_grid_points(self, Z: np.ndarray) -> np.ndarray:
        """Returns (N, 3) flattened array of current spacetime 3D vertices."""
        points = np.stack([self.X.flatten(), self.Y.flatten(), Z.flatten()], axis=1)
        return points.astype(np.float32)

    def get_max_residue(self) -> float:
        """Returns peak residual gravitational distortion."""
        return float(np.max(self.residual_metric))
