"""
Simple visualization using matplotlib for the AI City Simulation.
This provides a basic but functional visualization that works with any Mesa version.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from model import CityModel
from agent import CitizenAgent, Food, House, Job, Market, Workshop, Temple, School


def agent_color_map(agent):
    """Get color for agents based on their state."""
    if isinstance(agent, CitizenAgent):
        if agent.is_dead:
            return "gray"  # Dead agent
        elif agent.social >= agent.social_threshold:
            return "purple"  # Lonely agent
        elif agent.hunger >= agent.hunger_threshold:
            return "red"  # Very hungry
        elif agent.energy <= agent.energy_threshold:
            return "orange"  # Very tired
        elif agent.health < 50:
            return "darkred"  # Unhealthy
        else:
            return "blue"  # Normal
    elif isinstance(agent, Food):
        return "green"
    elif isinstance(agent, House):
        return "darkblue"
    elif isinstance(agent, Job):
        return "yellow"
    elif isinstance(agent, Market):
        return "gold"
    elif isinstance(agent, Workshop):
        return "brown"
    elif isinstance(agent, Temple):
        return "violet"
    elif isinstance(agent, School):
        return "cyan"
    return "black"


def draw_grid(model, ax):
    """Draw the grid with agents."""
    ax.clear()
    ax.set_xlim(0, model.width)
    ax.set_ylim(0, model.height)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(f"AI City Simulation - Step {model.schedule.steps}")
    
    # Draw all agents
    for cell in model.grid.coord_iter():
        cell_content, (x, y) = cell
        for agent in cell_content:
            color = agent_color_map(agent)
            
            if isinstance(agent, CitizenAgent):
                # Draw citizens as circles
                color = agent_color_map(agent)
                circle = patches.Circle((x + 0.5, y + 0.5), 0.3, 
                                      facecolor=color, edgecolor='black', alpha=0.8)
                
                # Add family outline if agent is in a family
                if agent.family_id is not None:
                    # Use family ID to generate consistent color
                    family_hash = hash(agent.family_id) % 6
                    family_colors = ['red', 'orange', 'purple', 'brown', 'pink', 'darkgreen']
                    family_color = family_colors[family_hash]
                    circle.set_edgecolor(family_color)
                    circle.set_linewidth(3)
                
                ax.add_patch(circle)
                
                # Add profession indicator (top) and personality traits (bottom)
                if hasattr(agent, 'profession') and agent.profession:
                    profession_abbrev = agent.profession[0].upper()  # First letter
                    ax.text(x + 0.5, y + 0.8, profession_abbrev, ha='center', va='center', 
                           fontsize=8, color='black', weight='bold')
                
                trait_text = "".join([t[0].upper() for t in agent.personality_traits])
                ax.text(x + 0.5, y + 0.2, trait_text, ha='center', va='center', 
                       fontsize=6, color='white', weight='bold')
                       
            elif isinstance(agent, Food):
                # Draw food as green squares
                rect = patches.Rectangle((x + 0.2, y + 0.2), 0.6, 0.6, 
                                       facecolor=color, edgecolor='black', alpha=0.8)
                ax.add_patch(rect)
            elif isinstance(agent, House):
                # Draw houses as large blue squares with H label
                rect = patches.Rectangle((x + 0.05, y + 0.05), 0.9, 0.9, 
                                       facecolor=color, edgecolor='black', alpha=0.8)
                ax.add_patch(rect)
                ax.text(x + 0.5, y + 0.5, 'H', ha='center', va='center', 
                       fontsize=12, color='white', weight='bold')
            elif isinstance(agent, Job):
                # Draw jobs as yellow squares with J label
                rect = patches.Rectangle((x + 0.2, y + 0.2), 0.6, 0.6, 
                                       facecolor=color, edgecolor='black', alpha=0.8)
                ax.add_patch(rect)
                ax.text(x + 0.5, y + 0.5, 'J', ha='center', va='center', 
                       fontsize=10, color='black', weight='bold')
            elif isinstance(agent, Market):
                # Draw markets as gold squares with M label
                rect = patches.Rectangle((x + 0.1, y + 0.1), 0.8, 0.8, 
                                       facecolor=color, edgecolor='black', alpha=0.8)
                ax.add_patch(rect)
                ax.text(x + 0.5, y + 0.5, 'M', ha='center', va='center', 
                       fontsize=12, color='black', weight='bold')
            elif isinstance(agent, Workshop):
                # Draw workshops as brown squares with W label
                rect = patches.Rectangle((x + 0.1, y + 0.1), 0.8, 0.8, 
                                       facecolor=color, edgecolor='black', alpha=0.8)
                ax.add_patch(rect)
                ax.text(x + 0.5, y + 0.5, 'W', ha='center', va='center', 
                       fontsize=12, color='white', weight='bold')
            elif isinstance(agent, Temple):
                # Draw temples as violet squares with T label
                rect = patches.Rectangle((x + 0.1, y + 0.1), 0.8, 0.8, 
                                       facecolor=color, edgecolor='black', alpha=0.8)
                ax.add_patch(rect)
                ax.text(x + 0.5, y + 0.5, 'T', ha='center', va='center', 
                       fontsize=12, color='white', weight='bold')
            elif isinstance(agent, School):
                # Draw schools as cyan squares with S label
                rect = patches.Rectangle((x + 0.1, y + 0.1), 0.8, 0.8, 
                                       facecolor=color, edgecolor='black', alpha=0.8)
                ax.add_patch(rect)
                ax.text(x + 0.5, y + 0.5, 'S', ha='center', va='center', 
                       fontsize=12, color='black', weight='bold')
    
    # Add enhanced stats text
    agents = [a for a in model.schedule.agents if isinstance(a, CitizenAgent)]
    alive_agents = [a for a in agents if not a.is_dead]
    dead_agents = [a for a in agents if a.is_dead]
    
    # Count all building types
    food_count = len([a for a in model.schedule.agents if isinstance(a, Food)])
    job_count = len([a for a in model.schedule.agents if isinstance(a, Job)])
    market_count = len([a for a in model.schedule.agents if isinstance(a, Market)])
    workshop_count = len([a for a in model.schedule.agents if isinstance(a, Workshop)])
    temple_count = len([a for a in model.schedule.agents if isinstance(a, Temple)])
    school_count = len([a for a in model.schedule.agents if isinstance(a, School)])
    
    if alive_agents:
        avg_hunger = sum(a.hunger for a in alive_agents) / len(alive_agents)
        avg_energy = sum(a.energy for a in alive_agents) / len(alive_agents)
        avg_health = sum(a.health for a in alive_agents) / len(alive_agents)
        avg_coins = sum(a.coins for a in alive_agents) / len(alive_agents)
        avg_social = sum(a.social for a in alive_agents) / len(alive_agents)
        
        # Calculate average skills
        avg_farming = sum(getattr(a, 'farming', 0) for a in alive_agents) / len(alive_agents)
        avg_crafting = sum(getattr(a, 'crafting', 0) for a in alive_agents) / len(alive_agents)
        avg_trading = sum(getattr(a, 'trading', 0) for a in alive_agents) / len(alive_agents)
        avg_learning = sum(getattr(a, 'learning', 0) for a in alive_agents) / len(alive_agents)
        
        # Count professions
        professions = {}
        for agent in alive_agents:
            prof = getattr(agent, 'profession', 'unemployed') or 'unemployed'
            professions[prof] = professions.get(prof, 0) + 1
        
        # Calculate average friendship score
        total_friendships = 0
        friendship_count = 0
        for agent in alive_agents:
            for friendship_score in agent.friendships.values():
                total_friendships += friendship_score
                friendship_count += 1
        avg_friendship = total_friendships / max(1, friendship_count)
        
        # Count interactions (approximate by counting close agents)
        interactions = 0
        for agent in alive_agents:
            cell_contents = model.grid.get_cell_list_contents([agent.pos])
            other_agents = [obj for obj in cell_contents 
                           if isinstance(obj, CitizenAgent) and obj != agent and not obj.is_dead]
            if other_agents:
                interactions += 1
        
        # Count families and children
        families = set()
        children_count = 0
        for agent in alive_agents:
            if agent.family_id:
                families.add(agent.family_id)
            if agent.age < 100:  # Consider young agents as children
                children_count += 1
        
        # Create profession summary
        prof_summary = ", ".join([f"{k}: {v}" for k, v in list(professions.items())[:3]])
        
        # PHASE 2: Technology and leadership info
        tech_count = len(getattr(model, 'technologies', set()))
        tech_level = getattr(model, 'technological_level', 1)
        leader_count = len(getattr(model, 'leaders', {}))
        trade_volume = getattr(model, 'trade_volume', 0)
        
        # PHASE 3: Cultural and advanced civilization info
        cultural_level = getattr(model, 'cultural_level', 1)
        art_works = getattr(model, 'art_works', 0)
        monuments = getattr(model, 'monuments', 0)
        conflicts = len(getattr(model, 'conflicts', []))
        alliances = len(getattr(model, 'alliances', []))
        scientific_discoveries = getattr(model, 'scientific_discoveries', 0)
        infrastructure_level = getattr(model, 'infrastructure_level', 1)
        
        # PHASE 4: Advanced psychological and social metrics
        total_happiness = getattr(model, 'total_happiness', 0)
        community_stress = getattr(model, 'community_stress_level', 0)
        cultural_masterpieces = getattr(model, 'cultural_masterpieces', 0)
        wisdom_accumulated = getattr(model, 'wisdom_accumulated', 0)
        teaching_relationships = getattr(model, 'teaching_relationships', 0)
        life_goal_achievements = getattr(model, 'life_goal_achievements', 0)
        social_cohesion = getattr(model, 'social_cohesion', 50)
        psychological_wellbeing = getattr(model, 'psychological_wellbeing', 50)
        education_quality = getattr(model, 'education_system_quality', 0)
        
        stats_text = f"""=== AI CITY SIMULATION (PHASE 4: ADVANCED PSYCHOLOGY) ===
