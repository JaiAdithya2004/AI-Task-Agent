#!/usr/bin/env python3
"""
AI Agent - Main Application Script

This is the main script to run the AI agent. It initializes the agent,
sets up the environment, and provides an interactive interface for
users to interact with the agent.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from agents.gemini_agent import create_agent
from utils.logger import setup_logger

def main():
    """Main function to run the AI agent."""
    # Setup logging
    logger = setup_logger()
    logger.info("Starting AI Agent application...")
    
    try:
        # Create the agent
        logger.info("Initializing agent...")
        agent = create_agent()
        
        # Interactive loop
        logger.info("Agent ready! Type 'quit' or 'exit' to stop.")
        print("\n🤖 AI Agent is ready! Ask me anything or type 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye! 👋")
                    logger.info("User requested to exit. Shutting down...")
                    break
                
                if not user_input:
                    continue
                
                # Process user input with the agent
                logger.info(f"Processing user input: {user_input}")
                response = agent.invoke({"input": user_input})
                
                # Extract the response text from the agent output
                if isinstance(response, dict) and "output" in response:
                    response_text = response["output"]
                elif isinstance(response, str):
                    response_text = response
                else:
                    response_text = str(response)
                
                print(f"Agent: {response_text}")
                logger.info("Response generated successfully")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                logger.info("Application interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error processing input: {str(e)}")
                print(f"Sorry, I encountered an error: {str(e)}")
                
    except Exception as e:
        logger.error(f"Failed to initialize agent: {str(e)}")
        print(f"Failed to start the agent: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
