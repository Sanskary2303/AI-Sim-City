#!/usr/bin/env python3
"""
Simple test to verify Mesa is working
"""

from mesa import Model, Agent
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


class SimpleAgent(Agent):
    """A simple agent."""
    
    def __init__(self, model):
        super().__init__(model)
    
    def step(self):
        """Move randomly."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        if possible_steps:
            new_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)


class SimpleModel(Model):
    """A simple model."""
    
    def __init__(self, width=10, height=10, num_agents=5):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.steps = 0
        
        # Create agents
        for i in range(num_agents):
            agent = SimpleAgent(self)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
    
    def step(self):
        """Execute one step."""
        self.steps += 1
        for agent in self.agents:
            agent.step()


def test_mesa():
    """Test if Mesa is working."""
    print("Testing Mesa...")
    model = SimpleModel()
    print("Model created successfully!")
    
    model.step()
    print("Step executed successfully!")
    
    # Simple visualization
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, model.grid.width)
    ax.set_ylim(0, model.grid.height)
    ax.grid(True)
    ax.set_title("Simple Mesa Test")
    
    # Draw agents
    for agent in model.agents:
        if agent.pos:
            x, y = agent.pos
            circle = patches.Circle((x + 0.5, y + 0.5), 0.3, facecolor='blue')
            ax.add_patch(circle)
    
    plt.show()
    print("Visualization shown!")


if __name__ == "__main__":
    test_mesa()
