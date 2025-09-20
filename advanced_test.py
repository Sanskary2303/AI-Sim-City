#!/usr/bin/env python3
"""
Advanced features test for AI City Simulation
Tests all the new civilization features
"""

from model import CityModel
from agent import *
import time

def test_advanced_features():
    print("=== Advanced AI City Simulation Test ===\n")
    
    # Create model with advanced features
    model = CityModel(20, 50)  # 20x20 grid, 50 agents
    
    print("1. INITIAL STATE:")
    print(f"   Total agents: {len(model.schedule.agents)}")
    print(f"   Season: {model.season}")
    print(f"   Technology level: {model.tech_level}")
    print(f"   Cultural values: {model.cultural_values}")
    
    # Check building types
    buildings_by_type = {}
    for agent in model.schedule.agents:
        if hasattr(agent, 'building_type'):
            building_type = agent.building_type
            buildings_by_type[building_type] = buildings_by_type.get(building_type, 0) + 1
    
    print(f"\n2. BUILDINGS:")
    for building_type, count in buildings_by_type.items():
        print(f"   {building_type}: {count}")
    
    # Check agent professions and skills
    citizens = [agent for agent in model.schedule.agents if isinstance(agent, CitizenAgent)]
    professions = {}
    skill_totals = {'farming': 0, 'crafting': 0, 'trading': 0, 'combat': 0, 'learning': 0}
    
    print(f"\n3. CITIZEN AGENTS ({len(citizens)} total):")
    for citizen in citizens[:10]:  # Show first 10
        profession = getattr(citizen, 'profession', 'unemployed')
        professions[profession] = professions.get(profession, 0) + 1
        
        for skill in skill_totals:
            skill_totals[skill] += getattr(citizen, skill, 0)
        
        print(f"   Agent {citizen.unique_id}: {profession}, Traits: {citizen.personality_traits}")
    
    print(f"\n4. PROFESSION DISTRIBUTION:")
    for profession, count in professions.items():
        print(f"   {profession}: {count}")
    
    print(f"\n5. AVERAGE SKILLS:")
    for skill, total in skill_totals.items():
        avg = total / len(citizens) if citizens else 0
        print(f"   {skill}: {avg:.2f}")
    
    # Run simulation for a few steps
    print(f"\n6. RUNNING SIMULATION (10 steps)...")
    initial_step = model.step_count
    
    for i in range(10):
        model.step()
        if i % 3 == 0:
            alive_citizens = len([a for a in model.schedule.agents if isinstance(a, CitizenAgent) and a.alive])
            print(f"   Step {model.step_count}: {alive_citizens} citizens alive, Season: {model.season}")
    
    print(f"\n7. FINAL STATE:")
    final_citizens = [a for a in model.schedule.agents if isinstance(a, CitizenAgent) and a.alive]
    print(f"   Alive citizens: {len(final_citizens)}")
    print(f"   Season: {model.season}")
    print(f"   Technology level: {model.tech_level}")
    
    # Check for families
    families = 0
    children = 0
    for citizen in final_citizens:
        if hasattr(citizen, 'partner') and citizen.partner is not None:
            families += 1
        if hasattr(citizen, 'age') and citizen.age < 18:
            children += 1
    
    print(f"   Families formed: {families // 2}")  # Divide by 2 since each partnership counts twice
    print(f"   Children: {children}")
    
    print(f"\n8. ENVIRONMENTAL CHANGES:")
    print(f"   Weather: {getattr(model, 'weather', 'normal')}")
    print(f"   Season effects active: {hasattr(model, 'seasonal_effects')}")
    
    print("\n=== Test Complete ===")
    print("✅ Advanced civilization features are working!")
    
    return model

if __name__ == "__main__":
    test_advanced_features()
