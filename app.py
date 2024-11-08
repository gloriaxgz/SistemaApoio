import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Carregar dados dos setores censitários (substitua o caminho pelo seu arquivo GeoJSON)
# Assumindo que o arquivo GeoJSON contém uma coluna chamada "renda_per_capita"
gdf = gpd.read_file("seu_arquivo_setores_censitarios.geojson")

# Configurações do Streamlit
st.title("Dashboard de Setores Censitários por Renda Per Capita")
st.write("Este dashboard exibe setores censitários com coloração de acordo com a renda per capita média.")

# Slider de seleção de renda per capita (em salários mínimos)
salario_minimo = 1320  # Atualize com o valor do salário mínimo atual
renda_minima = st.slider("Selecione a renda per capita mínima (em salários mínimos):", 0, 10, 3)
renda_minima_absoluta = renda_minima * salario_minimo

# Filtrar o GeoDataFrame de acordo com o valor selecionado
gdf_filtrado = gdf[gdf["renda_per_capita"] >= renda_minima_absoluta]

# Função para gerar o mapa
def criar_mapa(gdf_filtrado):
    # Centralizar o mapa na área de estudo
    mapa = folium.Map(location=[-22.3156, -49.0606], zoom_start=12)  # Coordenadas para Bauru, SP

    # Adicionar setores censitários filtrados com coloração
    for _, row in gdf_filtrado.iterrows():
        cor = "#3186cc"  # Escolha uma cor
        folium.GeoJson(
            row.geometry,
            style_function=lambda feature, color=cor: {
                "fillColor": color,
                "color": color,
                "weight": 1,
                "fillOpacity": 0.6 if feature['properties']['renda_per_capita'] >= renda_minima_absoluta else 0
            }
        ).add_to(mapa)
    
    return mapa

# Gerar o mapa com os dados filtrados
mapa = criar_mapa(gdf_filtrado)

# Mostrar o mapa no Streamlit
st_folium(mapa, width=700, height=500)

