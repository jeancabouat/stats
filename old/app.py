import streamlit as st
import pandas as pd


# 1.Liste des départements
file_path = 'sources/dataset_dpt_circo_bv_test.csv'
df = pd.read_csv(file_path,low_memory=False)
df.rename(columns={'codeDepartement': 'id_dep','nomDepartement': 'dep_name'}, inplace=True)
df['id_dep'] = df['id_dep'].astype(str)
df['id_circo'] = df['id_circo'].astype(str)
df['id_bv'] = df['id_bv'].astype(str)

df_dpt = df.drop(columns=['id_circo','nomCirconscription','codeCommune','nomCommune','numeroBureauVote','codeBureauVote','id_bv']).drop_duplicates()
df_dpt['id_dep'] = df_dpt['id_dep'].astype(str)
df_dpt.sort_values(by='id_dep',inplace=True)
df_dpt['id_dep'] = df_dpt['id_dep'].astype(str)
df_dpt['dep_lib'] = df_dpt['id_dep'].str.cat(df_dpt['dep_name'], sep = ' - ')

dpt = df_dpt['dep_lib'].drop_duplicates().sort_values()
dpt_selected = st.sidebar.selectbox('Sélection du département:', dpt)
# ID dpt
dpt_id_selected = dpt_selected.split(" - ")[0]


# 2.Liste des circonscriptions du département sélectionné
df_circo = df[df['id_dep'] == dpt_id_selected].drop(columns=['codeCommune','nomCommune','numeroBureauVote','codeBureauVote','id_bv']).drop_duplicates()
df_circo['id_circo'] = df_circo['id_circo'].astype(str)
df_circo.sort_values(by='id_circo',inplace=True)
df_circo['circo_lib'] = df_circo['id_circo'].str.cat(df_circo['nomCirconscription'], sep = ' - ')

circo =  df_circo['circo_lib'].drop_duplicates().sort_values()
circo_selected = st.sidebar.selectbox('Sélection de la circonscription:', circo)
# ID circo
circo_id_selected = str(circo_selected).split(" - ")[0]


# 3.Liste des bureaux de vote de la circonscription sélectionnée
df_bv = df[df['id_circo'] == circo_id_selected].drop_duplicates()
df_bv['codeBureauVote'] = df_bv['codeBureauVote'].astype(str)
df_bv.sort_values(by='codeBureauVote',inplace=True)
df_bv['bv_lib'] = df_bv['codeBureauVote'].str.cat(df_bv['nomCommune'], sep = ' - ')

bv =  df_bv['bv_lib'].drop_duplicates().sort_values()
bv_selected = st.sidebar.selectbox('Sélection du bureau de vote:', bv)
# ID bv
bv_id_selected = str(bv_selected).split(" - ")[0]


# Load the HTML file
def read_html_file(filename):
    with open(filename, 'r') as f:
        return f.read()


# Read the HTML content from the file
html_content = read_html_file('sources/circo/map/map_' + circo_id_selected + '.html')
# Display the HTML content in Streamlit
st.components.v1.html(html_content, width=700, height=500)

st.write("")

df_circo_selected = pd.read_csv('sources/circo/data/data_' + circo_id_selected + '.csv')
df_circo_selected = df_circo_selected.set_index(df_circo_selected.columns[0]).T
st.dataframe(df_circo_selected)


# Read the HTML content from the file
html_content = read_html_file('sources/bv/map/map_' + bv_id_selected + '.html')
# Display the HTML content in Streamlit
st.components.v1.html(html_content, width=700, height=500)


df_bv_selected = pd.read_csv('sources/bv/data/data_' + bv_id_selected + '.csv')
df_bv_selected = df_bv_selected.set_index(df_bv_selected.columns[0]).T
st.dataframe(df_bv_selected)
