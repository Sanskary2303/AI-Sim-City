import random
from mesa import Agent


class CitizenAgent(Agent):
    """An agent representing a citizen in the city simulation."""
    
    def __init__(self, model):
        super().__init__(model)
        
        # Agent attributes (BETTER STARTING CONDITIONS)
        self.hunger = random.randint(20, 50)  # Was 30-70, less hungry start
        self.energy = random.randint(50, 80)  # Was 30-70, more energetic start
        self.health = 100  # Health starts at 100
        self.coins = 8  # Was 5, more starting coins
        self.social = random.randint(10, 30)  # Was 20-50, less lonely start
        self.is_dead = False  # Death state
        
        # Missing attributes for Phase 4
        self.age = random.randint(18, 35)
        self.gender = random.choice(['male', 'female'])
        self.food = random.randint(10, 30)
        self.tools = random.randint(5, 15)
        self.partner_id = None
        self.children = []
        self.skills = {
            'farming': random.randint(10, 30),
            'crafting': random.randint(10, 30),
            'trading': random.randint(10, 30),
            'learning': random.randint(10, 30),
            'leadership': random.randint(10, 30)
        }
        self.has_leadership_role = False
        self.friendships = {}  # For backward compatibility
        self.family_id = None  # For family tracking
        
        self.max_hunger = 100
        self.max_energy = 100
        self.max_health = 100
        self.max_social = 100
        
        # Thresholds for decision making (RELAXED THRESHOLDS)
        self.hunger_threshold = 70  # Was 80, less urgent
        self.energy_threshold = 25  # Was 20, less urgent  
        self.social_threshold = 60  # Was 70, easier to trigger social needs
        self.health_danger_hunger = 90  # Was 85, higher threshold for health loss
        self.health_danger_energy = 10  # Was 15, lower threshold for health loss
        
        # Personality traits (assign 1-2 randomly)
        all_traits = ['greedy', 'friendly', 'lazy', 'explorer']
        num_traits = random.choice([1, 2])
        self.personality_traits = random.sample(all_traits, num_traits)
        
        # Exploration rate based on personality
        self.exploration_rate = 0.4 if 'explorer' in self.personality_traits else 0.2
        
        # Memory of food and job locations (simple learning)
        self.known_food_locations = set()
        self.known_job_locations = set()
        
        # Skills system (0-100 scale)
        self.farming = random.randint(10, 30)    # Food production efficiency
        self.crafting = random.randint(10, 30)   # Item creation ability
        self.trading = random.randint(10, 30)    # Economic efficiency
        self.combat = random.randint(10, 30)     # Survival and protection
        self.learning = random.randint(10, 30)   # Knowledge acquisition speed
        
        # Profession system
        self.profession = None  # Will be assigned based on skills and opportunities
        
        # PHASE 3: Cultural and social attributes
        self.artistic_skill = random.randint(5, 25)    # Art creation ability
        self.philosophical_inclination = random.randint(5, 25)  # Deep thinking tendency
        self.diplomatic_skill = random.randint(5, 25)  # Conflict resolution ability
        self.research_focus = random.choice(['none', 'medicine', 'engineering', 'philosophy', 'astronomy'])
        
        # PHASE 3: Social and political attributes
        self.cultural_contributions = 0    # Number of cultural works created
        self.conflicts_mediated = 0        # Number of conflicts resolved
        self.research_progress = 0         # Progress on current research
        self.political_alignment = random.choice(['peaceful', 'aggressive', 'neutral'])
        
        # PHASE 3: Advanced memory systems
        self.cultural_memory = []          # Remember cultural events attended
        self.alliance_preferences = {}     # Preferred alliance partners
        self.research_projects = []        # Active research interests
        
        # PHASE 4: Complex Psychology & Emotions
        self.emotions = {
            'happiness': random.randint(30, 70),
            'anger': random.randint(0, 20),
            'fear': random.randint(0, 30),
            'sadness': random.randint(0, 20),
            'excitement': random.randint(10, 40),
            'stress': random.randint(0, 30),
            'love': random.randint(0, 20),
            'pride': random.randint(10, 30)
        }
        
        # PHASE 4: Advanced personality system
        self.personality_scores = {
            'openness': random.randint(20, 80),        # Creativity, curiosity
            'conscientiousness': random.randint(20, 80),  # Organization, discipline
            'extraversion': random.randint(20, 80),    # Sociability, energy
            'agreeableness': random.randint(20, 80),   # Cooperation, trust
            'neuroticism': random.randint(20, 80)      # Emotional stability
        }
        
        # PHASE 4: Complex memory and learning
        self.long_term_memory = []         # Important life events
        self.short_term_memory = []        # Recent experiences (last 10)
        self.learned_behaviors = {}        # Behavioral adaptations
        self.agent_relationships = {}      # Detailed relationship tracking
        self.life_goals = self.generate_life_goals()  # Personal aspirations
        
        # PHASE 4: Advanced decision-making
        self.decision_weights = {
            'survival': random.uniform(0.6, 1.0),
            'social': random.uniform(0.3, 0.8),
            'achievement': random.uniform(0.2, 0.7),
            'exploration': random.uniform(0.1, 0.6),
            'altruism': random.uniform(0.1, 0.5)
        }
        
        # PHASE 4: Skills specialization and mastery
        self.skill_preferences = random.choice(['generalist', 'farming', 'crafting', 'trading', 'learning', 'leadership'])
        self.mastery_level = 0             # Overall expertise level
        self.teaching_ability = random.randint(0, 30)  # Can teach others
        
        # PHASE 4: Advanced social dynamics
        self.charisma = random.randint(10, 60)
        self.empathy = random.randint(20, 80)
        self.social_network_size = 0
        self.social_influence_radius = random.randint(2, 8)
        
        # PHASE 4: Life stage and development
        self.life_stage = 'young_adult'    # young_adult, adult, mature, elder
        self.wisdom = 0                    # Accumulated through experience
        self.mentors = []                  # Agents who taught this agent
        self.students = []                 # Agents this agent has taught
        self.work_experience = 0  # Experience in current profession
        
        # PHASE 2: Enhanced social and leadership system
        self.influence = 0  # Social influence score
        self.reputation = 50  # Community reputation (0-100)
        self.is_leader = False  # Leadership status
        self.trade_partners = set()  # Regular trading partners
        self.resources_owned = {'tools': 0, 'luxury': 0}  # Additional resources
        self.leadership_ambition = random.randint(10, 90)  # Desire to lead

    def generate_life_goals(self):
        """Generate personal life goals based on personality and skills"""
        goals = []
        
        # Goal generation based on personality
        if self.personality_scores['openness'] > 60:
            goals.append(random.choice(['explore_new_lands', 'create_masterpiece', 'discover_technology']))
        
        if self.personality_scores['conscientiousness'] > 60:
            goals.append(random.choice(['become_leader', 'master_profession', 'build_legacy']))
            
        if self.personality_scores['extraversion'] > 60:
            goals.append(random.choice(['unite_community', 'expand_social_network', 'become_diplomat']))
            
        if self.personality_scores['agreeableness'] > 60:
            goals.append(random.choice(['help_community', 'resolve_conflicts', 'teach_others']))
        
        # Add survival/family goals
        goals.extend(['find_partner', 'raise_family', 'ensure_prosperity'])
        
        return goals[:random.randint(2, 4)]  # Keep 2-4 goals

    # PHASE 4: Advanced Psychological Methods
    
    def update_emotions(self, event_type, intensity=1):
        """Update emotions based on life events"""
        emotion_changes = {
            'success': {'happiness': 10, 'pride': 8, 'stress': -5},
            'failure': {'sadness': 8, 'anger': 5, 'stress': 10},
            'social_positive': {'happiness': 5, 'love': 3, 'excitement': 5},
            'social_negative': {'anger': 8, 'sadness': 5, 'stress': 7},
            'danger': {'fear': 15, 'stress': 12, 'anger': 3},
            'achievement': {'pride': 12, 'happiness': 8, 'excitement': 6}
        }
        
        if event_type in emotion_changes:
            for emotion, change in emotion_changes[event_type].items():
                self.emotions[emotion] = max(0, min(100, 
                    self.emotions[emotion] + (change * intensity)))
    
    def make_personality_decision(self, options):
        """Make decisions based on personality traits"""
        if not options:
            return None
            
        scored_options = []
        for option in options:
            score = 0
            
            # Weigh options based on personality
            if option == 'help_others' and self.personality_scores['agreeableness'] > 60:
                score += 20
            elif option == 'take_leadership' and self.personality_scores['extraversion'] > 60:
                score += 25
            elif option == 'explore_new' and self.personality_scores['openness'] > 60:
                score += 15
            elif option == 'organize_efficiently' and self.personality_scores['conscientiousness'] > 60:
                score += 20
            
            # Add randomness but personality-influenced
            score += random.randint(0, 30)
            scored_options.append((option, score))
        
        # Return highest scored option
        return max(scored_options, key=lambda x: x[1])[0]
    
    def add_memory(self, memory_type, content, importance=1):
        """Add experiences to memory systems"""
        memory_entry = {
            'type': memory_type,
            'content': content,
            'step': self.model.step_count,
            'importance': importance,
            'emotions_at_time': self.emotions.copy()
        }
        
        # Add to short-term memory
        self.short_term_memory.append(memory_entry)
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)
        
        # Important memories go to long-term
        if importance >= 3:
            self.long_term_memory.append(memory_entry)
            if len(self.long_term_memory) > 50:
                self.long_term_memory.pop(0)
    
    def update_relationship(self, agent_id, interaction_type, strength=1):
        """Track and update relationships with other agents"""
        if agent_id not in self.agent_relationships:
            self.agent_relationships[agent_id] = {
                'friendship': 0,
                'trust': 50,
                'cooperation': 0,
                'conflict': 0,
                'interactions': 0
            }
        
        rel = self.agent_relationships[agent_id]
        rel['interactions'] += 1
        
        if interaction_type == 'positive':
            rel['friendship'] += strength * 2
            rel['trust'] += strength
            rel['cooperation'] += strength
        elif interaction_type == 'negative':
            rel['friendship'] -= strength * 2
            rel['trust'] -= strength * 3
            rel['conflict'] += strength
        elif interaction_type == 'cooperation':
            rel['cooperation'] += strength * 2
            rel['trust'] += strength
        
        # Keep values in bounds
        for key in ['friendship', 'trust', 'cooperation', 'conflict']:
            rel[key] = max(-100, min(100, rel[key]))
    
    def learn_from_experience(self, skill_type, success=True):
        """Learn and adapt behaviors based on experience"""
        if skill_type not in self.learned_behaviors:
            self.learned_behaviors[skill_type] = 0
        
        if success:
            self.learned_behaviors[skill_type] += 1
            self.mastery_level += 0.1
        else:
            self.learned_behaviors[skill_type] = max(0, self.learned_behaviors[skill_type] - 0.5)
        
        # Update wisdom based on age and experience
        self.wisdom += 0.05 if success else 0.02
    
    def complex_decision_making(self, action_type):
        """Advanced decision making considering multiple factors"""
        decision_score = 0
        
        # Base decision on personality
        if action_type == 'help_community':
            decision_score += self.personality_scores['agreeableness'] * 0.3
            decision_score += self.decision_weights['altruism'] * 50
        elif action_type == 'pursue_leadership':
            decision_score += self.personality_scores['extraversion'] * 0.4
            decision_score += self.leadership_ambition * 0.3
        elif action_type == 'focus_research':
            decision_score += self.personality_scores['openness'] * 0.5
            decision_score += self.decision_weights['achievement'] * 40
        
        # Modify based on current emotions
        if self.emotions['happiness'] > 70:
            decision_score += 10
        if self.emotions['stress'] > 60:
            decision_score -= 15
        
        # Consider social relationships
        social_factor = sum(rel['friendship'] for rel in self.agent_relationships.values()) / max(1, len(self.agent_relationships))
        decision_score += social_factor * 0.1
        
        return decision_score > 50
    
    def teach_skill_to_agent(self, student_agent, skill_type):
        """Teach skills to other agents"""
        if self.teaching_ability > 20 and self.skills.get(skill_type, 0) > 15:
            teaching_effectiveness = (self.teaching_ability + self.skills[skill_type]) / 100
            
            # Student learns based on their openness and our teaching
            if hasattr(student_agent, 'personality_scores'):
                learning_rate = student_agent.personality_scores['openness'] / 100
                skill_gain = teaching_effectiveness * learning_rate * random.uniform(0.5, 2.0)
                
                student_agent.skills[skill_type] = min(100, 
                    student_agent.skills.get(skill_type, 0) + skill_gain)
                
                # Update relationships
                self.update_relationship(student_agent.unique_id, 'positive', 2)
                student_agent.update_relationship(self.unique_id, 'positive', 3)
                
                # Track mentorship
                if student_agent.unique_id not in self.students:
                    self.students.append(student_agent.unique_id)
                if self.unique_id not in student_agent.mentors:
                    student_agent.mentors.append(self.unique_id)
                
                return True
        return False
    
    # PHASE 4: Advanced Behavioral Methods
    
    def update_life_stage(self):
        """Update life stage based on age and experience"""
        if self.age < 25:
            self.life_stage = 'young_adult'
        elif self.age < 45:
            self.life_stage = 'adult'
        elif self.age < 65:
            self.life_stage = 'mature'
        else:
            self.life_stage = 'elder'
    
    def pursue_life_goals(self):
        """Actively work towards achieving life goals"""
        if not self.life_goals:
            return
            
        current_goal = random.choice(self.life_goals)
        
        if current_goal == 'become_leader' and not self.has_leadership_role:
            if self.complex_decision_making('pursue_leadership'):
                self.leadership_ambition += 2
                self.update_emotions('achievement', 0.5)
                
        elif current_goal == 'master_profession':
            skill_to_improve = self.skill_preferences if self.skill_preferences != 'generalist' else random.choice(['farming', 'crafting', 'trading'])
            if skill_to_improve in self.skills:
                self.skills[skill_to_improve] += random.uniform(0.5, 2.0)
                self.learn_from_experience(skill_to_improve, True)
                
        elif current_goal == 'help_community':
            if self.complex_decision_making('help_community'):
                # Look for ways to help nearby agents
                self.engage_in_altruistic_behavior()
                
        elif current_goal == 'expand_social_network':
            self.seek_new_relationships()
    
    def engage_in_complex_social_interactions(self):
        """Advanced social behaviors based on personality and relationships"""
        nearby_agents = [agent for agent in self.model.agents 
                        if isinstance(agent, CitizenAgent) and agent != self and 
                        hasattr(agent, 'pos') and agent.pos is not None and
                        self.get_distance_to_agent(agent) <= self.social_influence_radius]
        
        if not nearby_agents:
            return
            
        for agent in random.sample(nearby_agents, min(3, len(nearby_agents))):
            interaction_type = self.determine_interaction_type(agent)
            
            if interaction_type == 'mentoring' and hasattr(self, 'teaching_ability') and hasattr(agent, 'skills'):
                skill_to_teach = self.skill_preferences if hasattr(self, 'skill_preferences') else 'farming'
                if skill_to_teach in self.skills and self.skills[skill_to_teach] > agent.skills.get(skill_to_teach, 0):
                    if self.teach_skill_to_agent(agent, skill_to_teach):
                        self.add_memory('teaching', f'Taught {skill_to_teach} to Agent {agent.unique_id}', 3)
                    
            elif interaction_type == 'collaboration':
                self.collaborate_with_agent(agent)
                
            elif interaction_type == 'emotional_support':
                self.provide_emotional_support(agent)
    
    def demonstrate_teaching_and_learning(self):
        """Show teaching and learning behaviors"""
        # Seek mentors if we're still learning
        if hasattr(self, 'life_stage') and self.life_stage == 'young_adult' and len(self.mentors) < 2:
            potential_mentors = [agent for agent in self.model.agents 
                               if isinstance(agent, CitizenAgent) and 
                               hasattr(agent, 'teaching_ability') and 
                               agent.teaching_ability > 15 and 
                               hasattr(agent, 'life_stage') and
                               agent.life_stage in ['adult', 'mature', 'elder'] and
                               agent != self]
            
            if potential_mentors:
                mentor = random.choice(potential_mentors)
                if mentor.unique_id not in self.mentors:
                    self.mentors.append(mentor.unique_id)
                    self.update_relationship(mentor.unique_id, 'positive', 3)
        
        # Become a mentor if we have expertise
        if (hasattr(self, 'teaching_ability') and self.teaching_ability > 20 and 
            hasattr(self, 'life_stage') and self.life_stage in ['mature', 'elder']):
            potential_students = [agent for agent in self.model.agents 
                                if isinstance(agent, CitizenAgent) and
                                hasattr(agent, 'life_stage') and 
                                agent.life_stage == 'young_adult' and 
                                agent != self]
            
            for student in random.sample(potential_students, min(2, len(potential_students))):
                if hasattr(self, 'skills') and self.skills:
                    best_skill = max(self.skills.items(), key=lambda x: x[1])
                    if best_skill[1] > 30:  # Only teach if we're good at it
                        self.teach_skill_to_agent(student, best_skill[0])
    
    def make_strategic_decisions(self):
        """Make long-term strategic decisions"""
        # Evaluate current life satisfaction
        life_satisfaction = (self.emotions['happiness'] + 
                           (100 - self.emotions['stress']) + 
                           self.emotions['pride']) / 3
        
        if life_satisfaction < 40:
            # Need to make changes
            if self.complex_decision_making('change_profession'):
                self.consider_profession_change()
            elif self.complex_decision_making('relocate'):
                self.consider_relocation()
        
        # Long-term planning based on resources
        if self.food > 50 and self.tools > 20:
            # We're secure, can focus on higher goals
            if 'create_masterpiece' in self.life_goals:
                self.work_on_masterpiece()
            elif 'discover_technology' in self.life_goals:
                self.focus_on_research()
    
    def get_distance_to_agent(self, other_agent):
        """Calculate distance to another agent"""
        if not hasattr(other_agent, 'pos') or not hasattr(self, 'pos'):
            return float('inf')
        if other_agent.pos is None or self.pos is None:
            return float('inf')
            
        try:
            # Simple position extraction
            if isinstance(self.pos, tuple):
                x1, y1 = self.pos
            else:
                x1, y1 = 0, 0
                
            if isinstance(other_agent.pos, tuple):
                x2, y2 = other_agent.pos
            else:
                x2, y2 = 0, 0
                
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        except:
            return float('inf')
    
    def determine_interaction_type(self, other_agent):
        """Determine what type of interaction to have with another agent"""
        if other_agent.unique_id in self.agent_relationships:
            rel = self.agent_relationships[other_agent.unique_id]
            if rel['friendship'] > 30:
                return 'collaboration'
            elif rel['trust'] > 60:
                return 'mentoring'
        
        # Based on personality
        if self.personality_scores['agreeableness'] > 60:
            return 'emotional_support'
        elif self.personality_scores['openness'] > 60:
            return 'collaboration'
        else:
            return 'casual'
    
    def collaborate_with_agent(self, other_agent):
        """Collaborate on projects with another agent"""
        # Share resources for mutual benefit
        if self.food > other_agent.food + 10:
            transfer = min(5, self.food - other_agent.food)
            self.food -= transfer
            other_agent.food += transfer
            self.update_relationship(other_agent.unique_id, 'cooperation', 2)
            other_agent.update_relationship(self.unique_id, 'positive', 2)
            
        # Collaborate on research
        if self.research_focus == other_agent.research_focus and self.research_focus != 'none':
            self.research_progress += 2
            other_agent.research_progress += 2
            self.update_emotions('achievement', 1)
            other_agent.update_emotions('achievement', 1)
    
    def provide_emotional_support(self, other_agent):
        """Provide emotional support to stressed agents"""
        if other_agent.emotions['stress'] > 60 or other_agent.emotions['sadness'] > 50:
            # Reduce their negative emotions
            other_agent.emotions['stress'] = max(0, other_agent.emotions['stress'] - 10)
            other_agent.emotions['sadness'] = max(0, other_agent.emotions['sadness'] - 8)
            other_agent.emotions['happiness'] += 5
            
            # Build relationship
            self.update_relationship(other_agent.unique_id, 'positive', 3)
            other_agent.update_relationship(self.unique_id, 'positive', 4)
            
            # We feel good about helping
            self.update_emotions('achievement', 1)
            self.add_memory('helping', f'Helped Agent {other_agent.unique_id} with stress', 2)
    
    def engage_in_altruistic_behavior(self):
        """Help community members in need"""
        needy_agents = [agent for agent in self.model.agents 
                       if isinstance(agent, CitizenAgent) and
                       hasattr(agent, 'health') and hasattr(agent, 'food') and
                       (agent.health < 30 or agent.food < 10) and agent != self]
        
        if needy_agents and hasattr(self, 'food') and self.food > 20:
            helped_agent = random.choice(needy_agents)
            # Give food to help
            help_amount = min(5, self.food - 15)  # Keep some for ourselves
            self.food -= help_amount
            helped_agent.food += help_amount
            
            self.update_emotions('achievement', 2)
            self.add_memory('altruism', f'Helped Agent {helped_agent.unique_id} with food', 3)
            self.update_relationship(helped_agent.unique_id, 'positive', 4)
    
    def seek_new_relationships(self):
        """Actively seek to build new social connections"""
        potential_friends = [agent for agent in self.model.agents 
                           if isinstance(agent, CitizenAgent) and
                           agent != self and 
                           agent.unique_id not in self.agent_relationships and
                           hasattr(agent, 'pos') and agent.pos is not None and
                           self.get_distance_to_agent(agent) <= 5]
        
        if potential_friends:
            new_friend = random.choice(potential_friends)
            # Initiate friendly interaction
            self.update_relationship(new_friend.unique_id, 'positive', 1)
            if hasattr(new_friend, 'update_relationship'):
                new_friend.update_relationship(self.unique_id, 'positive', 1)
            if hasattr(self, 'social_network_size'):
                self.social_network_size += 1
            self.update_emotions('social_positive', 1)
    
    def consider_profession_change(self):
        """Consider changing profession based on circumstances"""
        current_skill_level = self.skills.get(self.profession, 0)
        
        # Look for profession where we might do better
        best_skill = max(self.skills.items(), key=lambda x: x[1])
        if best_skill[1] > current_skill_level + 20:
            old_profession = self.profession
            self.profession = best_skill[0]
            self.add_memory('career_change', f'Changed from {old_profession} to {self.profession}', 4)
            self.update_emotions('achievement', 2)
    
    def consider_relocation(self):
        """Consider moving to a better location"""
        # This would involve complex spatial analysis
        # For now, just move to a random nearby location
        if random.random() < 0.1:  # 10% chance to relocate
            x, y = self.pos
            new_x = max(0, min(self.model.grid.width - 1, x + random.randint(-3, 3)))
            new_y = max(0, min(self.model.grid.height - 1, y + random.randint(-3, 3)))
            self.model.grid.move_agent(self, (new_x, new_y))
            self.add_memory('relocation', f'Moved to better location ({new_x}, {new_y})', 2)
    
    def work_on_masterpiece(self):
        """Work on creating a cultural masterpiece"""
        if hasattr(self, 'artistic_skill') and self.artistic_skill > 30:
            self.artistic_skill += random.uniform(0.5, 2.0)
            if random.random() < 0.05:  # 5% chance to complete masterpiece
                if hasattr(self.model, 'art_works'):
                    self.model.art_works += 1
                self.cultural_contributions += 1
                self.update_emotions('achievement', 3)
                self.add_memory('masterpiece', 'Completed a cultural masterpiece', 5)
                total_art = getattr(self.model, 'art_works', 0)
                print(f"🎨 Agent {self.unique_id} created a masterpiece! (Total artworks: {total_art})")
    
    def focus_on_research(self):
        """Focus on advanced research and discovery"""
        if hasattr(self, 'research_focus') and self.research_focus != 'none':
            if hasattr(self, 'research_progress'):
                self.research_progress += random.uniform(1, 3)
                if self.research_progress > 50:
                    # Research breakthrough
                    if hasattr(self.model, 'research_projects'):
                        self.model.research_projects += 1
                    self.research_progress = 0
                    self.update_emotions('achievement', 3)
                    self.add_memory('research_breakthrough', f'Breakthrough in {self.research_focus}', 5)
                    print(f"🔬 Agent {self.unique_id} achieved research breakthrough in {self.research_focus}!")
        
        # Social system
        self.friendships = {}  # {agent_id: friendship_score}
        
        # Family & Community system
        self.gender = random.choice(['male', 'female'])
        self.family_id = None  # None if no family, otherwise shared ID
        self.partner_id = None  # ID of partner agent
        self.children = []  # List of child agent IDs
        self.age = 0  # Age in simulation steps
        self.family_survival_time = 0  # How long family has survived together
        self.community_id = None  # Which community this agent belongs to
        
        # State tracking
        self.is_dead = False
        
    def step(self):
        """Execute one step of the agent."""
        if self.is_dead:
            return  # Dead agents don't act
        
        # Increase age
        self.age += 1
        
        # Increase hunger and decrease energy each step (REDUCED RATES)
        self.hunger = min(self.max_hunger, self.hunger + random.randint(1, 2))  # Was 1-3
        self.energy = max(0, self.energy - random.randint(0, 1))  # Was 1-2
        
        # Increase social need over time (REDUCED RATE)
        self.social = min(self.max_social, self.social + random.randint(0, 1))  # Was 1-2
        
        # Health management
        self.update_health()
        
        # Check if agent dies
        if self.health <= 0:
            self.die()
            return
        
        # Skill development and profession management
        self.develop_skills()
        self.update_profession()
        
        # PHASE 2: Enhanced social dynamics
        self.update_influence_and_reputation()
        self.attempt_trading()
        self.consider_leadership_actions()
        
        # PHASE 3: Advanced civilization behaviors
        self.engage_in_cultural_activities()
        self.conduct_research_activities()
        self.participate_in_conflict_resolution()
        self.develop_diplomatic_relations()
        
        # PHASE 4: Advanced psychological behaviors
        self.update_life_stage()
        self.pursue_life_goals()
        self.engage_in_complex_social_interactions()
        self.demonstrate_teaching_and_learning()
        self.make_strategic_decisions()
        
        # Family management
        self.manage_family()
        
        # Choose action based on current state and personality
        self.choose_action()
        
        
        # Check for social interactions at current location
        self.check_for_social_interactions()
        
        # Community influence
        self.apply_community_influence()
    
    def update_health(self):
        """Update health based on hunger and energy levels (LESS HARSH)."""
        health_loss = 0
        
        # Lose health if very hungry (REDUCED PENALTY)
        if self.hunger >= self.health_danger_hunger:
            health_loss += random.randint(0, 2)  # Was 1-3
        
        # Lose health if very tired (REDUCED PENALTY)
        if self.energy <= self.health_danger_energy:
            health_loss += random.randint(0, 1)  # Was 1-2
        
        self.health = max(0, self.health - health_loss)
    
    def die(self):
        """Mark agent as dead."""
        self.is_dead = True
        print(f"Agent {self.unique_id} has died! (Hunger: {self.hunger}, Energy: {self.energy}, Coins: {self.coins}) [Traits: {self.personality_traits}]")
        
    def get_action_priorities(self):
        """Get action priorities based on personality traits."""
        if 'greedy' in self.personality_traits:
            return ['work', 'food', 'sleep', 'social', 'learning']
        elif 'friendly' in self.personality_traits:
            return ['social', 'food', 'work', 'sleep', 'learning']
        elif 'lazy' in self.personality_traits:
            return ['sleep', 'food', 'work', 'social', 'learning']
        else:
            # Default/explorer personality
            return ['food', 'work', 'sleep', 'social', 'learning']
    
    def seek_social_interaction(self):
        """Look for other agents to socialize with."""
        if self.pos is None:
            return False
            
        # Look for agents across the grid (simplified approach)
        nearby_agents = []
        current_x, current_y = self.pos
        
        for cell in self.model.grid.coord_iter():
            cell_contents = cell[0]  # List of agents at this cell
            x, y = cell[1]
            
            for obj in cell_contents:
                if isinstance(obj, CitizenAgent) and obj != self and not obj.is_dead:
                    # Check friendship score - prefer friends
                    friendship_bonus = self.friendships.get(obj.unique_id, 0) * 0.1
                    distance = abs(x - current_x) + abs(y - current_y)
                    
                    # Only consider nearby agents (within 5 cells)
                    if distance <= 5:
                        score = friendship_bonus - distance
                        nearby_agents.append((obj, (x, y), score))
        
        if nearby_agents:
            # Choose the best target (highest score)
            target_agent, target_pos, _ = max(nearby_agents, key=lambda x: x[2])
            self.move_towards(target_pos)
            return True
        return False
    
    def check_for_social_interactions(self):
        """Check if there are other agents at the same location to interact with."""
        if self.pos is None:
            return
            
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        other_agents = [obj for obj in cell_contents 
                       if isinstance(obj, CitizenAgent) and obj != self and not obj.is_dead]
        
        if other_agents:
            # Social interaction happens!
            for other_agent in other_agents:
                # Both agents reduce social need
                self.social = max(0, self.social - 40)
                other_agent.social = max(0, other_agent.social - 40)
                
                # Increase friendship scores
                if other_agent.unique_id not in self.friendships:
                    self.friendships[other_agent.unique_id] = 0
                if self.unique_id not in other_agent.friendships:
                    other_agent.friendships[self.unique_id] = 0
                    
                self.friendships[other_agent.unique_id] += 5
                other_agent.friendships[self.unique_id] += 5
                
                # Cap friendship at 100
                self.friendships[other_agent.unique_id] = min(100, self.friendships[other_agent.unique_id])
                other_agent.friendships[self.unique_id] = min(100, other_agent.friendships[self.unique_id])
    
    def manage_family(self):
        """Handle family formation, maintenance, and reproduction."""
        if self.family_id is not None:
            # Already in a family, increment survival time
            self.family_survival_time += 1
            
            # Check if it's time to have children (after 30 steps, was 50)
            if self.family_survival_time >= 30 and len(self.children) == 0 and random.random() < 0.15:  # Was 0.1, higher chance
                self.try_reproduce()
        else:
            # Not in a family, look for a partner
            self.try_form_family()
    
    def try_form_family(self):
        """Try to form a family with a compatible agent."""
        if self.pos is None:
            return
            
        # Look for potential partners (opposite gender, high friendship, nearby)
        for agent_id, friendship_score in self.friendships.items():
            if friendship_score >= 50:  # Was 60, easier family formation
                partner = self.model.get_agent_by_id(agent_id)
                if (partner and not partner.is_dead and 
                    partner.gender != self.gender and 
                    partner.family_id is None):
                    
                    # Check if they're close enough (within 4 cells, was 3)
                    if partner.pos is not None:
                        distance = abs(partner.pos[0] - self.pos[0]) + abs(partner.pos[1] - self.pos[1])
                        if distance <= 4:
                            # Form family!
                            family_id = f"family_{self.unique_id}_{partner.unique_id}"
                            self.family_id = family_id
                            self.partner_id = partner.unique_id
                            partner.family_id = family_id
                            partner.partner_id = self.unique_id
                            
                            # Start family survival time
                            self.family_survival_time = 0
                            partner.family_survival_time = 0
                            
                            print(f"Family formed: Agent {self.unique_id} + Agent {partner.unique_id}")
                            break
    
    def try_reproduce(self):
        """Try to create a child agent."""
        partner = self.model.get_agent_by_id(self.partner_id)
        if partner and not partner.is_dead and partner.family_id == self.family_id:
            # Create child with mixed personality traits
            child = self.model.create_child_agent(self, partner)
            if child:
                self.children.append(child.unique_id)
                partner.children.append(child.unique_id)
                print(f"Child born! Parents: {self.unique_id} & {partner.unique_id}, Child: {child.unique_id}")
    
    def develop_skills(self):
        """Develop skills based on actions and personality."""
        # Base skill development rate
        base_rate = 0.1
        
        # Personality influences skill development
        if 'greedy' in self.personality_traits:
            self.trading = min(100, self.trading + base_rate * 2)
        if 'friendly' in self.personality_traits:
            self.learning = min(100, self.learning + base_rate * 1.5)
        if 'lazy' in self.personality_traits:
            # Lazy agents develop skills slower but still learn
            all_skills = [self.farming, self.crafting, self.trading, self.combat, self.learning]
            slowest_skill = min(all_skills)
            if slowest_skill == self.farming:
                self.farming = min(100, self.farming + base_rate * 0.8)
            elif slowest_skill == self.crafting:
                self.crafting = min(100, self.crafting + base_rate * 0.8)
        if 'explorer' in self.personality_traits:
            self.combat = min(100, self.combat + base_rate * 1.5)
        
        # Random general skill improvement
        if random.random() < 0.3:
            skill_choice = random.choice(['farming', 'crafting', 'trading', 'combat', 'learning'])
            current_skill = getattr(self, skill_choice)
            setattr(self, skill_choice, min(100, current_skill + base_rate))
    
    def update_profession(self):
        """Update profession based on highest skills and opportunities."""
        # Only update profession every 20 steps to avoid constant changes
        if self.age % 20 != 0:
            return
            
        skills = {
            'farmer': self.farming,
            'craftsman': self.crafting,
            'merchant': self.trading,
            'guard': self.combat,
            'scholar': self.learning
        }
        
        # Find the profession with highest skill
        best_profession = max(skills.keys(), key=lambda k: skills[k])
        best_skill_level = skills[best_profession]
        
        # Only change profession if skill is significantly higher (>15 points) or no profession
        current_skill = 0
        if self.profession is not None:
            profession_skill_map = {
                'farmer': self.farming,
                'craftsman': self.crafting,
                'merchant': self.trading,
                'guard': self.combat,
                'scholar': self.learning
            }
            current_skill = profession_skill_map.get(self.profession, 0)
        
        if self.profession is None or best_skill_level > current_skill + 15:
            old_profession = self.profession
            self.profession = best_profession
            self.work_experience = 0  # Reset experience in new profession
            
            if old_profession != best_profession and old_profession is not None:
                print(f"Agent {self.unique_id} changed profession from {old_profession} to {best_profession}")
    
    def apply_community_influence(self):
        """Apply community-based behavioral modifications."""
        community = self.model.get_community_at_position(self.pos)
        if community:
            self.community_id = community['id']
            
            # Community influence based on dominant personality traits
            if community['dominant_trait'] == 'greedy':
                # Greedy communities increase competition and stealing
                if 'greedy' not in self.personality_traits and random.random() < 0.1:
                    # Non-greedy agents become more selfish in greedy communities
                    self.coins += 1  # Small selfish bonus
            elif community['dominant_trait'] == 'friendly':
                # Friendly communities encourage cooperation
                if 'friendly' in self.personality_traits and random.random() < 0.2:
                    self.share_resources_with_family()
    
    def share_resources_with_family(self):
        """Share resources with family members if friendly."""
        if self.family_id is None or 'friendly' not in self.personality_traits:
            return
            
        partner = self.model.get_agent_by_id(self.partner_id)
        if partner and not partner.is_dead:
            # Share coins if one partner is poor
            if self.coins > 5 and partner.coins < 3:
                transfer = min(2, self.coins - 3)
                self.coins -= transfer
                partner.coins += transfer
                # Increase friendship for sharing
                if partner.unique_id in self.friendships:
                    self.friendships[partner.unique_id] = min(100, self.friendships[partner.unique_id] + 2)
                if self.unique_id in partner.friendships:
                    partner.friendships[self.unique_id] = min(100, partner.friendships[self.unique_id] + 2)


    def choose_action(self):
        """Decide what action to take based on current needs and personality."""
        # Check if we should explore randomly (especially for explorers)
        if random.random() < self.exploration_rate:
            self.move_randomly()
            return
        
        # Get decision priorities based on personality
        priorities = self.get_action_priorities()
        
        # Execute actions based on priority order
        for action in priorities:
            if action == 'social' and self.social >= self.social_threshold:
                # Try temple first for social needs, then regular social interaction
                if not self.seek_temple() and not self.seek_social_interaction():
                    pass
                else:
                    break
            elif action == 'food' and self.hunger >= self.hunger_threshold:
                if 'greedy' in self.personality_traits and self.coins < 3:
                    # Greedy agents prefer jobs even when hungry if low on coins
                    if self.seek_job():
                        break
                elif self.coins > 0:
                    self.seek_food()
                    break
                elif self.hunger >= self.hunger_threshold:
                    # Desperate for food, go to job or steal
                    if not self.seek_job():
                        self.seek_food()  # Will steal if necessary
                    break
            elif action == 'work' and (self.coins < 3 or ('greedy' in self.personality_traits and self.coins < 8)):
                # Try profession-specific buildings first, then regular jobs
                if not self.seek_profession_building() and not self.seek_job():
                    pass
                else:
                    break
            elif action == 'sleep' and self.energy <= self.energy_threshold:
                self.seek_house()
                break
            elif action == 'learning' and random.random() < 0.3:
                # Occasional learning-focused behavior
                if self.seek_school():
                    break
        else:
            # No urgent needs, consider skill development or move randomly
            if random.random() < 0.4:
                # 40% chance to seek skill development when no urgent needs
                if not self.seek_skill_development_building():
                    self.move_randomly()
            else:
                self.move_randomly()
            
        # Check if we can interact with environment at current location
        self.interact_with_environment()
    
    def seek_food(self):
        """Move towards the nearest food source."""
        food_positions = []
        
        # Look for food in the grid
        for cell in self.model.grid.coord_iter():
            cell_content, (x, y) = cell
            for obj in cell_content:
                if hasattr(obj, 'type') and obj.type == 'food':
                    food_positions.append((x, y))
                    self.known_food_locations.add((x, y))
        
        if food_positions and self.pos is not None:
            # Find nearest food
            current_x, current_y = self.pos
            nearest_food = min(food_positions, 
                             key=lambda pos: abs(pos[0] - current_x) + abs(pos[1] - current_y))
            self.move_towards(nearest_food)
        else:
            # No food visible, move randomly
            self.move_randomly()
    
    def seek_house(self):
        """Move towards the nearest house."""
        house_positions = []
        
        # Look for houses in the grid
        for cell in self.model.grid.coord_iter():
            cell_content, (x, y) = cell
            for obj in cell_content:
                if hasattr(obj, 'type') and obj.type == 'house':
                    house_positions.append((x, y))
        
        if house_positions and self.pos is not None:
            # Find nearest house
            current_x, current_y = self.pos
            nearest_house = min(house_positions,
                              key=lambda pos: abs(pos[0] - current_x) + abs(pos[1] - current_y))
            self.move_towards(nearest_house)
        else:
            # No house visible, move randomly
            self.move_randomly()
    
    def seek_temple(self):
        """Move towards the nearest temple for social and spiritual needs."""
        temple_positions = []
        
        # Look for temples in the grid
        for cell in self.model.grid.coord_iter():
            cell_content, (x, y) = cell
            for obj in cell_content:
                if hasattr(obj, 'type') and obj.type == 'temple':
                    temple_positions.append((x, y))
        
        if temple_positions and self.pos is not None:
            # Find nearest temple
            current_x, current_y = self.pos
            nearest_temple = min(temple_positions,
                               key=lambda pos: abs(pos[0] - current_x) + abs(pos[1] - current_y))
            self.move_towards(nearest_temple)
            return True
        return False
    
    def seek_school(self):
        """Move towards the nearest school for learning."""
        school_positions = []
        
        # Look for schools in the grid
        for cell in self.model.grid.coord_iter():
            cell_content, (x, y) = cell
            for obj in cell_content:
                if hasattr(obj, 'type') and obj.type == 'school':
                    school_positions.append((x, y))
        
        if school_positions and self.pos is not None:
            # Find nearest school
            current_x, current_y = self.pos
            nearest_school = min(school_positions,
                               key=lambda pos: abs(pos[0] - current_x) + abs(pos[1] - current_y))
            self.move_towards(nearest_school)
            return True
        return False
    
    def seek_profession_building(self):
        """Seek a building that matches agent's profession."""
        if self.profession is None:
            return False
        
        target_building = None
        if self.profession == 'merchant':
            target_building = 'market'
        elif self.profession == 'craftsman':
            target_building = 'workshop'
        elif self.profession == 'scholar':
            target_building = 'school'
        else:
            return False  # No specific building for this profession
        
        # Look for the target building
        building_positions = []
        for cell in self.model.grid.coord_iter():
            cell_content, (x, y) = cell
            for obj in cell_content:
                if hasattr(obj, 'type') and obj.type == target_building:
                    building_positions.append((x, y))
        
        if building_positions and self.pos is not None:
            # Find nearest building
            current_x, current_y = self.pos
            nearest_building = min(building_positions,
                                 key=lambda pos: abs(pos[0] - current_x) + abs(pos[1] - current_y))
            self.move_towards(nearest_building)
            return True
        return False
    
    def seek_skill_development_building(self):
        """Seek a building to develop the agent's weakest skill."""
        if self.pos is None:
            return False
        
        # Find weakest skill
        skills = {
            'farming': self.farming,
            'crafting': self.crafting,
            'trading': self.trading,
            'combat': self.combat,
            'learning': self.learning
        }
        
        weakest_skill = min(skills.keys(), key=lambda k: skills[k])
        
        # Map skills to buildings
        skill_to_building = {
            'trading': 'market',
            'crafting': 'workshop',
            'learning': 'school'
            # farming and combat don't have specific buildings
        }
        
        target_building = skill_to_building.get(weakest_skill)
        if target_building is None:
            return False
        
        # Look for the target building
        building_positions = []
        for cell in self.model.grid.coord_iter():
            cell_content, (x, y) = cell
            for obj in cell_content:
                if hasattr(obj, 'type') and obj.type == target_building:
                    building_positions.append((x, y))
        
        if building_positions:
            # Find nearest building
            current_x, current_y = self.pos
            nearest_building = min(building_positions,
                                 key=lambda pos: abs(pos[0] - current_x) + abs(pos[1] - current_y))
            self.move_towards(nearest_building)
            return True
        return False
    
    def move_towards(self, target_pos):
        """Move one step towards the target position."""
        if self.pos is None:
            return
            
        current_x, current_y = self.pos
        target_x, target_y = target_pos
        
        # Calculate direction to move
        dx = 0 if current_x == target_x else (1 if target_x > current_x else -1)
        dy = 0 if current_y == target_y else (1 if target_y > current_y else -1)
        
        # Try to move in the calculated direction
        new_x = current_x + dx
        new_y = current_y + dy
        
        # Make sure the new position is within bounds
        if (0 <= new_x < self.model.grid.width and 
            0 <= new_y < self.model.grid.height):
            self.model.grid.move_agent(self, (new_x, new_y))
    
    def seek_job(self):
        """Move towards the nearest job."""
        closest_job = None
        min_distance = float('inf')
        current_x, current_y = self.pos
        
        # Find closest job
        for cell in self.model.grid.coord_iter():
            cell_contents = cell[0]  # List of agents at this cell
            x, y = cell[1]
            
            for obj in cell_contents:
                if hasattr(obj, 'type') and obj.type == 'job':
                    distance = abs(x - current_x) + abs(y - current_y)
                    if distance < min_distance:
                        min_distance = distance
                        closest_job = (x, y)
        
        # Move towards closest job
        if closest_job:
            target_x, target_y = closest_job
            # Simple movement towards target
            if current_x < target_x:
                new_x = min(current_x + 1, target_x)
            elif current_x > target_x:
                new_x = max(current_x - 1, target_x)
            else:
                new_x = current_x
                
            if current_y < target_y:
                new_y = min(current_y + 1, target_y)
            elif current_y > target_y:
                new_y = max(current_y - 1, target_y)
            else:
                new_y = current_y
                
            # Move to new position if valid
            if (0 <= new_x < self.model.grid.width and
                0 <= new_y < self.model.grid.height):
                self.model.grid.move_agent(self, (new_x, new_y))
            return True
        else:
            # No jobs found, move randomly
            self.move_randomly()
            return False

    def move_randomly(self):
        """Move to a random neighboring cell."""
        if self.pos is None:
            return
            
        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        if possible_moves:
            new_position = random.choice(possible_moves)
            self.model.grid.move_agent(self, new_position)
    
    def interact_with_environment(self):
        """Check if the agent can eat food, sleep, or work at current location."""
        if self.pos is None:
            return
            
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        
        for obj in cell_contents:
            if hasattr(obj, 'type'):
                if obj.type == 'food' and self.hunger > 0:
                    # IMPROVED FOOD AFFORDABILITY
                    if self.coins > 0:
                        self.hunger = max(0, self.hunger - 60)  # Was 50, more nutrition
                        # Food is now FREE to encourage survival!
                        # self.coins -= 1  # Commented out - food is now free
                        self.model.remove_agent(obj)  # Remove food from model
                        break
                    # If no coins but very hungry, eat anyway (less penalty)
                    elif self.hunger >= self.hunger_threshold:
                        self.hunger = max(0, self.hunger - 40)  # Was 30, better nutrition when stealing
                        self.health -= 2  # Was 5, less guilt/stress
                        self.model.remove_agent(obj)
                        break
                        
                elif obj.type == 'house' and self.energy < self.max_energy:
                    # IMPROVED SLEEP RECOVERY
                    self.energy = min(self.max_energy, self.energy + 50)  # Was 40, better rest
                    
                elif obj.type == 'job':
                    # IMPROVED JOB ECONOMICS with profession bonus
                    base_pay = 3  # Was 2, better wages
                    profession_bonus = 1 if self.profession in ['farmer', 'craftsman'] else 0
                    job_pay = base_pay + profession_bonus
                    self.coins += job_pay
                    self.energy -= 5  # Was 10, less tiring work
                    
                    # Develop farming skill when working
                    self.farming = min(100, self.farming + 0.5)
                    self.work_experience += 1
                    
                    # Remember this job location
                    if self.pos not in self.known_job_locations:
                        self.known_job_locations.add(self.pos)
                    break
                    
                elif obj.type == 'market':
                    # Market interactions - trading and skill development
                    if self.coins > 2:
                        # Simulate trading activity
                        self.coins -= 1  # Trading cost
                        self.trading = min(100, self.trading + 1.0)  # Develop trading skill
                        
                        # Chance to get better deals based on trading skill
                        if random.random() < (self.trading / 100) * 0.3:
                            self.coins += 2  # Successful trade profit
                    break
                    
                elif obj.type == 'workshop':
                    # Workshop interactions - crafting and skill development
                    if self.energy > 10:
                        self.energy -= 10  # Crafting is tiring
                        self.crafting = min(100, self.crafting + 1.5)  # Develop crafting skill
                        
                        # Chance to create valuable items based on crafting skill
                        if random.random() < (self.crafting / 100) * 0.4:
                            self.coins += 4  # Sell crafted items
                    break
                    
                elif obj.type == 'temple':
                    # Temple interactions - spiritual peace and community
                    self.social = max(0, self.social - 20)  # Reduce loneliness
                    self.health = min(100, self.health + 2)  # Slight health boost from peace
                    
                    # Influence cultural values (simplified)
                    if random.random() < 0.1:
                        print(f"Agent {self.unique_id} found peace at the temple")
                    break
                    
                elif obj.type == 'school':
                    # School interactions - learning and knowledge
                    if self.energy > 5:
                        self.energy -= 5  # Learning requires focus
                        self.learning = min(100, self.learning + 2.0)  # Significant learning boost
                        
                        # Chance to improve other skills through education
                        if random.random() < (self.learning / 100) * 0.3:
                            skill_to_improve = random.choice(['farming', 'crafting', 'trading', 'combat'])
                            current_skill = getattr(self, skill_to_improve)
                            setattr(self, skill_to_improve, min(100, current_skill + 1.0))
                    break


    def update_influence_and_reputation(self):
        """Update agent's social influence and reputation (PHASE 2)."""
        # Influence grows with friendships, wealth, and leadership
        base_influence = len(self.friendships) * 2 + self.coins * 0.05
        
        if self.is_leader:
            base_influence *= 1.5
        
        # Profession-based influence
        if self.profession == 'scholar':
            base_influence += self.learning * 0.2
        elif self.profession == 'merchant':
            base_influence += self.trading * 0.3
        elif self.profession == 'guard':
            base_influence += self.combat * 0.25
        
        self.influence = min(100, base_influence)
        
        # Reputation changes based on actions and social interactions
        if random.random() < 0.1:  # 10% chance per step
            # Random reputation events
            if 'friendly' in self.personality_traits:
                self.reputation = min(100, self.reputation + 1)
            elif 'greedy' in self.personality_traits and random.random() < 0.3:
                self.reputation = max(0, self.reputation - 0.5)
    
    def attempt_trading(self):
        """Attempt to trade with other agents (PHASE 2)."""
        if self.profession != 'merchant' and random.random() > 0.2:
            return  # Non-merchants trade less frequently
        
        # Find potential trade partners nearby
        if self.pos is None:
            return
        
        nearby_agents = []
        current_x, current_y = self.pos
        
        for agent in self.model.schedule.agents:
            if (isinstance(agent, CitizenAgent) and agent != self and 
                not agent.is_dead and agent.pos is not None):
                
                ax, ay = agent.pos
                distance = abs(ax - current_x) + abs(ay - current_y)
                if distance <= 3:  # Close enough to trade
                    nearby_agents.append(agent)
        
        if nearby_agents:
            trade_partner = random.choice(nearby_agents)
            self.execute_trade(trade_partner)
    
    def execute_trade(self, partner):
        """Execute a trade with another agent."""
        # Simple resource exchange
        if self.coins > 5 and partner.coins > 5:
            # Basic coin exchange with skill bonus
            trade_skill_bonus = (self.trading + partner.trading) * 0.01
            
            if random.random() < 0.5 + trade_skill_bonus:
                # Successful trade
                trade_amount = min(3, self.coins // 3, partner.coins // 3)
                
                # Both agents benefit from trade
                self.coins += trade_amount
                partner.coins += trade_amount
                
                # Build trade relationship
                self.trade_partners.add(partner.unique_id)
                partner.trade_partners.add(self.unique_id)
                
                # Improve trading skills
                self.trading = min(100, self.trading + 0.5)
                partner.trading = min(100, partner.trading + 0.5)
                
                # Track global trade volume
                self.model.trade_volume += trade_amount * 2
                
                if random.random() < 0.1:  # 10% chance to announce
                    print(f"💰 Trade: Agent {self.unique_id} ⟷ Agent {partner.unique_id} ({trade_amount} coins each)")
    
    def consider_leadership_actions(self):
        """Consider taking leadership actions if agent is ambitious (PHASE 2)."""
        if not self.is_leader and self.leadership_ambition > 70:
            # Try to become a leader
            if (self.influence > 30 and self.reputation > 60 and 
                len(self.friendships) > 5 and random.random() < 0.05):
                
                # Challenge for leadership or start new community
                if len(self.model.leaders) < 3:  # Max 3 leaders
                    self.is_leader = True
                    community_id = f"new_community_{self.unique_id}"
                    self.model.leaders[community_id] = self.unique_id
                    print(f"👑 Agent {self.unique_id} rises to leadership!")
        
        elif self.is_leader:
            # Leaders take community actions
            if random.random() < 0.2:  # 20% chance per step
                self.perform_leadership_action()
    
    def perform_leadership_action(self):
        """Perform an action as a community leader."""
        # Leaders can influence their followers
        followers = [a for a in self.model.schedule.agents 
                    if (isinstance(a, CitizenAgent) and not a.is_dead and 
                        a.unique_id in self.friendships and self.friendships[a.unique_id] > 70)]
        
        if followers and random.random() < 0.3:
            action_type = random.choice(['inspire', 'organize', 'mediate'])
            
            if action_type == 'inspire':
                # Boost follower skills
                for follower in followers[:3]:  # Max 3 at a time
                    follower.energy = min(follower.max_energy, follower.energy + 10)
                    follower.social = max(0, follower.social - 15)
                    
            elif action_type == 'organize':
                # Coordinate resource sharing
                wealthy_followers = [f for f in followers if f.coins > 50]
                poor_followers = [f for f in followers if f.coins < 20]
                
                for wealthy in wealthy_followers[:2]:
                    for poor in poor_followers[:2]:
                        transfer = min(5, wealthy.coins // 10)
                        wealthy.coins -= transfer
                        poor.coins += transfer
                        
            elif action_type == 'mediate':
                # Resolve conflicts and improve relationships
                for follower in followers[:2]:
                    follower.reputation = min(100, follower.reputation + 2)

    # PHASE 3: Advanced civilization behaviors
    
    def engage_in_cultural_activities(self):
        """Participate in cultural development and artistic creation."""
        # Artists create artworks when they have high artistic skill and good conditions
        if (self.artistic_skill > 50 or self.profession == 'merchant') and self.energy > 60:
            if random.random() < 0.02:  # 2% chance per step
                self.cultural_contributions += 1
                self.model.art_works += 1
                self.artistic_skill = min(100, self.artistic_skill + 2)
                print(f"🎨 Agent {self.unique_id} creates art! (Skill: {self.artistic_skill})")
                
                # Art creation boosts social satisfaction
                self.social = max(0, self.social - 20)
                self.energy -= 15
        
        # Participate in festivals when they happen
        if (hasattr(self.model, 'festivals_held') and 
            len(self.cultural_memory) < self.model.festivals_held):
            self.cultural_memory.append(f"festival_{self.model.festivals_held}")
            self.social = max(0, self.social - 15)
            self.health = min(self.max_health, self.health + 3)
    
    def conduct_research_activities(self):
        """Engage in scientific research and knowledge development."""
        # Scholars with high learning engage in research
        if (self.profession == 'scholar' and self.learning > 40 and 
            'education' in self.model.technologies):
            
            # Choose research focus if not set
            if self.research_focus == 'none':
                available_topics = ['medicine', 'engineering', 'philosophy', 'astronomy']
                self.research_focus = random.choice(available_topics)
            
            # Make research progress
            if random.random() < 0.1:  # 10% chance per step for scholars
                self.research_progress += self.learning // 10
                self.learning = min(100, self.learning + 1)
                
                # Significant discovery chance
                if self.research_progress > 100:
                    self.model.scientific_discoveries += 1
                    print(f"🔬 Agent {self.unique_id} makes breakthrough in {self.research_focus}!")
                    self.research_progress = 0
                    self.reputation = min(100, self.reputation + 10)
                    
                    # Reset to new research topic
                    topics = ['medicine', 'engineering', 'philosophy', 'astronomy', 'mathematics']
                    self.research_focus = random.choice(topics)
    
    def participate_in_conflict_resolution(self):
        """Mediate conflicts and promote peace."""
        # Agents with high diplomatic skill can resolve conflicts
        if (self.diplomatic_skill > 40 and self.political_alignment == 'peaceful' and 
            len(self.model.conflicts) > 0):
            
            if random.random() < 0.05:  # 5% chance per step
                # Try to mediate an ongoing conflict
                conflict = random.choice(self.model.conflicts)
                mediation_success = self.diplomatic_skill + random.randint(1, 30)
                
                if mediation_success > 70:
                    # Successful mediation!
                    self.model.conflicts.remove(conflict)
                    self.model.conflicts_resolved += 1
                    self.conflicts_mediated += 1
                    self.diplomatic_skill = min(100, self.diplomatic_skill + 3)
                    self.reputation = min(100, self.reputation + 5)
                    print(f"🕊️ Agent {self.unique_id} successfully mediates conflict!")
                    
                    # Boost health and social satisfaction from helping others
                    self.health = min(self.max_health, self.health + 5)
                    self.social = max(0, self.social - 10)
                else:
                    # Failed mediation
                    self.energy -= 10  # Mediation attempts are exhausting
    
    def develop_diplomatic_relations(self):
        """Form alliances and diplomatic relationships."""
        # High-reputation agents can form political alliances
        if self.reputation > 60 and len(self.alliance_preferences) < 5:
            
            # Look for potential alliance partners from all agents
            potential_partners = []
            for agent in self.model.agents:
                if (isinstance(agent, CitizenAgent) and agent != self and 
                    not agent.is_dead and agent.reputation > 50):
                    potential_partners.append(agent)
            
            # Form alliance with compatible agent
            if potential_partners and random.random() < 0.01:  # Reduced chance for stability
                partner = random.choice(potential_partners)
                compatibility = (
                    (self.political_alignment == partner.political_alignment) * 30 +
                    (abs(self.reputation - partner.reputation) < 20) * 20 +
                    random.randint(1, 50)
                )
                
                if compatibility > 70:
                    # Successful alliance formation
                    self.alliance_preferences[partner.unique_id] = compatibility
                    partner.alliance_preferences[self.unique_id] = compatibility
                    
                    # Simple alliance tracking - just print success
                    print(f"🤝 Personal alliance formed between Agent {self.unique_id} and {partner.unique_id}")


class Food(Agent):
    """Food object that agents can eat."""
    
    def __init__(self, model):
        super().__init__(model)
        self.type = 'food'
    
    def step(self):
        pass  # Food doesn't do anything on its own


class Job(Agent):
    """A stationary job that provides income."""
    
    def __init__(self, model):
        super().__init__(model)
        self.type = 'job'
        self.pay_per_work = 2  # Coins earned per work session
        
    def step(self):
        """Jobs don't do anything on their own."""
        pass


class House(Agent):
    """House object where agents can sleep."""
    
    def __init__(self, model):
        super().__init__(model)
        self.type = 'house'
    
    def step(self):
        pass  # Houses don't do anything on their own


class Market(Agent):
    """Market where agents can trade resources and improve trading skills."""
    
    def __init__(self, model):
        super().__init__(model)
        self.type = 'market'
        self.trade_bonus = 1.5  # Trading skill improvement multiplier
        
    def step(self):
        pass


class Workshop(Agent):
    """Workshop where agents can craft items and improve crafting skills."""
    
    def __init__(self, model):
        super().__init__(model)
        self.type = 'workshop'
        self.craft_bonus = 1.5  # Crafting skill improvement multiplier
        
    def step(self):
        pass


class Temple(Agent):
    """Temple where agents can find peace and community influence."""
    
    def __init__(self, model):
        super().__init__(model)
        self.type = 'temple'
        self.spiritual_bonus = 20  # Social need reduction
        
    def step(self):
        pass


class School(Agent):
    """School where agents can learn and improve learning skills."""
    
    def __init__(self, model):
        super().__init__(model)
        self.type = 'school'
        self.learning_bonus = 2.0  # Learning skill improvement multiplier
        
    def step(self):
        pass
