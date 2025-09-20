#!/usr/bin/env python3
"""
Test script to verify family and community system functionality.
Creates a smaller, easier simulation to test family formation.
"""

import random
from model import CityModel
from agent import CitizenAgent

def test_family_system():
    """Test family formation with easier survival conditions."""
    print("Testing Family & Community System...")
    
    # Create a smaller model with more resources
    model = CityModel(width=10, height=10, num_agents=6, num_food=20, num_houses=5, num_jobs=8)
    
    # Manually boost friendship between some agents to test family formation
    agents = [a for a in model.agents if isinstance(a, CitizenAgent)]
    
    if len(agents) >= 4:
        # Create two potential couples by boosting friendships
        agent1, agent2 = agents[0], agents[1]  
        agent3, agent4 = agents[2], agents[3]
        
        # Make sure they have opposite genders
        agent1.gender = 'male'
        agent2.gender = 'female'
        agent3.gender = 'male' 
        agent4.gender = 'female'
        
        # Boost friendship scores to trigger family formation
        agent1.friendships[agent2.unique_id] = 70
        agent2.friendships[agent1.unique_id] = 70
        agent3.friendships[agent4.unique_id] = 65
        agent4.friendships[agent3.unique_id] = 65
        
        # Give them better health to survive longer
        for agent in agents:
            agent.coins = 10  # More starting coins
            agent.hunger = 20  # Less hungry
            agent.energy = 80  # More energetic
            agent.health = 100
        
        print(f"Set up potential families:")
        print(f"  Couple 1: Agent {agent1.unique_id} ({agent1.gender}) + Agent {agent2.unique_id} ({agent2.gender})")
        print(f"  Couple 2: Agent {agent3.unique_id} ({agent3.gender}) + Agent {agent4.unique_id} ({agent4.gender})")
        print(f"Starting simulation for 100 steps...")
        
        # Run simulation
        families_formed = set()
        children_born = []
        
        for step in range(100):
            model.step()
            
            # Check for new families
            for agent in agents:
                if agent.family_id and agent.family_id not in families_formed:
                    families_formed.add(agent.family_id)
                    partner = model.get_agent_by_id(agent.partner_id)
                    print(f"Step {step}: Family formed! {agent.family_id}")
                    print(f"  Members: Agent {agent.unique_id} + Agent {partner.unique_id}")
                
                # Check for children
                if len(agent.children) > len([c for c in children_born if c[1] == agent.unique_id]):
                    for child_id in agent.children:
                        if not any(c[0] == child_id for c in children_born):
                            children_born.append((child_id, agent.unique_id))
                            child = model.get_agent_by_id(child_id)
                            print(f"Step {step}: Child born! Agent {child_id}")
                            print(f"  Parents: Agent {agent.unique_id} + Agent {agent.partner_id}")
                            print(f"  Child traits: {child.personality_traits}")
            
            # Print periodic status
            if step % 25 == 0:
                alive_count = len([a for a in agents if not a.is_dead])
                family_count = len(families_formed)
                children_count = len(children_born)
                print(f"Step {step}: {alive_count} alive, {family_count} families, {children_count} children")
        
        print(f"\nFinal Results:")
        print(f"  Families formed: {len(families_formed)}")
        print(f"  Children born: {len(children_born)}")
        print(f"  Agents alive: {len([a for a in agents if not a.is_dead])}")
        
        return len(families_formed) > 0 or len(children_born) > 0
    
    else:
        print("Not enough agents to test family formation")
        return False

if __name__ == "__main__":
    success = test_family_system()
    if success:
        print("\n✅ Family system is working!")
    else:
        print("\n❌ Family system needs debugging")
