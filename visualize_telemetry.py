"""
visualize_telemetry.py
======================
Generates scientific, multi-panel diagnostic plots from saved Actor Hypothesis
simulation telemetry data (CSV files in the data/ folder).
"""

import os
import glob
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt


def plot_telemetry(csv_path: str, output_image_path: str) -> None:
    """Reads telemetry CSV and creates a 5-panel scientific analysis plot."""
    print(f"[Plotting] Reading telemetry from: {csv_path}")

    times = []
    focus = []
    entropy = []
    frohlich = []
    coherence = []
    eg = []
    tau = []
    tension = []
    is_collapsed = []
    force = []
    work = []
    dissipation = []
    residue = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row["time_s"]))
            focus.append(float(row["focus_density"]))
            entropy.append(float(row["entropy_bits"]))
            frohlich.append(float(row["frohlich_condensation"]))
            coherence.append(float(row["coherence_time_ms"]))
            eg.append(float(row["eg_energy_J"]))
            tau.append(float(row["tau_collapse_s"]))
            tension.append(float(row["collapse_tension"]))
            is_collapsed.append(int(row["is_collapsed"]))
            force.append(float(row["contact_force_N"]))
            work.append(float(row["cumulative_work_J"]))
            dissipation.append(float(row["dissipated_energy_J"]))
            residue.append(float(row["spacetime_residue_d_g00"]))

    times = np.array(times)

    # Create dark-theme high-contrast scientific plot
    plt.style.use("dark_background")
    fig, axes = plt.subplots(5, 1, figsize=(14, 18), sharex=True)
    plt.subplots_adjust(hspace=0.28)

    # 1. Focus Density & Shannon Entropy
    ax1 = axes[0]
    ax1.plot(times, focus, color="#00E5FF", linewidth=2.2, label="Focus Density $D_f$")
    ax1_twin = ax1.twinx()
    ax1_twin.plot(times, entropy, color="#FF007F", linewidth=2.2, linestyle="--", label="Entropy $S(\\Psi)$ (bits)")
    ax1.set_ylabel("Focus Density $D_f$", color="#00E5FF", fontsize=11, fontweight="bold")
    ax1_twin.set_ylabel("Entropy (bits)", color="#FF007F", fontsize=11, fontweight="bold")
    ax1.set_title("Stage 2 & 3: Conscious Intent & Informational Superposition Entropy", fontsize=13, fontweight="bold", pad=8)
    ax1.grid(True, linestyle=":", alpha=0.4)

    # 2. Microtubule Fröhlich Condensation & Coherence Time
    ax2 = axes[1]
    ax2.plot(times, frohlich, color="#B388FF", linewidth=2.2, label="Fröhlich Condensation")
    ax2_twin = ax2.twinx()
    ax2_twin.plot(times, coherence, color="#7C4DFF", linewidth=2.0, linestyle=":", label="Coherence $\\tau_{coh}$ (ms)")
    ax2.set_ylabel("Condensation Order", color="#B388FF", fontsize=11, fontweight="bold")
    ax2_twin.set_ylabel("$\\tau_{coh}$ (ms)", color="#7C4DFF", fontsize=11, fontweight="bold")
    ax2.set_title("Stage 4: Microtubule Biological Transducer (Orch-OR Dipole Resonance)", fontsize=13, fontweight="bold", pad=8)
    ax2.grid(True, linestyle=":", alpha=0.4)

    # 3. Gravitational Self-Energy & Objective Reduction Threshold Tension
    ax3 = axes[2]
    ax3.plot(times, eg, color="#FFD700", linewidth=2.2, label="Self-Energy $E_G$ (J)")
    ax3.plot(times, tension, color="#FF9100", linewidth=2.5, linestyle="-.", label="Tension Integral $I_{OR}$")
    ax3.axhline(1.0, color="#FF1744", linestyle="--", linewidth=1.8, label="Penrose Threshold ($I_{OR} = 1.0$)")
    
    # Mark collapse point if triggered
    collapse_indices = np.where(np.array(is_collapsed) == 1)[0]
    if len(collapse_indices) > 0:
        c_time = times[collapse_indices[0]]
        ax3.axvline(c_time, color="#FFFFFF", linestyle="-", linewidth=2.0, alpha=0.9)
        ax3.text(c_time + 0.05, 0.5, f"COLLAPSE\n(t = {c_time:.2f}s)", color="#FFFFFF", fontweight="bold", fontsize=10)

    ax3.set_ylabel("Energy & Tension", color="#FFD700", fontsize=11, fontweight="bold")
    ax3.set_title("Stage 5: Penrose Objective Reduction Threshold $\\tau \\approx \\hbar / E_G$", fontsize=13, fontweight="bold", pad=8)
    ax3.legend(loc="upper left", framealpha=0.3)
    ax3.grid(True, linestyle=":", alpha=0.4)

    # 4. Physical Action: Contact Force & Mechanical Work
    ax4 = axes[3]
    ax4.plot(times, work, color="#00E676", linewidth=2.4, label="Mechanical Work $W$ (J)")
    ax4_twin = ax4.twinx()
    ax4_twin.plot(times, force, color="#76FF03", linewidth=1.8, linestyle="--", label="Contact Force (N)")
    ax4.set_ylabel("Work $W$ (Joules)", color="#00E676", fontsize=11, fontweight="bold")
    ax4_twin.set_ylabel("Force (N)", color="#76FF03", fontsize=11, fontweight="bold")
    ax4.set_title("Stage 6: Physical Robotic Actuation & Thermodynamic Energy Transfer", fontsize=13, fontweight="bold", pad=8)
    ax4.grid(True, linestyle=":", alpha=0.4)

    # 5. Thermodynamics of the Unacted: Dissipation vs Spacetime Residue
    ax5 = axes[4]
    ax5.plot(times, dissipation, color="#40C4FF", linewidth=2.2, label="Pathway 1: Dissipation back to Actor Field (J)")
    ax5.plot(times, residue, color="#E040FB", linewidth=2.2, linestyle="-.", label="Pathway 2: Spacetime Metric Residue $\\Delta g_{00}$")
    ax5.set_ylabel("Unacted Quantities", color="#40C4FF", fontsize=11, fontweight="bold")
    ax5.set_xlabel("Simulated Spacetime (seconds)", fontsize=12, fontweight="bold")
    ax5.set_title("Thermodynamics of the Unacted (Dissipation vs Gravitational Imprint)", fontsize=13, fontweight="bold", pad=8)
    ax5.legend(loc="upper left", framealpha=0.3)
    ax5.grid(True, linestyle=":", alpha=0.4)

    plt.savefig(output_image_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"[Success] Scientific telemetry plot exported to:\n  {os.path.abspath(output_image_path)}")


def main():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

    if not csv_files:
        print(f"[Notice] No CSV telemetry files found in {data_dir}. Run the simulation first to generate telemetry.")
        return

    # Sort to pick newest file
    csv_files.sort(key=os.path.getmtime, reverse=True)
    latest_csv = csv_files[0]
    out_img = os.path.join(data_dir, "telemetry_analysis.png")
    plot_telemetry(latest_csv, out_img)


if __name__ == "__main__":
    main()
