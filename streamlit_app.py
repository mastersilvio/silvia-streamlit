import streamlit as st
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from crewai import Crew
from agents import QuestionAgents
from tasks import QuestionTasks

load_dotenv()

st.set_page_config(page_title="SilvIA", page_icon="images/silvIA.png")
st.image("images/silvIA.png", width=100)
st.title('SilvIA')
st.subheader('A sua assistente para gerar questões utilizando Inteligência Artificial')

disciplines = [
               'Língua Portuguesa',
                'Matemática',
                'Biologia',
                'Física',
                'Química',
                'História',
                'Geografia',
                'Sociologia',
                'Filosofia'
              ]
grades = [
          '6º ano do Ensino Fundamental',
          '7º ano do Ensino Fundamental',
          '8º ano do Ensino Fundamental',
          '9º ano do Ensino Fundamental',
          '1ª série do Ensino Médio',
          '2ª série do Ensino Médio',
          '3º série do Ensino Médio'
        ]

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("A chave da API do OpenAI não está definida. Verifique o arquivo .env.")
    st.stop()

discipline = st.selectbox('Escolha uma disciplina:', disciplines)
grade = st.selectbox('Escolha uma série:', grades)
content = st.text_input('Conteúdo:')
quantity = st.number_input('Quantidade de questões:', min_value=1, max_value=10, value=1)
multiple_choice = st.checkbox('Com questões de múltipla escolha?')
problem_situation = st.checkbox('Com situação problema?')
competition = st.checkbox('Com questões de concurso?')
answer = st.checkbox('Com resposta no final?')

def generate_response(params):
    try:
        with st.spinner('Gerando questões...'):
            # Configurar o modelo
            llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-3.5-turbo",
                openai_api_key=openai_api_key
            )

            # Criar instâncias de agentes e tarefas
            agents = QuestionAgents(llm=llm)
            tasks = QuestionTasks()

            # Criar e executar o crew
            crew = Crew(
                agents=[
                    agents.content_specialist,
                    agents.question_reviewer,
                    agents.format_specialist
                ],
                tasks=[
                    tasks.create_content_task(agents.content_specialist, params),
                    tasks.create_review_task(agents.question_reviewer, ""),
                    tasks.create_format_task(agents.format_specialist, "", params)
                ],
                verbose=True
            )

            result = crew.kickoff()
            st.success("Questões geradas com sucesso!")
            st.markdown(result)
    except Exception as e:
        st.error(f"Erro ao gerar questões: {str(e)}")

with st.form('my_form'):
    text = (
        'Crie uma prova para que eu possa estudar e contenha as seguintes características:\n'
        f'- Disciplina: {discipline}\n'
        f'- Série: {grade}\n'
        f'- Conteúdo: {content}\n'
        f'- Quantidade de questões: {quantity}\n'
        f'- Questões de múltipla escolha: {multiple_choice}\n'
        f'- Situação problema: {problem_situation}\n'
        f'- Com as repostas/gabarito no final: {answer}\n'
        f'- Questões de bancas de concurso público: {competition} e a descrição no início do enunciado quando for o caso\n'
    )

    submitted = st.form_submit_button('Solicitar Questões')
    if submitted:
        params = {
            'discipline': discipline,
            'grade': grade,
            'content': content,
            'quantity': quantity,
            'multiple_choice': multiple_choice,
            'problem_situation': problem_situation,
            'competition': competition,
            'answer': answer
        }
        generate_response(params)
