import os
from typing import List, Dict
from crewai import Agent, Task, Crew, Process, LLM
from custom_tools import search_tool
from dotenv import load_dotenv
from logger import log_progress

# Load environment variables
load_dotenv()


def get_default_llm(model_name: str = "deepseek-chat"):
    """Configure the LLM based on user selection or fallback safely for tests"""
    if "deepseek" in model_name:
        api_key = (
            os.getenv("DEEPSEEK_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or "mock-deepseek-key"
        )
        model_str = (
            f"deepseek/{model_name}"
            if not model_name.startswith("deepseek/")
            else model_name
        )
        return LLM(
            model=model_str,
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
            temperature=0.7,
            max_tokens=4000,
        )
    elif "gpt" in model_name:
        api_key = os.getenv("OPENAI_API_KEY") or "mock-openai-key"
        return LLM(
            model=model_name,
            api_key=api_key,
            temperature=0.7,
        )
    elif "claude" in model_name:
        api_key = os.getenv("ANTHROPIC_API_KEY") or "mock-anthropic-key"
        model_str = (
            f"anthropic/{model_name}"
            if not model_name.startswith("anthropic/")
            else model_name
        )
        return LLM(
            model=model_str,
            api_key=api_key,
            temperature=0.7,
        )
    else:
        api_key = (
            os.getenv("DEEPSEEK_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or "mock-deepseek-key"
        )
        return LLM(
            model="deepseek/deepseek-chat",
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
            temperature=0.7,
            max_tokens=4000,
        )


class ContentGenerationCrew:
    """Multi-agent content generation system with dynamic model support"""

    def __init__(self, model: str = "deepseek-chat"):
        log_progress(f"Initializing NarrativeNexus Crew with engine: {model}...")
        self.model_name = model
        self.llm = self._setup_llm()
        self.agents = self._create_agents()
        log_progress("NarrativeNexus initialized successfully.")

    def _setup_llm(self):
        """Configure the LLM based on user selection"""
        return get_default_llm(self.model_name)

    def _create_agents(self) -> Dict[str, Agent]:
        """Create specialized content agents"""

        log_progress("Creating agents...")
        # 1. Research Analyst
        researcher = Agent(
            role="Senior Research Analyst",
            goal="Discover accurate, current information and credible sources on any topic",
            backstory="""You are an expert research analyst with a PhD in Information Science.
            You have 15 years of experience in investigative research and fact-finding.
            You excel at finding authoritative sources, verifying information, and
            synthesizing complex data into clear insights. You never cite unverified
            information and always provide source URLs.""",
            tools=[search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=False,
        )

        # 2. Content Writer
        writer = Agent(
            role="Expert Content Writer",
            goal="Create engaging, well-structured content that captivates readers",
            backstory="""You are an award-winning content writer with a background in
            journalism and creative writing. You've written for top publications like
            Medium, TechCrunch, and The Atlantic. Your writing is clear, engaging, and
            accessible. You excel at storytelling, using compelling hooks, and maintaining
            reader interest throughout. You always write in active voice and use concrete
            examples.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=False,
        )

        # 3. Senior Editor
        editor = Agent(
            role="Senior Content Editor",
            goal="Refine content to perfection through editing and structural improvements",
            backstory="""You are a meticulous editor with 20 years of experience in
            publishing. You've edited content for major media outlets and have a keen eye
            for clarity, flow, and impact. You improve structure, enhance readability,
            eliminate redundancy, and ensure every sentence adds value. You catch
            grammatical errors, awkward phrasing, and logical inconsistencies.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=False,
        )

        # 4. Fact Checker
        fact_checker = Agent(
            role="Professional Fact Checker",
            goal="Verify all claims, statistics, and assertions in content",
            backstory="""You are a professional fact-checker who worked for major news
            organizations. You have an obsessive attention to detail and never let false
            information slip through. You verify every claim, cross-reference sources,
            and flag anything that seems questionable. You provide corrections with
            proper citations.""",
            tools=[search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=False,
        )

        # 5. SEO Specialist
        seo_specialist = Agent(
            role="SEO Optimization Expert",
            goal="Optimize content for search engines while maintaining quality and readability",
            backstory="""You are an SEO expert with deep knowledge of search engine
            algorithms, keyword research, and content optimization. You've helped dozens
            of websites rank #1 for competitive keywords. You optimize headlines, meta
            descriptions, keyword placement, and content structure. You balance SEO best
            practices with user experience.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=False,
        )

        log_progress("All agents created.")
        return {
            "researcher": researcher,
            "writer": writer,
            "editor": editor,
            "fact_checker": fact_checker,
            "seo_specialist": seo_specialist,
        }

    def _create_tasks(self, topic: str, content_type: str = "blog_post") -> List[Task]:
        """Create content generation tasks"""

        agents = self.agents

        # Task 1: Research
        research_task = Task(
            description=f"""
            Conduct comprehensive research on the topic: "{topic}"

            Your research should include:
            1. Current trends and latest developments (last 6-12 months)
            2. Key statistics and data points with sources
            3. Expert opinions and notable quotes
            4. Real-world examples and case studies
            5. Common questions or misconceptions

            Focus on authoritative sources:
            - Academic papers and research studies
            - Reputable news outlets and industry publications
            - Expert blogs and official documentation
            - Government or institutional reports

            Topic: {topic}
            """,
            expected_output="""
            A comprehensive research report in markdown format containing:

            # Research Report: [Topic]

            ## Executive Summary
            [2-3 sentences summarizing key findings]

            ## Key Findings
            1. [Finding with source]
            2. [Finding with source]
            ... (5-7 findings total)

            ## Statistics & Data
            - [Statistic with source and date]
            - [Statistic with source and date]
            ... (3-5 statistics)

            ## Expert Insights
            - "[Quote]" - [Expert Name, Title, Source]
            ... (2-3 quotes)

            ## Examples & Case Studies
            [2-3 relevant examples with details]

            ## Sources
            1. [Full source citation with URL]
            2. [Full source citation with URL]
            ... (All sources used)
            """,
            agent=agents["researcher"],
        )

        # Task 2: Content Outlining
        outline_task = Task(
            description=f"""
            Based on the research findings, create a detailed content outline.

            Content Type: {content_type}
            Topic: {topic}

            Your outline should:
            1. Start with a compelling hook
            2. Have a clear logical flow
            3. Include main sections and subsections
            4. Note where to include statistics, quotes, or examples
            5. End with a strong conclusion and call-to-action
            """,
            expected_output="""
            A detailed content outline in this format:

            # Content Outline: [Title]
            ...
            """,
            agent=agents["writer"],
            context=[research_task],
        )

        # Task 3: Content Writing
        write_task = Task(
            description=f"""
            Write a complete, engaging {content_type} based on the outline and research.

            Length: Aim for 1500-2000 words
            Format: Markdown with proper headers, lists, and emphasis
            """,
            expected_output="""
            A complete, polished article in markdown format.
            """,
            agent=agents["writer"],
            context=[research_task, outline_task],
        )

        # Task 4: Editing
        edit_task = Task(
            description="""
            Edit the content to perfection. Focus on Structure, Clarity, Engagement, and Technical correctness.
            """,
            expected_output="""
            Edited article with editorial notes.
            """,
            agent=agents["editor"],
            context=[write_task],
        )

        # Task 5: Fact Checking
        fact_check_task = Task(
            description="""
            Thoroughly fact-check all claims in the content.
            """,
            expected_output="""
            Detailed Fact-Check Report.
            """,
            agent=agents["fact_checker"],
            context=[edit_task],
        )

        # Task 6: SEO Optimization
        seo_task = Task(
            description=f"""
            Optimize the content for search engines while maintaining quality.
            Topic: {topic}
            """,
            expected_output="""
            SEO Optimization Report and the Final Optimized Content.
            """,
            agent=agents["seo_specialist"],
            context=[edit_task, fact_check_task],
        )

        return [
            research_task,
            outline_task,
            write_task,
            edit_task,
            fact_check_task,
            seo_task,
        ]

    def generate_content(self, topic: str, content_type: str = "blog_post") -> Dict:
        """
        Generate content using the multi-agent crew
        """

        log_progress(f"🚀 Starting content generation for: {topic}")

        # Create tasks
        tasks = self._create_tasks(topic, content_type)
        log_progress(f"Tasks created. Number of tasks: {len(tasks)}")

        # Create crew
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

        # Execute crew
        log_progress("Executing crew.kickoff()...")
        result = crew.kickoff()
        log_progress("crew.kickoff() finished successfully.")

        return {
            "final_content": str(result),
            "topic": topic,
            "content_type": content_type,
            "agents_used": len(self.agents),
            "tasks_completed": len(tasks),
        }


if __name__ == "__main__":
    content_crew = ContentGenerationCrew()
