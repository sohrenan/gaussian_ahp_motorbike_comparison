import pandas as pd
from mcdm.ahp import AHPGaussiano
import streamlit as st
import os

def load_data():
    current_dir = os.path.dirname(__file__)
    return pd.read_csv(os.path.join(current_dir, 'bike_stats.csv'))

def display_header(title):
    st.markdown(f"<h1 style='text-align: center;font-size:40px;'>{title}</h1>", unsafe_allow_html=True)

def display_comparison_columns(bike_names):
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        display_header("Moto 1")
        modelo_1 = st.selectbox('Selecione a primeira moto', bike_names)
        preco_1 = st.number_input(f"Por qual preço você pretende comprar o primeiro modelo?")

    with col3:
        display_header("Moto 2")
        modelo_2 = st.selectbox('Selecione a segunda moto', bike_names)
        preco_2 = st.number_input(f"Por qual preço você pretende comprar o segundo modelo?")

    return modelo_1, preco_1, modelo_2, preco_2

def display_comparison_button():
    with st.container():
        st.empty()

    left_column, center_column, right_column = st.columns([2.3, 1, 2])

    with center_column:
        st.empty()
        predict_button = st.button('Comparar')
        return predict_button

def perform_comparison(df, modelo_1, preco_1, modelo_2, preco_2):
    criterio = 'preco'
    dados = df[df['modelo'].isin([modelo_1, modelo_2])]

    # Add missing columns if not present
    for col in ['cilindrada', 'potencia', 'torque', 'consumo', 'peso', 'tanque', criterio]:
        if col not in dados.columns:
            dados[col] = None

    # Set index to 'modelo's
    dados.set_index('modelo', inplace=True)

    # Fill in the missing data
    dados.loc[modelo_1, criterio] = preco_1
    dados.loc[modelo_2, criterio] = preco_2

    minimizar_criterio = [criterio]
    ahp_gaussiano = AHPGaussiano(dados, minimizar_criterio)
    return ahp_gaussiano.preferencia_global()


def main():
    st.set_page_config(
        page_title="Previsão Resultados CBLOL 2024",
        page_icon="images/cblol.ico",  # Provide the path to your favicon
        layout="centered"
    )

    df = load_data()
    bike_names = df['modelo'].tolist()

    display_header("Moto Comparison")
    modelo_1, preco_1, modelo_2, preco_2 = display_comparison_columns(bike_names)
    predict_button = display_comparison_button()

    if predict_button:
        escolha_ahp_gaussiano = perform_comparison(df, modelo_1, preco_1, modelo_2, preco_2)
        st.write(escolha_ahp_gaussiano)

    hide_default_format = """
           <style>
           #MainMenu {visibility: hidden; }
           footer {visibility: hidden;}
           </style>
           """
    st.markdown(hide_default_format, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
