"""
Expanded Specialized AI Agents for VHS Horror Game Development

This module adds the specialized agents you requested for comprehensive
game development with multi-phase collaboration and Ollama optimization.

New Agents Added:
- Story Weaver Agent - Masterful narrative construction
- Psychology Agent - Player retention and engagement strategies  
- Game Expert Agent - Puzzle-story integration mapping
- 80s Pop Culture Agent - Nostalgic callback integration
- UX/UI Agent - Interface and user experience design
- Creative Features Agent - Innovative gameplay mechanics
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from mcp.types import TextContent
from tools.models import ToolOutput
from tools.shared.exceptions import ToolExecutionError
from utils.conversation_memory import add_turn, get_thread
from utils.model_context import ModelContext
from utils.token_utils import estimate_tokens

logger = logging.getLogger(__name__)


class StoryWeaverAgent:
    """Masterful narrative construction with exceptional wordcraft"""
    
    def __init__(self):
        self.name = "story_weaver"
        self.description = "Masterful story construction with exceptional wordcraft and emotional impact"
        self.preferred_model = "ollama"  # Use local for creative writing to save costs
        self.thinking_mode = "high"
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "story_prompt": {
                    "type": "string",
                    "description": "Core story concept or theme"
                },
                "tone": {
                    "type": "string",
                    "enum": ["atmospheric", "visceral", "psychological", "cosmic", "slasher"],
                    "description": "Desired narrative tone",
                    "default": "atmospheric"
                },
                "word_craft_level": {
                    "type": "string",
                    "enum": ["standard", "elevated", "literary", "poetic"],
                    "description": "Level of wordcraft sophistication",
                    "default": "elevated"
                },
                "scenes": {
                    "type": "integer",
                    "description": "Number of scenes to develop",
                    "default": 5
                },
                "emotional_arc": {
                    "type": "string",
                    "description": "Emotional journey of the story",
                    "default": "dread to terror to revelation"
                }
            },
            "required": ["story_prompt"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute story weaving with masterful wordcraft"""
        story_prompt = arguments["story_prompt"]
        tone = arguments.get("tone", "atmospheric")
        word_craft = arguments.get("word_craft_level", "elevated")
        scenes = arguments.get("scenes", 5)
        emotional_arc = arguments.get("emotional_arc", "dread to terror to revelation")
        
        # Build sophisticated narrative context
        context = self._build_story_weaving_context(story_prompt, tone, word_craft, scenes, emotional_arc)
        
        # Execute with local model for cost efficiency
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]
    
    def _build_story_weaving_context(self, story_prompt: str, tone: str, word_craft: str, scenes: int, emotional_arc: str) -> str:
        return f"""
🎭 MASTERFUL STORY WEAVING SESSION

**Core Concept:** {story_prompt}
**Narrative Tone:** {tone}
**Wordcraft Level:** {word_craft}
**Emotional Arc:** {emotional_arc}
**Scenes Required:** {scenes}

**ARTISTIC REQUIREMENTS:**
- Craft prose with exceptional word choice and rhythm
- Build atmosphere through sensory details and subtext
- Create emotional resonance that lingers beyond the page
- Use language that feels both timeless and immediate
- Employ metaphors and imagery that enhance rather than distract

**CRAFTSMANSHIP STANDARDS:**
- Sentence structure should vary for musicality
- Word choice must be precise and evocative
- Pacing should match the emotional beats
- Dialogue (if any) must reveal character and advance plot
- Descriptions should serve multiple purposes

**HORROR-SPECIFIC ELEMENTS:**
- Build dread through implication rather than explicit description
- Use silence and what's not said as powerfully as what is
- Create unease through familiar things made strange
- Make the reader complicit in the horror
- Leave room for the imagination to amplify fear

**OUTPUT FORMAT:**
For each scene:
1. **Scene Title** (evocative and thematic)
2. **Atmospheric Setup** (sensory details)
3. **Narrative Flow** (the story beats)
4. **Emotional Payoff** (what the reader feels)
5. **Lingering Elements** (what stays with them)

**WORDCRAFT CHALLENGE:**
- Use at least 3 unique metaphors per scene
- Employ alliteration and assonance where natural
- Vary sentence length for rhythm
- Choose words that carry emotional weight
- Make every paragraph earn its place

Begin weaving this story with the care of a master artisan. 🖋️
"""


