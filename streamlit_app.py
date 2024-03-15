import pandas as pd
import streamlit as st
from functions import AHPGaussiano


def load_data():
    return pd.read_csv('data/bike_stats.csv')

def display_header(title):
    st.markdown(f"<h1 style='text-align: center;font-size:40px;'>{title}</h1>", unsafe_allow_html=True)


def min_max_scaler(values):
    results = []
    X = values
    min_val = min(X)
    max_val = max(X)

    if max_val == min_val:

        for i in range(len(X)):
            results.append(0.5)
    else:
        for i in range(len(X)):
            X_std = (X[i] - min_val) / (max_val - min_val)
            results.append(X_std)

    return results


def display_comparison_columns(bike_names):
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        display_header("Moto 1")
        modelo_1 = st.selectbox('Selecione a primeira moto', bike_names)
        preco_1 = st.number_input(f"Por qual preço você pretende comprar o primeiro modelo?",min_value=100)



    with col3:
        display_header("Moto 2")
        modelo_2 = st.selectbox('Selecione a segunda moto', bike_names)
        preco_2 = st.number_input(f"Por qual preço você pretende comprar o segundo modelo?",min_value=100)




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
    criterio = ['preco']
    dados = df[df['modelo'].isin([modelo_1, modelo_2])]

    # Add missing columns if not present
    for col in ['cilindrada', 'potencia', 'torque', 'peso', 'tanque']:
        if col not in dados.columns:
            dados[col] = None

    for col in criterio:
        if col not in dados.columns:
            dados[col] = None

    # Set index to 'modelo's
    dados.set_index('modelo', inplace=True)

    # Fill in the missing data
    dados.loc[modelo_1, criterio[0]] = preco_1
    dados.loc[modelo_2, criterio[0]] = preco_2



    minimizar_criterio = ['preco','peso']
    ahp_gaussiano = AHPGaussiano(dados, minimizar_criterio)
    return ahp_gaussiano.preferencia_global()


def main():
    st.set_page_config(
        page_title="Calculadora de Custo Beneficio de Motocicletas 2024",
        layout="centered")
    with open('styles.css', 'r') as file:
        css = file.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    st.image('images/background.jpg')


    df = load_data()
    bike_names = df['modelo'].tolist()


    display_header("Comparador de Custo/Beneficio de Motos")
    modelo_1, preco_1, modelo_2, preco_2 = display_comparison_columns(bike_names)
    predict_button = display_comparison_button()

    if predict_button:
        escolha_ahp_gaussiano = perform_comparison(df, modelo_1, preco_1, modelo_2, preco_2)
        st.write(f'Melhor escolha é {escolha_ahp_gaussiano.index[0]} com peso {escolha_ahp_gaussiano.iloc[0][1]:.2f}')
        st.write(escolha_ahp_gaussiano, width=0)  # Set width to 0 to make it fill the available space

    hide_default_format = """
           <style>
           #MainMenu {visibility: hidden; }
           footer {visibility: hidden;}
           </style>
           """
    st.markdown(hide_default_format, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
