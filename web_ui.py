#!/usr/bin/env python3
"""
Advanced AI Agent Web UI

A sophisticated web interface for an autonomous agent that can perform
multi-step tasks including searching, summarizing, and extracting information.
Built for internship preparation showcasing Generative AI and software engineering skills.
"""

import streamlit as st
import sys
from pathlib import Path
import time
from datetime import datetime
import json

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from agents.gemini_agent import create_agent, get_agent_info
from utils.logger import setup_logger

# Configure Streamlit page
st.set_page_config(
    page_title="Autonomous AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .agent-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    
    .task-message {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: #4caf50;
    }
    
    .status-offline {
        background-color: #f44336;
    }
    
    .sidebar-info {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .capability-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #007bff;
        color: #111;
    }
    
    .workflow-step {
        background-color: #fff3cd;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        border-left: 3px solid #ffc107;
    }

    /* Ensure readability in dark theme */
    .stApp[theme="dark"] .sidebar-info,
    .stApp[theme="dark"] .capability-card,
    .stApp[theme="dark"] .workflow-step {
        background-color: rgba(255,255,255,0.08) !important;
        color: #fff !important;
    }

    .stApp[theme="dark"] .sidebar-info strong { color: #fff !important; }
    .stApp[theme="dark"] .capability-card b { color: #fff !important; }
    .stApp[theme="dark"] .workflow-step { color: #222; background-color: #ffe9a6 !important; }

    /* Streamlit v1.30+ dark selector fallback */
    [data-theme="dark"] .sidebar-info,
    [data-theme="dark"] .capability-card,
    [data-theme="dark"] .workflow-step {
        background-color: rgba(255,255,255,0.08) !important;
        color: #fff !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "agent_initialized" not in st.session_state:
        st.session_state.agent_initialized = False
    if "task_history" not in st.session_state:
        st.session_state.task_history = []
    if "workflow_steps" not in st.session_state:
        st.session_state.workflow_steps = []

def initialize_agent():
    """Initialize the AI agent."""
    try:
        if not st.session_state.agent_initialized:
            with st.spinner("Initializing Autonomous AI Agent..."):
                st.session_state.agent = create_agent()
                st.session_state.agent_initialized = True
            st.success("🤖 Autonomous AI Agent initialized successfully!")
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return False

def display_chat_message(role, content, is_error=False, is_task=False):
    """Display a chat message with appropriate styling."""
    if is_error:
        st.markdown(f"""
        <div class="chat-message error-message">
            <strong>{role}:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    elif is_task:
        st.markdown(f"""
        <div class="chat-message task-message">
            <strong>{role}:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    elif role == "You":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>{role}:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message agent-message">
            <strong>{role}:</strong> {content}
        </div>
        """, unsafe_allow_html=True)

def process_multi_step_task(user_input):
    """Process multi-step tasks with workflow tracking."""
    workflow_steps = []
    
    # Analyze the task
    analysis_prompt = f"""
    Analyze this task and break it down into steps:
    "{user_input}"
    
    Return a JSON list of steps like:
    ["Step 1: Search for information about X", "Step 2: Summarize the findings", "Step 3: Extract key insights"]
    """
    
    try:
        # Get task breakdown
        analysis_response = st.session_state.agent.invoke({"input": analysis_prompt})
        workflow_steps = [f"📋 Task Analysis: {user_input}"]
        
        # Execute the main task
        main_response = st.session_state.agent.invoke({"input": user_input})
        
        # Add workflow steps
        workflow_steps.extend([
            f"🔍 Information Gathering",
            f"📊 Data Processing", 
            f"📝 Response Generation"
        ])
        
        st.session_state.workflow_steps = workflow_steps
        st.session_state.task_history.append({
            "task": user_input,
            "steps": workflow_steps,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        return main_response["output"]
        
    except Exception as e:
        return f"Error processing multi-step task: {str(e)}"

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Autonomous AI Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Multi-Step Task Execution • Information Extraction • Intelligent Summarization</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📊 Agent Status")
        
        # Agent info
        if st.session_state.agent_initialized:
            st.markdown("""
            <div class="sidebar-info">
                <span class="status-indicator status-online"></span>
                <strong>Status:</strong> Online<br>
                <strong>Model:</strong> Gemini 2.0 Flash<br>
                <strong>Provider:</strong> Google<br>
                <strong>Capabilities:</strong> Multi-Step Tasks<br>
                <strong>Memory:</strong> Enabled
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sidebar-info">
                <span class="status-indicator status-offline"></span>
                <strong>Status:</strong> Offline<br>
                <em>Click "Initialize Agent" to start</em>
            </div>
            """, unsafe_allow_html=True)
        
        # Initialize button
        if not st.session_state.agent_initialized:
            if st.button("🚀 Initialize Agent", type="primary", use_container_width=True):
                initialize_agent()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.task_history = []
            st.session_state.workflow_steps = []
            st.rerun()
        
        # Agent capabilities
        st.markdown("## 🛠️ Agent Capabilities")
        capabilities = [
            "🔍 **Information Search** - Find and retrieve relevant data",
            "📊 **Data Analysis** - Process and analyze information",
            "📝 **Summarization** - Create concise summaries",
            "🎯 **Information Extraction** - Extract key insights",
            "🔄 **Multi-Step Workflows** - Execute complex tasks",
            "💬 **Conversational AI** - Natural language interaction"
        ]
        
        for capability in capabilities:
            st.markdown(f'<div class="capability-card">{capability}</div>', unsafe_allow_html=True)
        
        # Task history
        if st.session_state.task_history:
            st.markdown("## 📋 Recent Tasks")
            for task in st.session_state.task_history[-3:]:  # Show last 3 tasks
                st.markdown(f"**{task['timestamp']}**: {task['task'][:50]}...")
        
        # Agent info button
        if st.button("ℹ️ Technical Details", use_container_width=True):
            try:
                info = get_agent_info()
                st.json(info)
            except Exception as e:
                st.error(f"Error getting agent info: {str(e)}")
    
    # Main interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 💬 Autonomous Agent Interface")
        
        # Display chat history
        for message in st.session_state.messages:
            display_chat_message(
                message["role"], 
                message["content"], 
                message.get("is_error", False),
                message.get("is_task", False)
            )
        
        # Workflow steps display
        if st.session_state.workflow_steps:
            st.markdown("### 🔄 Current Workflow")
            for step in st.session_state.workflow_steps:
                st.markdown(f'<div class="workflow-step">{step}</div>', unsafe_allow_html=True)
        
        # Chat input
        if st.session_state.agent_initialized:
            user_input = st.chat_input("Describe your multi-step task...")
            
            if user_input:
                # Add user message to chat
                st.session_state.messages.append({"role": "You", "content": user_input})
                display_chat_message("You", user_input)
                
                # Process the task
                with st.spinner("🤖 Agent is executing multi-step task..."):
                    try:
                        # Check if it's a complex task
                        complex_keywords = ["search", "summarize", "extract", "analyze", "research", "find", "compare"]
                        is_complex_task = any(keyword in user_input.lower() for keyword in complex_keywords)
                        
                        if is_complex_task:
                            # Process as multi-step task
                            response = process_multi_step_task(user_input)
                            st.session_state.messages.append({
                                "role": "AI Agent", 
                                "content": response,
                                "is_task": True
                            })
                            display_chat_message("AI Agent", response, is_task=True)
                        else:
                            # Simple conversation
                            response = st.session_state.agent.invoke({"input": user_input})
                            agent_response = response.get("output", "Sorry, I couldn't generate a response.")
                            
                            st.session_state.messages.append({"role": "AI Agent", "content": agent_response})
                            display_chat_message("AI Agent", agent_response)
                        
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.session_state.messages.append({"role": "AI Agent", "content": error_msg, "is_error": True})
                        display_chat_message("AI Agent", error_msg, is_error=True)
                
                st.rerun()
        else:
            st.info("👆 Please initialize the agent from the sidebar to start executing tasks!")
    
    with col2:
        st.markdown("### 📈 Performance Metrics")
        
        # Display stats
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "You"])
        agent_messages = len([m for m in st.session_state.messages if m["role"] == "AI Agent"])
        tasks_completed = len(st.session_state.task_history)
        
        st.metric("Total Messages", total_messages)
        st.metric("Tasks Completed", tasks_completed)
        st.metric("Agent Responses", agent_messages)
        
        # Current time
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f"**Current Time:** {current_time}")
        
        # Sample tasks
        st.markdown("### 🎯 Sample Tasks")
        sample_tasks = [
            "Search for information about renewable energy trends",
            "Summarize the latest AI developments",
            "Extract key insights from market data",
            "Analyze customer feedback patterns",
            "Research best practices in software engineering"
        ]
        
        for task in sample_tasks:
            if st.button(task, key=f"sample_{task}", use_container_width=True):
                st.session_state.messages.append({"role": "You", "content": task})
                st.rerun()
        
        # Footer
        st.markdown("""
        ---
        **Autonomous AI Agent v2.0**  
        Built for Internship Preparation  
        Powered by Google Gemini & Streamlit
        """)

if __name__ == "__main__":
    main()