"""
run_simulation.py
=================
Main entry point for executing the Actor Hypothesis Simulation in NVIDIA Isaac Sim 5.0.1+.

Usage Examples:
    # 1. Run full transduction with visual GUI:
    python run_simulation.py --mode collapse

    # 2. Run Pathway 1: Daydream Dissipation (unacted thought returning to Actor Field):
    python run_simulation.py --mode daydream

    # 3. Run Pathway 2: Spacetime Residue (cumulative gravitational footprint):
    python run_simulation.py --mode residue

    # 4. Run Testable Vector 2: Anesthesia Disruption (halting the Actor Operator):
    python run_simulation.py --mode anesthesia

    # 5. Headless automated run:
    python run_simulation.py --mode collapse --headless --duration 6.0
"""

import os
import sys
import argparse

# Add project root and Isaac Sim paths to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# 1. Parse command-line arguments BEFORE initializing SimulationApp
parser = argparse.ArgumentParser(description="NVIDIA Isaac Sim Actor Hypothesis Simulation")
parser.add_argument(
    "--mode",
    type=str,
    default="collapse",
    choices=["collapse", "daydream", "residue", "anesthesia", "interactive"],
    help="Simulation scenario mode to execute",
)
parser.add_argument(
    "--headless",
    action="store_true",
    default=False,
    help="Run in headless mode (no GUI window)",
)
parser.add_argument(
    "--duration",
    type=float,
    default=-1.0,
    help="Duration of simulation in seconds (-1 for continuous execution)",
)
parser.add_argument(
    "--focus",
    type=float,
    default=None,
    help="Override conscious focus density [0.0 - 1.0]",
)
parser.add_argument(
    "--save_usd",
    type=str,
    default=os.path.join(SCRIPT_DIR, "models", "usd", "actor_hypothesis_scene.usda"),
    help="Path to save the generated OpenUSD stage",
)
parser.add_argument(
    "--config",
    type=str,
    default=os.path.join(SCRIPT_DIR, "config", "simulation_config.json"),
    help="Path to simulation configuration JSON",
)

args, unknown = parser.parse_known_args()

# In headless mode without explicit duration, default to 10.0s for automated termination
if args.headless and args.duration <= 0:
    args.duration = 10.0

# 2. Launch Isaac Sim SimulationApp
print("=====================================================================")
print("  NVIDIA ISAAC SIM 5.0.1+ - THE ACTOR HYPOTHESIS SIMULATION")
print("  Transduction of Conscious Intent & Cognitive Wave-Particle Duality")
print("=====================================================================")
print(f"Mode: {args.mode.upper()} | Headless: {args.headless} | Duration: {'Continuous (Until Closed)' if args.duration < 0 else f'{args.duration} s'}")

from isaacsim import SimulationApp

# SimulationApp config
app_cfg = {
    "headless": args.headless,
    "width": 1600,
    "height": 900,
    "renderer": "RayTracedLighting",
}
kit = SimulationApp(app_cfg)

try:
    from src.simulation_engine import ActorHypothesisSimulation

    # Mode mapping
    mode_map = {
        "collapse": "COLLAPSE_ACTION",
        "daydream": "DAYDREAM_DISSIPATION",
        "residue": "SPACETIME_RESIDUE",
        "anesthesia": "ANESTHESIA_DISRUPTION",
        "interactive": "INTERACTIVE_CYCLE",
    }
    selected_mode = mode_map.get(args.mode, "COLLAPSE_ACTION")

    # Initialize master simulation
    sim = ActorHypothesisSimulation(
        kit_app=kit,
        config_path=args.config,
        mode=selected_mode,
    )

    if args.focus is not None:
        sim.quantum_wave.set_focus(args.focus)

    print("\n[Simulation Started] Press Ctrl+C in terminal or close window to exit.")
    
    # Save the initial USD stage
    if args.save_usd:
        os.makedirs(os.path.dirname(args.save_usd), exist_ok=True)
        sim.stage.Export(args.save_usd)
        print(f"[USD Scene Saved] Exported stage to: {args.save_usd}")

    # Main execution loop
    sim_dt = sim.dt
    total_time = 0.0
    step_idx = 0

    while kit.is_running():
        state = sim.step()
        total_time += sim_dt
        step_idx += 1

        if args.duration > 0 and total_time >= args.duration:
            print(f"\n[Completed] Reached duration limit of {args.duration} s.")
            break

    # Export telemetry time-series data to data/ folder
    log_file_base = f"telemetry_log_{args.mode}"
    sim.telemetry.export_logs(base_name=log_file_base)

    # Re-export final state of USD stage
    if args.save_usd:
        sim.stage.Export(args.save_usd)
        print(f"[USD Scene Saved] Final stage saved to: {os.path.abspath(args.save_usd)}")

    print("\n=====================================================================")
    print("  SIMULATION RUN COMPLETE")
    print(f"  Total Steps: {step_idx} | Simulated Time: {total_time:.2f} s")
    print(f"  Final Quantum State: {'COLLAPSED' if sim.quantum_wave.is_collapsed else 'UNACTED SUPERPOSITION'}")
    print(f"  Cumulative Mechanical Work: {sim.actuator.cumulative_work_joules:.4f} Joules")
    print(f"  Spacetime Metric Residue: {sim.spacetime_grid.get_max_residue():.4f} d_g00")
    print(f"  Energy Returned to Actor Field: {sim.quantum_wave.dissipation_energy:.4f} Joules")
    print("=====================================================================")
    print(f"\n[Note] You can re-open and inspect the USD scene directly at:")
    print(f"       {os.path.abspath(args.save_usd)}")
    print("=====================================================================")

finally:
    print("[Cleaning up] Closing Isaac Sim application...")
    kit.close()
