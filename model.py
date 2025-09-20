import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import CitizenAgent, Food, House, Job, Market, Workshop, Temple, School


class CityModel(Model):
    """A model representing a simple city with agents, food, and houses."""
    
    def __init__(self, width=20, height=20, num_agents=50, num_food=60, num_houses=20, num_jobs=25):
        super().__init__()
        
        # Model parameters (SCALED UP FOR LARGER POPULATION)
        self.width = width
        self.height = height
        self.num_agents = num_agents  # Increased from 10 to 50
        self.num_food = num_food  # Increased from 25 to 60
        self.num_houses = num_houses  # Increased from 8 to 20
        self.num_jobs = num_jobs  # Increased from 8 to 25
        
        # Create grid 
        self.grid = MultiGrid(width, height, torus=False)
        
        # Track unique IDs
        self.next_id = 0
        self.steps = 0
        
        # Family and community tracking
        self.families = {}  # {family_id: {'members': [agent_ids], 'children': [agent_ids]}}
        self.communities = {}  # {community_id: {'center': (x,y), 'agents': [agent_ids], 'dominant_trait': str}}
        
        # Advanced buildings (SCALED UP)
        self.num_markets = 5      # Increased from 2 to 5
        self.num_workshops = 4    # Increased from 2 to 4
        self.num_temples = 3      # Increased from 1 to 3
        self.num_schools = 2      # Increased from 1 to 2
        
        # Weather and seasonal system
        self.season = 'spring'
        self.season_cycle = 0
        self.weather = 'normal'  # normal, rain, drought, storm
        self.technological_level = 1
        self.cultural_values = {'cooperation': 50, 'individualism': 50, 'tradition': 50}
        
        # Technology progression system (PHASE 2)
        self.technologies = set()  # Discovered technologies
        self.technology_points = 0  # Accumulated through learning
        self.tech_tree = {
            'agriculture': {'cost': 50, 'prereq': None, 'benefits': 'food_boost'},
            'craftsmanship': {'cost': 100, 'prereq': 'agriculture', 'benefits': 'workshop_efficiency'},
            'trade_routes': {'cost': 150, 'prereq': 'craftsmanship', 'benefits': 'market_bonus'},
            'education': {'cost': 200, 'prereq': 'trade_routes', 'benefits': 'learning_boost'},
            'metallurgy': {'cost': 250, 'prereq': 'education', 'benefits': 'tool_efficiency'},
            'governance': {'cost': 300, 'prereq': 'metallurgy', 'benefits': 'leadership_system'},
            # PHASE 3 TECHNOLOGIES
            'philosophy': {'cost': 400, 'prereq': 'governance', 'benefits': 'cultural_growth'},
            'military': {'cost': 450, 'prereq': 'governance', 'benefits': 'defense_system'},
            'engineering': {'cost': 500, 'prereq': 'metallurgy', 'benefits': 'infrastructure'},
            'medicine': {'cost': 550, 'prereq': 'philosophy', 'benefits': 'health_boost'},
            'astronomy': {'cost': 600, 'prereq': 'philosophy', 'benefits': 'navigation'},
            'mathematics': {'cost': 650, 'prereq': 'astronomy', 'benefits': 'advanced_research'}
        }
        
        # Resource scarcity and trade system (PHASE 2)
        self.resource_prices = {'food': 1, 'tools': 5, 'luxury': 10}
        self.global_resources = {'food': 100, 'tools': 50, 'luxury': 20}
        self.trade_volume = 0
        
        # Leadership and social hierarchy (PHASE 2)
        self.leaders = {}  # {community_id: agent_id}
        self.social_rankings = {}  # {agent_id: influence_score}
        self.policies = []  # Active community policies
        
        # PHASE 3: Cultural development
        self.cultural_level = 1
        self.cultural_achievements = []
        self.art_works = 0
        self.monuments = 0
        self.festivals_held = 0
        self.philosophical_schools = []
        
        # PHASE 3: Warfare and conflicts
        self.conflicts = []
        self.alliances = []
        self.peace_treaties = []
        self.military_strength = 0
        self.conflicts_resolved = 0
        
        # PHASE 3: Advanced infrastructure
        self.infrastructure_level = 1
        self.trade_routes_established = []
        self.road_network = set()  # Set of connected coordinates
        
        # PHASE 3: Research and innovation
        self.research_projects = []
        self.innovations = []
        self.scientific_discoveries = 0
        
        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Total Agents": lambda m: len([a for a in m.agents if isinstance(a, CitizenAgent)]),
                "Alive Agents": lambda m: len([a for a in m.agents if isinstance(a, CitizenAgent) and not a.is_dead]),
                "Dead Agents": lambda m: len([a for a in m.agents if isinstance(a, CitizenAgent) and a.is_dead]),
                "Average Hunger": lambda m: self.get_average_hunger(),
                "Average Energy": lambda m: self.get_average_energy(),
                "Average Health": lambda m: self.get_average_health(),
                "Average Social": lambda m: self.get_average_social(),
                "Average Coins": lambda m: self.get_average_coins(),
                "Average Friendship": lambda m: self.get_average_friendship(),
                "Food Count": lambda m: len([a for a in m.agents if isinstance(a, Food)]),
                "Job Count": lambda m: len([a for a in m.agents if isinstance(a, Job)]),
                "Market Count": lambda m: len([a for a in m.agents if isinstance(a, Market)]),
                "Workshop Count": lambda m: len([a for a in m.agents if isinstance(a, Workshop)]),
                "Temple Count": lambda m: len([a for a in m.agents if isinstance(a, Temple)]),
                "School Count": lambda m: len([a for a in m.agents if isinstance(a, School)]),
                "Interactions": lambda m: self.count_interactions(),
                "Families": lambda m: self.update_family_stats()[0],
                "Children": lambda m: self.update_family_stats()[1],
            }
        )
        
        # Create environment objects
        self.create_houses()
        self.create_jobs()
        self.create_advanced_buildings()  # NEW: Create markets, workshops, temples, schools
        self.create_initial_food()
        
        # Initialize communities based on house/job clusters
        self.initialize_communities()
        
        # Create agents
        self.create_agents()
        
        # Start data collection
        self.datacollector.collect(self)
        
        self.running = True
        
    def get_next_id(self):
        """Get the next unique ID for agents."""
        current_id = self.next_id
        self.next_id += 1
        return current_id
    
    def create_houses(self):
        """Create houses randomly distributed in the city."""
        for _ in range(self.num_houses):
            # Find an empty location
            attempts = 0
            while attempts < 100:  # Avoid infinite loop
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                
                if self.grid.is_cell_empty((x, y)):
                    house = House(self)
                    self.grid.place_agent(house, (x, y))
                    break
                attempts += 1
    
    def create_jobs(self):
        """Create job locations randomly distributed in the city."""
        for _ in range(self.num_jobs):
            # Find an empty location
            attempts = 0
            while attempts < 100:  # Avoid infinite loop
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                
                if self.grid.is_cell_empty((x, y)):
                    job = Job(self)
                    self.grid.place_agent(job, (x, y))
                    break
                attempts += 1
    
    def create_advanced_buildings(self):
        """Create advanced buildings: markets, workshops, temples, schools."""
        # Create markets
        for _ in range(self.num_markets):
            attempts = 0
            while attempts < 100:
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                if self.grid.is_cell_empty((x, y)):
                    market = Market(self)
                    self.grid.place_agent(market, (x, y))
                    break
                attempts += 1
        
        # Create workshops
        for _ in range(self.num_workshops):
            attempts = 0
            while attempts < 100:
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                if self.grid.is_cell_empty((x, y)):
                    workshop = Workshop(self)
                    self.grid.place_agent(workshop, (x, y))
                    break
                attempts += 1
        
        # Create temples
        for _ in range(self.num_temples):
            attempts = 0
            while attempts < 100:
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                if self.grid.is_cell_empty((x, y)):
                    temple = Temple(self)
                    self.grid.place_agent(temple, (x, y))
                    break
                attempts += 1
        
        # Create schools
        for _ in range(self.num_schools):
            attempts = 0
            while attempts < 100:
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                if self.grid.is_cell_empty((x, y)):
                    school = School(self)
                    self.grid.place_agent(school, (x, y))
                    break
                attempts += 1
    
    def create_initial_food(self):
        """Create initial food distribution."""
        for _ in range(self.num_food):
            self.spawn_food()
    
    def spawn_food(self):
        """Spawn a single food item at a random empty location."""
        attempts = 0
        while attempts < 100:  # Avoid infinite loop
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            
            # Check if location is suitable for food (not on a house)
            cell_contents = self.grid.get_cell_list_contents([(x, y)])
            has_house = any(isinstance(obj, House) for obj in cell_contents)
            
            if not has_house:
                food = Food(self)
                self.grid.place_agent(food, (x, y))
                break
            attempts += 1
    
    def create_agents(self):
        """Create citizen agents and place them randomly in the city."""
        for _ in range(self.num_agents):
            agent = CitizenAgent(self)
            
            # Find a location for the agent
            attempts = 0
            while attempts < 100:  # Avoid infinite loop
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                
                # Agents can be placed anywhere
                self.grid.place_agent(agent, (x, y))
                break
    
    def step(self):
        """Execute one step of the model."""
        # Update weather and seasonal effects
        self.update_weather_and_seasons()
        
        # PHASE 2: Technology and leadership progression
        self.advance_technology()
        self.update_resource_economy()
        self.process_leadership_actions()
        
        # PHASE 3: Advanced civilization systems
        self.advance_culture()
        self.manage_conflicts()
        self.develop_infrastructure()
        self.conduct_research()
        
        # Execute all agents
        agents_copy = list(self.agents)  # Copy to avoid modification during iteration
        for agent in agents_copy:
            if agent in self.agents:  # Check if agent still exists
                agent.step()
        
        # Weather-affected food spawning with technology bonus
        base_food_chance = 0.3
        if 'agriculture' in self.technologies:
            base_food_chance *= 1.5  # Agriculture tech boosts food production
            
        if self.weather == 'rain':
            food_chance = base_food_chance * 1.5  # Rain boosts food growth
        elif self.weather == 'drought':
            food_chance = base_food_chance * 0.3  # Drought reduces food
        elif self.weather == 'storm':
            food_chance = base_food_chance * 0.1  # Storms severely limit food
        else:
            food_chance = base_food_chance
        
        if random.random() < food_chance:
            self.spawn_food()
            
        # Occasionally spawn extra food when population is high
        alive_agents = len([a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead])
        if alive_agents > 5 and random.random() < 0.2:
            self.spawn_food()  # Extra food for large populations
        
        # Increment step counter
        self.steps += 1
        
        # Collect data
        self.datacollector.collect(self)
    
    def remove_agent(self, agent):
        """Remove an agent from the model."""
        if agent in self.agents:
            self.agents.remove(agent)
            self.grid.remove_agent(agent)
    
    def get_average_hunger(self):
        """Calculate average hunger of all alive agents."""
        agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        if not agents:
            return 0
        return sum(agent.hunger for agent in agents) / len(agents)
    
    def get_average_energy(self):
        """Calculate average energy of all alive agents."""
        agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        if not agents:
            return 0
        return sum(agent.energy for agent in agents) / len(agents)
    
    def get_average_health(self):
        """Calculate average health of all alive agents."""
        agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        if not agents:
            return 0
        return sum(agent.health for agent in agents) / len(agents)
    
    def get_average_social(self):
        """Calculate average social need of all alive agents."""
        agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        if not agents:
            return 0
        return sum(agent.social for agent in agents) / len(agents)
    
    def get_average_coins(self):
        """Calculate average coins of all alive agents."""
        agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        if not agents:
            return 0
        return sum(agent.coins for agent in agents) / len(agents)
    
    def get_average_friendship(self):
        """Calculate average friendship score across all alive agents."""
        agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        if not agents:
            return 0
        
        total_friendships = 0
        friendship_count = 0
        for agent in agents:
            for friendship_score in agent.friendships.values():
                total_friendships += friendship_score
                friendship_count += 1
        
        return total_friendships / max(1, friendship_count)
    
    def count_interactions(self):
        """Count the number of agents currently interacting (same cell)."""
        agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        interactions = 0
        
        for agent in agents:
            if agent.pos is not None:
                cell_contents = self.grid.get_cell_list_contents([agent.pos])
                other_agents = [obj for obj in cell_contents 
                               if isinstance(obj, CitizenAgent) and obj != agent and not obj.is_dead]
                if other_agents:
                    interactions += 1
        
        return interactions
    
    def get_agent_by_id(self, agent_id):
        """Get an agent by its unique ID."""
        for agent in self.agents:
            if isinstance(agent, CitizenAgent) and agent.unique_id == agent_id:
                return agent
        return None
    
    def create_child_agent(self, parent1, parent2):
        """Create a child agent with mixed traits from two parents."""
        # Mix personality traits from both parents
        all_parent_traits = parent1.personality_traits + parent2.personality_traits
        # Remove duplicates and randomly select 1-2 traits
        unique_traits = list(set(all_parent_traits))
        num_traits = random.choice([1, 2])
        child_traits = random.sample(unique_traits, min(num_traits, len(unique_traits)))
        
        # Create child agent
        child = CitizenAgent(self)
        child.personality_traits = child_traits
        child.exploration_rate = 0.4 if 'explorer' in child_traits else 0.2
        
        # Place child near parents
        attempts = 0
        while attempts < 20:
            # Try to place near parent1
            px, py = parent1.pos if parent1.pos else (self.width//2, self.height//2)
            x = max(0, min(self.width-1, px + random.randint(-2, 2)))
            y = max(0, min(self.height-1, py + random.randint(-2, 2)))
            
            # Check if position is reasonable (not overcrowded)
            cell_contents = self.grid.get_cell_list_contents([(x, y)])
            if len(cell_contents) < 3:  # Max 3 agents per cell
                self.grid.place_agent(child, (x, y))
                break
            attempts += 1
        else:
            # Fallback: place randomly
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            self.grid.place_agent(child, (x, y))
        
        return child
    
    def initialize_communities(self):
        """Initialize communities based on house/job clusters."""
        house_positions = []
        job_positions = []
        
        # Collect house and job positions
        for cell in self.grid.coord_iter():
            cell_content, (x, y) = cell
            if cell_content:  # Check if cell has content
                # cell_content is a list of agents in Mesa
                if isinstance(cell_content, list):
                    for obj in cell_content:
                        if isinstance(obj, House):
                            house_positions.append((x, y))
                        elif isinstance(obj, Job):
                            job_positions.append((x, y))
                else:
                    # Single agent case
                    if isinstance(cell_content, House):
                        house_positions.append((x, y))
                    elif isinstance(cell_content, Job):
                        job_positions.append((x, y))
        
        # Create communities around clusters of houses/jobs
        community_centers = house_positions + job_positions
        self.communities = {}
        
        for i, center in enumerate(community_centers[:3]):  # Max 3 communities
            community_id = f"community_{i}"
            self.communities[community_id] = {
                'id': community_id,
                'center': center,
                'agents': [],
                'dominant_trait': random.choice(['greedy', 'friendly', 'lazy', 'explorer'])
            }
    
    def get_community_at_position(self, pos):
        """Get the community that influences this position."""
        if pos is None:
            return None
            
        px, py = pos
        closest_community = None
        min_distance = float('inf')
        
        for community in self.communities.values():
            cx, cy = community['center']
            distance = abs(px - cx) + abs(py - cy)
            if distance < min_distance and distance <= 5:  # Community influence radius
                min_distance = distance
                closest_community = community
        
        return closest_community
    
    def update_family_stats(self):
        """Update family statistics."""
        # Count families and children
        families = set()
        children_count = 0
        
        for agent in self.agents:
            if isinstance(agent, CitizenAgent) and not agent.is_dead:
                if agent.family_id:
                    families.add(agent.family_id)
                if agent.age < 100:  # Consider agents under 100 steps as children
                    children_count += 1
        
        return len(families), children_count
    
    def advance_technology(self):
        """Check for technology advancement opportunities."""
        # Accumulate tech points from scholar agents and schools
        scholars = [a for a in self.agents if isinstance(a, CitizenAgent) 
                   and not a.is_dead and getattr(a, 'profession', None) == 'scholar']
        
        # Tech points from scholars
        for scholar in scholars:
            self.technology_points += scholar.learning * 0.01
        
        # Tech points from active schools
        school_count = len([a for a in self.agents if isinstance(a, School)])
        self.technology_points += school_count * 0.5
        
        # Check if we can discover new technologies
        for tech_name, tech_data in self.tech_tree.items():
            if (tech_name not in self.technologies and 
                self.technology_points >= tech_data['cost'] and
                (tech_data['prereq'] is None or tech_data['prereq'] in self.technologies)):
                
                # Discover technology!
                self.technologies.add(tech_name)
                self.technology_points -= tech_data['cost']
                self.technological_level += 1
                self.apply_technology_benefits(tech_name, tech_data['benefits'])
                print(f"🔬 Technology discovered: {tech_name.title()}! (Level {self.technological_level})")
                break
    
    def apply_technology_benefits(self, tech_name, benefits):
        """Apply benefits of discovered technology."""
        if benefits == 'food_boost':
            # Agriculture: Increase food spawn rate
            self.global_resources['food'] += 50
        elif benefits == 'workshop_efficiency':
            # Craftsmanship: Workshops become more efficient
            for agent in self.agents:
                if isinstance(agent, Workshop):
                    agent.craft_bonus *= 1.5
        elif benefits == 'market_bonus':
            # Trade routes: Markets provide better profits
            for agent in self.agents:
                if isinstance(agent, Market):
                    agent.trade_bonus *= 1.3
        elif benefits == 'learning_boost':
            # Education: Schools become more effective
            for agent in self.agents:
                if isinstance(agent, School):
                    agent.learning_bonus *= 1.5
        elif benefits == 'tool_efficiency':
            # Metallurgy: Better tools
            self.global_resources['tools'] += 30
        elif benefits == 'leadership_system':
            # Governance: Enable formal leadership
            self.establish_leadership()
        # PHASE 3 TECHNOLOGY BENEFITS
        elif benefits == 'cultural_growth':
            # Philosophy: Boost cultural development
            self.cultural_level += 1
            print(f"🎭 Cultural level increased to {self.cultural_level}")
        elif benefits == 'defense_system':
            # Military: Improve conflict resolution
            self.military_strength += 10
            print(f"🛡️ Military strength increased to {self.military_strength}")
        elif benefits == 'infrastructure':
            # Engineering: Enable road building
            self.infrastructure_level += 2
            print(f"🏗️ Infrastructure level increased to {self.infrastructure_level}")
        elif benefits == 'health_boost':
            # Medicine: Improve agent health
            for agent in self.agents:
                if isinstance(agent, CitizenAgent) and not agent.is_dead:
                    agent.max_health = min(120, agent.max_health + 10)
            print(f"💊 Medicine improves maximum health for all citizens")
        elif benefits == 'navigation':
            # Astronomy: Enable better trade routes
            for route in self.trade_routes_established:
                route['profit'] = int(route['profit'] * 1.3)
            print(f"🌟 Astronomy improves trade route efficiency")
        elif benefits == 'advanced_research':
            # Mathematics: Enable complex research
            self.technology_points += 20  # Boost future tech development
            print(f"🧮 Mathematics accelerates future discoveries")
    
    def establish_leadership(self):
        """Establish leadership system when governance is discovered."""
        # Find potential leaders (high social skills, long survival)
        candidates = []
        for agent in self.agents:
            if (isinstance(agent, CitizenAgent) and not agent.is_dead and 
                agent.age > 100):  # Mature agents only
                
                leadership_score = (
                    len(agent.friendships) * 2 +  # Social connections
                    agent.coins * 0.1 +           # Economic success
                    (agent.learning + agent.trading) * 0.5 +  # Skills
                    agent.age * 0.01              # Experience
                )
                candidates.append((agent, leadership_score))
        
        if candidates:
            # Select top candidates as leaders
            candidates.sort(key=lambda x: x[1], reverse=True)
            for i, (agent, score) in enumerate(candidates[:3]):  # Top 3 leaders
                community_id = f"leadership_{i}"
                self.leaders[community_id] = agent.unique_id
                self.social_rankings[agent.unique_id] = score
                agent.is_leader = True
                print(f"👑 {agent.unique_id} becomes community leader with score {score:.1f}")
    
    def update_resource_economy(self):
        """Update resource prices based on supply and demand."""
        # Count resource production and consumption
        alive_agents = len([a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead])
        
        # Food demand vs supply
        food_demand = alive_agents * 2  # Each agent needs ~2 food per cycle
        food_supply = len([a for a in self.agents if isinstance(a, Food)]) * 10
        
        if food_demand > food_supply:
            self.resource_prices['food'] = min(5, self.resource_prices['food'] * 1.1)  # Scarcity drives prices up
        else:
            self.resource_prices['food'] = max(0.5, self.resource_prices['food'] * 0.95)  # Abundance lowers prices
        
        # Tools production (from workshops)
        workshop_count = len([a for a in self.agents if isinstance(a, Workshop)])
        tool_production = workshop_count * 2
        self.global_resources['tools'] = min(200, self.global_resources['tools'] + tool_production)
        
        # Luxury goods (from high-skill merchants)
        merchants = [a for a in self.agents if isinstance(a, CitizenAgent) 
                    and not a.is_dead and getattr(a, 'profession', None) == 'merchant']
        luxury_production = sum(a.trading * 0.1 for a in merchants if a.trading > 70)
        self.global_resources['luxury'] = min(100, self.global_resources['luxury'] + luxury_production)
    
    def process_leadership_actions(self):
        """Process actions taken by community leaders."""
        for community_id, leader_id in self.leaders.items():
            leader = self.get_agent_by_id(leader_id)
            if leader and not leader.is_dead:
                # Leaders can influence community policies
                if random.random() < 0.1:  # 10% chance per step
                    policy = self.generate_leadership_policy(leader)
                    if policy:
                        self.policies.append(policy)
                        self.apply_policy(policy)
                        print(f"📜 Leader {leader_id} enacts policy: {policy['name']}")
    
    def generate_leadership_policy(self, leader):
        """Generate a policy based on leader's traits and situation."""
        # Policy based on leader's personality
        if 'greedy' in leader.personality_traits:
            return {'name': 'Taxation', 'effect': 'redistribute_wealth', 'duration': 50}
        elif 'friendly' in leader.personality_traits:
            return {'name': 'Community Cooperation', 'effect': 'boost_social', 'duration': 30}
        elif 'explorer' in leader.personality_traits:
            return {'name': 'Expansion Initiative', 'effect': 'boost_exploration', 'duration': 40}
        return None
    
    def apply_policy(self, policy):
        """Apply the effects of a leadership policy."""
        alive_agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        
        if policy['effect'] == 'redistribute_wealth':
            # Redistribute wealth from rich to poor
            wealthy = [a for a in alive_agents if a.coins > 100]
            poor = [a for a in alive_agents if a.coins < 20]
            for rich_agent in wealthy:
                if poor:
                    poor_agent = random.choice(poor)
                    transfer = min(10, rich_agent.coins * 0.1)
                    rich_agent.coins -= transfer
                    poor_agent.coins += transfer
                    
        elif policy['effect'] == 'boost_social':
            # Improve social connections
            for agent in alive_agents:
                agent.social = max(0, agent.social - 10)
                
        elif policy['effect'] == 'boost_exploration':
            # Increase exploration rates
            for agent in alive_agents:
                if 'explorer' in agent.personality_traits:
                    agent.exploration_rate = min(0.8, agent.exploration_rate * 1.2)
    
    def update_weather_and_seasons(self):
        """Update weather patterns and seasonal cycles."""
        # Update season every 50 steps
        self.season_cycle += 1
        if self.season_cycle >= 50:
            self.season_cycle = 0
            seasons = ['spring', 'summer', 'autumn', 'winter']
            current_idx = seasons.index(self.season)
            self.season = seasons[(current_idx + 1) % 4]
            print(f"Season changed to {self.season}")
        
        # Update weather every 10-20 steps
        if random.random() < 0.1:  # 10% chance each step
            weather_options = ['normal', 'rain', 'drought', 'storm']
            
            # Season influences weather probability
            if self.season == 'spring':
                weights = [0.6, 0.3, 0.05, 0.05]  # More rain in spring
            elif self.season == 'summer':
                weights = [0.5, 0.2, 0.25, 0.05]  # More drought in summer
            elif self.season == 'autumn':
                weights = [0.7, 0.2, 0.05, 0.05]  # Mostly normal
            else:  # winter
                weights = [0.6, 0.1, 0.1, 0.2]   # More storms in winter
            
            self.weather = random.choices(weather_options, weights=weights)[0]
            
        # Apply weather effects to agents
        self.apply_weather_effects()
    
    def apply_weather_effects(self):
        """Apply current weather effects to all agents."""
        alive_agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        
        for agent in alive_agents:
            if self.weather == 'storm':
                # Storms drain energy and can cause health loss
                agent.energy = max(0, agent.energy - 2)
                if random.random() < 0.05:  # 5% chance of health loss
                    agent.health = max(0, agent.health - 5)
            elif self.weather == 'drought':
                # Drought increases hunger rate slightly
                agent.hunger = min(agent.max_hunger, agent.hunger + 1)
            elif self.weather == 'rain':
                # Rain improves health slightly and reduces social needs
                if random.random() < 0.3:
                    agent.health = min(agent.max_health, agent.health + 1)
                    agent.social = max(0, agent.social - 2)  # Rain feels refreshing
       
    # PHASE 3: Advanced civilization systems
    
    def advance_culture(self):
        """Manage cultural development and achievements."""
        # Count cultural contributors
        artists = [a for a in self.agents if isinstance(a, CitizenAgent) 
                  and not a.is_dead and getattr(a, 'profession', None) == 'merchant']
        philosophers = [a for a in self.agents if isinstance(a, CitizenAgent) 
                       and not a.is_dead and getattr(a, 'profession', None) == 'scholar']
        
        # Generate art works
        if len(artists) > 2 and random.random() < 0.05:
            self.art_works += 1
            if random.random() < 0.3:
                print(f"🎨 New artwork created! Total: {self.art_works}")
        
        # Philosophical developments
        if len(philosophers) > 3 and 'philosophy' in self.technologies:
            if random.random() < 0.03:
                school_name = random.choice(['Stoic', 'Empirical', 'Rational', 'Mystical', 'Practical'])
                self.philosophical_schools.append(school_name)
                print(f"🧠 New philosophical school: {school_name} Philosophy")
        
        # Build monuments when culturally advanced
        if self.cultural_level > 3 and random.random() < 0.01:
            self.monuments += 1
            print(f"🏛️ New monument erected! Total: {self.monuments}")
        
        # Hold festivals
        if self.steps % 100 == 0 and len([a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]) > 20:
            self.festivals_held += 1
            print(f"🎉 Festival celebrated! Community joy increases.")
            # Boost social and health for all agents
            for agent in self.agents:
                if isinstance(agent, CitizenAgent) and not agent.is_dead:
                    agent.social = max(0, agent.social - 10)
                    agent.health = min(agent.max_health, agent.health + 5)
    
    def manage_conflicts(self):
        """Handle warfare, conflicts, and peace treaties."""
        alive_agents = [a for a in self.agents if isinstance(a, CitizenAgent) and not a.is_dead]
        
        # Resource scarcity can lead to conflicts
        if self.global_resources['food'] < 30 and len(alive_agents) > 15:
            if random.random() < 0.02:
                # Resource conflict emerges
                conflict = {
                    'type': 'resource_dispute',
                    'severity': random.choice(['minor', 'moderate', 'severe']),
                    'duration': random.randint(5, 20)
                }
                self.conflicts.append(conflict)
                print(f"⚔️ Resource conflict erupted! Severity: {conflict['severity']}")
        
        # Process ongoing conflicts
        for conflict in self.conflicts[:]:
            conflict['duration'] -= 1
            
            # Conflicts affect agents negatively
            for agent in alive_agents[:10]:  # Affect up to 10 agents
                agent.health = max(0, agent.health - 2)
                agent.social = min(agent.max_social, agent.social + 3)
            
            # Try to resolve conflicts
            if 'military' in self.technologies and random.random() < 0.3:
                self.conflicts.remove(conflict)
                self.conflicts_resolved += 1
                print(f"🕊️ Conflict resolved through military organization!")
            elif conflict['duration'] <= 0:
                self.conflicts.remove(conflict)
                self.conflicts_resolved += 1
                print(f"🕊️ Conflict ended naturally.")
        
        # Form alliances between communities
        if len(self.communities) > 1 and random.random() < 0.01:
            community_ids = list(self.communities.keys())
            if len(community_ids) >= 2:
                ally1, ally2 = random.sample(community_ids, 2)
                alliance = {'communities': [ally1, ally2], 'strength': random.randint(1, 10)}
                self.alliances.append(alliance)
                print(f"🤝 Alliance formed between communities {ally1} and {ally2}")
    
    def develop_infrastructure(self):
        """Manage infrastructure development and trade routes."""
        # Engineering technology enables infrastructure
        if 'engineering' in self.technologies:
            self.infrastructure_level = min(10, self.infrastructure_level + 0.01)
            
            # Build road networks
            if random.random() < 0.02:
                # Connect random locations
                x1, y1 = random.randint(0, self.width-1), random.randint(0, self.height-1)
                x2, y2 = random.randint(0, self.width-1), random.randint(0, self.height-1)
                self.road_network.add(((x1, y1), (x2, y2)))
                print(f"🛤️ New road built connecting ({x1},{y1}) to ({x2},{y2})")
        
        # Trade routes technology enables long-distance trade
        if 'trade_routes' in self.technologies:
            if random.random() < 0.03:
                route = {
                    'origin': random.choice(list(self.communities.keys())) if self.communities else 'central',
                    'destination': 'external',
                    'goods': random.choice(['luxury', 'tools', 'food']),
                    'profit': random.randint(50, 200)
                }
                self.trade_routes_established.append(route)
                self.global_resources[route['goods']] += route['profit'] // 10
                print(f"📦 New trade route established for {route['goods']}")
    
    def conduct_research(self):
        """Manage scientific research and innovation."""
        researchers = [a for a in self.agents if isinstance(a, CitizenAgent) 
                      and not a.is_dead and getattr(a, 'profession', None) == 'scholar']
        
        # Advanced technologies enable research projects
        if 'mathematics' in self.technologies and len(researchers) > 2:
            if random.random() < 0.02:
                research_topics = ['Navigation', 'Agriculture', 'Medicine', 'Architecture', 'Astronomy']
                topic = random.choice(research_topics)
                project = {
                    'topic': topic,
                    'progress': 0,
                    'required': random.randint(50, 150),
                    'researchers': len(researchers)
                }
                self.research_projects.append(project)
                print(f"🔬 New research project started: {topic}")
        
        # Progress research projects
        for project in self.research_projects[:]:
            project['progress'] += len(researchers) * 2
            
            if project['progress'] >= project['required']:
                # Research completed!
                innovation = {
                    'name': project['topic'],
                    'benefit': random.choice(['efficiency', 'health', 'happiness', 'production'])
                }
                self.innovations.append(innovation)
                self.scientific_discoveries += 1
                self.research_projects.remove(project)
                print(f"💡 Scientific breakthrough: {innovation['name']} improves {innovation['benefit']}!")
                
                # Apply innovation benefits
                if innovation['benefit'] == 'health':
                    for agent in self.agents:
                        if isinstance(agent, CitizenAgent) and not agent.is_dead:
                            agent.max_health = min(120, agent.max_health + 5)
                elif innovation['benefit'] == 'efficiency':
                    self.global_resources['tools'] += 20
                elif innovation['benefit'] == 'production':
                    self.global_resources['food'] += 30
       
    # Compatibility properties for the schedule
    @property
    def schedule(self):
        """Compatibility property for schedule-like access."""
        class ScheduleCompat:
            def __init__(self, agents, steps):
                self.agents = agents
                self.steps = steps
        return ScheduleCompat(self.agents, self.steps)
