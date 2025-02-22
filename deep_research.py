import os
from dotenv import load_dotenv
import datetime
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

search_tool = SerperDevTool()

def create_research_agent():
    llm = ChatOpenAI(model="gpt-4o")

    return Agent(
        role='Research Specialist',
        goal='Conduct thorough research on given topics',
        backstory='You are an experienced researcher with expertise in finding and synthesizing information from various sources.',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

def create_research_task(agent, topic):
    return Task(
        description=f"Research the following topic and provide a comprehensive summary: {topic}",
        agent=agent,
        expected_output="""A detailed summary of the research findings, including key points, trends, and insights related to the topic. A fully fledge reports with the mains topics, each with a full section of information.
                        Formatted as markdown without ``` Please cite the sources and at the end have a list of references.""",
        output_file=get_output_filename()
    )

def get_output_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"deepresearch_reports/research_result_{timestamp}.md"
    return filename

def run_research(topic):
    agent = create_research_agent()
    task = create_research_task(agent, topic)
    crew = Crew(agents=[agent], tasks=[task])
    crew.kickoff()


if __name__ == "__main__":
    print("Welcome to the Research Agent!")
    topic = input("Enter the research topic: ")
    
    run_research(topic)
    print("\nResearch completed successfully!")