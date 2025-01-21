import pandas as pd
import streamlit as st
import joblib 

# Dicionário de valores numéricos
x_numbers = {'host_listings_count': 0, 'latitude': 0, 'longitude': 0, 'accommodates': 0,
             'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
             'minimum_nights': 0, 'month': 0, 'year': 0, 'amenities_number': 0}

# Dicionário de categorias
x_list = {'property_type': ['Apartment', 'Condominium', 'House', 'Loft', 'Others', 'Serviced apartment'],
          'room_type': ['Hotel room', 'Private room', 'Shared room', 'Entire home/apt'],
          'cancelation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period'],
          'bed_type': ['Airbed', 'Couch', 'Futon', 'Pull-out Sofa', 'Real Bed']}

# Coleta de inputs numéricos do usuário
for item in x_numbers:
    if item == 'latitude':
        number = st.number_input(f'{item}', step=0.00001, value=0.0, format='%.5f')
    elif item == 'longitude':
        number = st.number_input(f'{item}', step=0.00001, value=0.0, format='%.5f')
    elif item == 'extra_people':
        number = st.number_input(f'{item}', step=0.1, value=0.0)
    else:
        number = st.number_input(f'{item}', step=1, value=0)
    x_numbers[item] = number

# Criação do dicionário para as variáveis categóricas
dictAux = {}
for item in x_list:
    for value in x_list[item]:
        dictAux[f'{item}_{value}'] = 0

# Seleção de categorias
for item in x_list:
    user_choice = st.selectbox(f'{item}', x_list[item])
    dictAux[f'{item}_{user_choice}'] = 1

# Botão para prever o preço
button = st.button('Prever Valor do Imóvel')

if button:
    # Atualizar o dicionário com as variáveis numéricas
    dictAux.update(x_numbers)
    
    # Criar DataFrame a partir do dicionário
    predict = pd.DataFrame([dictAux])
    
    # Garantir que as colunas correspondam ao modelo
    model = joblib.load('modelo.joblib')
    expected_columns = model.feature_names_in_  # Colunas esperadas pelo modelo
    for col in expected_columns:
        if col not in predict.columns:
            predict[col] = 0  # Adicionar as colunas faltantes com valor 0
    
    # Ordenar as colunas na mesma ordem do treinamento
    predict = predict[expected_columns]
    
    # Prever o preço
    price = model.predict(predict)
    st.write(f"Preço estimado do imóvel: {price[0]:.2f}")
