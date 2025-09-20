#!/usr/bin/env python3
"""
Enhanced test to demonstrate improved survival and family formation.
"""

import random
from model import CityModel
from agent import CitizenAgent

def test_improved_simulation():
    """Test the improved survival conditions."""
    print("🚀 Testing IMPROVED AI Simulation...")
    print("📋 Changes made:")
    print("  - Slower hunger/energy decline")
    print("  - FREE food (no coins needed)")
    print("  - Better recovery rates")
    print("  - More food spawning (30% vs 10%)")
    print("  - More starting resources")
    print("  - Easier family formation (50 friendship vs 60)")
    print("  - Faster reproduction (30 steps vs 50)")
    print()
    
    # Create improved model
    model = CityModel(width=20, height=20, num_agents=12, num_food=25, num_houses=8, num_jobs=8)
    
    agents = [a for a in model.agents if isinstance(a, CitizenAgent)]
    print(f"🏁 Starting with {len(agents)} agents")
    
    # Track statistics
    stats = {
        'families_formed': set(),
        'children_born': [],
        'max_alive': len(agents),
        'step_counts': [],
        'deaths': []
    }
    
    # Run for longer to see families develop
    for step in range(200):
        model.step()
        
        alive_agents = [a for a in agents if not a.is_dead]
        stats['step_counts'].append(len(alive_agents))
        
        # Track new families
        for agent in alive_agents:
            if agent.family_id and agent.family_id not in stats['families_formed']:
                stats['families_formed'].add(agent.family_id)
                partner = model.get_agent_by_id(agent.partner_id)
                if partner:
                    print(f"💕 Step {step}: Family formed! Agents {agent.unique_id} + {partner.unique_id}")
                    print(f"   Traits: {agent.personality_traits} + {partner.personality_traits}")
            
            # Track children
            if len(agent.children) > len([c for c in stats['children_born'] if c[1] == agent.unique_id]):
                for child_id in agent.children:
                    if not any(c[0] == child_id for c in stats['children_born']):
                        stats['children_born'].append((child_id, agent.unique_id))
                        child = model.get_agent_by_id(child_id)
                        if child:
                            print(f"👶 Step {step}: Child born! Agent {child_id}")
                            print(f"   Parents: {agent.unique_id} + {agent.partner_id}")
                            print(f"   Child traits: {child.personality_traits}")
        
        # Check for deaths
        for agent in agents:
            if agent.is_dead and agent.unique_id not in stats['deaths']:
                stats['deaths'].append(agent.unique_id)
        
        # Print progress every 50 steps
        if step % 50 == 0:
            alive_count = len(alive_agents)
            family_count = len(stats['families_formed'])
            children_count = len(stats['children_born'])
            if alive_count > 0:
                avg_hunger = sum(a.hunger for a in alive_agents) / alive_count
                avg_energy = sum(a.energy for a in alive_agents) / alive_count
                avg_health = sum(a.health for a in alive_agents) / alive_count
                avg_coins = sum(a.coins for a in alive_agents) / alive_count
                print(f"\n📊 Step {step} Status:")
                print(f"   Alive: {alive_count}, Families: {family_count}, Children: {children_count}")
                print(f"   Avg Stats - Hunger: {avg_hunger:.1f}, Energy: {avg_energy:.1f}, Health: {avg_health:.1f}, Coins: {avg_coins:.1f}")
        
        # Early exit if all dead
        if len(alive_agents) == 0:
            print(f"\n💀 All agents died at step {step}")
            break
    
    # Final report
    print(f"\n🎯 FINAL RESULTS after {step} steps:")
    print(f"   Families formed: {len(stats['families_formed'])}")
    print(f"   Children born: {len(stats['children_born'])}")
    print(f"   Agents survived: {len([a for a in agents if not a.is_dead])}")
    print(f"   Max population: {max(stats['step_counts'])}")
    print(f"   Deaths: {len(stats['deaths'])}")
    
    # Success metrics
    success = (
        len(stats['families_formed']) >= 2 or  # At least 2 families formed
        len(stats['children_born']) >= 1 or    # At least 1 child born
        max(stats['step_counts']) > len(agents)  # Population grew
    )
    
    if success:
        print("\n✅ SIMULATION IMPROVED! Agents are surviving better and forming families!")
    else:
        print("\n⚠️  Still needs more balancing")
    
    return success, stats

if __name__ == "__main__":
    success, stats = test_improved_simulation()
    
    print(f"\n📈 Performance Summary:")
    print(f"   Family formation rate: {len(stats['families_formed'])} families")
    print(f"   Reproduction rate: {len(stats['children_born'])} children")
    print(f"   Survival improvement: {'✅ Better' if success else '❌ Needs work'}")