class PsychologyAgent:
    """Player retention and engagement strategy expert"""
    
    def __init__(self):
        self.name = "psychology"
        self.description = "Player psychology and retention strategy optimization"
        self.preferred_model = "ollama"  # Local for sensitive player data
        self.thinking_mode = "medium"
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "player_data": {
                    "type": "object",
                    "description": "Anonymous player behavior data"
                },
                "retention_goals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific retention objectives",
                    "default": ["session length", "return rate", "engagement depth"]
                },
                "game_type": {
                    "type": "string",
                    "enum": ["puzzle", "horror", "narrative", "hybrid"],
                    "description": "Primary game genre",
                    "default": "hybrid"
                },
                "difficulty_profile": {
                    "type": "string",
                    "enum": ["easy", "medium", "hard", "adaptive"],
                    "description": "Current difficulty approach",
                    "default": "adaptive"
                }
            },
            "required": ["player_data"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute psychology analysis for retention optimization"""
        player_data = arguments["player_data"]
        retention_goals = arguments.get("retention_goals", ["session length", "return rate"])
        game_type = arguments.get("game_type", "hybrid")
        difficulty_profile = arguments.get("difficulty_profile", "adaptive")
        
        context = self._build_psychology_context(player_data, retention_goals, game_type, difficulty_profile)
        
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]
    
    def _build_psychology_context(self, player_data: Dict, retention_goals: List[str], game_type: str, difficulty_profile: str) -> str:
        return f"""
🧠 PLAYER PSYCHOLOGY ANALYSIS

**Game Type:** {game_type}
**Difficulty Profile:** {difficulty_profile}
**Retention Goals:** {', '.join(retention_goals)}
**Player Data:** {json.dumps(player_data, indent=2)}

**PSYCHOLOGICAL ANALYSIS REQUIREMENTS:**
1. **Flow State Optimization** - Identify moments where players enter/exit flow
2. **Reward Scheduling** - Optimize timing and type of rewards
3. **Challenge Curve** - Ensure difficulty progression matches skill development
4. **Emotional Arc** - Map emotional journey and identify drop-off points
5. **Cognitive Load** - Assess mental fatigue and complexity management

**RETENTION STRATEGIES TO ANALYZE:**
- **Variable Ratio Reinforcement** - Unpredictable rewards
- **Progressive Disclosure** - Gradual revelation of complexity
- **Competence Building** - Skill development and mastery
- **Social Proof** - Leaderboards, sharing, community
- **Sunk Cost** - Investment and completion motivation
- **Curiosity Gap** - Information gaps that drive continued play

**HORROR-SPECIFIC PSYCHOLOGY:**
- **Safe Fear** - Balance between terror and comfort
- **Catharsis Timing** - When to release tension
- **Anticipation vs. Payoff** - Buildup management
- **Control vs. Helplessness** - Player agency optimization
- **Uncanny Valley** - Familiar made strange

**OUTPUT FORMAT:**
1. **Current State Analysis** - What's working/not working
2. **Retention Leaks** - Where players disengage
3. **Optimization Strategies** - Specific, actionable improvements
4. **Implementation Priority** - What to fix first
5. **Success Metrics** - How to measure improvement

Provide data-driven psychological insights for maximum player retention. 📊
"""


class GameExpertAgent:
    """Puzzle-story integration mapping specialist"""
    
    def __init__(self):
        self.name = "game_expert"
        self.description = "Puzzle-story integration and game design mapping"
        self.preferred_model = "gemini-pro"  # Need advanced analysis for complex integration
        self.thinking_mode = "high"
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "puzzle_mechanics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of puzzle mechanics to integrate"
                },
                "story_elements": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key story beats and themes"
                },
                "integration_goals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "How puzzles should serve the story",
                    "default": ["thematic resonance", "progression", "revelation"]
                },
                "player_experience": {
                    "type": "string",
                    "enum": ["linear", "branching", "exploration", "mystery"],
                    "description": "Desired player journey",
                    "default": "mystery"
                }
            },
            "required": ["puzzle_mechanics", "story_elements"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute game design integration mapping"""
        puzzle_mechanics = arguments["puzzle_mechanics"]
        story_elements = arguments["story_elements"]
        integration_goals = arguments.get("integration_goals", ["thematic resonance"])
        player_experience = arguments.get("player_experience", "mystery")
        
        context = self._build_integration_context(puzzle_mechanics, story_elements, integration_goals, player_experience)
        
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]
    
    def _build_integration_context(self, puzzle_mechanics: List[str], story_elements: List[str], 
                                 integration_goals: List[str], player_experience: str) -> str:
        return f"""
🎮 GAME DESIGN INTEGRATION MAPPING

**Puzzle Mechanics:** {', '.join(puzzle_mechanics)}
**Story Elements:** {', '.join(story_elements)}
**Integration Goals:** {', '.join(integration_goals)}
**Player Experience:** {player_experience}

**INTEGRATION REQUIREMENTS:**
1. **Mechanical Storytelling** - How puzzles advance narrative
2. **Thematic Resonance** - Puzzles that reflect story themes
3. **Progressive Complexity** - Difficulty curve matching story arc
4. **Revelation Timing** - When story beats are revealed through puzzles
5. **Player Agency** - How choices in puzzles affect story

**DESIGN PRINCIPLES TO APPLY:**
- **Show, Don't Tell** - Story revealed through gameplay
- **Environmental Storytelling** - Puzzles as narrative devices
- **Metaphorical Mechanics** - Puzzles as story metaphors
- **Pacing Integration** - Puzzle difficulty matching story tension
- **Choice Consequences** - Player decisions having narrative weight

**PUZZLE-STORY MAPPING:**
For each puzzle mechanic, define:
- **Narrative Purpose** - What story element it reveals
- **Thematic Connection** - How it reflects story themes
- **Emotional Impact** - What feeling it should evoke
- **Progression Role** - How it advances the overall arc
- **Integration Method** - Specific ways to weave story into mechanics

**OUTPUT FORMAT:**
1. **Integration Matrix** - Puzzle mechanics vs story elements
2. **Progression Map** - How complexity builds with story
3. **Thematic Weaving** - Specific integration techniques
4. **Player Journey** - Complete experience flow
5. **Implementation Guide** - Step-by-step integration plan

Create a comprehensive blueprint for seamless puzzle-story integration. 🗺️
"""


