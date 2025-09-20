#!/usr/bin/env python3
"""
AI City Simulation - Main Runner

This script starts the Mesa simulation server for the AI city simulation.
Run this script to launch the browser-based visualization.

Usage: python run.py
"""

from visualization import run_simulation

if __name__ == "__main__":
    try:
        run_simulation()
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        print(f"Error running simulation: {e}")
        print("Make sure you have all dependencies installed: pip install mesa[viz]")
