@echo off
setlocal enabledelayedexpansion

:: ============================================================================
::  NVIDIA Isaac Sim 5.0.1+ - The Actor Hypothesis Simulation Launcher
::  Simulating the Transduction of Conscious Intent and Cognitive Wave-Particle Duality
:: ============================================================================

set "ISAAC_SIM_DIR=D:\0-NVIDIA-Omniverse\isaac-sim"
set "PYTHON_BAT=%ISAAC_SIM_DIR%\python.bat"
set "ISAAC_BAT=%ISAAC_SIM_DIR%\isaac-sim.bat"
set "USDA_SCENE=%~dp0models\usd\actor_hypothesis_scene.usda"

if not exist "%PYTHON_BAT%" (
    echo [ERROR] Could not find Isaac Sim python launcher at:
    echo         %PYTHON_BAT%
    echo Please verify your Isaac Sim installation path.
    pause
    exit /b 1
)

if not "%~1"=="" goto RunCustomArgs

echo ============================================================================
echo   THE ACTOR HYPOTHESIS - NVIDIA ISAAC SIM SIMULATION
echo ============================================================================
echo   Note: GUI scenarios run CONTINUOUSLY so you can inspect the 3D scene.
echo         Close the Isaac Sim window or press Ctrl+C in terminal to finish.
echo ============================================================================
echo   1. Full Transduction Chain [Thought Wave to Collapse to Robotic Action]
echo   2. Pathway 1: Daydream Dissipation [Return to Actor Field]
echo   3. Pathway 2: Spacetime Residue [Cumulative Gravitational Footprint]
echo   4. Testable Vector 2: Anesthesia Disruption [Severed Bridge]
echo   5. Automated Headless Test Suite [Verification and Invariants]
echo   6. Open Exported USDA Scene in Isaac Sim GUI Viewport [Direct Inspection]
echo   7. Generate Scientific Telemetry Plots [PNG graphs of S, EG, Work, Residue]
echo   8. Custom Arguments / Duration Override
echo ============================================================================

set "CHOICE=1"
set /p "CHOICE=Select simulation scenario to run [1-8] (Default: 1): "

:: Clean input: strip dots and spaces
set "CHOICE=%CHOICE:.=%"
set "CHOICE=%CHOICE: =%"

if "%CHOICE%"=="1" goto Case1
if "%CHOICE%"=="2" goto Case2
if "%CHOICE%"=="3" goto Case3
if "%CHOICE%"=="4" goto Case4
if "%CHOICE%"=="5" goto Case5
if "%CHOICE%"=="6" goto Case6
if "%CHOICE%"=="7" goto Case7
if "%CHOICE%"=="8" goto Case8

echo [WARNING] Unrecognized choice "%CHOICE%". Defaulting to Scenario 1...
goto Case1

:Case1
echo [LAUNCHING] Scenario 1: Full Transduction Chain [Continuous GUI]...
call "%PYTHON_BAT%" run_simulation.py --mode collapse --duration -1
goto End

:Case2
echo [LAUNCHING] Scenario 2: Pathway 1 - Daydream Dissipation [Continuous GUI]...
call "%PYTHON_BAT%" run_simulation.py --mode daydream --duration -1
goto End

:Case3
echo [LAUNCHING] Scenario 3: Pathway 2 - Spacetime Residue [Continuous GUI]...
call "%PYTHON_BAT%" run_simulation.py --mode residue --duration -1
goto End

:Case4
echo [LAUNCHING] Scenario 4: Testable Vector 2 - Anesthesia Disruption [Continuous GUI]...
call "%PYTHON_BAT%" run_simulation.py --mode anesthesia --duration -1
goto End

:Case5
echo [LAUNCHING] Running Automated Verification Test Suite...
call "%PYTHON_BAT%" test_simulation.py
goto End

:Case6
echo [LAUNCHING] Opening USDA Scene directly in Isaac Sim GUI:
echo            %USDA_SCENE%
call "%ISAAC_BAT%" "%USDA_SCENE%"
goto End

:Case7
echo [LAUNCHING] Generating Scientific Telemetry Analysis Plot...
call "%PYTHON_BAT%" visualize_telemetry.py
goto End

:Case8
set "EXTRA_ARGS="
set /p "EXTRA_ARGS=Enter command-line arguments (e.g. --mode residue --duration 30): "
call "%PYTHON_BAT%" run_simulation.py !EXTRA_ARGS!
goto End

:RunCustomArgs
call "%PYTHON_BAT%" run_simulation.py %*
goto End

:End
echo.
echo ============================================================================
echo Operation finished.
echo Telemetry data saved in:  %~dp0data\
echo OpenUSD scene saved in:   %USDA_SCENE%
echo ============================================================================
pause
endlocal