Season: {model.season.title()} | Weather: {model.weather.title()}
Tech Level: {tech_level} | Discoveries: {tech_count}
Leaders: {leader_count} | Trade Volume: {trade_volume:.0f}

ADVANCED CIVILIZATION:
Culture Level: {cultural_level} | Art Works: {art_works}
Masterpieces: {cultural_masterpieces} | Research: {scientific_discoveries}
Infrastructure: {infrastructure_level:.1f} | Conflicts: {conflicts}
Alliances: {alliances}

PSYCHOLOGICAL WELLBEING:
Community Happiness: {total_happiness:.1f}/100
Community Stress: {community_stress:.1f}/100
Social Cohesion: {social_cohesion:.1f}/100
Psychological Health: {psychological_wellbeing:.1f}/100

KNOWLEDGE & WISDOM:
Wisdom Accumulated: {wisdom_accumulated:.1f}
Teaching Relationships: {teaching_relationships}
Education Quality: {education_quality:.1f}%
Life Goals Achieved: {life_goal_achievements}

POPULATION:
Alive: {len(alive_agents)} | Dead: {len(dead_agents)}
Families: {len(families)} | Children: {children_count}

BUILDINGS:
Food: {food_count} | Jobs: {job_count}
Markets: {market_count} | Workshops: {workshop_count}
Temples: {temple_count} | Schools: {school_count}

