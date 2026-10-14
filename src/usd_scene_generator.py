"""
usd_scene_generator.py
======================
Generates and populates the OpenUSD stage for Isaac Sim 5.0.1+:
- Actor Field (Universal conscious background aura)
- Conscious Entity (Hilbert space excitation diamond)
- Thought Wave Superposition (Dynamic quantum wave filament)
- Microtubules (13-protofilament tubulin lattice with dipole glow)
- Projection Tensor (Crystalline prism & star operator)
- Spacetime Curvature Grid (Deformable metric mesh)
- Physical Environment (PhysX table, robotic arm, target interactive objects)
"""

import math
import numpy as np
from pxr import Usd, UsdGeom, UsdShade, UsdPhysics, UsdLux, Gf, Sdf
from typing import Dict, Any, List, Optional


def create_material(
    stage: Usd.Stage,
    path: str,
    diffuse_color: Gf.Vec3f,
    emissive_color: Optional[Gf.Vec3f] = None,
    opacity: float = 1.0,
    metallic: float = 0.0,
    roughness: float = 0.4,
) -> UsdShade.Material:
    """Creates a UsdPreviewSurface material with customizable colors and emission."""
    material = UsdShade.Material.Define(stage, Sdf.Path(path))
    shader = UsdShade.Shader.Define(stage, Sdf.Path(f"{path}/Shader"))
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(diffuse_color)
    shader.CreateInput("opacity", Sdf.ValueTypeNames.Float).Set(opacity)
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(metallic)
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(roughness)

    if emissive_color is not None:
        shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set(emissive_color)

    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    return material


def bind_material(prim: Usd.Prim, material: UsdShade.Material) -> None:
    """Binds a UsdShade Material to a Usd Prim."""
    UsdShade.MaterialBindingAPI.Apply(prim).Bind(material)


