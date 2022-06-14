from cProfile import label
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import plotly.express as px
import numpy as np

def app():
    plt.style.use('ggplot')
    plt.style.use('dark_background')
    
    def mapa():
        if unidad == 'Número de embarcamientos':
            temporal = data.groupby('Código país').size().reset_index()
            temporal.columns = ['Código país', 'Embarcamientos']
            fig2 = px.choropleth(temporal, locations=temporal['Código país'], color='Embarcamientos',color_continuous_scale="Teal")
        elif unidad == 'Cantidad (Peso bruto en kg)':
            temporal = data.groupby('Código país').sum().reset_index()
            fig2 = px.choropleth(temporal, locations=temporal['Código país'], color='Cantidad (Peso bruto en kg)',color_continuous_scale="Blues")
        elif unidad == 'Cantidad (TEUS)':
            temporal1 = data.groupby('Código país').sum().reset_index()
            fig2 = px.choropleth(temporal1, locations=temporal1['Código país'], color='Cantidad (TEUS)',color_continuous_scale="bluered")
        elif unidad == 'Cantidad (FEUS)':
            temporal1 = data.groupby('Código país').sum().reset_index()
            fig2 = px.choropleth(temporal1, locations=temporal1['Código país'], color='Cantidad (TEUS)',color_continuous_scale="blugrn")
        else:
            temporal = data.groupby('Código país').sum().reset_index()
            fig2 = px.choropleth(temporal,locations=temporal['Código país'], color='Cantidad (Peso neto en kg)', color_continuous_scale="bluyl")
        fig2.update_coloraxes(showscale=False)
        c1.plotly_chart(fig2)

        

    def barras(columna, unidad):
        tabla = data.groupby(columna).sum().reset_index().sort_values(unidad, ascending = False).reset_index()[:10]
        fig = plt.figure()
        sns.barplot(y = columna, x = unidad , data = tabla, color =  'skyblue').set(xlabel=unidad, ylabel='')


        return fig

    

    @st.cache
    def leer_data():
        df = pd.read_csv('data/datos_dian_julio_2020.csv')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Producto'] = df['Descripción Capítulo'].str[0:40]

        return df


    with st.spinner('En proceso...'):
       df = leer_data()


    st.write('# Filtros')
    st.write('Información disponible desde: 2002/06/25 hasta: 2020/07/04')


    c1, c2, c3, c4 = st.columns(4)
    c1.write('### Rango de fechas')

    fecha_inicial = c1.date_input('Fecha de inicio', datetime.date(2020, 6, 1))
    fecha_final = c1.date_input('Fecha final', datetime.date(2020, 6, 30))
    c2.write('### Tipo de comercio')
    tipo_comercio = c2.radio( 'Tipo de comercio', ['Todos']+list(set(df['Tipo de transporte'])))
    c3.write('### Embarcamiento')
    origenes = c3.multiselect('País del embarcamiento', ['Seleccionar']+list(set(df['País exportador'])))
    origenes_ciu = c3.multiselect('Ciudad del embarcamiento', ['Seleccionar']+list(set(df['Ciudad de procedencia'])))
    #destinos = c3.multiselect('Destino del embarcamiento', ['Seleccionar', 'Colombia'])
    c4.write('### Producto')
    cap = c4.selectbox('Filtrar por capítulo', ['Seleccionar']+list(set(df['Descripción Capítulo'])))
    partida = c4.selectbox('Filtrar por subpartida', ['Seleccionar']+list(set(df['Descripción supbartida'])))
    seguir = c1.checkbox('Filtrar')
    st.write('--------------')

    if seguir:
        if tipo_comercio == 'Marítimo':
            unidad = st.radio(label = 'Radio buttons', options = ['Cantidad (TEUS)','Cantidad (FEUS)','Número de embarcamientos'])
            
            with st.spinner('En proceso...'):
                a = (df['Fecha']>pd.to_datetime(fecha_inicial))&(df['Fecha']<pd.to_datetime(fecha_final))
                if origenes == []:
                    b = df['Tipo de transporte']!= 'nada'
                else:
                    b = df['País exportador'].isin(origenes)
                if origenes_ciu == []:
                    c = df['Tipo de transporte']!= 'nada'
                else:
                    c = df['Ciudad de procedencia'].isin(origenes)
                if cap != 'Seleccionar':
                    d = df['Descripción Capítulo'] == cap
                else:
                    d = df['Tipo de transporte']!= 'nada'
                if partida != 'Seleccionar':
                    e = df['Descripción supbartida'] == partida
                else:
                    e = df['Tipo de transporte']!= 'nada'
                data = df[a&c&d&e].copy()
                data['Número de embarcamientos']= 1

            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            c1, c2 , c3= st.columns(3)
            c1.write('## Principales países exportadores')


            mapa()
            #totales = data.sum()
            c3,c4= st.columns(2)
            c3.write('### Total de embarcamientos')
            t1 = str(data['Número de embarcamientos'].sum())
            c4.write(f'### {t1}' )
            c3.write('### Total TEUS')
            t2 = str(round(df['Cantidad (TEUS)'].astype(float).sum(),2))
            c4.write(f'### {t2}')
            c3.write('### Total FEUS')
            t3 = str(round(df['Cantidad (FEUS)'].astype(float).sum(),2))
            c4.write(f'### {t3}')

            c1, c2= st.columns([3, 1])
            c1.write('## Principales puertos')
            c1.pyplot(barras('Ciudad de ingreso', unidad))

            c3, c4= st.columns([3, 1])
            c3, c4 = st.columns([3, 1])
            c3.write('## Principales orígenes')
            c3.pyplot(barras('Ciudad de procedencia', unidad))

            c4, c3 = st.columns([3, 1])
            c4.write('## Principales navieras')
            c4.pyplot(barras('Agente Naviero', unidad))

            c5, c6 = st.columns([3, 1])
            c5.write('## Principales importadores')
            c5.pyplot(barras('Empresa importador', unidad))

            c6,c7 = st.columns([3,1])
            c6.write('## Principales productos')
            c6.pyplot(barras('Producto', unidad))

            st.write(data.head(20))
        
        else:
            unidad = st.radio(label = 'Radio buttons', options = ['Cantidad (Peso bruto en kg)','Cantidad (Peso neto en kg)','Número de embarcamientos'])

            with st.spinner('En proceso...'):
                a = (df['Fecha']>pd.to_datetime(fecha_inicial))&(df['Fecha']<pd.to_datetime(fecha_final))

                if tipo_comercio == 'Todos':
                    b = df['Tipo de transporte']!= 'nada'
                else:
                    b = df['Tipo de transporte'] == tipo_comercio
                if origenes == []:
                    c = df['Tipo de transporte']!= 'nada'
                else:
                    c = df['País exportador'].isin(origenes)
                if origenes_ciu == []:
                    f = df['Tipo de transporte']!= 'nada'
                else:
                    f = df['Ciudad de procedencia'].isin(origenes_ciu)
                if cap != 'Seleccionar':
                    d = df['Descripción Capítulo'] == cap
                else:
                    d = df['Tipo de transporte']!= 'nada'
                if partida != 'Seleccionar':
                    e = df['Descripción supbartida'] == partida
                else:
                    e = df['Tipo de transporte']!= 'nada'
                data = df[a&b&c&f&d&e].copy()
                data['Número de embarcamientos']= 1

            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            c1,c2= st.columns(2)
            c1.write('## Principales países exportadores')


            mapa()
            #totales = data.sum()
            c3,c4= st.columns(2)
            c3.write('### Total de embarcamientos:')
            t1 = str(data['Número de embarcamientos'].sum())
            c4.write(f'### {t1}' )
            c3.write('### Total peso bruto en kg:')
            t2 = str(data['Cantidad (Peso bruto en kg)'].sum())
            c4.write(f'### {t2}')
            c3.write('### Total peso neto en kg:')
            t3 = str(data['Cantidad (Peso neto en kg)'].sum())
            c4.write(f'### {t3}')

            c1, c2= st.columns([3, 1])
            c1.write('## Principales destinos')
            c1.pyplot(barras('Ciudad de ingreso', unidad))

            c3, c4= st.columns([3, 1])
            c3, c4 = st.columns([3, 1])
            c3.write('## Principales orígenes')
            c3.pyplot(barras('Ciudad de procedencia', unidad))

            if tipo_comercio == 'Aéreo':
                c4, c3 = st.columns([3, 1])
                c4.write('## Principales aerolíneas')
                c4.pyplot(barras('Agente Naviero', unidad))

            else:
                c4, c3 = st.columns([3, 1])
                c4.write('## Principales empresas de transporte')
                c4.pyplot(barras('Agente Naviero', unidad))
            
            c5, c6 = st.columns([3, 1])
            c5.write('## Principales importadores')
            c5.pyplot(barras('Empresa importador', unidad))

            c6,c7 = st.columns([3,1])
            c6.write('## Principales productos')
            c6.pyplot(barras('Producto', unidad))

            if tipo_comercio == 'Todos':
                c2,c7 = st.columns([3,1])
                c2.write('## Principales tipos de transporte')
                c2.pyplot(barras('Tipo de transporte', unidad))
                st.write(data.head(20))
            else:
                st.write(data.head(20))




