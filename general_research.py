from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from crewai_tools import (
    SerperDevTool,
    FileReadTool,
    WebsiteSearchTool
)
import argparse
from datetime import datetime

# Load and verify environment variables
load_dotenv()
required_keys = ['OPENAI_API_KEY', 'SERPER_API_KEY']
for key in required_keys:
    if not os.getenv(key):
        raise ValueError(f"{key} not found in environment variables")

def run_research(research_prompt):
    try:
        # Initialize tools
        search_tool = SerperDevTool()
        file_tool = FileReadTool()
        website_tool = WebsiteSearchTool()

        # Initialize the LLM with proper error handling
        try:
            openai = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7
            )
        except Exception as e:
            print(f"Error initializing ChatOpenAI: {str(e)}")
            return None

        # Create Agents
        researcher = Agent(
            role='Researcher',
            goal='Conduct thorough research on topics related to AI and humanity',
            backstory='Expert at analyzing technological and societal trends',
            tools=[search_tool, website_tool],
            llm=openai
        )

        # Create Tasks
        research_task = Task(
            description=f"""Thoroughly research the following topic: {research_prompt}
            
            Consider:
            1. Latest developments and trends
            2. Key statistics and data
            3. Expert opinions and analyses
            4. Real-world applications and examples
            5. Potential challenges and solutions""",
            agent=researcher,
            expected_output="""Provide a comprehensive research report with the following sections:
                1. Executive Summary
                2. Key Findings
                3. Detailed Analysis
                4. Expert Opinions
                5. Conclusions and Implications"""
        )

        # Create and run the crew
        crew = Crew(
            agents=[researcher],
            tasks=[research_task],
            verbose=True
        )

        print(f"\nStarting research on: {research_prompt}")
        result = crew.kickoff()
        return result

    except Exception as e:
        print(f"\nError during research: {str(e)}")
        return None

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run research on a specific topic')
    parser.add_argument('prompt', type=str, help='The research prompt/topic')
    args = parser.parse_args()

    # Setup output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/general_research_{timestamp}.txt"

    # Run research with proper error handling
    try:
        result = run_research(args.prompt)
        if result:
            # Handle CrewOutput type
            result_str = str(result.raw) if hasattr(result, 'raw') else str(result)
            
            with open(output_file, 'w') as f:
                f.write(f"Research Topic: {args.prompt}\n")
                f.write("=" * 50 + "\n")
                f.write(result_str)
            print(f"\nResults saved to: {output_file}")
        else:
            print("\nNo results to save due to an error.")
    except Exception as e:
        print(f"\nError in main execution: {str(e)}")