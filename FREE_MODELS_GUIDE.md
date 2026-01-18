# Free Model Options for PAL MCP Server

## Option 1: OpenRouter Free Models (Recommended)

### Setup
1. Visit [OpenRouter.ai](https://openrouter.ai) and sign up
2. Get your API key from dashboard
3. Update your `.env` file:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   ```

### Free/Cheap Models Available

| Model | Use Case | Cost | Performance |
|-------|----------|------|-------------|
| **Gemini Flash** | Quick analysis, file reviews | $0.00035/1K tokens | Fast, good for routine tasks |
| **Claude Haiku** | Documentation, brainstorming | $0.00025/1K tokens | Fast, conversational |
| **GPT-3.5 Turbo** | General purpose | $0.0005/1K tokens | Reliable, widely compatible |
| **Llama 3.1 8B** | Code generation | $0.00015/1K tokens | Good for coding tasks |

### Usage Examples
```bash
# Quick file analysis
"Use pal with gemini-flash to analyze src/main.js"

# Documentation generation  
"Use pal with claude-haiku to generate README.md"

# Code review
"Use pal with gemini-pro for detailed code review"

# Architecture planning
"Use pal with gpt-4o for system design"
```

## Option 2: Local Models (Completely Free)

### Setup Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull free models
ollama pull llama3.2
ollama pull codellama
ollama pull mistral
ollama pull phi3

# Configure in .env
CUSTOM_API_URL=http://localhost:11434
CUSTOM_MODEL_NAME=llama3.2
```

### Local Model Benefits
- ✅ **Zero API costs**
- ✅ **No internet required**
- ✅ **Privacy-focused**
- ✅ **No rate limits**
- ✅ **Instant responses**

### Local Model Performance
| Model | Size | Use Case | Speed |
|-------|------|----------|-------|
| **Phi-3** | 3.8B | Quick tasks, chat | ⚡ Very Fast |
| **Llama 3.2** | 3B | General purpose | 🚀 Fast |
| **CodeLlama** | 7B | Code generation | 📝 Fast |
| **Mistral** | 7B | Reasoning | 🧠 Medium |

## Option 3: Provider-Specific Free Tiers

### Google Gemini
```bash
# Get API key from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your-gemini-key-here
```

**Free Tier:** $5/month credit
**Best For:** Code analysis, documentation

### OpenAI
```bash
# Get API key from https://platform.openai.com/api-keys  
OPENAI_API_KEY=your-openai-key-here
```

**Free Tier:** $5 credit for new accounts
**Best For:** General purpose, GPT-3.5 Turbo

## Cost Optimization Strategies

### 1. Model Selection by Task Type
```bash
# Routine tasks → Cheap models
"Use gemini-flash for quick file analysis"

# Complex reasoning → Better models  
"Use gemini-pro for architecture decisions"

# Code generation → Local models
"Use ollama for generating new code"
```

### 2. Token Management
```bash
# Use conversation continuity
"Continue with gemini-flash using the previous context"

# Limit file analysis scope
"Analyze only src/components/ with gemini-flash"

# Use thinking modes wisely
"Use gemini-pro with medium thinking mode"
```

### 3. Caching Strategy
- Enable model caching in `.env`: `ENABLE_MODEL_CACHING=true`
- Use consistent model names for better cache hits
- Reuse conversation threads when possible

## Recommended Setup for Different Use Cases

### Game Development (VHS Puzzles)
```bash
# Primary: Local models for rapid iteration
CUSTOM_API_URL=http://localhost:11434
CUSTOM_MODEL_NAME=llama3.2

# Secondary: Gemini Flash for reviews
OPENROUTER_API_KEY=your-key-here
```

### Development Tools (Superpowers)
```bash
# Primary: OpenRouter with mixed models
OPENROUTER_API_KEY=your-key-here
DEFAULT_MODEL=auto

# Use specific models per task:
# - Architecture: gemini-pro
# - Code review: gemini-flash  
# - Documentation: claude-haiku
```

### CI/CD Automation
```bash
# Use cheapest models for automated tasks
DEFAULT_MODEL=gemini-flash
LOG_LEVEL=ERROR  # Reduce logging overhead
```

## Monitoring Costs

### OpenRouter Dashboard
- Visit https://openrouter.ai/dashboard
- Monitor usage by model
- Set up usage alerts
- View cost breakdown

### Local Model Monitoring
- Monitor CPU/RAM usage
- Track model loading times
- Watch disk space for model files

## Troubleshooting

### Common Issues
1. **API Key Not Working**: Check for typos, ensure key has permissions
2. **Models Not Found**: Verify model names, check provider availability  
3. **High Costs**: Switch to cheaper models, enable caching, reduce thinking mode
4. **Slow Responses**: Use local models, reduce context window, choose faster models

### Performance Tips
- Use `LOG_LEVEL=WARNING` to reduce overhead
- Set `MAX_CONVERSATION_TURNS=30` to prevent context bloat
- Enable `CONVERSATION_CONTINUITY=true` for efficient context reuse