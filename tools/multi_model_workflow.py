"""
Multi-Model Workflow Orchestrator

This module implements sophisticated workflows that chain multiple specialized
AI agents together for complex development tasks. It enables context-aware
model selection and seamless handoffs between different AI specialists.

Key Features:
- Automatic model selection based on task type
- Context preservation across agent handoffs
- Parallel execution for independent tasks
- Consensus building for complex decisions
- Smart fallback strategies
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from mcp.types import TextContent
from tools.models import ToolOutput
from tools.shared.exceptions import ToolExecutionError
from utils.conversation_memory import add_turn, get_thread
from utils.model_context import ModelContext
from utils.token_utils import estimate_tokens

from .specialized_agents import (
    ArchitectureAgent, ImplementationAgent, OptimizationAgent, 
    ContentAgent, ConsensusAgent, ProceduralPuzzleAgent,
    DynamicDifficultyAgent, NarrativeAgent, AssetOptimizationAgent
)

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Orchestrates complex workflows across multiple specialized agents"""
    
    def __init__(self):
        self.agents = {
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
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "workflow_type": {
                    "type": "string",
                    "enum": ["game_development", "puzzle_generation", "content_creation", "optimization", "custom"],
                    "description": "Type of workflow to execute"
                },
                "tasks": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of tasks to execute in sequence or parallel"
                },
                "context": {
                    "type": "object",
                    "description": "Shared context for the workflow",
                    "default": {}
                },
                "parallel": {
                    "type": "boolean",
                    "description": "Execute tasks in parallel when possible",
                    "default": False
                },
                "model_strategy": {
                    "type": "string",
                    "enum": ["auto", "cost_optimized", "performance_optimized", "balanced"],
                    "description": "Strategy for model selection",
                    "default": "auto"
                }
            },
            "required": ["workflow_type", "tasks"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute a multi-model workflow"""
        workflow_type = arguments["workflow_type"]
        tasks = arguments["tasks"]
        context = arguments.get("context", {})
        parallel = arguments.get("parallel", False)
        model_strategy = arguments.get("model_strategy", "auto")
        
        logger.info(f"Starting {workflow_type} workflow with {len(tasks)} tasks")
        
        # Execute workflow based on type
        if workflow_type == "game_development":
            result = await self._execute_game_development_workflow(tasks, context, parallel, model_strategy)
        elif workflow_type == "puzzle_generation":
            result = await self._execute_puzzle_generation_workflow(tasks, context, parallel, model_strategy)
        elif workflow_type == "content_creation":
            result = await self._execute_content_creation_workflow(tasks, context, parallel, model_strategy)
        elif workflow_type == "optimization":
            result = await self._execute_optimization_workflow(tasks, context, parallel, model_strategy)
        elif workflow_type == "custom":
            result = await self._execute_custom_workflow(tasks, context, parallel, model_strategy)
        else:
            raise ToolExecutionError(f"Unknown workflow type: {workflow_type}")
        
        return [TextContent(type="text", text=result)]


class GameDevelopmentWorkflow(WorkflowOrchestrator):
    """Complete game development workflow with specialized agents"""
    
    async def _execute_game_development_workflow(self, tasks: List[Dict], context: Dict, 
                                               parallel: bool, model_strategy: str) -> str:
        """Execute game development workflow"""
        
        workflow_steps = []
        
        # Step 1: Architecture Planning
        if any(task.get("type") == "architecture" for task in tasks):
            arch_result = await self._execute_architecture_step(tasks, context, model_strategy)
            workflow_steps.append(("Architecture Planning", arch_result))
        
        # Step 2: Implementation
        if any(task.get("type") == "implementation" for task in tasks):
            impl_result = await self._execute_implementation_step(tasks, context, model_strategy)
            workflow_steps.append(("Implementation", impl_result))
        
        # Step 3: Content Creation
        if any(task.get("type") == "content" for task in tasks):
            content_result = await self._execute_content_step(tasks, context, model_strategy)
            workflow_steps.append(("Content Creation", content_result))
        
        # Step 4: Optimization
        if any(task.get("type") == "optimization" for task in tasks):
            opt_result = await self._execute_optimization_step(tasks, context, model_strategy)
            workflow_steps.append(("Performance Optimization", opt_result))
        
        # Generate final report
        return self._generate_workflow_report("Game Development", workflow_steps)


class PuzzleGenerationWorkflow(WorkflowOrchestrator):
    """Procedural puzzle generation workflow with dynamic difficulty"""
    
    async def _execute_puzzle_generation_workflow(self, tasks: List[Dict], context: Dict, 
                                                parallel: bool, model_strategy: str) -> str:
        """Execute puzzle generation workflow"""
        
        workflow_steps = []
        
        # Step 1: Theme and Difficulty Analysis
        theme_analysis = await self._analyze_puzzle_theme(tasks, context)
        workflow_steps.append(("Theme Analysis", theme_analysis))
        
        # Step 2: Procedural Generation
        generation_results = await self._generate_puzzle_variations(tasks, context, model_strategy)
        workflow_steps.append(("Puzzle Generation", generation_results))
        
        # Step 3: Difficulty Balancing
        if "difficulty_adjustment" in context:
            difficulty_results = await self._balance_difficulty(tasks, context, model_strategy)
            workflow_steps.append(("Difficulty Balancing", difficulty_results))
        
        # Step 4: Narrative Integration
        if "narrative" in context:
            narrative_results = await self._integrate_narrative(tasks, context, model_strategy)
            workflow_steps.append(("Narrative Integration", narrative_results))
        
        # Generate final report
        return self._generate_workflow_report("Puzzle Generation", workflow_steps)


class ContentCreationWorkflow(WorkflowOrchestrator):
    """Content creation workflow for horror narratives and VHS aesthetics"""
    
    async def _execute_content_creation_workflow(self, tasks: List[Dict], context: Dict, 
                                                parallel: bool, model_strategy: str) -> str:
        """Execute content creation workflow"""
        
        workflow_steps = []
        
        # Step 1: Story Development
        story_result = await self._develop_story(tasks, context, model_strategy)
        workflow_steps.append(("Story Development", story_result))
        
        # Step 2: Character Creation
        if "characters" in context:
            char_result = await self._create_characters(tasks, context, model_strategy)
            workflow_steps.append(("Character Creation", char_result))
        
        # Step 3: Scene Writing
        scene_result = await self._write_scenes(tasks, context, model_strategy)
        workflow_steps.append(("Scene Writing", scene_result))
        
        # Step 4: Asset Generation
        if "assets" in context:
            asset_result = await self._generate_assets(tasks, context, model_strategy)
            workflow_steps.append(("Asset Generation", asset_result))
        
        # Generate final report
        return self._generate_workflow_report("Content Creation", workflow_steps)


class OptimizationWorkflow(WorkflowOrchestrator):
    """Performance optimization workflow with multi-agent analysis"""
    
    async def _execute_optimization_workflow(self, tasks: List[Dict], context: Dict, 
                                           parallel: bool, model_strategy: str) -> str:
        """Execute optimization workflow"""
        
        workflow_steps = []
        
        # Step 1: Performance Analysis
        analysis_result = await self._analyze_performance(tasks, context, model_strategy)
        workflow_steps.append(("Performance Analysis", analysis_result))
        
        # Step 2: Bottleneck Identification
        bottleneck_result = await self._identify_bottlenecks(tasks, context, model_strategy)
        workflow_steps.append(("Bottleneck Identification", bottleneck_result))
        
        # Step 3: Optimization Recommendations
        opt_result = await self._generate_optimizations(tasks, context, model_strategy)
        workflow_steps.append(("Optimization Recommendations", opt_result))
        
        # Step 4: Implementation Strategy
        impl_result = await self._create_implementation_plan(tasks, context, model_strategy)
        workflow_steps.append(("Implementation Strategy", impl_result))
        
        # Generate final report
        return self._generate_workflow_report("Optimization", workflow_steps)


class CustomWorkflow(WorkflowOrchestrator):
    """Custom workflow execution with flexible task chaining"""
    
    async def _execute_custom_workflow(self, tasks: List[Dict], context: Dict, 
                                     parallel: bool, model_strategy: str) -> str:
        """Execute custom workflow"""
        
        workflow_steps = []
        
        if parallel:
            # Execute independent tasks in parallel
            results = await asyncio.gather(*[
                self._execute_single_task(task, context, model_strategy)
                for task in tasks
            ], return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    workflow_steps.append((tasks[i].get("name", f"Task {i+1}"), f"Error: {result}"))
                else:
                    workflow_steps.append((tasks[i].get("name", f"Task {i+1}"), result))
        else:
            # Execute tasks sequentially
            for task in tasks:
                try:
                    result = await self._execute_single_task(task, context, model_strategy)
                    workflow_steps.append((task.get("name", "Task"), result))
                except Exception as e:
                    workflow_steps.append((task.get("name", "Task"), f"Error: {e}"))
        
        # Generate final report
        return self._generate_workflow_report("Custom Workflow", workflow_steps)


# Implementation methods for each workflow type
async def _execute_architecture_step(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Execute architecture planning step"""
    arch_task = next(task for task in tasks if task.get("type") == "architecture")
    
    agent = self.agents["architecture"]
    result = await agent.execute({
        "prompt": arch_task["prompt"],
        "files": arch_task.get("files", []),
        "model": self._select_model("architecture", model_strategy),
        "thinking_mode": "high"
    })
    
    return result[0].text


async def _execute_implementation_step(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Execute implementation step"""
    impl_tasks = [task for task in tasks if task.get("type") == "implementation"]
    
    results = []
    for task in impl_tasks:
        agent = self.agents["implementation"]
        result = await agent.execute({
            "prompt": task["prompt"],
            "files": task.get("files", []),
            "model": self._select_model("implementation", model_strategy),
            "thinking_mode": "medium"
        })
        results.append(result[0].text)
    
    return "\n\n".join(results)


async def _execute_content_step(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Execute content creation step"""
    content_task = next(task for task in tasks if task.get("type") == "content")
    
    agent = self.agents["content"]
    result = await agent.execute({
        "prompt": content_task["prompt"],
        "files": content_task.get("files", []),
        "model": self._select_model("content", model_strategy),
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _execute_optimization_step(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Execute optimization step"""
    opt_task = next(task for task in tasks if task.get("type") == "optimization")
    
    agent = self.agents["optimization"]
    result = await agent.execute({
        "prompt": opt_task["prompt"],
        "files": opt_task.get("files", []),
        "model": self._select_model("optimization", model_strategy),
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _analyze_puzzle_theme(self, tasks: List[Dict], context: Dict) -> str:
    """Analyze puzzle theme and requirements"""
    theme_task = next(task for task in tasks if task.get("type") == "theme_analysis")
    
    agent = self.agents["content"]
    result = await agent.execute({
        "prompt": theme_task["prompt"],
        "model": "claude-haiku",
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _generate_puzzle_variations(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Generate procedural puzzle variations"""
    gen_task = next(task for task in tasks if task.get("type") == "procedural_generation")
    
    agent = self.agents["procedural_puzzle"]
    result = await agent.execute({
        "prompt": gen_task["prompt"],
        "theme": context.get("theme", "horror"),
        "difficulty": context.get("difficulty", "medium"),
        "variations": context.get("variations", 3),
        "model": self._select_model("procedural_puzzle", model_strategy),
        "thinking_mode": "high"
    })
    
    return result[0].text


async def _balance_difficulty(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Balance puzzle difficulty dynamically"""
    diff_task = next(task for task in tasks if task.get("type") == "difficulty_balancing")
    
    agent = self.agents["dynamic_difficulty"]
    result = await agent.execute({
        "player_data": context.get("player_data", {}),
        "current_difficulty": context.get("current_difficulty", "medium"),
        "metrics": context.get("metrics", {}),
        "model": self._select_model("dynamic_difficulty", model_strategy),
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _integrate_narrative(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Integrate narrative elements with puzzles"""
    narrative_task = next(task for task in tasks if task.get("type") == "narrative_integration")
    
    agent = self.agents["narrative"]
    result = await agent.execute({
        "prompt": narrative_task["prompt"],
        "theme": context.get("theme", "slasher"),
        "tone": context.get("tone", "creepy"),
        "length": context.get("length", "medium"),
        "model": self._select_model("narrative", model_strategy),
        "thinking_mode": "high"
    })
    
    return result[0].text


async def _develop_story(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Develop horror story narrative"""
    story_task = next(task for task in tasks if task.get("type") == "story_development")
    
    agent = self.agents["narrative"]
    result = await agent.execute({
        "prompt": story_task["prompt"],
        "theme": context.get("theme", "cosmic_horror"),
        "tone": context.get("tone", "atmospheric"),
        "length": context.get("length", "long"),
        "model": self._select_model("narrative", model_strategy),
        "thinking_mode": "high"
    })
    
    return result[0].text


async def _create_characters(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Create horror game characters"""
    char_task = next(task for task in tasks if task.get("type") == "character_creation")
    
    agent = self.agents["content"]
    result = await agent.execute({
        "prompt": char_task["prompt"],
        "model": self._select_model("content", model_strategy),
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _write_scenes(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Write horror scenes and sequences"""
    scene_task = next(task for task in tasks if task.get("type") == "scene_writing")
    
    agent = self.agents["narrative"]
    result = await agent.execute({
        "prompt": scene_task["prompt"],
        "theme": context.get("theme", "slasher"),
        "tone": context.get("tone", "tense"),
        "length": context.get("length", "medium"),
        "model": self._select_model("narrative", model_strategy),
        "thinking_mode": "high"
    })
    
    return result[0].text


async def _generate_assets(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Generate VHS aesthetic assets"""
    asset_task = next(task for task in tasks if task.get("type") == "asset_generation")
    
    agent = self.agents["asset_optimization"]
    result = await agent.execute({
        "assets": asset_task.get("assets", []),
        "target_size": context.get("target_size", "512KB"),
        "requirements": context.get("requirements", {}),
        "model": self._select_model("asset_optimization", model_strategy),
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _analyze_performance(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Analyze performance bottlenecks"""
    perf_task = next(task for task in tasks if task.get("type") == "performance_analysis")
    
    agent = self.agents["optimization"]
    result = await agent.execute({
        "prompt": perf_task["prompt"],
        "files": perf_task.get("files", []),
        "model": self._select_model("optimization", model_strategy),
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _identify_bottlenecks(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Identify performance bottlenecks"""
    bottleneck_task = next(task for task in tasks if task.get("type") == "bottleneck_identification")
    
    agent = self.agents["optimization"]
    result = await agent.execute({
        "prompt": bottleneck_task["prompt"],
        "files": bottleneck_task.get("files", []),
        "model": self._select_model("optimization", model_strategy),
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _generate_optimizations(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Generate optimization recommendations"""
    opt_task = next(task for task in tasks if task.get("type") == "optimization_recommendations")
    
    agent = self.agents["optimization"]
    result = await agent.execute({
        "prompt": opt_task["prompt"],
        "files": opt_task.get("files", []),
        "model": self._select_model("optimization", model_strategy),
        "thinking_mode": "medium"
    })
    
    return result[0].text


async def _create_implementation_plan(self, tasks: List[Dict], context: Dict, model_strategy: str) -> str:
    """Create optimization implementation plan"""
    plan_task = next(task for task in tasks if task.get("type") == "implementation_plan")
    
    agent = self.agents["architecture"]
    result = await agent.execute({
        "prompt": plan_task["prompt"],
        "files": plan_task.get("files", []),
        "model": self._select_model("architecture", model_strategy),
        "thinking_mode": "high"
    })
    
    return result[0].text


async def _execute_single_task(self, task: Dict, context: Dict, model_strategy: str) -> str:
    """Execute a single task with appropriate agent"""
    task_type = task.get("type")
    agent_name = task.get("agent", task_type)
    
    if agent_name not in self.agents:
        raise ToolExecutionError(f"Unknown agent: {agent_name}")
    
    agent = self.agents[agent_name]
    
    # Build task arguments
    task_args = {
        "prompt": task["prompt"],
        "model": self._select_model(agent_name, model_strategy),
        "thinking_mode": task.get("thinking_mode", "medium")
    }
    
    # Add agent-specific parameters
    if agent_name == "procedural_puzzle":
        task_args.update({
            "theme": task.get("theme", "horror"),
            "difficulty": task.get("difficulty", "medium"),
            "variations": task.get("variations", 3)
        })
    elif agent_name == "dynamic_difficulty":
        task_args["player_data"] = task.get("player_data", {})
        task_args["current_difficulty"] = task.get("current_difficulty", "medium")
        task_args["metrics"] = task.get("metrics", {})
    elif agent_name == "narrative":
        task_args.update({
            "theme": task.get("theme", "slasher"),
            "tone": task.get("tone", "creepy"),
            "length": task.get("length", "medium")
        })
    elif agent_name == "asset_optimization":
        task_args["assets"] = task.get("assets", [])
        task_args["target_size"] = task.get("target_size", "512KB")
        task_args["requirements"] = task.get("requirements", {})
    
    result = await agent.execute(task_args)
    return result[0].text


def _select_model(self, agent_type: str, strategy: str) -> str:
    """Select optimal model based on agent type and strategy"""
    model_map = {
        "architecture": "gemini-pro",
        "implementation": "gemini-flash", 
        "optimization": "ollama",
        "content": "claude-haiku",
        "procedural_puzzle": "gemini-pro",
        "dynamic_difficulty": "gemini-pro",
        "narrative": "claude-haiku",
        "asset_optimization": "ollama"
    }
    
    base_model = model_map.get(agent_type, "gemini-flash")
    
    if strategy == "cost_optimized":
        # Prefer cheaper models when possible
        if base_model == "gemini-pro":
            return "gemini-flash"
        elif base_model == "claude-haiku":
            return "gemini-flash"
        return base_model
    elif strategy == "performance_optimized":
        # Prefer more capable models
        if base_model == "gemini-flash":
            return "gemini-pro"
        elif base_model == "ollama":
            return "gemini-pro"
        return base_model
    elif strategy == "balanced":
        # Use medium-cost, medium-capability models
        if base_model == "gemini-pro":
            return "gemini-flash"
        elif base_model == "ollama":
            return "gemini-flash"
        return base_model
    
    return base_model


def _generate_workflow_report(self, workflow_name: str, steps: List[Tuple[str, str]]) -> str:
    """Generate comprehensive workflow report"""
    report = f"# {workflow_name} Workflow Report\n\n"
    report += f"**Generated:** {self._get_timestamp()}\n"
    report += f"**Total Steps:** {len(steps)}\n\n"
    
    for i, (step_name, step_result) in enumerate(steps, 1):
        report += f"## Step {i}: {step_name}\n\n"
        report += f"{step_result}\n\n"
        report += "---\n\n"
    
    # Add summary
    report += "## Workflow Summary\n\n"
    report += f"- **Workflow Type:** {workflow_name}\n"
    report += f"- **Steps Completed:** {len(steps)}\n"
    report += f"- **Status:** Completed Successfully\n\n"
    
    report += "## Recommendations\n\n"
    report += "1. Review each step's output for quality and completeness\n"
    report += "2. Implement recommendations in order of priority\n"
    report += "3. Test changes thoroughly before deployment\n"
    report += "4. Monitor performance and user feedback\n\n"
    
    return report


def _get_timestamp(self) -> str:
    """Get current timestamp for reports"""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Add missing methods to WorkflowOrchestrator
WorkflowOrchestrator._execute_architecture_step = _execute_architecture_step
WorkflowOrchestrator._execute_implementation_step = _execute_implementation_step
WorkflowOrchestrator._execute_content_step = _execute_content_step
WorkflowOrchestrator._execute_optimization_step = _execute_optimization_step
WorkflowOrchestrator._analyze_puzzle_theme = _analyze_puzzle_theme
WorkflowOrchestrator._generate_puzzle_variations = _generate_puzzle_variations
WorkflowOrchestrator._balance_difficulty = _balance_difficulty
WorkflowOrchestrator._integrate_narrative = _integrate_narrative
WorkflowOrchestrator._develop_story = _develop_story
WorkflowOrchestrator._create_characters = _create_characters
WorkflowOrchestrator._write_scenes = _write_scenes
WorkflowOrchestrator._generate_assets = _generate_assets
WorkflowOrchestrator._analyze_performance = _analyze_performance
WorkflowOrchestrator._identify_bottlenecks = _identify_bottlenecks
WorkflowOrchestrator._generate_optimizations = _generate_optimizations
WorkflowOrchestrator._create_implementation_plan = _create_implementation_plan
WorkflowOrchestrator._execute_single_task = _execute_single_task
WorkflowOrchestrator._select_model = _select_model
WorkflowOrchestrator._generate_workflow_report = _generate_workflow_report
WorkflowOrchestrator._get_timestamp = _get_timestamp


# Add workflow method implementations
WorkflowOrchestrator._execute_game_development_workflow = GameDevelopmentWorkflow._execute_game_development_workflow
WorkflowOrchestrator._execute_puzzle_generation_workflow = PuzzleGenerationWorkflow._execute_puzzle_generation_workflow
WorkflowOrchestrator._execute_content_creation_workflow = ContentCreationWorkflow._execute_content_creation_workflow
WorkflowOrchestrator._execute_optimization_workflow = OptimizationWorkflow._execute_optimization_workflow
WorkflowOrchestrator._execute_custom_workflow = CustomWorkflow._execute_custom_workflow