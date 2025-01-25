from crewai import Agent
from typing import Any

class QuestionAgents:
    def __init__(self, llm: Any):
        self.content_specialist = Agent(
            role='Especialista em Conteúdo',
            goal='Analisar o conteúdo e criar questões adequadas ao nível escolar',
            backstory='Especialista em educação com vasta experiência em criar material didático',
            allow_delegation=False,
            verbose=True,
            llm=llm,
            tools=[]
        )

        self.question_reviewer = Agent(
            role='Revisor de Questões',
            goal='Revisar e garantir a qualidade das questões geradas',
            backstory='Professor experiente especializado em avaliação educacional',
            allow_delegation=False,
            verbose=True,
            llm=llm,
            tools=[]
        )

        self.format_specialist = Agent(
            role='Especialista em Formatação',
            goal='Formatar as questões de acordo com os requisitos específicos',
            backstory='Especialista em design instrucional e formatação de material didático',
            allow_delegation=False,
            verbose=True,
            llm=llm,
            tools=[]
        )

