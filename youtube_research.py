from dotenv import load_dotenv
import os

# Force reload environment variables
os.environ.clear()
load_dotenv(override=True)

# Enhanced debug statements
print("\n=== Environment Check ===")
print(f"Working Directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists('.env')}")
print(f"API Key loaded: {'OPENAI_API_KEY' in os.environ}")

# Read and print the .env file content (safely)
print("\n=== .env File Content ===")
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        content = f.read().strip()
        print(f"Length of content: {len(content)}")
        print(f"First 10 chars: {content[:10]}...")
        print(f"Last 10 chars: {content[-10:]}")
        print(f"Contains 'your-act': {'your-act' in content}")
        print(f"Contains 'sk-proj': {'sk-proj' in content}")

# Print the actual environment variable
key = os.getenv('OPENAI_API_KEY', 'NOT_FOUND')
print("\n=== Environment Variable ===")
print(f"Length of key: {len(key)}")
print(f"First 10 chars: {key[:10]}...")
print(f"Last 10 chars: {key[-10:]}")
print(f"Contains 'your-act': {'your-act' in key}")
print(f"Contains 'sk-proj': {'sk-proj' in key}")
print("=" * 30 + "\n")

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai_tools import (
    YoutubeChannelSearchTool,
    YoutubeVideoSearchTool,
    SerperDevTool,
    WebsiteSearchTool
)
import argparse
from datetime import datetime

# 1. Add required API keys at the top
load_dotenv()
required_keys = ['OPENAI_API_KEY', 'SERPER_API_KEY']
for key in required_keys:
    if not os.getenv(key):
        raise ValueError(f"{key} not found in environment variables")

def run_youtube_research(niche_description):
    try:
        # Initialize tools
        youtube_channel_tool = YoutubeChannelSearchTool()
        youtube_video_tool = YoutubeVideoSearchTool()
        search_tool = SerperDevTool()
        website_tool = WebsiteSearchTool()

        # Initialize the LLM
        openai = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7
        )

        # Create Agents (your existing agent definitions)
        topic_researcher = Agent(
            role='Topic Researcher',
            goal='Research trending topics and identify content gaps in the YouTube market',
            backstory="""You are an expert YouTube trend analyst. You understand 
            what makes content viral and can identify promising content opportunities.""",
            tools=[youtube_channel_tool, search_tool],
            verbose=True,
            llm=openai
        )

        competitor_analyst = Agent(
            role='Competitor Analyst',
            goal='Analyze successful videos in the niche and identify winning patterns',
            backstory="""You are a YouTube strategy expert who excels at analyzing 
            successful channels and videos to extract winning formulas.""",
            tools=[youtube_video_tool, youtube_channel_tool],
            verbose=True,
            llm=openai
        )

        content_strategist = Agent(
            role='Content Strategist',
            goal='Create engaging video concepts and optimize for YouTube algorithm',
            backstory="""You are a YouTube content strategist who knows how to craft 
            viral video concepts and optimize them for maximum reach.""",
            tools=[search_tool, website_tool],
            verbose=True,
            llm=openai
        )

        # Create progress tracking
        tasks_completed = 0
        total_tasks = 3

        def update_progress():
            nonlocal tasks_completed
            tasks_completed += 1
            print(f"\nProgress: {tasks_completed}/{total_tasks} tasks completed")
            if tasks_completed < total_tasks:
                proceed = input("Continue to next task? (y/n): ")
                if proceed.lower() != 'y':
                    raise KeyboardInterrupt

        # Define Tasks with dynamic niche description
        research_task = Task(
            description=f"""Research current trending topics in the following niche and identify 
            3 potential video ideas with high potential. Use YouTube channel search to 
            analyze what's working in the market.
            
            Niche Description: {niche_description}""",
            expected_output="""A detailed analysis of trending topics and 3 video ideas, including:
            - Current market trends
            - Popular content formats
            - Potential audience interest
            - Competition level""",
            agent=topic_researcher,
            callbacks=[update_progress]
        )

        competitor_analysis_task = Task(
            description=f"""Analyze top 5 performing videos in this niche: {niche_description}. 
            Identify their hooks, structure, and engagement patterns. What makes them successful?""",
            expected_output="""Analysis of 5 top-performing videos including:
            - Video structure breakdown
            - Hook effectiveness
            - Engagement metrics
            - Success patterns""",
            agent=competitor_analyst,
            callbacks=[update_progress]
        )

        content_strategy_task = Task(
            description="""Based on the research and analysis, create a detailed video
            concept including:
            1. Catchy title options
            2. Hook ideas (first 15 seconds)
            3. Video structure
            4. Keywords for SEO
            5. Thumbnail concept ideas""",
            expected_output="""Complete video concept with:
            - 3-5 title options
            - Hook script
            - Detailed structure
            - SEO keywords
            - Thumbnail ideas""",
            agent=content_strategist,
            callbacks=[update_progress]
        )

        # Create Crew
        youtube_crew = Crew(
            agents=[topic_researcher, competitor_analyst, content_strategist],
            tasks=[research_task, competitor_analysis_task, content_strategy_task],
            verbose=True,
            process=Process.sequential
        )

        # Execute with error handling
        result = youtube_crew.kickoff()
        return result

    except KeyboardInterrupt:
        print("\n\nResearch interrupted by user.")
        return None
    except Exception as e:
        print(f"\nError during research: {str(e)}")
        return None

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run YouTube content research')
    parser.add_argument('niche', type=str, help='Description of your YouTube niche')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/youtube_research_{timestamp}.txt"

    # Run research and save results
    result = run_youtube_research(args.niche)
    
    # Convert CrewOutput to string if necessary
    if hasattr(result, 'raw'):
        result_str = str(result.raw)
    else:
        result_str = str(result)

    # Only write to file if we have results
    if result:
        with open(output_file, 'w') as f:
            f.write(f"Research for: {args.niche}\n")
            f.write("=" * 50 + "\n")
            f.write(result_str)
        print(f"\nResults saved to: {output_file}")
    else:
        print("\nNo results to save due to an error.")