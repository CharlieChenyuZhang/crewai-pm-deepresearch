from dotenv import load_dotenv
import datetime
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

load_dotenv()

def product_manager_agent():
    llm = ChatOpenAI(model="gpt-4o")

    return Agent(
        role='Senior Product Manager',
        goal='Conduct thorough product research on given topics',
        backstory='You are a senior product manager at a big tech FAANG company with deep understanding of software product development.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def product_manager_task(agent, topic):
    return Task(
        description=f"Analyze the following topic and provide a comprehensive Product Requirements Document (PRD): {topic}",
        agent=agent,
        expected_output="""A detailed Product Requirements Document (PRD), which will be used by a team of software engineers to develop the products. A Product Requirements Document (PRD) provides engineers with a clear, comprehensive guide to building a product or feature. It includes an overview of the product’s purpose, goals, and target users, along with detailed feature descriptions, user stories, acceptance criteria, and edge cases. The document outlines technical requirements, including platform specifications, API needs, performance metrics, and security considerations. It also provides design requirements with wireframes or prototypes, identifies dependencies, and details testing plans to ensure quality. Finally, it includes a timeline, milestones, and any known risks or open questions to guide development and ensure alignment across teams. Focus on the feature details and be as specific as possible.
                        Formatted as markdown without ``` Please cite the sources if necessary and at the end have a list of references if needed.""",
        output_file=get_output_filename()
    )

def get_output_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prd_reports/prd_report_{timestamp}.md"
    return filename

def run_research(topic):
    agent = product_manager_agent()
    task = product_manager_task(agent, topic)
    crew = Crew(agents=[agent], tasks=[task])
    crew.kickoff()


if __name__ == "__main__":
    print("Welcome to the Product Manager Agent!")
    topic = input("What do you want to build: ")
    
    run_research(topic)
    print("\nPRD generated successfully!")