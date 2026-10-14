"""
telemetry_overlay.py
====================
Provides real-time state monitoring, diagnostic logging, formatted
scientific telemetry displays, and CSV/JSON data logging across all 6 stages
of the Actor Hypothesis.
"""

import os
import csv
import json
from typing import Dict, Any, List


class TelemetryReporter:
    """Formats, prints, and logs live telemetry data during simulation execution."""

    def __init__(self, log_dir: str = "data"):
        self.step_counter = 0
        self.log_dir = log_dir
        self.history: List[Dict[str, Any]] = []

    def record_step(self, state: Dict[str, Any]) -> None:
        """Appends the current state snapshot to the history buffer."""
        # Create a shallow copy with serializable scalar types
        entry = {
            "time_s": round(float(state.get("time_s", 0.0)), 4),
            "focus_density": round(float(state.get("focus_density", 0.0)), 4),
            "entropy_bits": round(float(state.get("entropy", 0.0)), 4),
            "frohlich_condensation": round(float(state.get("frohlich_condensation", 0.0)), 4),
            "coherence_time_ms": round(float(state.get("coherence_time_s", 0.0)) * 1000.0, 2),
            "anesthesia_active": int(1 if state.get("anesthesia_active", False) else 0),
            "eg_energy_J": round(float(state.get("eg_energy", 0.0)), 4),
            "tau_collapse_s": round(float(state.get("tau_collapse_s", 999.0)), 3),
            "collapse_tension": round(float(state.get("collapse_tension", 0.0)), 4),
            "is_collapsed": int(1 if state.get("is_collapsed", False) else 0),
            "collapsed_state_idx": state.get("collapsed_state_idx", -1) if state.get("collapsed_state_idx") is not None else -1,
            "collapsed_action_name": str(state.get("collapsed_action_name", "")),
            "contact_force_N": round(float(state.get("contact_force_N", 0.0)), 4),
            "cumulative_work_J": round(float(state.get("work_joules", 0.0)), 4),
            "entropy_reduction_rate_W_per_K": round(float(state.get("entropy_reduction_rate", 0.0)), 5),
            "dissipated_energy_J": round(float(state.get("dissipated_energy", 0.0)), 4),
            "spacetime_residue_d_g00": round(float(state.get("spacetime_residue", 0.0)), 5),
        }
        self.history.append(entry)

    def format_status_box(self, state: Dict[str, Any]) -> str:
        """Constructs an ASCII dashboard of the Transduction Chain."""
        time_s = state.get("time_s", 0.0)
        focus = state.get("focus_density", 0.0)
        entropy = state.get("entropy", 0.0)
        frohlich = state.get("frohlich_condensation", 0.0)
        coherence = state.get("coherence_time_s", 0.0)
        anesthesia = state.get("anesthesia_active", False)
        eg = state.get("eg_energy", 0.0)
        tau = state.get("tau_collapse_s", 999.0)
        tension = state.get("collapse_tension", 0.0)
        is_collapsed = state.get("is_collapsed", False)
        chosen_id = state.get("collapsed_state_idx", None)
        action_name = state.get("collapsed_action_name", "Superposition (Uncollapsed)")
        residue = state.get("spacetime_residue", 0.0)
        dissipation = state.get("dissipated_energy", 0.0)
        force = state.get("contact_force_N", 0.0)
        work = state.get("work_joules", 0.0)
        ds_dt = state.get("entropy_reduction_rate", 0.0)

        # Progress bar for Objective Reduction tension
        bar_len = 20
        filled = int(min(1.0, tension) * bar_len)
        bar = "#" * filled + "." * (bar_len - filled)

        lines = [
            "+-----------------------------------------------------------------------------+",
            f"|  ACTOR HYPOTHESIS SIMULATION TELEMETRY  |  Time: {time_s:6.2f} s                |",
            "+-----------------------------------------------------------------------------+",
            f"| Stage 1: ACTOR FIELD      | Vacuum Energy: 1.25e-9 J/m3                     |",
            f"| Stage 2: CONSCIOUS ENTITY | Focus Density (Df): {focus:4.2f} | Entropy: {entropy:4.2f} bits  |",
            f"| Stage 3: THOUGHT WAVE     | State: {'COLLAPSED' if is_collapsed else 'SUPERPOSITION':12s}                           |",
            f"| Stage 4: MICROTUBULES     | Frohlich Condensation: {frohlich:4.2f} | Coh: {coherence*1000:5.1f} ms     |",
            f"|                           | Anesthesia Disruption: {'ACTIVE (BLOCKED)' if anesthesia else 'OFF (COHERENT)':16s}     |",
            f"| Stage 5: OBJECTIVE RED.   | EG: {eg:5.2f} J | tau: {tau:5.2f} s | Tension: [{bar}] {tension*100:4.1f}%|",
            f"|                           | Actor Operator: {'FIRED -> ' + str(chosen_id) if is_collapsed else 'WAITING':16s}             |",
            f"| Stage 6: PHYSICAL ACTION  | Selected: {action_name[:36]:36s}|",
            f"|                           | Force: {force:5.2f} N | Work: {work:6.3f} J | dS/dt: {ds_dt:6.3f} W/K  |",
            "+-----------------------------------------------------------------------------+",
            f"| THERMODYNAMICS OF UNACTED | Pathway 1 (Dissipation): {dissipation:6.4f} J              |",
            f"|                           | Pathway 2 (Metric Residue): {residue:6.4f} d_g00        |",
            "+-----------------------------------------------------------------------------+",
        ]
        return "\n".join(lines)

    def log_step(self, state: Dict[str, Any], frequency: int = 30) -> None:
        """Logs telemetry periodically to keep console clean and readable."""
        self.step_counter += 1
        self.record_step(state)
        if self.step_counter % frequency == 0:
            print(self.format_status_box(state))

    def export_logs(self, base_name: str = "telemetry_log") -> None:
        """Exports the recorded step history to CSV and JSON on disk."""
        if not self.history:
            return

        os.makedirs(self.log_dir, exist_ok=True)
        csv_path = os.path.join(self.log_dir, f"{base_name}.csv")
        json_path = os.path.join(self.log_dir, f"{base_name}.json")

        # 1. Export CSV
        fieldnames = list(self.history[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.history)

        # 2. Export JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)

        print(f"\n[Telemetry Saved] Time-series data saved to:")
        print(f"  CSV:  {os.path.abspath(csv_path)}")
        print(f"  JSON: {os.path.abspath(json_path)}")
