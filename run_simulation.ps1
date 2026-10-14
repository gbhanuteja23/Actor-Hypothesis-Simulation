# ============================================================================
#  NVIDIA Isaac Sim 5.0.1+ - The Actor Hypothesis Simulation Launcher (PowerShell)
#  Simulating the Transduction of Conscious Intent and Cognitive Wave-Particle Duality
# ============================================================================

param(
    [string]$Mode,
    [double]$Duration,
    [double]$Focus,
    [switch]$Headless
)

$IsaacSimDir = "D:\0-NVIDIA-Omniverse\isaac-sim"
$PythonBat   = Join-Path $IsaacSimDir "python.bat"
$IsaacBat    = Join-Path $IsaacSimDir "isaac-sim.bat"
$ScriptDir   = $PSScriptRoot
$UsdScene    = Join-Path $ScriptDir "models\usd\actor_hypothesis_scene.usda"

if (-not (Test-Path $PythonBat)) {
    Write-Host "[ERROR] Could not find Isaac Sim python launcher at: $PythonBat" -ForegroundColor Red
    exit 1
}

# If arguments were passed directly, forward them
if ($PSBoundParameters.Count -gt 0) {
    $cliArgs = @("run_simulation.py")
    if ($Mode) { $cliArgs += "--mode"; $cliArgs += $Mode }
    if ($Duration) { $cliArgs += "--duration"; $cliArgs += $Duration }
    if ($Focus) { $cliArgs += "--focus"; $cliArgs += $Focus }
    if ($Headless) { $cliArgs += "--headless" }
    & $PythonBat $cliArgs
    exit $LASTEXITCODE
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  THE ACTOR HYPOTHESIS - NVIDIA ISAAC SIM SIMULATION" -ForegroundColor White
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  Note: GUI scenarios run CONTINUOUSLY so you can inspect the 3D scene." -ForegroundColor Yellow
Write-Host "        Close the Isaac Sim window or press Ctrl+C in terminal to finish." -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  1. Full Transduction Chain [Thought Wave -> Collapse -> Robotic Action]"
Write-Host "  2. Pathway 1: Daydream Dissipation [Return to Actor Field]"
Write-Host "  3. Pathway 2: Spacetime Residue [Cumulative Gravitational Footprint]"
Write-Host "  4. Testable Vector 2: Anesthesia Disruption [Severed Bridge]"
Write-Host "  5. Automated Headless Test Suite [Verification and Invariants]"
Write-Host "  6. Open Exported USDA Scene in Isaac Sim GUI Viewport [Direct Inspection]"
Write-Host "  7. Generate Scientific Telemetry Plots [PNG graphs]"
Write-Host "  8. Custom Arguments / Duration Override"
Write-Host "============================================================================" -ForegroundColor Cyan

$Choice = Read-Host "Select simulation scenario to run [1-8] (Default: 1)"
if ([string]::IsNullOrWhiteSpace($Choice)) { $Choice = "1" }
$Choice = $Choice.Trim().TrimEnd('.')

switch ($Choice) {
    "1" {
        Write-Host "[LAUNCHING] Scenario 1: Full Transduction Chain (Continuous GUI)..." -ForegroundColor Green
        & $PythonBat run_simulation.py --mode collapse --duration -1
    }
    "2" {
        Write-Host "[LAUNCHING] Scenario 2: Pathway 1 - Daydream Dissipation (Continuous GUI)..." -ForegroundColor Green
        & $PythonBat run_simulation.py --mode daydream --duration -1
    }
    "3" {
        Write-Host "[LAUNCHING] Scenario 3: Pathway 2 - Spacetime Residue (Continuous GUI)..." -ForegroundColor Green
        & $PythonBat run_simulation.py --mode residue --duration -1
    }
    "4" {
        Write-Host "[LAUNCHING] Scenario 4: Testable Vector 2 - Anesthesia Disruption (Continuous GUI)..." -ForegroundColor Green
        & $PythonBat run_simulation.py --mode anesthesia --duration -1
    }
    "5" {
        Write-Host "[LAUNCHING] Running Automated Verification Test Suite..." -ForegroundColor Green
        & $PythonBat test_simulation.py
    }
    "6" {
        Write-Host "[LAUNCHING] Opening USDA Scene directly in Isaac Sim GUI Viewport..." -ForegroundColor Green
        Write-Host "           $UsdScene" -ForegroundColor Gray
        & $IsaacBat "$UsdScene"
    }
    "7" {
        Write-Host "[LAUNCHING] Generating Scientific Telemetry Analysis Plot..." -ForegroundColor Green
        & $PythonBat visualize_telemetry.py
    }
    "8" {
        $extraArgs = Read-Host "Enter command-line arguments (e.g. --mode residue --duration 20)"
        & $PythonBat run_simulation.py ($extraArgs -split ' ')
    }
    default {
        Write-Host "[WARNING] Unrecognized option '$Choice'. Running Scenario 1..." -ForegroundColor Yellow
        & $PythonBat run_simulation.py --mode collapse --duration -1
    }
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Operation finished." -ForegroundColor Green
Write-Host "Telemetry data saved in:  $ScriptDir\data\" -ForegroundColor White
Write-Host "OpenUSD scene saved in:   $UsdScene" -ForegroundColor White
Write-Host "============================================================================" -ForegroundColor Cyan
