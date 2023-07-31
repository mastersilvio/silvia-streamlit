import streamlit as st
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.title('silvIA')

openai_api_key = os.getenv('OPENAI_API_KEY')
discipline = st.selectbox('Escolha uma disciplina', ['Matemática', 'Lingua Portuguesa', 'História', 'Geografia', 'Ciências'])
multiple_choice = st.checkbox('Múltipla escolha')
problem_situation = st.checkbox('Situação problema')
quantity = st.number_input('Quantidade de questões', min_value=1, max_value=10, value=1)

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.info(llm(input_text))

with st.form('my_form'):
  text = 'Crie uma prova de {} com {} questões que seja múltipla escolha {} e com situação problema {}'.format(discipline, quantity, 'sim' if multiple_choice else 'não', 'sim' if problem_situation else 'não')
  submitted = st.form_submit_button('Submit')
  if submitted:
    generate_response(text)
