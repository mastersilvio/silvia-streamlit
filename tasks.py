from crewai import Task
from typing import Dict, Any

class QuestionTasks:
    def create_content_task(self, agent, params: Dict[str, Any]) -> Task:
        return Task(
            description=f"""
            Gere exatamente {params['quantity']} questões para:
            Disciplina: {params['discipline']}
            Série: {params['grade']}
            Conteúdo: {params['content']}

            Instruções específicas:
            1. Gere apenas o número solicitado de questões
            2. Mantenha o nível adequado à série especificada
            3. Foque apenas na criação do conteúdo básico das questões
            4. Retorne apenas as questões sem formatação especial
            """,
            expected_output="Lista numerada de questões brutas",
            agent=agent
        )

    def create_review_task(self, agent, questions: str) -> Task:
        return Task(
            description=f"""
            Revise as seguintes questões:
            {questions}

            Instruções específicas:
            1. Verifique a clareza dos enunciados
            2. Confirme a precisão do conteúdo
            3. Sugira correções necessárias
            4. NÃO altere a quantidade de questões
            5. Retorne as questões revisadas
            """,
            expected_output="Lista de questões revisadas",
            agent=agent
        )

    def create_format_task(self, agent, questions: str, params: Dict[str, Any]) -> Task:
        format_instructions = []
        if params['multiple_choice']:
            format_instructions.append("- Adicione 5 alternativas (A a E) para cada questão")
        if params['problem_situation']:
            format_instructions.append("- Inclua um contexto ou situação problema")
        if params['competition']:
            format_instructions.append("- Adicione referência de banca de concurso")
        if params['answer']:
            format_instructions.append("- Inclua gabarito comentado ao final")

        return Task(
            description=f"""
            Formate as seguintes questões:
            {questions}

            Aplicar as seguintes formatações:
            {chr(10).join(format_instructions)}

            Instruções específicas:
            1. Mantenha a quantidade original de questões
            2. Aplique apenas as formatações solicitadas
            3. Retorne o resultado final formatado
            """,
            expected_output="Questões formatadas de acordo com as especificações",
            agent=agent
        )