AVERAGES:
Hunger: {avg_hunger:.1f} | Energy: {avg_energy:.1f}
Health: {avg_health:.1f} | Coins: {avg_coins:.1f}
Social: {avg_social:.1f} | Friendship: {avg_friendship:.1f}

SKILLS:
Farm: {avg_farming:.1f} | Craft: {avg_crafting:.1f}
Trade: {avg_trading:.1f} | Learn: {avg_learning:.1f}

PROFESSIONS:
{prof_summary}

Active Interactions: {interactions}"""
    else:
        tech_count = len(getattr(model, 'technologies', set()))
        tech_level = getattr(model, 'technological_level', 1)
        leader_count = len(getattr(model, 'leaders', {}))
        cultural_level = getattr(model, 'cultural_level', 1)
        
        stats_text = f"""=== AI CITY SIMULATION (PHASE 3) ===
Season: {model.season.title()} | Weather: {model.weather.title()}
Tech Level: {tech_level} | Discoveries: {tech_count} | Leaders: {leader_count}
Culture Level: {cultural_level} | All agents dead!
Buildings: F:{food_count} J:{job_count} M:{market_count} W:{workshop_count} T:{temple_count} S:{school_count}"""
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))


def run_simulation():
    """Run the simulation with matplotlib visualization."""
    print("Starting AI City Simulation...")
    print("Close the window to stop the simulation")
    
    # Create model (SCALED UP POPULATION)
    model = CityModel(width=20, height=20, num_agents=50, num_food=60, num_houses=20, num_jobs=25)
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Add enhanced legend with new building types
    legend_elements = [
        patches.Circle((0, 0), 0.1, facecolor='blue', label='Normal Agent'),
        patches.Circle((0, 0), 0.1, facecolor='red', label='Hungry Agent'),
        patches.Circle((0, 0), 0.1, facecolor='orange', label='Tired Agent'),
        patches.Circle((0, 0), 0.1, facecolor='purple', label='Lonely Agent'),
        patches.Circle((0, 0), 0.1, facecolor='darkred', label='Unhealthy Agent'),
        patches.Circle((0, 0), 0.1, facecolor='gray', label='Dead Agent'),
        patches.Rectangle((0, 0), 0.1, 0.1, facecolor='green', label='Food'),
        patches.Rectangle((0, 0), 0.1, 0.1, facecolor='yellow', label='Job (J)'),
        patches.Rectangle((0, 0), 0.1, 0.1, facecolor='darkblue', label='House (H)'),
        patches.Rectangle((0, 0), 0.1, 0.1, facecolor='gold', label='Market (M)'),
        patches.Rectangle((0, 0), 0.1, 0.1, facecolor='brown', label='Workshop (W)'),
        patches.Rectangle((0, 0), 0.1, 0.1, facecolor='violet', label='Temple (T)'),
        patches.Rectangle((0, 0), 0.1, 0.1, facecolor='cyan', label='School (S)')
    ]
    
    def animate(frame):
        """Animation function for matplotlib."""
        model.step()
        draw_grid(model, ax)
        return []
    
    # Create animation
    ani = FuncAnimation(fig, animate, interval=500, blit=False, cache_frame_data=False)
    
    # Add legend to the figure
    fig.legend(handles=legend_elements, loc='upper right')
    
    # Show the plot
    plt.tight_layout()
    plt.show()
    
    return ani  # Return animation to keep it alive
