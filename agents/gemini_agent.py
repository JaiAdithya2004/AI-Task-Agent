"""
Gemini Agent Module

This module contains the function to create and configure a Google Gemini agent
with proper initialization and conversation handling.
"""

import os
from typing import Optional
import google.generativeai as genai
from utils.logger import setup_logger

# Try to import config, fall back to environment variables
try:
    import config
    API_KEY = config.GEMINI_API_KEY
    MODEL_NAME = config.GEMINI_MODEL
    TEMPERATURE = config.GEMINI_TEMPERATURE
    MAX_TOKENS = config.GEMINI_MAX_TOKENS
except ImportError:
    API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    MAX_TOKENS = os.getenv("GEMINI_MAX_TOKENS")

logger = setup_logger()

class GeminiAgent:
    """An advanced Gemini agent wrapper with multi-step task capabilities."""
    
    def __init__(self, model):
        self.model = model
        self.conversation_history = []
        self.chat_session = None
        self.task_context = {}
    
    def invoke(self, input_data):
        """Process user input and return response with multi-step task support."""
        user_input = input_data.get("input", "")
        
        try:
            # Start a new chat session if we don't have one
            if self.chat_session is None:
                self.chat_session = self.model.start_chat(history=[])
            
            # Enhanced system prompt for multi-step tasks
            enhanced_prompt = f"""
            You are an advanced autonomous AI agent capable of performing multi-step tasks including:
            
            1. **Information Search & Retrieval**: Finding relevant data from various sources
            2. **Data Analysis & Processing**: Analyzing information and identifying patterns
            3. **Summarization**: Creating concise, accurate summaries
            4. **Information Extraction**: Extracting key insights and structured data
            5. **Workflow Orchestration**: Breaking down complex tasks into manageable steps
            
            For the following request: "{user_input}"
            
            If this is a complex multi-step task, provide a comprehensive response that demonstrates:
            - Step-by-step reasoning
            - Information gathering approach
            - Analysis methodology
            - Clear conclusions and insights
            
            Be thorough, accurate, and demonstrate advanced reasoning capabilities.
            """
            
            # Send enhanced prompt to Gemini
            response = self.chat_session.send_message(enhanced_prompt)
            
            # Return response
            return {"output": response.text}
            
        except Exception as e:
            logger.error(f"Error in Gemini agent invoke: {str(e)}")
            return {"output": f"Sorry, I encountered an error: {str(e)}"}
    
    def execute_multi_step_task(self, task_description):
        """Execute a complex multi-step task with detailed workflow tracking."""
        try:
            # Step 1: Task Analysis
            analysis_prompt = f"""
            Analyze this task and create a detailed execution plan:
            "{task_description}"
            
            Provide:
            1. Task breakdown into clear steps
            2. Required information sources
            3. Analysis methodology
            4. Expected deliverables
            
            Format as a structured plan.
            """
            
            analysis_response = self.chat_session.send_message(analysis_prompt)
            
            # Step 2: Information Gathering
            gathering_prompt = f"""
            Based on the task: "{task_description}"
            
            Gather comprehensive information by:
            1. Identifying key concepts and requirements
            2. Suggesting information sources
            3. Outlining search strategies
            4. Defining success criteria
            
            Provide detailed information gathering approach.
            """
            
            gathering_response = self.chat_session.send_message(gathering_prompt)
            
            # Step 3: Analysis and Synthesis
            synthesis_prompt = f"""
            For the task: "{task_description}"
            
            Perform comprehensive analysis including:
            1. Data processing and organization
            2. Pattern identification
            3. Insight extraction
            4. Conclusion synthesis
            
            Provide detailed analysis and findings.
            """
            
            synthesis_response = self.chat_session.send_message(synthesis_prompt)
            
            # Combine all responses
            final_response = f"""
            **MULTI-STEP TASK EXECUTION COMPLETE**
            
            **Task:** {task_description}
            
            **Step 1 - Task Analysis:**
            {analysis_response.text}
            
            **Step 2 - Information Gathering:**
            {gathering_response.text}
            
            **Step 3 - Analysis & Synthesis:**
            {synthesis_response.text}
            
            **Final Deliverable:**
            Task execution completed with comprehensive analysis and actionable insights.
            """
            
            return {"output": final_response}
            
        except Exception as e:
            logger.error(f"Error in multi-step task execution: {str(e)}")
            return {"output": f"Error executing multi-step task: {str(e)}"}

def create_agent(
    model_name: str = None,
    temperature: float = None,
    max_tokens: Optional[int] = None,
    memory_enabled: bool = True
) -> GeminiAgent:
    """
    Create and configure a Google Gemini agent.
    
    Args:
        model_name: Gemini model to use (default: from config or gemini-1.5-flash)
        temperature: Model temperature for response creativity (default: from config or 0.7)
        max_tokens: Maximum tokens for responses (default: from config or None)
        memory_enabled: Whether to enable conversation memory (default: True)
    
    Returns:
        Configured GeminiAgent instance
    """
    try:
        # Use config values if not provided
        if model_name is None:
            model_name = MODEL_NAME
        if temperature is None:
            temperature = TEMPERATURE
        if max_tokens is None:
            max_tokens = MAX_TOKENS
        
        # Check for Gemini API key
        if not API_KEY:
            raise ValueError("Gemini API key is required. Please set it in config.py or as GEMINI_API_KEY environment variable")
        
        logger.info(f"Creating Gemini agent with model: {model_name}")
        
        # Configure Gemini
        genai.configure(api_key=API_KEY)
        
        # Create generation config
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        # Initialize the model
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
        
        # Create the Gemini agent
        agent = GeminiAgent(model)
        
        logger.info("Gemini agent created successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create Gemini agent: {str(e)}")
        raise

def get_agent_info() -> dict:
    """
    Get information about the current agent configuration.
    
    Returns:
        Dictionary containing agent configuration details
    """
    return {
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "api_key_configured": bool(API_KEY),
        "agent_type": "GeminiAgent",
        "provider": "Google Gemini"
    }
