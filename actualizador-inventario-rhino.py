import pandas as pd
import streamlit as st

st.set_page_config(page_title="Rhino Inventarios", page_icon="🦏")
st.title("Actualizador de Inventario")

st.markdown("Carga de Archivos")

# Subir archivos
file1 = st.file_uploader(
    "Arrastra el archivo CSV exportado de la página Rhino", type=['csv'])
file2 = st.file_uploader(
    "Arrastra el archivo archivo excel del inventario diario", type=['xlsx', 'xls'])

if file1 and file2:
    # leer datos
    df1 = pd.read_csv(file1)
    df2 = pd.read_excel(file2)
    # Procesamiento

    # Extraer skus en Backorder
    df_backorder = df2[df2['TIPO DE ABASTO'] == 'BACKORDER']
    skus_backorder = df_backorder['MODELO']
    # Devolver todo el inventario a 1
    df1['¿En inventario?'] = 1
    # Cambiar a 0 los skus en backorder
    df1.loc[df1['SKU'].isin(skus_backorder), '¿En inventario?'] = 0

    # Resumen para el usuario
    st.success("Archivos procesados correctamente")
    st.balloons()
    col1, col2 = st.columns(2)
    col1.metric("Encontrados en Backorder", len(skus_backorder))

    with st.expander("Ver lista de SKUs modificados"):
        st.dataframe(df1[['SKU']].head(len(skus_backorder)))

    # Creación y codificación de archivo nuevo
    csv_data = df1.to_csv(index=False, encoding='utf-8-sig')
    csv_resultado = csv_data.encode('utf-8-sig')

    # Descargar Archivo nuevo
    st.download_button(
        label='Descargar Inventario Actualizado',
        data=csv_resultado,
        file_name='wc-product-ACTUALIZADO.csv',
    )

    st.markdown('Que la fuerza los acompañe')
