"""
Specialized AI Agents for Different Development Phases

This module implements specialized MCP tools that use different AI models
optimized for specific development tasks and phases. Each agent is designed
to leverage the strengths of different models for maximum efficiency.

Architecture:
- ArchitectureAgent: Uses gemini-pro for system design and planning
- ImplementationAgent: Uses gemini-flash for rapid coding tasks  
- OptimizationAgent: Uses local models for performance tuning
- ContentAgent: Uses claude-haiku for narrative and creative content
- ConsensusAgent: Uses multi-model consensus for complex decisions
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from mcp.types import TextContent
from providers.registry import ModelProviderRegistry
from tools import ToolOutput
from tools.models import ToolOutput
from tools.shared.exceptions import ToolExecutionError
from utils.conversation_memory import add_turn, get_thread
from utils.file_utils import check_total_file_size
from utils.model_context import ModelContext
from utils.token_utils import estimate_tokens

logger = logging.getLogger(__name__)


class SpecializedAgent:
    """Base class for specialized AI agents with model optimization"""
    
    def __init__(self, name: str, description: str, preferred_model: str, 
                 thinking_mode: str = "medium", requires_model: bool = True):
        self.name = name
        self.description = description
        self.preferred_model = preferred_model
        self.thinking_mode = thinking_mode
        self.requires_model = requires_model
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The task or request for the agent"
                },
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional files to analyze (paths)",
                    "default": []
                },
                "model": {
                    "type": "string",
                    "description": f"Override model (default: {self.preferred_model})",
                    "default": self.preferred_model
                },
                "thinking_mode": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": f"Thinking depth (default: {self.thinking_mode})",
                    "default": self.thinking_mode
                },
                "continuation_id": {
                    "type": "string",
                    "description": "Optional conversation thread ID",
                    "default": None
                }
            },
            "required": ["prompt"]
        }
    
    def requires_model(self) -> bool:
        return self.requires_model
    
    def get_model_category(self):
        from providers.registry import ModelCategory
        if "gemini" in self.preferred_model:
            return ModelCategory.GEMINI
        elif "gpt" in self.preferred_model:
            return ModelCategory.OPENAI
        elif "ollama" in self.preferred_model or "custom" in self.preferred_model:
            return ModelCategory.CUSTOM
        else:
            return ModelCategory.GENERAL


class ArchitectureAgent(SpecializedAgent):
    """Specialized agent for system architecture and planning"""
    
    def __init__(self):
        super().__init__(
            name="architecture",
            description="System architecture design and technical planning",
            preferred_model="gemini-pro",
            thinking_mode="high"
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute architecture planning with gemini-pro"""
        prompt = arguments["prompt"]
        files = arguments.get("files", [])
        model = arguments.get("model", self.preferred_model)
        thinking_mode = arguments.get("thinking_mode", self.thinking_mode)
        
        # Build context-aware prompt
        context = self._build_architecture_context(prompt, files)
        
        # Execute with optimized model
        result = await self._execute_with_model(model, context, thinking_mode)
        
        return [TextContent(type="text", text=result)]