class USDSceneBuilder:
    """Constructs the complete 6-Stage Actor Hypothesis simulation stage in OpenUSD."""

    def __init__(self, stage: Usd.Stage, config: dict):
        self.stage = stage
        self.config = config
        self.materials: Dict[str, UsdShade.Material] = {}
        self.tubulin_prims: List[UsdGeom.Sphere] = []
        self.flash_light: Optional[UsdLux.SphereLight] = None
        self.wave_points_prim: Optional[UsdGeom.Points] = None
        self.grid_mesh: Optional[UsdGeom.Mesh] = None

    def build_all(self) -> None:
        """Constructs all visual and physics elements in the stage."""
        self._setup_stage_metadata()
        self._create_materials()
        self._create_lighting()
        self._build_actor_field()
        self._build_conscious_entity()
        self._build_thought_wave()
        self._build_microtubule_transducer()
        self._build_projection_tensor_and_prism()
        self._build_spacetime_grid()
        self._build_physical_environment()

    def _setup_stage_metadata(self) -> None:
        """Sets stage units and up-axis."""
        UsdGeom.SetStageUpAxis(self.stage, UsdGeom.Tokens.z)
        UsdGeom.SetStageMetersPerUnit(self.stage, 1.0)
        # Clean existing prim if re-initializing stage
        if self.stage.GetPrimAtPath("/World"):
            self.stage.RemovePrim(Sdf.Path("/World"))
        # Create /World root xform
        UsdGeom.Xform.Define(self.stage, Sdf.Path("/World"))

    def _create_materials(self) -> None:
        """Initializes all visual shader materials."""
        mat_root = "/World/Looks"
        UsdGeom.Scope.Define(self.stage, Sdf.Path(mat_root))

        # Actor Field: Deep ethereal purple
        self.materials["ActorField"] = create_material(
            self.stage, f"{mat_root}/ActorFieldMat",
            diffuse_color=Gf.Vec3f(0.18, 0.02, 0.35),
            emissive_color=Gf.Vec3f(0.28, 0.05, 0.55),
            opacity=0.45, roughness=0.1
        )

        # Conscious Entity: Silver-diamond crystal
        self.materials["ConsciousEntity"] = create_material(
            self.stage, f"{mat_root}/ConsciousEntityMat",
            diffuse_color=Gf.Vec3f(0.85, 0.9, 1.0),
            emissive_color=Gf.Vec3f(0.4, 0.7, 1.0),
            metallic=0.8, roughness=0.1
        )

        # Thought Wave: Neon electric violet/cyan
        self.materials["ThoughtWave"] = create_material(
            self.stage, f"{mat_root}/ThoughtWaveMat",
            diffuse_color=Gf.Vec3f(0.2, 0.6, 1.0),
            emissive_color=Gf.Vec3f(0.6, 0.3, 1.0),
            roughness=0.1
        )

        # Microtubule Tubulin: Quantum bio-lattice
        self.materials["TubulinAlpha"] = create_material(
            self.stage, f"{mat_root}/TubulinAlphaMat",
            diffuse_color=Gf.Vec3f(0.3, 0.4, 0.8),
            emissive_color=Gf.Vec3f(0.2, 0.3, 0.9),
            roughness=0.2
        )
        self.materials["TubulinBeta"] = create_material(
            self.stage, f"{mat_root}/TubulinBetaMat",
            diffuse_color=Gf.Vec3f(0.6, 0.2, 0.8),
            emissive_color=Gf.Vec3f(0.5, 0.1, 0.7),
            roughness=0.2
        )

        # Projection Prism: Diamond dielectric crystal
        self.materials["ProjectionPrism"] = create_material(
            self.stage, f"{mat_root}/ProjectionPrismMat",
            diffuse_color=Gf.Vec3f(0.95, 0.98, 1.0),
            emissive_color=Gf.Vec3f(0.2, 0.4, 0.8),
            opacity=0.65, metallic=0.2, roughness=0.05
        )

        # Star Actor Operator: Polished gold / chrome
        self.materials["StarOperator"] = create_material(
            self.stage, f"{mat_root}/StarOperatorMat",
            diffuse_color=Gf.Vec3f(1.0, 0.85, 0.3),
            emissive_color=Gf.Vec3f(0.9, 0.7, 0.1),
            metallic=0.95, roughness=0.15
        )

        # Spacetime Grid
        self.materials["SpacetimeGrid"] = create_material(
            self.stage, f"{mat_root}/SpacetimeGridMat",
            diffuse_color=Gf.Vec3f(0.08, 0.15, 0.25),
            emissive_color=Gf.Vec3f(0.12, 0.35, 0.65),
            roughness=0.3
        )

        # Table & Robotics
        self.materials["MetalRobot"] = create_material(
            self.stage, f"{mat_root}/MetalRobotMat",
            diffuse_color=Gf.Vec3f(0.85, 0.85, 0.88),
            metallic=0.9, roughness=0.2
        )
        self.materials["DarkTable"] = create_material(
            self.stage, f"{mat_root}/DarkTableMat",
            diffuse_color=Gf.Vec3f(0.15, 0.16, 0.18),
            roughness=0.5
        )

    def _create_lighting(self) -> None:
        """Sets up key lights, rim lights, and collapse flash."""
        # Main key light
        key_light = UsdLux.SphereLight.Define(self.stage, Sdf.Path("/World/Lighting/KeyLight"))
        key_light.CreateRadiusAttr(0.2)
        key_light.CreateIntensityAttr(8000.0)
        key_light.CreateColorAttr(Gf.Vec3f(0.9, 0.95, 1.0))
        key_light.AddTranslateOp().Set(Gf.Vec3f(2.0, -3.0, 3.5))

        # Fill light with subtle blue tint
        fill_light = UsdLux.SphereLight.Define(self.stage, Sdf.Path("/World/Lighting/FillLight"))
        fill_light.CreateRadiusAttr(0.3)
        fill_light.CreateIntensityAttr(3500.0)
        fill_light.CreateColorAttr(Gf.Vec3f(0.4, 0.6, 1.0))
        fill_light.AddTranslateOp().Set(Gf.Vec3f(-3.0, -2.0, 2.5))

        # Objective Reduction flash light (activated on collapse)
        self.flash_light = UsdLux.SphereLight.Define(self.stage, Sdf.Path("/World/Lighting/CollapseFlash"))
        self.flash_light.CreateRadiusAttr(0.15)
        self.flash_light.CreateIntensityAttr(0.0)  # Starts off
        self.flash_light.CreateColorAttr(Gf.Vec3f(1.0, 0.95, 0.8))
        self.flash_light.AddTranslateOp().Set(Gf.Vec3f(0.5, 0.0, 1.2))

    def _build_actor_field(self) -> None:
        """Constructs Stage 1: The Actor Field."""
        field_scope = UsdGeom.Scope.Define(self.stage, Sdf.Path("/World/ActorField"))
        sphere = UsdGeom.Sphere.Define(self.stage, Sdf.Path("/World/ActorField/AuraDome"))
        sphere.CreateRadiusAttr(2.8)
        sphere.AddTranslateOp().Set(Gf.Vec3f(-2.0, 0.0, 1.2))
        bind_material(sphere.GetPrim(), self.materials["ActorField"])

    def _build_conscious_entity(self) -> None:
        """Constructs Stage 2: Conscious Entity (Energy excitation in Hilbert Space)."""
        entity_scope = UsdGeom.Scope.Define(self.stage, Sdf.Path("/World/ConsciousEntity"))
        diamond = UsdGeom.Cube.Define(self.stage, Sdf.Path("/World/ConsciousEntity/DiamondCore"))
        diamond.CreateSizeAttr(0.25)
        xform = diamond.AddTransformOp()
        # Rotate 45 deg around X and Y to create diamond/octahedral appearance
        mat = Gf.Matrix4d()
        mat.SetRotate(Gf.Rotation(Gf.Vec3d(1, 1, 0), 45))
        mat.SetTranslateOnly(Gf.Vec3d(-2.5, 0.0, 1.2))
        xform.Set(mat)
        bind_material(diamond.GetPrim(), self.materials["ConsciousEntity"])

    def _build_thought_wave(self) -> None:
        """Constructs Stage 3: The Thought Wave."""
        self.wave_points_prim = UsdGeom.Points.Define(self.stage, Sdf.Path("/World/ThoughtWave/WaveFilament"))
        num_pts = 45
        pts = [Gf.Vec3f(-2.3 + i * (1.1 / num_pts), 0.0, 1.2) for i in range(num_pts)]
        widths = [0.035 for _ in range(num_pts)]
        self.wave_points_prim.CreatePointsAttr(pts)
        self.wave_points_prim.CreateWidthsAttr(widths)
        bind_material(self.wave_points_prim.GetPrim(), self.materials["ThoughtWave"])

    def _build_microtubule_transducer(self) -> None:
        """Constructs Stage 4: 13-Protofilament Microtubule Lattice."""
        mt_scope = UsdGeom.Scope.Define(self.stage, Sdf.Path("/World/Microtubules"))
        protofilaments = 13
        subunits_per_ring = 14
        radius = 0.12
        length = 0.9
        base_x = -1.0
        center_z = 1.2

        dz = length / max(1, subunits_per_ring - 1)
        d_theta = 2.0 * math.pi / protofilaments

        idx = 0
        for ring in range(subunits_per_ring):
            z = -0.5 * length + ring * dz
            skew = (ring * 3.0 / protofilaments) * d_theta
            mat = self.materials["TubulinAlpha"] if (ring % 2 == 0) else self.materials["TubulinBeta"]

            for f in range(protofilaments):
                theta = f * d_theta + skew
                x = base_x + radius * math.cos(theta)
                y = radius * math.sin(theta)

                prim_path = Sdf.Path(f"/World/Microtubules/Tubulin_{idx}")
                sphere = UsdGeom.Sphere.Define(self.stage, prim_path)
                sphere.CreateRadiusAttr(0.018)
                sphere.AddTranslateOp().Set(Gf.Vec3f(x, y, center_z + z))
                bind_material(sphere.GetPrim(), mat)
                self.tubulin_prims.append(sphere)
                idx += 1

    def _build_projection_tensor_and_prism(self) -> None:
        """Constructs Stage 5: Projection Prism and Star Operator."""
        # Prism
        prism = UsdGeom.Cone.Define(self.stage, Sdf.Path("/World/ProjectionTensor/PrismLens"))
        prism.CreateRadiusAttr(0.22)
        prism.CreateHeightAttr(0.45)
        prism_xf = prism.AddTransformOp()
        mat = Gf.Matrix4d()
        mat.SetRotate(Gf.Rotation(Gf.Vec3d(0, 1, 0), -90))
        mat.SetTranslateOnly(Gf.Vec3d(0.0, 0.0, 1.2))
        prism_xf.Set(mat)
        bind_material(prism.GetPrim(), self.materials["ProjectionPrism"])

        # Star Actor Operator
        star_scope = UsdGeom.Scope.Define(self.stage, Sdf.Path("/World/ProjectionTensor/StarOperator"))
        for i in range(3):
            beam = UsdGeom.Cube.Define(self.stage, Sdf.Path(f"/World/ProjectionTensor/StarOperator/Blade_{i}"))
            beam.CreateSizeAttr(0.28)
            xf = beam.AddTransformOp()
            rot_mat = Gf.Matrix4d()
            rot_mat.SetRotate(Gf.Rotation(Gf.Vec3d(1, 0, 0), i * 60))
            rot_mat.SetScale(Gf.Vec3d(0.3, 1.2, 0.3))
            rot_mat.SetTranslateOnly(Gf.Vec3d(0.5, 0.0, 1.2))
            xf.Set(rot_mat)
            bind_material(beam.GetPrim(), self.materials["StarOperator"])

    def _build_spacetime_grid(self) -> None:
        """Constructs Spacetime Curvature Grid Mesh."""
        self.grid_mesh = UsdGeom.Mesh.Define(self.stage, Sdf.Path("/World/SpacetimeGrid/CurvatureSurface"))
        nx, ny = 30, 20
        xs = np.linspace(-2.5, 2.5, nx)
        ys = np.linspace(-1.5, 1.5, ny)
        points = []
        for y in ys:
            for x in xs:
                points.append(Gf.Vec3f(x, y, 0.0))

        face_vertex_counts = []
        face_vertex_indices = []
        for j in range(ny - 1):
            for i in range(nx - 1):
                p0 = j * nx + i
                p1 = j * nx + (i + 1)
                p2 = (j + 1) * nx + (i + 1)
                p3 = (j + 1) * nx + i
                face_vertex_counts.append(4)
                face_vertex_indices.extend([p0, p1, p2, p3])

        self.grid_mesh.CreatePointsAttr(points)
        self.grid_mesh.CreateFaceVertexCountsAttr(face_vertex_counts)
        self.grid_mesh.CreateFaceVertexIndicesAttr(face_vertex_indices)
        bind_material(self.grid_mesh.GetPrim(), self.materials["SpacetimeGrid"])

    def _build_physical_environment(self) -> None:
        """Constructs Stage 6: Physical Environment (Table, Robot Manipulator, Target Objects)."""
        env_scope = UsdGeom.Scope.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment"))

        # Ground Plane with physics
        ground = UsdGeom.Cube.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment/GroundPlane"))
        ground.CreateSizeAttr(1.0)
        ground_xf = ground.AddTransformOp()
        g_mat = Gf.Matrix4d()
        g_mat.SetScale(Gf.Vec3d(20.0, 20.0, 0.02))
        g_mat.SetTranslateOnly(Gf.Vec3d(0.0, 0.0, -0.01))
        ground_xf.Set(g_mat)
        UsdPhysics.CollisionAPI.Apply(ground.GetPrim())

        # Work table
        table = UsdGeom.Cube.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment/WorkTable"))
        table.CreateSizeAttr(1.0)
        table_xf = table.AddTransformOp()
        mat = Gf.Matrix4d()
        mat.SetScale(Gf.Vec3d(0.8, 1.2, 0.35))
        mat.SetTranslateOnly(Gf.Vec3d(0.5, 0.0, 0.175))
        table_xf.Set(mat)
        UsdPhysics.CollisionAPI.Apply(table.GetPrim())
        bind_material(table.GetPrim(), self.materials["DarkTable"])

        # Robotic Manipulator Links (Base, Arm, Gripper)
        robot_root = UsdGeom.Xform.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment/RoboticManipulator"))
        
        # Base
        base = UsdGeom.Cylinder.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment/RoboticManipulator/Base"))
        base.CreateRadiusAttr(0.08)
        base.CreateHeightAttr(0.12)
        base.CreateAxisAttr("Z")
        base.AddTranslateOp().Set(Gf.Vec3f(0.1, 0.0, 0.41))
        bind_material(base.GetPrim(), self.materials["MetalRobot"])

        # Forearm / Effector Link
        arm = UsdGeom.Cube.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment/RoboticManipulator/Forearm"))
        arm.CreateSizeAttr(0.06)
        arm_xf = arm.AddTransformOp()
        arm_mat = Gf.Matrix4d()
        arm_mat.SetScale(Gf.Vec3d(3.5, 0.6, 0.6))
        arm_mat.SetTranslateOnly(Gf.Vec3d(0.28, 0.0, 0.45))
        arm_xf.Set(arm_mat)
        bind_material(arm.GetPrim(), self.materials["MetalRobot"])

        # Physical Interactive Targets on Table:
        # Target 0: Cyan Physical Cylinder (Graspable)
        cyl = UsdGeom.Cylinder.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment/TargetCylinder_Alpha"))
        cyl.CreateRadiusAttr(0.03)
        cyl.CreateHeightAttr(0.12)
        cyl.CreateAxisAttr("Z")
        cyl.AddTranslateOp().Set(Gf.Vec3f(0.45, 0.20, 0.41))
        UsdPhysics.CollisionAPI.Apply(cyl.GetPrim())
        UsdPhysics.RigidBodyAPI.Apply(cyl.GetPrim())
        mat_cyl = create_material(self.stage, "/World/Looks/TargetCylMat", diffuse_color=Gf.Vec3f(0.1, 0.8, 1.0), roughness=0.3)
        bind_material(cyl.GetPrim(), mat_cyl)

        # Target 1: Orange Heavy Block (Pushable)
        cube = UsdGeom.Cube.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment/TargetBlock_Beta"))
        cube.CreateSizeAttr(0.07)
        cube.AddTranslateOp().Set(Gf.Vec3f(0.45, -0.20, 0.385))
        UsdPhysics.CollisionAPI.Apply(cube.GetPrim())
        UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim())
        mat_block = create_material(self.stage, "/World/Looks/TargetBlockMat", diffuse_color=Gf.Vec3f(1.0, 0.5, 0.1), roughness=0.2)
        bind_material(cube.GetPrim(), mat_block)

        # Target 2: Green Precision Switch
        sw_base = UsdGeom.Cube.Define(self.stage, Sdf.Path("/World/PhysicalEnvironment/TargetSwitch_Gamma"))
        sw_base.CreateSizeAttr(0.05)
        sw_base.AddTranslateOp().Set(Gf.Vec3f(0.55, 0.0, 0.375))
        UsdPhysics.CollisionAPI.Apply(sw_base.GetPrim())
        mat_sw = create_material(self.stage, "/World/Looks/TargetSwitchMat", diffuse_color=Gf.Vec3f(0.2, 1.0, 0.4), roughness=0.2)
        bind_material(sw_base.GetPrim(), mat_sw)

    def update_dynamic_visuals(
        self,
        wave_xs: np.ndarray,
        wave_ys: np.ndarray,
        wave_zs: np.ndarray,
        grid_points: np.ndarray,
        flash_intensity: float,
        tubulin_dipoles: np.ndarray,
    ) -> None:
        """Updates per-frame dynamic geometry and lighting in the OpenUSD stage."""
        # 1. Update thought wave filament points
        if self.wave_points_prim is not None:
            num = len(wave_xs)
            base_x = -2.3
            base_z = 1.2
            pts = [Gf.Vec3f(float(base_x + wave_xs[i]), float(wave_ys[i]), float(base_z + wave_zs[i])) for i in range(num)]
            self.wave_points_prim.GetPointsAttr().Set(pts)

        # 2. Update spacetime curvature grid vertices
        if self.grid_mesh is not None:
            pts = [Gf.Vec3f(float(p[0]), float(p[1]), float(p[2])) for p in grid_points]
            self.grid_mesh.GetPointsAttr().Set(pts)

        # 3. Update collapse flash light intensity
        if self.flash_light is not None:
            self.flash_light.GetIntensityAttr().Set(float(flash_intensity))
