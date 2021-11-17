import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from difflib import SequenceMatcher
plt.style.use('dark_background')

def app():
    color_x = '#7ee1bd'
    color_u = '#4eafd7'
    def tabla_dinamica_GTT(columna, titulo):
        tabla = df.groupby(columna).sum().reset_index().sort_values( 'GRAN TOTAL TEUS', ascending = False).reset_index()[:10]
        tabla['Total Contenedores 40 (Feus)']=tabla['Total Contenedores 40 (Feus)']*2
        fig = plt.figure()
        sns.barplot(y = columna, x = 'Total Contenedores 20 (Teus)' , data = tabla, color =  color_u, label = 'Teus' )
        sns.barplot(y = columna, x = 'Total Contenedores 40 (Feus)' , data = tabla, left=tabla['Total Contenedores 20 (Teus)'], color = color_x,label = 'Feus')
        T = tabla.loc[0]['GRAN TOTAL TEUS']
        t = T/21
        for i in tabla.index:
            plt.text(t + tabla.loc[i]['GRAN TOTAL TEUS'], i + 0.15 , round(tabla.loc[i]['GRAN TOTAL TEUS']),color = 'w',  ha="center")

        plt.ylabel('')
        plt.xlabel('GRAN TOTAL TEUS')
        plt.legend(loc = 'lower right')
        plt.title(titulo, size = 16)
        st.pyplot(fig)

    st.write('# United Logistic Services')

    file = st.file_uploader('Cargar archivo', type='xlsx')


    if file is not None:
        df = pd.read_excel(file, sheet_name = 'Data')

        principales_navieras = st.checkbox('Principales navieras',True)
        if principales_navieras:
            tabla_dinamica_GTT('Naviera', 'Principales navieras')

        principales_puertos = st.checkbox('Principales puertos', True)
        if principales_puertos :
            tabla_dinamica_GTT('Puerto Extranjero', 'Principales puertos extranjeros')
            tabla_dinamica_GTT('Puerto Colombiano', 'Principales puertos colombianos')
        principales_agentes = st.checkbox('Principales agentes', True)
        if principales_agentes:
            tabla_dinamica_GTT('Consolidador', 'Principales agentes')
            tabla = df.groupby('Consolidador').sum().reset_index().sort_values( 'GRAN TOTAL TEUS', ascending = False).set_index('Consolidador')
            tabla['Posición'] = tabla[ 'GRAN TOTAL TEUS'].rank(ascending = False)
            st.write(tabla[['GRAN TOTAL TEUS', 'Posición']])

        principales_productos = st.checkbox('Principales productos', True)
        if principales_productos:
            tabla_dinamica_GTT('Descripción BL ', 'Principales productos')
        principales_productos2 = st.checkbox('Principales productos ', True)
        if principales_productos2:
            tabla_dinamica_GTT('Descripción Capitulo ', 'Principales categorías')

        cliente_final = st.checkbox('Cliente final', True)
        if cliente_final:
            tabla = df.groupby('Empresa Colombiana Impo/Expo').sum().reset_index().sort_values('GRAN TOTAL TEUS', ascending = False)
            st.write(tabla.set_index('Empresa Colombiana Impo/Expo')['GRAN TOTAL TEUS'])
