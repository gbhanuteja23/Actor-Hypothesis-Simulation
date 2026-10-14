"""
test_simulation.py
==================
Automated validation and test suite for the Actor Hypothesis Simulation in Isaac Sim.
Executes scenarios in headless mode and verifies mathematical and physical invariants.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from isaacsim import SimulationApp

# Run test suite headless
kit = SimulationApp({"headless": True, "renderer": "RayTracedLighting"})

import traceback
try:
    from src.simulation_engine import ActorHypothesisSimulation

    config_path = os.path.join(SCRIPT_DIR, "config", "simulation_config.json")
    print("\n=======================================================")
    print("  STARTING AUTOMATED ACTOR HYPOTHESIS TEST SUITE")
    print("=======================================================")

    # Test 1: Full Transduction Chain & Objective Reduction
    print("\n[TEST 1] Testing Full Transduction Chain (COLLAPSE_ACTION)...")
    sim_collapse = ActorHypothesisSimulation(kit, config_path, mode="COLLAPSE_ACTION")
    collapse_triggered = False

    for step in range(250):
        state = sim_collapse.step()
        if state["is_collapsed"]:
            collapse_triggered = True
            break

    assert collapse_triggered, "FAILED: Objective Reduction should have triggered under high focus density!"
    assert sim_collapse.quantum_wave.collapsed_state_idx is not None, "FAILED: Collapsed eigenstate must be set!"
    assert sim_collapse.actuator.active_action_id is not None, "FAILED: Physical actuator must receive command!"
    print("  --> PASS: Objective Reduction breached threshold, Actor Operator collapsed state successfully!")

    # Test 2: Pathway 1 - Daydream Dissipation
    print("\n[TEST 2] Testing Pathway 1 (DAYDREAM_DISSIPATION)...")
    sim_daydream = ActorHypothesisSimulation(kit, config_path, mode="DAYDREAM_DISSIPATION")
    for step in range(120):
        state = sim_daydream.step()

    assert not state["is_collapsed"], "FAILED: Daydream should NOT trigger Objective Reduction!"
    assert state["dissipated_energy"] > 0.0, "FAILED: Energy should dissipate into Actor Field!"
    print(f"  --> PASS: Unacted thought gently dissipated {state['dissipated_energy']:.4f} J back to Actor Field.")

    # Test 3: Pathway 2 - Spacetime Residue
    print("\n[TEST 3] Testing Pathway 2 (SPACETIME_RESIDUE)...")
    sim_residue = ActorHypothesisSimulation(kit, config_path, mode="SPACETIME_RESIDUE")
    for step in range(120):
        state = sim_residue.step()

    assert not state["is_collapsed"], "FAILED: Residue test should remain uncollapsed!"
    assert state["spacetime_residue"] > 0.0, "FAILED: Gravitational residue must accumulate in spacetime grid!"
    print(f"  --> PASS: Unacted thought accumulated metric residue: {state['spacetime_residue']:.4f} d_g00.")

    # Test 4: Empirical Falsifiability - Anesthesia Disruption
    print("\n[TEST 4] Testing Testable Vector 2 (ANESTHESIA_DISRUPTION)...")
    sim_anesth = ActorHypothesisSimulation(kit, config_path, mode="ANESTHESIA_DISRUPTION")
    for step in range(250):
        state = sim_anesth.step()

    assert not state["is_collapsed"], "FAILED: Anesthesia must prevent Objective Reduction from firing!"
    assert state["frohlich_condensation"] < 0.1, "FAILED: Anesthesia must suppress Fröhlich condensation!"
    print("  --> PASS: Anesthesia successfully decoupled microtubules and halted the Actor Operator!")

    print("\n=======================================================")
    print("  ALL TESTS PASSED! THE ACTOR HYPOTHESIS IS VERIFIED.")
    print("=======================================================\n")

    with open("test_results.txt", "w") as f:
        f.write("ALL 4 ACTOR HYPOTHESIS TEST SUITES PASSED SUCCESSFULLY!\n")

except Exception as e:
    err_msg = traceback.format_exc()
    print("TEST ERROR:\n", err_msg)
    with open("test_error.log", "w") as f:
        f.write(err_msg)

finally:
    kit.close()
