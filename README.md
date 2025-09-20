# AI City Simulation

A lightweight Python simulation where multiple AI agents live in a 2D grid city. Each agent has simple needs (hunger, energy) and takes actions (move, eat, sleep) based on basic decision rules.

## Features

- **20x20 grid city** with agents, food, and houses
- **Intelligent agents** that make decisions based on hunger and energy levels
- **Real-time browser visualization** using Mesa's CanvasGrid
- **Simple learning** through random exploration
- **Interactive controls** to adjust simulation parameters

## Agent Behavior

Each citizen agent has:
- **Hunger level** (increases each step)
- **Energy level** (decreases each step)

Decision rules:
1. If very hungry (hunger ≥ 80) → seek nearest food
2. If very tired (energy ≤ 20) → seek nearest house to sleep
3. Otherwise → move randomly
4. 20% chance to explore randomly regardless of needs

## Visualization

- **Agents**: Colored circles
  - Blue: Normal state
  - Red: Very hungry
  - Orange: Very tired
- **Food**: Green squares
- **Houses**: Dark blue squares

## Requirements

- Python 3.7+
- Mesa
- NumPy
- Matplotlib

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulation

```bash
python run.py
```

This will:
1. Start the Mesa server
2. Open your browser to `http://localhost:8521`
3. Show the simulation with real-time visualization
4. Allow you to adjust parameters and control the simulation

## Controls

- **Start/Stop**: Control simulation execution
- **Step**: Execute one simulation step
- **Reset**: Reset the simulation with new parameters
- **Sliders**: Adjust number of agents, food, and houses

## Project Structure

```
AI_sim/
├── agent.py          # Agent classes (CitizenAgent, Food, House)
├── model.py          # CityModel class (simulation logic)
├── visualization.py  # Mesa visualization setup
├── run.py           # Main script to start simulation
├── requirements.txt # Python dependencies
└── README.md       # This file
```

## Future Enhancements

- Add more complex agent memory
- Implement simple reinforcement learning
- Add agent communication
- Include more environmental factors
- Add agent reproduction/death mechanics