class ImplementationAgent(SpecializedAgent):
    """Specialized agent for coding and implementation tasks"""
    
    def __init__(self):
        super().__init__(
            name="implementation", 
            description="Code generation, refactoring, and implementation",
            preferred_model="gemini-flash",
            thinking_mode="medium"
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute implementation tasks with gemini-flash"""
        prompt = arguments["prompt"]
        files = arguments.get("files", [])
        model = arguments.get("model", self.preferred_model)
        thinking_mode = arguments.get("thinking_mode", self.thinking_mode)
        
        # Build implementation-focused context
        context = self._build_implementation_context(prompt, files)
        
        # Execute with fast, cost-effective model
        result = await self._execute_with_model(model, context, thinking_mode)
        
        return [TextContent(type="text", text=result)]


class OptimizationAgent(SpecializedAgent):
    """Specialized agent for performance optimization and analysis"""
    
    def __init__(self):
        super().__init__(
            name="optimization",
            description="Performance analysis, optimization, and debugging",
            preferred_model="ollama",  # Local models for privacy and cost
            thinking_mode="medium"
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute optimization analysis with local models"""
        prompt = arguments["prompt"]
        files = arguments.get("files", [])
        model = arguments.get("model", self.preferred_model)
        thinking_mode = arguments.get("thinking_mode", self.thinking_mode)
        
        # Build optimization-focused context
        context = self._build_optimization_context(prompt, files)
        
        # Execute with local model for privacy and cost efficiency
        result = await self._execute_with_model(model, context, thinking_mode)
        
        return [TextContent(type="text", text=result)]


class ContentAgent(SpecializedAgent):
    """Specialized agent for creative content and narrative generation"""
    
    def __init__(self):
        super().__init__(
            name="content",
            description="Creative content, documentation, and narrative generation",
            preferred_model="claude-haiku",
            thinking_mode="medium"
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute content generation with claude-haiku"""
        prompt = arguments["prompt"]
        files = arguments.get("files", [])
        model = arguments.get("model", self.preferred_model)
        thinking_mode = arguments.get("thinking_mode", self.thinking_mode)
        
        # Build content-focused context
        context = self._build_content_context(prompt, files)
        
        # Execute with creative model
        result = await self._execute_with_model(model, context, thinking_mode)
        
        return [TextContent(type="text", text=result)]


class ConsensusAgent(SpecializedAgent):
    """Specialized agent for multi-model consensus and complex decisions"""
    
    def __init__(self):
        super().__init__(
            name="consensus",
            description="Multi-model consensus for complex analysis and decisions",
            preferred_model="consensus",
            thinking_mode="high",
            requires_model=False  # Handles multiple models internally
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute consensus analysis with multiple models"""
        prompt = arguments["prompt"]
        files = arguments.get("files", [])
        models = arguments.get("models", ["gemini-pro", "gpt-5", "claude-haiku"])
        thinking_mode = arguments.get("thinking_mode", self.thinking_mode)
        
        # Execute consensus workflow
        result = await self._execute_consensus_workflow(prompt, files, models, thinking_mode)
        
        return [TextContent(type="text", text=result)]


class ProceduralPuzzleAgent(SpecializedAgent):
    """Specialized agent for procedural puzzle generation"""
    
    def __init__(self):
        super().__init__(
            name="procedural_puzzle",
            description="Generate varied puzzle configurations using AI",
            preferred_model="gemini-pro",
            thinking_mode="high"
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute procedural puzzle generation"""
        prompt = arguments["prompt"]
        theme = arguments.get("theme", "horror")
        difficulty = arguments.get("difficulty", "medium")
        variation_count = arguments.get("variations", 3)
        
        # Build puzzle generation context
        context = self._build_puzzle_generation_context(prompt, theme, difficulty, variation_count)
        
        # Execute with creative model
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]


class DynamicDifficultyAgent(SpecializedAgent):
    """Specialized agent for dynamic difficulty adjustment"""
    
    def __init__(self):
        super().__init__(
            name="dynamic_difficulty",
            description="Analyze player performance and adjust difficulty dynamically",
            preferred_model="gemini-pro",
            thinking_mode="medium"
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute dynamic difficulty analysis"""
        player_data = arguments["player_data"]
        current_difficulty = arguments.get("current_difficulty", "medium")
        performance_metrics = arguments.get("metrics", {})
        
        # Build difficulty adjustment context
        context = self._build_difficulty_context(player_data, current_difficulty, performance_metrics)
        
        # Execute with analytical model
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]


class NarrativeAgent(SpecializedAgent):
    """Specialized agent for horror narrative content creation"""
    
    def __init__(self):
        super().__init__(
            name="narrative",
            description="Generate horror story elements and VHS aesthetic content",
            preferred_model="claude-haiku",
            thinking_mode="high"
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute narrative content generation"""
        story_prompt = arguments["prompt"]
        theme = arguments.get("theme", "slasher")
        tone = arguments.get("tone", "creepy")
        length = arguments.get("length", "medium")
        
        # Build narrative context
        context = self._build_narrative_context(story_prompt, theme, tone, length)
        
        # Execute with creative model
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]


class AssetOptimizationAgent(SpecializedAgent):
    """Specialized agent for VHS aesthetic asset optimization"""
    
    def __init__(self):
        super().__init__(
            name="asset_optimization",
            description="Optimize assets for VHS aesthetic and performance",
            preferred_model="ollama",
            thinking_mode="medium"
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute asset optimization"""
        asset_paths = arguments["assets"]
        target_size = arguments.get("target_size", "512KB")
        aesthetic_requirements = arguments.get("requirements", {})
        
        # Build asset optimization context
        context = self._build_asset_context(asset_paths, target_size, aesthetic_requirements)
        
        # Execute with local model for privacy
        result = await self._execute_with_model(self.preferred_model, context, self.thinking_mode)
        
        return [TextContent(type="text", text=result)]


# Helper methods for context building
def _build_architecture_context(self, prompt: str, files: List[str]) -> str:
    """Build architecture-focused context"""
    return f"""
🏗️ SYSTEM ARCHITECTURE ANALYSIS

**Task:** {prompt}

**Context:** Analyze the provided files and design system architecture.

**Requirements:**
- Focus on scalability, maintainability, and performance
- Consider security implications
- Provide clear technical recommendations
- Use architectural patterns where appropriate

**Files to analyze:** {', '.join(files) if files else 'None provided'}

**Output Format:**
1. Architecture Overview
2. Component Design
3. Data Flow
4. Technology Recommendations
5. Implementation Phases

Please provide a comprehensive architecture analysis.
"""

def _build_implementation_context(self, prompt: str, files: List[str]) -> str:
    """Build implementation-focused context"""
    return f"""
💻 IMPLEMENTATION TASK

**Task:** {prompt}

**Context:** Implement the specified feature or fix.

**Requirements:**
- Follow existing code patterns
- Maintain code quality standards
- Include necessary error handling
- Add appropriate comments

**Files to reference:** {', '.join(files) if files else 'None provided'}

**Output Format:**
- Code implementation
- Explanation of approach
- Any assumptions made
- Testing recommendations

Please provide the implementation.
"""

def _build_optimization_context(self, prompt: str, files: List[str]) -> str:
    """Build optimization-focused context"""
    return f"""
⚡ PERFORMANCE OPTIMIZATION ANALYSIS

**Task:** {prompt}

**Context:** Analyze performance issues and provide optimization recommendations.

**Requirements:**
- Identify bottlenecks and inefficiencies
- Suggest specific improvements
- Consider memory usage, CPU usage, and I/O
- Provide measurable optimization targets

**Files to analyze:** {', '.join(files) if files else 'None provided'}

**Output Format:**
1. Performance Issues Identified
2. Optimization Recommendations
3. Expected Performance Gains
4. Implementation Priority

Please provide detailed optimization analysis.
"""

def _build_content_context(self, prompt: str, files: List[str]) -> str:
    """Build content-focused context"""
    return f"""
📝 CONTENT GENERATION

**Task:** {prompt}

**Context:** Create engaging, well-structured content.

**Requirements:**
- Use clear, professional language
- Structure content logically
- Include relevant examples where appropriate
- Maintain consistent tone and style

**Reference materials:** {', '.join(files) if files else 'None provided'}

**Output Format:**
- Well-structured content
- Clear explanations
- Appropriate formatting
- Actionable insights

Please generate the requested content.
"""

def _build_consensus_context(self, prompt: str, files: List[str], models: List[str]) -> str:
    """Build consensus-focused context"""
    return f"""
🤝 MULTI-MODEL CONSENSUS ANALYSIS

**Task:** {prompt}

**Models participating:** {', '.join(models)}

**Context:** Multiple AI models will analyze this task from different perspectives.

**Requirements:**
- Each model provides unique insights
- Models should challenge and build on each other's ideas
- Focus on comprehensive analysis
- Reach consensus on key recommendations

**Files to analyze:** {', '.join(files) if files else 'None provided'}

**Output Format:**
1. Model 1 Analysis
2. Model 2 Analysis  
3. Model 3 Analysis
4. Consensus Recommendations
5. Action Items

Please provide comprehensive consensus analysis.
"""

def _build_puzzle_generation_context(self, prompt: str, theme: str, difficulty: str, variation_count: int) -> str:
    """Build puzzle generation context"""
    return f"""
🧩 PROCEDURAL PUZZLE GENERATION

**Theme:** {theme}
**Difficulty:** {difficulty}
**Variations:** {variation_count}

**Task:** {prompt}

**Context:** Generate multiple puzzle variations for a horror-themed game.

**Requirements:**
- Each variation should be unique but thematically consistent
- Maintain appropriate difficulty level
- Include clear solution paths
- Support replayability

**Output Format:**
For each variation:
1. Puzzle Description
2. Solution Logic
3. Difficulty Assessment
4. Replay Value

Please generate {variation_count} puzzle variations.
"""

def _build_difficulty_context(self, player_data: Dict, current_difficulty: str, metrics: Dict) -> str:
    """Build dynamic difficulty context"""
    return f"""
🎯 DYNAMIC DIFFICULTY ADJUSTMENT

**Current Difficulty:** {current_difficulty}
**Player Performance:** {json.dumps(player_data, indent=2)}
**Metrics:** {json.dumps(metrics, indent=2)}

**Context:** Analyze player performance and suggest difficulty adjustments.

**Requirements:**
- Consider player skill progression
- Balance challenge vs frustration
- Maintain engagement
- Provide specific adjustment recommendations

**Output Format:**
1. Performance Analysis
2. Difficulty Assessment
3. Adjustment Recommendations
4. Implementation Strategy

Please provide difficulty adjustment recommendations.
"""

def _build_narrative_context(self, story_prompt: str, theme: str, tone: str, length: str) -> str:
    """Build narrative content context"""
    return f"""
📖 HORROR NARRATIVE GENERATION

**Theme:** {theme}
**Tone:** {tone}
**Length:** {length}

**Task:** {story_prompt}

**Context:** Create engaging horror narrative content for VHS aesthetic game.

**Requirements:**
- Maintain consistent horror atmosphere
- Use appropriate VHS-era references
- Build tension and suspense
- Support multiple narrative paths

**Output Format:**
- Narrative text
- Scene descriptions
- Character development
- Plot progression

Please generate compelling horror narrative content.
"""

def _build_asset_context(self, asset_paths: List[str], target_size: str, requirements: Dict) -> str:
    """Build asset optimization context"""
    return f"""
🎨 VHS ASSET OPTIMIZATION

**Assets:** {', '.join(asset_paths)}
**Target Size:** {target_size}
**Requirements:** {json.dumps(requirements, indent=2)}

**Context:** Optimize assets for VHS aesthetic while maintaining performance.

**Requirements:**
- Preserve VHS aesthetic qualities
- Optimize for target file size
- Maintain visual quality
- Consider loading performance

**Output Format:**
1. Current Asset Analysis
2. Optimization Recommendations
3. Expected Results
4. Implementation Steps

Please provide detailed asset optimization analysis.
"""

# Add missing methods to SpecializedAgent base class
SpecializedAgent._build_architecture_context = _build_architecture_context
SpecializedAgent._build_implementation_context = _build_implementation_context
SpecializedAgent._build_optimization_context = _build_optimization_context
SpecializedAgent._build_content_context = _build_content_context
SpecializedAgent._build_consensus_context = _build_consensus_context
SpecializedAgent._build_puzzle_generation_context = _build_puzzle_generation_context
SpecializedAgent._build_difficulty_context = _build_difficulty_context
SpecializedAgent._build_narrative_context = _build_narrative_context
SpecializedAgent._build_asset_context = _build_asset_context


async def _execute_with_model(self, model: str, context: str, thinking_mode: str) -> str:
    """Execute the task with the specified model"""
    try:
        # Create model context
        model_context = ModelContext(model, thinking_mode)
        
        # Get provider for the model
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


async def _execute_consensus_workflow(self, prompt: str, files: List[str], 
                                     models: List[str], thinking_mode: str) -> str:
    """Execute consensus workflow with multiple models"""
    try:
        # Get provider registry
        registry = ModelProviderRegistry()
        
        # Collect responses from all models
        responses = []
        for model in models:
            provider = registry.get_provider_for_model(model)
            if provider:
                context = self._build_consensus_context(prompt, files, models)
                response = await provider.generate_response(
                    messages=[{"role": "user", "content": context}],
                    model=model,
                    thinking_mode=thinking_mode
                )
                responses.append({"model": model, "response": response.content})
        
        # Analyze consensus
        consensus_analysis = await self._analyze_consensus(responses)
        
        return consensus_analysis
        
    except Exception as e:
        logger.error(f"Error in consensus workflow: {e}")
        raise ToolExecutionError(f"Consensus workflow failed: {e}")


async def _analyze_consensus(self, responses: List[Dict]) -> str:
    """Analyze responses from multiple models to find consensus"""
    # Simple consensus analysis - could be enhanced with more sophisticated logic
    analysis = "## CONSENSUS ANALYSIS\n\n"
    
    for response in responses:
        analysis += f"### {response['model'].upper()} Analysis:\n"
        analysis += f"{response['response']}\n\n"
    
    analysis += "## SYNTHESIS AND RECOMMENDATIONS\n\n"
    analysis += "Based on the multiple model analyses, here are the key consensus points:\n\n"
    analysis += "1. **Common Recommendations**\n"
    analysis += "2. **Areas of Agreement**\n"
    analysis += "3. **Divergent Opinions**\n"
    analysis += "4. **Final Recommendations**\n\n"
    
    return analysis


# Add missing methods to SpecializedAgent base class
SpecializedAgent._execute_with_model = _execute_with_model
SpecializedAgent._execute_consensus_workflow = _execute_consensus_workflow
SpecializedAgent._analyze_consensus = _analyze_consensus


# Registry of specialized agents
SPECIALIZED_AGENTS = {
    "architecture": ArchitectureAgent(),
    "implementation": ImplementationAgent(),
    "optimization": OptimizationAgent(),
    "content": ContentAgent(),
    "consensus": ConsensusAgent(),
    "procedural_puzzle": ProceduralPuzzleAgent(),
    "dynamic_difficulty": DynamicDifficultyAgent(),
    "narrative": NarrativeAgent(),
    "asset_optimization": AssetOptimizationAgent(),
}


def get_specialized_agent(agent_type: str) -> Optional[SpecializedAgent]:
    """Get a specialized agent by type"""
    return SPECIALIZED_AGENTS.get(agent_type)