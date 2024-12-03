# AI Research Assistant

This project contains two AI-powered research assistants built using CrewAI that help with general research and YouTube content strategy.

## Author
Fitzroy Meyer-Petgrave

## Repository
[github.com/fitzroypet/ai-research-agent](https://github.com/fitzroypet/ai-research-agent)

## Features

- **General Research Assistant**: Conducts comprehensive research on any topic using multiple web sources
- **YouTube Content Strategy Assistant**: Analyzes niches, competitors, and generates content strategies

## Prerequisites

- Python 3.8+
- OpenAI API key
- Serper API key

## Installation

1. Clone the repository: 

bash
git clone https://github.com/fitzroypet/ai-research-agent.git

cd ai-research-agent

2. Install required packages:

bash
pip install crewai langchain-openai crewai-tools python-dotenv langchain-community

3. Set up your environment:
   - Create a `.env` file in the project root
   - Get your OpenAI API key: https://platform.openai.com/api-keys
   - Get your Serper key: https://serper.dev/api-key

Add keys in the .env file

OPENAI_API_KEY=your-api-key-here

SERPER_API_KEY=your-api-key-here

4. Create a `.gitignore` file:

text
.env
.venv
__pycache__/
output/
.DS_Store
.venv/


## Scripts

### 1. General Research (`general_research.py`)

A research assistant that uses multiple AI agents to gather and synthesize information.

**Features:**
- Web searching and browsing
- Information synthesis
- Structured report generation

**Tools Used:**
- SerperDevTool (web search)
- WebsiteSearchTool (website analysis)
- FileReadTool (file reading)

**Usage:**

bash
python general_research.py "Your research topic here"


### 2. YouTube Research (`youtube_research.py`)

A specialized assistant for YouTube content strategy and niche analysis.

**Features:**
- Niche validation
- Competitor analysis
- Content strategy development
- SEO optimization

**Tools Used:**
- YoutubeChannelSearchTool
- YoutubeVideoSearchTool
- SerperDevTool
- BrowserbaseLoadTool

**Usage:**

bash
python youtube_research.py "Your niche description here"


## Output

Both scripts create output files in an `output` directory with timestamps:
- `output/general_research_YYYYMMDD_HHMMSS.txt`
- `output/youtube_research_YYYYMMDD_HHMMSS.txt`

## Example Usage

### General Research Example:

bash
python general_research.py "being human in the age of AI"

### YouTube Research Example:

bash
python youtube_research.py "what it means to be human in the age of AI"


## Output Format

### General Research Output:
1. Executive Summary
2. Key Findings
3. Supporting Evidence
4. Practical Implications
5. Recommendations

### YouTube Research Output:
1. Niche Analysis
2. Content Opportunities
3. Competitor Insights
4. Video Concepts
5. SEO Recommendations

## Project Structure

ai-research-agent/
├── README.md
├── general_research.py
├── youtube_research.py
└── output/
├── general_research_.txt
└── youtube_research_.txt

## Environment Variables

The project uses a `.env` file to manage environment variables. This approach:
- Keeps your API key secure
- Prevents accidental exposure in version control
- Makes it easy to share code without sharing sensitive information

New contributors should:
1. Create their own `.env` file
2. Add their OpenAI API key
3. Never commit the `.env` file to version control

## Customization

### Modifying Agent Behavior

You can adjust the OpenAI model and temperature in either script:

python
openai = ChatOpenAI(
model="gpt-4-turbo-preview", # or "gpt-3.5-turbo"
temperature=0.7 # 0.0 for focused, 1.0 for creative
)


### Adding New Tools

Additional CrewAI tools can be imported and added to agents:

python
from crewai_tools import NewTool
new_tool = NewTool()
agent.tools.append(new_tool)


## Limitations

- Requires active internet connection
- API key usage may incur costs
- Processing time varies with research complexity

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

## Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Powered by OpenAI's GPT models