class PopCultureAgent:
    """80s pop culture callback integration specialist"""
    
    def __init__(self):
        self.name = "pop_culture"
        self.description = "80s pop culture callback integration and nostalgic elements"
        self.preferred_model = "ollama"  # Local for creative callback generation
        self.thinking_mode = "medium"
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "decade": {
                    "type": "string",
                    "enum": ["80s", "90s", "retro"],
                    "description": "Primary nostalgic era",
                    "default": "80s"
                },
                "callback_type": {
                    "type": "array",
                    "items": {"type": "string"},
                    "enum": ["movies", "music", "tv", "games", "fashion", "technology"],
                    "description": "Types of callbacks to generate",
                    "default": ["movies", "music", "games"]
                },
                "integration_level": {
                    "type": "string",
                    "enum": ["subtle", "prominent", "thematic", "environmental"],
                    "description": "How prominent callbacks should be",
                    "default": "subtle"
                },
                "target_audience": {
                    "type": "string",
                    "enum": ["nostalgic adults", "retro enthusiasts", "general gamers"],
                    "description": "Primary audience for callbacks",
                    "default": "nostalgic adults"
                }
            },
            "required": ["decade"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute pop culture callback generation"""
        decade = arguments["decade"]
        callback_types = arguments.get("callback_type", ["movies", "music"])
        integration_level = arguments.get("integration_level", "subtle")
        target_audience = arguments.get("target_audience", "nostalgic adults")
        
        context = self._build_pop_culture_context(decade, callback_types, integration_level, target_audience)
        
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]
    
    def _build_pop_culture_context(self, decade: str, callback_types: List[str], 
                                  integration_level: str, target_audience: str) -> str:
        return f"""
📼 80s POP CULTURE CALLBACK GENERATION

**Era:** {decade}
**Callback Types:** {', '.join(callback_types)}
**Integration Level:** {integration_level}
**Target Audience:** {target_audience}

**CULTURAL ELEMENTS TO DRAW FROM:**
- **Movies:** Horror classics, sci-fi epics, action blockbusters
- **Music:** Synthwave, new wave, hair metal, early hip-hop
- **TV:** Saturday morning cartoons, prime time dramas, variety shows
- **Games:** Arcade cabinets, early home consoles, text adventures
- **Fashion:** Neon colors, big hair, leg warmers, Members Only jackets
- **Technology:** VHS tapes, CRT TVs, early computers, boomboxes

**INTEGRATION METHODS:**
- **Environmental Details** - Background elements that evoke era
- **Audio Cues** - Sound effects and music that trigger nostalgia
- **Visual Style** - Aesthetic choices that reference period media
- **Dialogue References** - Subtle nods in character speech
- **Item Descriptions** - Flavor text with period-appropriate references
- **UI Elements** - Interface design that feels era-appropriate

**CALLBACK REQUIREMENTS:**
- **Authenticity** - Accurate representation of the era
- **Accessibility** - Meaningful even to those who didn't live through it
- **Integration** - Natural fit within game world, not forced references
- **Variety** - Mix of obvious and subtle callbacks
- **Emotional Resonance** - Evoke feelings associated with the era

**OUTPUT FORMAT:**
For each callback type:
1. **Specific References** - Exact movies, songs, shows, etc.
2. **Integration Ideas** - How to incorporate into game
3. **Subtlety Levels** - From Easter eggs to prominent features
4. **Cross-References** - How different callbacks can work together
5. **Modern Twists** - How to make old references feel fresh

Generate nostalgic callbacks that enhance immersion without breaking suspension of disbelief. 🎵
"""


class UXUIAgent:
    """User experience and interface design specialist"""
    
    def __init__(self):
        self.name = "ux_ui"
        self.description = "UX/UI design for optimal player experience and accessibility"
        self.preferred_model = "ollama"  # Local for design iteration
        self.thinking_mode = "medium"
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "game_genre": {
                    "type": "string",
                    "enum": ["puzzle", "horror", "adventure", "simulation"],
                    "description": "Primary game genre",
                    "default": "puzzle"
                },
                "platform": {
                    "type": "string",
                    "enum": ["web", "mobile", "desktop", "console"],
                    "description": "Target platform",
                    "default": "web"
                },
                "accessibility_needs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "enum": ["color_blind", "motor_impairments", "hearing_impairments", "cognitive_accessibility"],
                    "description": "Accessibility requirements",
                    "default": []
                },
                "aesthetic_requirements": {
                    "type": "string",
                    "description": "Visual style requirements",
                    "default": "VHS horror aesthetic"
                }
            },
            "required": ["game_genre", "platform"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute UX/UI design optimization"""
        game_genre = arguments["game_genre"]
        platform = arguments["platform"]
        accessibility_needs = arguments.get("accessibility_needs", [])
        aesthetic_requirements = arguments.get("aesthetic_requirements", "VHS horror aesthetic")
        
        context = self._build_ux_ui_context(game_genre, platform, accessibility_needs, aesthetic_requirements)
        
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]
    
    def _build_ux_ui_context(self, game_genre: str, platform: str, 
                           accessibility_needs: List[str], aesthetic_requirements: str) -> str:
        return f"""
🎨 UX/UI DESIGN OPTIMIZATION

**Game Genre:** {game_genre}
**Platform:** {platform}
**Accessibility Needs:** {', '.join(accessibility_needs) if accessibility_needs else 'None specified'}
**Aesthetic Requirements:** {aesthetic_requirements}

**UX PRINCIPLES TO APPLY:**
1. **Intuitive Navigation** - Players should never feel lost
2. **Clear Feedback** - Immediate response to all player actions
3. **Progressive Disclosure** - Reveal complexity gradually
4. **Consistent Patterns** - Familiar interactions across the game
5. **Error Prevention** - Design to minimize mistakes
6. **Accessibility First** - Universal design principles

**UI DESIGN REQUIREMENTS:**
- **Visual Hierarchy** - Clear prioritization of information
- **Readability** - Text and icons easily distinguishable
- **Responsive Design** - Adapts to different screen sizes
- **Performance** - Fast loading and smooth interactions
- **Aesthetic Consistency** - Visual style matches game theme
- **Brand Identity** - UI reinforces game's personality

**HORROR-SPECIFIC UX CONSIDERATIONS:**
- **Atmospheric UI** - Interface elements enhance mood
- **Diegetic Design** - UI elements exist within game world
- **Tension Management** - UI can build or release tension
- **Immersion Preservation** - Minimize breaking suspension of disbelief
- **Accessibility in Darkness** - Ensure visibility in low-light scenarios

**ACCESSIBILITY REQUIREMENTS:**
- **Color Blind Support** - Don't rely solely on color
- **Motor Impairment Support** - Large targets, alternative input methods
- **Hearing Impairment Support** - Visual alternatives to audio cues
- **Cognitive Accessibility** - Clear instructions, manageable complexity
- **Customization** - Allow players to adjust interface to their needs

**OUTPUT FORMAT:**
1. **Wireframe Concepts** - Layout and element placement
2. **Interaction Patterns** - How players interact with UI
3. **Accessibility Solutions** - Specific accommodations for each need
4. **Aesthetic Integration** - How UI supports VHS horror theme
5. **Implementation Guidelines** - Technical requirements and best practices

Design an interface that's both beautiful and functional, enhancing rather than hindering the player experience. 🖱️
"""


