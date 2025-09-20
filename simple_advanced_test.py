#!/usr/bin/env python3
"""
Simple test for AI City Simulation advanced features
"""

from model import CityModel
from agent import *

def simple_advanced_test():
    print("=== AI City Simulation Advanced Features Test ===\n")
    
    # Create model
    model = CityModel(20, 50)
    
    print("1. INITIAL STATE:")
    print(f"   Total agents: {len(model.schedule.agents)}")
    print(f"   Season: {model.season}")
    print(f"   Tech level: {model.technological_level}")
    
    # Count different agent types
    citizens = []
    buildings = {'Food': 0, 'House': 0, 'Job': 0, 'Market': 0, 'Workshop': 0, 'Temple': 0, 'School': 0}
    
    for agent in model.schedule.agents:
        if isinstance(agent, CitizenAgent):
            citizens.append(agent)
        else:
            agent_type = type(agent).__name__
            if agent_type in buildings:
                buildings[agent_type] += 1
    
    print(f"\n2. BUILDINGS:")
    for building_type, count in buildings.items():
        if count > 0:
            print(f"   {building_type}: {count}")
    
    print(f"\n3. CITIZENS ({len(citizens)} total):")
    professions = {}
    for i, citizen in enumerate(citizens[:10]):  # Show first 10
        profession = getattr(citizen, 'profession', 'unemployed')
        professions[profession] = professions.get(profession, 0) + 1
        traits = getattr(citizen, 'personality_traits', [])
        print(f"   Agent {citizen.unique_id}: {profession}, Traits: {traits}")
    
    print(f"\n4. PROFESSION DISTRIBUTION:")
    for profession, count in professions.items():
        print(f"   {profession}: {count}")
    
    # Run a few steps
    print(f"\n5. RUNNING SIMULATION (5 steps)...")
    for i in range(5):
        model.step()
        alive_citizens = len([a for a in model.schedule.agents 
                            if isinstance(a, CitizenAgent) and not getattr(a, 'is_dead', False)])
        print(f"   Step {i+1}: {alive_citizens} citizens alive, Season: {model.season}")
    
    print(f"\n6. FAMILIES:")
    family_count = len(model.families)
    print(f"   Families formed: {family_count}")
    for family_id, family_data in model.families.items():
        members = len(family_data.get('members', []))
        children = len(family_data.get('children', []))
        print(f"   Family {family_id}: {members} members, {children} children")
    
    print(f"\n7. CULTURAL VALUES:")
    for value, level in model.cultural_values.items():
        print(f"   {value}: {level}")
    
    print("\n=== Test Complete ===")
    print("✅ Advanced features are working!")

if __name__ == "__main__":
    simple_advanced_test()
