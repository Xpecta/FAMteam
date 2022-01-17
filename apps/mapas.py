import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import plotly.express as px

def app():
    plt.style.use('ggplot')
    plt.style.use('dark_background')
    
    def mapa():
        if unidad == 'Número de embarcamientos':
            temporal = data.groupby('Código país').size().reset_index()
            temporal.columns = ['Código país', 'Embarcamientos']
            fig2 = px.choropleth(temporal, locations=temporal['Código país'], color='Embarcamientos',color_continuous_scale="Teal")
        elif unidad == 'Peso bruto en Kg':
            temporal = data.groupby('Código país').sum().reset_index()
            fig2 = px.choropleth(temporal, locations=temporal['Código país'], color='Cantidad (Peso bruto en kg)',color_continuous_scale="Blues")
        else:
            temporal = data.groupby('Código país').sum().reset_index()
            fig2 = px.choropleth(temporal,locations=temporal['Código país'], color='Cantidad (Peso neto en kg)', color_continuous_scale="Blues")
        fig2.update_coloraxes(showscale=False)
        c1.plotly_chart(fig2)

    def barras(columna, unidad):
        tabla = data.groupby(columna).sum().reset_index().sort_values(unidad, ascending = False).reset_index()[:10]
        fig = plt.figure()
        sns.barplot(y = columna, x = unidad , data = tabla, color =  'skyblue')
        return fig

    @st.cache
    def leer_data():
        df = pd.read_csv('data/datos_dian_julio_2020.csv')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df

    with st.spinner('En proseso...'):
       df = leer_data()


    st.write('# Filtros')

    c1, c2, c3, c4 = st.columns(4)
    c1.write('### Rango de fechas')
    fecha_inicial = c1.date_input('Fecha de inicio', datetime.date(2020, 6, 1))
    fecha_final = c1.date_input('Fecha final', datetime.date(2020, 6, 30))
    c2.write('### Tipo de comercio')
    tipo_comercio = c2.radio( 'Tipo de comercio', ['Todos']+list(set(df['Tipo de transporte'])))
    c3.write('### Embarcamiento')
    origenes = c3.multiselect('Origen del embarcamiento', ['Seleccionar']+list(set(df['País exportador'])))
    detinos = c3.multiselect('Destino del embarcamiento', ['Seleccionar', 'Colombia'])
    c4.write('### Producto')
    cap = c4.selectbox('Filtrar por capítulo', ['Seleccionar']+list(set(df['Descripción Capítulo'])))
    partida = c4.selectbox('Filtrar por subpartida', ['Seleccionar']+list(set(df['Descripción supbartida'])))
    seguir = c1.checkbox('Filtrar')
    st.write('--------------')

    if seguir:
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
            if cap != 'Seleccionar':
                d = df['Descripción Capítulo'] == cap
            else:
                d = df['Tipo de transporte']!= 'nada'
            if partida != 'Seleccionar':
                e = df['Descripción supbartida'] == partida
            else:
                e = df['Tipo de transporte']!= 'nada'
            data = df[a&b&c&d&e].copy()
            data['Número de embarcamientos']= 1

        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        c1, c2 , c3= st.columns(3)
        c1.write('## Principales países exportadores')

        mapa()
        #totales = data.sum()

        c3.write('### Total de embarcamientos')
        t1 = str(data['Número de embarcamientos'].sum())
        c3.write(f'# {t1}' )
        c3.write('### Total peso bruto en kg')
        t2 = str(data['Cantidad (Peso bruto en kg)'].sum())
        c3.write(f'# {t2}')
        c3.write('### Total peso neto en kg')
        t3 = str(data['Cantidad (Peso neto en kg)'].sum())
        c3.write(f'# {t3}')

        c1, c2 = st.columns(2)

        c1.write('## Principales navieras')
        c1.pyplot(barras('Agente Naviero', unidad))
        c2.write('## Principales productos')
        c2.pyplot(barras('Descripción Capítulo', unidad))
        c2.write('## Principales tipos de transporte')
        c2.pyplot(barras('Tipo de transporte', unidad))
        st.write(data.head(20))






    def mapas():
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
        fig2 = px.choropleth(df,
                            locations=df['CODE'],
                            color='GDP (BILLIONS)',
                            color_continuous_scale="Viridis")

        fig2.update_layout(width=8,height=8)
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(fig2, width=8,height=8)

        #, width=800,height=500)
        fig = go.Figure(data=go.Choropleth(
            locations = df['CODE'],
            z = df['GDP (BILLIONS)'],
            text = df['COUNTRY'],
            colorscale = 'Blues',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
        #    colorbar_tickprefix = '$',
        #    colorbar_title = 'GDP<br>Billions US$',
        ))

        fig.update_layout(
            width=800,
            height=800,
            coloraxis_showscale=False,
        #    showscale=False,
            title_text='2014 Global GDP',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )

        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, width=800,height=800)
        st.write(df)
        paises = pd.read_csv('../workspace/data/paises.csv')
    def plotear_globo():
        fig = go.Figure()

        for i, row in paises.iterrows():
            slat = row['Lat']
            dlat = 4
            slon = row['Lon']
            dlon = -72

            fig.add_trace(go.Scattergeo(
                                lat = [slat,dlat],
                                lon = [slon, dlon],
                                mode = 'lines',
                                line = dict(width = row['Importaciones']/10000, color="blue")
                                ))

        fig.update_layout(title_text="Connection Map Depicting Flights from Brazil to All Other Countries (Orthographic Projection)",
                          height=500, width=500,
                          margin={"t":0,"b":0,"l":0, "r":0, "pad":0},
                          showlegend=False,
                          geo= dict(projection_type = 'orthographic', showland = True, landcolor = 'grey',countrycolor = 'black'))
        st.plotly_chart(fig)
    def plotear_mundo():
        fig = go.Figure()
        for i, row in paises.iterrows():
            slat = row['Lat']
            slon = row['Lon']

            fig.add_trace(go.Scattergeo(
                                lat = [slat, 4],
                                lon = [slon, -72],
                                mode = 'lines',
                                line = dict(width = row['Importaciones']/10000, color="blue")
                                ))

        fig.update_layout(title_text="Importaciones de Colombia diciembre 2016",
                          height=500, width=500,
                          margin={"t":0,"b":0,"l":0, "r":0, "pad":0},
                          showlegend=False,
                          geo= dict( showland = True, landcolor = 'grey',countrycolor = 'black'))
        st.plotly_chart(fig)
    def todaviano():
        plotear_mundo()
        columnas_input = ['SUBPARTIDA ARANCELARIA_C59','NOMBRE EXPORTADOR O PROVEEDOR EN EL EXTERIOR_C46', 'RAZÓN SOCIAL_C11']
        data = pd.read_csv('datos Dian limpiados Junio 2016.csv')
        filtros = [ 'RAZÓN SOCIAL IMPORTADOR', 'PROVEEDOR EN EL EXTERIOR', 'PAIS PROCEDENCIA','Descripción subpartida']
        columna = c1.radio('Seleccione por cual opción buscar', filtros )
        nombre_filtro = 'Seleccione '+ columna

        opciones = ['Seleccionar..']+list(data[columna].unique())
        filtro  = st.selectbox(nombre_filtro, opciones, 0)
        if opciones != 'Seleccionar..':
            info = data[data[columna]== filtro]