class CreativeFeaturesAgent:
    """Innovative gameplay mechanics and feature design"""
    
    def __init__(self):
        self.name = "creative_features"
        self.description = "Innovative gameplay mechanics and feature design"
        self.preferred_model = "gemini-pro"  # Need advanced creativity for innovation
        self.thinking_mode = "high"
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "core_mechanic": {
                    "type": "string",
                    "description": "Primary gameplay mechanic"
                },
                "innovation_level": {
                    "type": "string",
                    "enum": ["incremental", "novel", "revolutionary"],
                    "description": "Level of innovation desired",
                    "default": "novel"
                },
                "technical_constraints": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Technical limitations to consider",
                    "default": []
                },
                "player_expectations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "What players expect from this genre",
                    "default": []
                }
            },
            "required": ["core_mechanic"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute creative feature design"""
        core_mechanic = arguments["core_mechanic"]
        innovation_level = arguments.get("innovation_level", "novel")
        technical_constraints = arguments.get("technical_constraints", [])
        player_expectations = arguments.get("player_expectations", [])
        
        context = self._build_creative_context(core_mechanic, innovation_level, technical_constraints, player_expectations)
        
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]
    
    def _build_creative_context(self, core_mechanic: str, innovation_level: str, 
                              technical_constraints: List[str], player_expectations: List[str]) -> str:
        return f"""
💡 CREATIVE FEATURE INNOVATION SESSION

**Core Mechanic:** {core_mechanic}
**Innovation Level:** {innovation_level}
**Technical Constraints:** {', '.join(technical_constraints) if technical_constraints else 'None specified'}
**Player Expectations:** {', '.join(player_expectations) if player_expectations else 'Standard genre expectations'}

**INNOVATION REQUIREMENTS:**
1. **Break Expectations** - Challenge genre conventions in meaningful ways
2. **Player Delight** - Create moments of genuine surprise and joy
3. **Meaningful Complexity** - Add depth without overwhelming simplicity
4. **Replay Value** - Features that encourage multiple playthroughs
5. **Shareability** - Moments players want to show others

**CREATIVE CONSTRAINTS TO WORK WITHIN:**
- **Technical Feasibility** - Must work within specified constraints
- **Player Skill Curve** - Should match expected learning progression
- **Thematic Consistency** - Must fit within game's overall theme
- **Development Resources** - Should be implementable within reasonable scope
- **Platform Limitations** - Must work on target platform

**FEATURE CATEGORIES TO EXPLORE:**
- **Mechanical Innovations** - New ways to interact with game systems
- **Narrative Integration** - How story affects gameplay
- **Social Features** - Multiplayer or community elements
- **Procedural Elements** - Dynamic content generation
- **Meta Features** - Game elements that exist outside the game world
- **Accessibility Innovations** - New ways to make games more inclusive

**YOUR SPECIFIC REQUEST:**
You mentioned: "connections bars are colored like normal, but shuffled, followed by simon says?"

This is a brilliant example of creative feature thinking! Let's explore variations:
- **Visual Deception** - UI elements that lie or mislead
- **Memory Challenges** - Testing player recall in novel ways
- **Pattern Recognition** - Hidden systems players must discover
- **Timing Mechanics** - Precision and rhythm-based challenges
- **Choice Consequences** - Decisions that have unexpected outcomes

**OUTPUT FORMAT:**
1. **Feature Concepts** - 3-5 innovative feature ideas
2. **Implementation Approach** - How each could be built
3. **Player Impact** - What each adds to the experience
4. **Risk Assessment** - Potential challenges and solutions
5. **Integration Strategy** - How features work together

Think outside the box and propose features that will make this game truly memorable! 🚀
"""


# Multi-Phase Collaboration System
class PhaseCoordinator:
    """Coordinates multi-phase agent collaboration"""
    
    def __init__(self):
        self.agents = {
            "story_weaver": StoryWeaverAgent(),
            "psychology": PsychologyAgent(),
            "game_expert": GameExpertAgent(),
            "pop_culture": PopCultureAgent(),
            "ux_ui": UXUIAgent(),
            "creative_features": CreativeFeaturesAgent()
        }
    
    async def execute_phase_1(self, project_requirements: Dict[str, Any]) -> Dict[str, str]:
        """Execute Phase 1: Individual agent analysis"""
        logger.info("Starting Phase 1: Individual agent analysis")
        
        phase_1_results = {}
        
        # Run agents in parallel for maximum efficiency
        tasks = []
        
        # Story Weaver Analysis
        if "story" in project_requirements:
            tasks.append(self._run_agent("story_weaver", project_requirements["story"]))
        
        # Psychology Analysis  
        if "player_data" in project_requirements:
            tasks.append(self._run_agent("psychology", {"player_data": project_requirements["player_data"]}))
        
        # Game Expert Analysis
        if "puzzles" in project_requirements and "story" in project_requirements:
            tasks.append(self._run_agent("game_expert", {
                "puzzle_mechanics": project_requirements["puzzles"],
                "story_elements": project_requirements["story"]
            }))
        
        # Pop Culture Analysis
        if "aesthetic" in project_requirements:
            tasks.append(self._run_agent("pop_culture", {"decade": "80s"}))
        
        # UX/UI Analysis
        tasks.append(self._run_agent("ux_ui", {"game_genre": "puzzle", "platform": "web"}))
        
        # Creative Features Analysis
        if "core_mechanic" in project_requirements:
            tasks.append(self._run_agent("creative_features", {"core_mechanic": project_requirements["core_mechanic"]}))
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Agent {i} failed: {result}")
            else:
                phase_1_results[f"agent_{i}"] = result
        
        logger.info(f"Phase 1 completed with {len(phase_1_results)} agent results")
        return phase_1_results
    
    async def execute_phase_2(self, phase_1_results: Dict[str, str]) -> str:
        """Execute Phase 2: Multi-agent consensus and integration"""
        logger.info("Starting Phase 2: Multi-agent consensus and integration")
        
        # Build consensus context from Phase 1 results
        consensus_context = self._build_consensus_context(phase_1_results)
        
        # Use consensus agent for Phase 2
        consensus_agent = self.agents["game_expert"]  # Use game expert for final integration
        result = await consensus_agent.execute({"prompt": consensus_context})
        
        logger.info("Phase 2 completed with consensus integration")
        return result[0].text
    
    async def _run_agent(self, agent_name: str, arguments: Dict[str, Any]) -> str:
        """Run a single agent and return its result"""
        agent = self.agents[agent_name]
        try:
            result = await agent.execute(arguments)
            return result[0].text
        except Exception as e:
            logger.error(f"Agent {agent_name} failed: {e}")
            return f"Error in {agent_name}: {e}"
    
    def _build_consensus_context(self, phase_1_results: Dict[str, str]) -> str:
        """Build context for consensus integration"""
        context = "## MULTI-AGENT CONSENSUS INTEGRATION\n\n"
        context += "### Phase 1 Results Summary:\n\n"
        
        for agent_name, result in phase_1_results.items():
            context += f"#### {agent_name.upper()} Analysis:\n"
            context += f"{result}\n\n"
        
        context += "### Integration Requirements:\n"
        context += "1. **Synthesize** all agent recommendations into cohesive design\n"
        context += "2. **Resolve** any conflicting suggestions\n"
        context += "3. **Prioritize** recommendations by impact and feasibility\n"
        context += "4. **Create** unified implementation roadmap\n"
        context += "5. **Ensure** all elements work together harmoniously\n\n"
        
        context += "### Output Format:\n"
        context += "1. **Unified Design Vision** - Complete integrated approach\n"
        context += "2. **Implementation Priority** - What to build first\n"
        context += "3. **Integration Points** - How all elements connect\n"
        context += "4. **Risk Mitigation** - Address potential conflicts\n"
        context += "5. **Success Metrics** - How to measure success\n\n"
        
        return context


# Add missing methods to all agent classes
def _execute_with_model(self, model: str, context: str, thinking_mode: str) -> str:
    """Execute the task with the specified model"""
    try:
        # Create model context
        model_context = ModelContext(model, thinking_mode)
        
        # Get provider for the model
        from providers.registry import ModelProviderRegistry
        provider = ModelProviderRegistry.get_provider_for_model(model)
        if not provider:
            raise ToolExecutionError(f"Model {model} not available")
        
        # Execute with provider
        result = await provider.generate_response(
            messages=[{"role": "user", "content": context}],
            model=model,
            thinking_mode=thinking_mode
        )
        
        return result.content
        
    except Exception as e:
        logger.error(f"Error executing with model {model}: {e}")
        raise ToolExecutionError(f"Failed to execute with model {model}: {e}")


# Add method to all agent classes
for agent_class in [StoryWeaverAgent, PsychologyAgent, GameExpertAgent, 
                   PopCultureAgent, UXUIAgent, CreativeFeaturesAgent]:
    agent_class._execute_with_model = _execute_with_model


# Export the new agents
NEW_SPECIALIZED_AGENTS = {
    "story_weaver": StoryWeaverAgent(),
    "psychology": PsychologyAgent(),
    "game_expert": GameExpertAgent(),
    "pop_culture": PopCultureAgent(),
    "ux_ui": UXUIAgent(),
    "creative_features": CreativeFeaturesAgent(),
    "phase_coordinator": PhaseCoordinator()
}


def get_new_specialized_agent(agent_type: str):
    """Get a new specialized agent by type"""
    return NEW_SPECIALIZED_AGENTS.get(agent_type)