import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(page_title="Rhino Inventarios", page_icon="🦏")
st.title("Actualizador de Inventario Página Rhino")

st.markdown("Carga de Archivos")

# Subir archivos
file1 = st.file_uploader(
    "Arrastra el archivo CSV exportado de la página Rhino", type=['csv'])
file2 = st.file_uploader(
    "Arrastra el archivo archivo excel del inventario diario", type=['xlsx', 'xls'], key="excel_rhino")

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

    with st.expander("Ver Resultado"):
        st.dataframe(df1[df1['¿En inventario?'] == 0]
                     [['SKU', '¿En inventario?']])

    # Creación y codificación de archivo nuevo
    csv_data = df1.to_csv(index=False, encoding='utf-8-sig')
    csv_resultado = csv_data.encode('utf-8-sig')

    # Descargar Archivo nuevo
    st.download_button(
        label='Descargar Inventario Rhino Actualizado',
        data=csv_resultado,
        file_name='wc-product-ACTUALIZADO.csv',
    )

st.title("Actualizador de Inventario Básculas Electrónicas")

st.markdown("Carga de Archivos")

# Subir archivos
file3 = st.file_uploader(
    "Arrastra el archivo CSV exportado de la página Básculas electrónicas", type=['csv'])
file4 = st.file_uploader(
    "Arrastra el archivo archivo excel del inventario diario", type=['xlsx', 'xls'], key="excel_basculas")

if file3 and file4:
    # leer datos
    df3 = pd.read_csv(file3)
    df4 = pd.read_excel(file4)
    # Procesamiento

    # Extraer skus en Backorder
    df_backorder = df4[df4['TIPO DE ABASTO'] == 'BACKORDER']
    skus_backorder = df_backorder['MODELO']

    # Devolver todo el inventario a 999
    tiene_contenido = df3['Type'].notna() & (
        df3['Type'].astype(str).str.strip() != '')
    df3.loc[tiene_contenido, 'Variant Inventory Qty'] = 999

    # Cambiar a 0 los skus en backorder
    en_backorder_y_con_contenido = df3['Type'].isin(
        skus_backorder) & tiene_contenido
    df3.loc[en_backorder_y_con_contenido, 'Variant Inventory Qty'] = 0

    # Resumen para el usuario
    st.success("Archivos procesados correctamente")
    st.balloons()
    col1, col2 = st.columns(2)
    col1.metric("Encontrados en Backorder", len(skus_backorder))

    with st.expander("Ver Resultado"):
        st.dataframe(df3[df3['Variant Inventory Qty'] == 0]
                     [['Type', 'Variant Inventory Qty']])

    # Creación y codificación de archivo nuevo
    csv_data = df3.to_csv(index=False, encoding='utf-8-sig')
    csv_resultado = csv_data.encode('utf-8-sig')

    # Descargar Archivo nuevo
    st.download_button(
        label='Descargar Inventario Básculas Actualizado',
        data=csv_resultado,
        file_name='inventory_export_Actualizado.csv',
    )

st.title("Soy uno con la fuerza, la fuerza está conmigo...")
