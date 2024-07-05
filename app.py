import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")

# Load the HTML file
def read_html_file(filename):
    with open(filename, 'r') as f:
        return f.read()


# Stats definitions
df_stats_def = pd.read_csv('sources/stats_def.csv',sep=';')
df_stats_def_demo = df_stats_def[(df_stats_def['Catégorie'] == 'Démographie') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_acti = df_stats_def[(df_stats_def['Catégorie'] == 'Activité') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_qualif = df_stats_def[(df_stats_def['Catégorie'] == 'Qualification') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_secteur = df_stats_def[(df_stats_def['Catégorie'] == 'Secteur') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_log = df_stats_def[(df_stats_def['Catégorie'] == 'Logement') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_fam = df_stats_def[(df_stats_def['Catégorie'] == 'Famille') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_mob = df_stats_def[(df_stats_def['Catégorie'] == 'Mobilité') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_rev = df_stats_def[(df_stats_def['Catégorie'] == 'Revenus') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_niv_vie = df_stats_def[(df_stats_def['Catégorie'] == 'Niveau de vie') | (df_stats_def['Variable'] == 'Nom de la circonscription')]
df_stats_def_autres = df_stats_def[(df_stats_def['Catégorie'] == 'Autres') | (df_stats_def['Variable'] == 'Nom de la circonscription')]

    
# 1.Liste des départements
file_path = 'output/dataset_dpt_circo_bv_test.csv'
df = pd.read_csv(file_path,low_memory=False)
df.rename(columns={'codeDepartement': 'id_dep','nomDepartement': 'dep_name'}, inplace=True)
df['id_dep'] = df['id_dep'].astype(str)
df['id_circo'] = df['id_circo'].astype(str)
df['id_bv'] = df['id_bv'].astype(str)

df_dpt = df.drop(columns=['id_circo','libCirco','codeCommune','nomCommune','numeroBureauVote','codeBureauVote','id_bv','libBv']).drop_duplicates()
df_dpt['id_dep'] = df_dpt['id_dep'].astype(str)
df_dpt.sort_values(by='id_dep',inplace=True)
df_dpt['id_dep'] = df_dpt['id_dep'].astype(str)
df_dpt['dep_lib'] = df_dpt['id_dep'].str.cat(df_dpt['libDep'], sep = ' - ')

dpt = df_dpt['dep_lib'].drop_duplicates().sort_values()
dpt_selected = st.sidebar.selectbox('Sélection du département:', dpt)
# ID dpt
dpt_id_selected = dpt_selected.split(" - ")[0]

#dpt_id_selected = '14'

file_path_dpt_resultats = 'output/dpt/data/resultats_' + dpt_id_selected + '.csv'
dpt_resultats = pd.read_csv(file_path_dpt_resultats,low_memory=False)

# a. Résultats - Stats descriptives - DPT
dpt_resultats_overview = dpt_resultats[['libDepartement', 'Inscrits', 'Votants', '% Votants', 'Abstentions', '% Abstentions', 'Exprimés', '% Exprimés/inscrits', '% Exprimés/votants', 'Blancs', '% Blancs/inscrits', '% Blancs/votants', 'Nuls', '% Nuls/inscrits', '% Nuls/votants']]
dpt_resultats_overview = dpt_resultats_overview.drop_duplicates()

data_container = st.container()
with data_container:
    st.write("Département - Elections législatives:")
    st.dataframe(dpt_resultats_overview,hide_index=True)

# b. Résultats (top10) - DPT
dpt_resultats_details = dpt_resultats[['indicateur','valeur']]
dpt_resultats_details['id_candidat'] = dpt_resultats_details['indicateur'].str[-2:]
dpt_resultats_details['id_candidat'] = dpt_resultats_details['id_candidat'].str.strip()

dpt_resultats_details['indicateur'] = dpt_resultats_details['indicateur'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))
dpt_resultats_details['indicateur']= dpt_resultats_details['indicateur'].apply(lambda x: x[:-1] if isinstance(x, str) else x)

dpt_resultats_details = dpt_resultats_details.pivot(index ='id_candidat', columns='indicateur', values='valeur')
dpt_resultats_details = pd.DataFrame(dpt_resultats_details.to_records())
dpt_resultats_details["Voix"] = dpt_resultats_details["Voix"].fillna(0).astype(float).round().astype(int)
dpt_resultats_details = dpt_resultats_details.nlargest(10, 'Voix')
dpt_resultats_details = dpt_resultats_details[['Nuance candidat', 'Voix','% Voix/exprimés','% Voix/inscrits']]
dpt_resultats_details = dpt_resultats_details.dropna(axis=0, subset=['Nuance candidat'])

data_container2 = st.container()
with data_container2:
    st.write("Département - Résultats législatives (top10):")
    st.dataframe(dpt_resultats_details,hide_index=True)

    
# 2.Circonscriptions du département sélectionné

# a.Carte
#Read the HTML content from the file
html_content = read_html_file('output/circo/map/map_' + dpt_id_selected + '.html')
# Display the HTML content in Streamlit
map_container1 = st.container()

with map_container1:
    st.write("Circonscriptions:")
    st.components.v1.html(html_content,height=500)

# b.Stats des circonscriptions du département sélectionné
file_path_circo_stats = 'output/circo/data/stats_' + dpt_id_selected + '.csv'
df_stats_circo_selected = pd.read_csv(file_path_circo_stats,low_memory=False)

df_stats_circo_demo = df_stats_circo_selected[['Nom de la circonscription','Inscrit_22','pop_légal_19','pop_légal_13','tvar_pop','pop_pole_aav','pop_cour_aav','pop_horsaav','pop_urb','pop_rur_periu','pop_rur_non_periu','age_moyen','dec90','dec75','dec50','dec25','dec10']]
df_stats_circo_acti = df_stats_circo_selected[['Nom de la circonscription','actemp','actcho','inactret','inactetu','inactm14','inactaut','actemp_hom','actcho_hom','inactret_hom','inactetu_hom','inactm14_hom','inactaut_hom','actemp_fem','actcho_fem','inactret_fem','inactetu_fem','inactm14_fem','inactaut_fem']]
df_stats_circo_qualif = df_stats_circo_selected[['Nom de la circonscription','actdip_PEU','actdip_CAP','actdip_BAC','actdip_BAC2','actdip_BAC3','actdip_BAC5','actdip_BAC3P']]
df_stats_circo_secteur = df_stats_circo_selected[['Nom de la circonscription','act_agr','act_art','act_cad','act_int','act_emp','act_ouv','act_cho']]
df_stats_circo_log = df_stats_circo_selected[['Nom de la circonscription','log_res','log_sec','log_vac','proprio','locatai','gratuit','maison','ach90','mfuel']]
df_stats_circo_fam = df_stats_circo_selected[['Nom de la circonscription','men_seul','men_coupae','men_coupse','men_monop','men_sfam','men_seul_com','men_coupse_com','men_coupae_com','men_monop_com','men_complexe_com']]
df_stats_circo_mob = df_stats_circo_selected[['Nom de la circonscription','iranr_com','iranr_dep','iranr_fra','iranr_etr','mobresid','ilt_com','ilt_dep','ilt_fra','ilt_etr','mobtrav','modtrans_aucun','modtrans_pied','modtrans_velo','modtrans_moto','modtrans_voit','modtrans_commun']]
df_stats_circo_niv_vie = df_stats_circo_selected[['Nom de la circonscription','tx_pauvrete60_diff','nivvie_median_diff','part_pauvres_diff','part_modestes_diff','part_medians_diff','part_plutot_aises_diff','part_aises_diff','D1_diff','D9_diff','rpt_D9_D1_diff','tx_pauvrete60_diff_trageRF1','tx_pauvrete60_diff_trageRF2','tx_pauvrete60_diff_trageRF3','tx_pauvrete60_diff_trageRF4','tx_pauvrete60_diff_trageRF5','tx_pauvrete60_diff_trageRF6']]
df_stats_circo_rev = df_stats_circo_selected[['Nom de la circonscription','PACT','PPEN','PPAT','PPSOC','PIMPOT']]
df_stats_circo_autres = df_stats_circo_selected[['Nom de la circonscription','acc_ecole','acc_college','acc_lycee','acc_medecin','acc_dentiste','acc_pharmacie','part_eloig']]

with st.expander(:red[Statistiques descriptives:],icon=":material/analytics:"):

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["Démographie", "Activité/inactivité:", "Qualification","Secteurs","Logement","Famille","Mobilité","Niveau de vie","Revenus","Autres" ])
    
    with tab1:
        st.dataframe(df_stats_circo_demo,hide_index=True)
        st.dataframe(df_stats_def_demo,hide_index=True)
    with tab2:  
        st.dataframe(df_stats_circo_acti,hide_index=True)
        st.dataframe(df_stats_def_acti,hide_index=True)
    with tab3: 
        st.dataframe(df_stats_circo_qualif,hide_index=True)
        st.dataframe(df_stats_def_qualif,hide_index=True)
    with tab4:
        st.dataframe(df_stats_circo_secteur,hide_index=True)
        st.dataframe(df_stats_def_secteur,hide_index=True)
    with tab5:  
        st.dataframe(df_stats_circo_log,hide_index=True)
        st.dataframe(df_stats_def_log,hide_index=True)
    with tab6:
        st.dataframe(df_stats_circo_fam,hide_index=True)
        st.dataframe(df_stats_def_fam,hide_index=True)
    with tab7: 
        st.dataframe(df_stats_circo_mob,hide_index=True)
        st.dataframe(df_stats_def_mob,hide_index=True)
    with tab8: 
        st.dataframe(df_stats_circo_niv_vie,hide_index=True)
        st.dataframe(df_stats_def_niv_vie,hide_index=True)
    with tab9:  
        st.dataframe(df_stats_circo_rev,hide_index=True)
        st.dataframe(df_stats_def_rev,hide_index=True)
    with tab10:
        st.dataframe(df_stats_circo_autres,hide_index=True)
        st.dataframe(df_stats_def_autres,hide_index=True)

# c.Résultats des circonscriptions du département sélectionné
file_path_circo_resultats = 'output/circo/data/resultats_' + dpt_id_selected + '.csv'
df_resultats_circo_selected = pd.read_csv(file_path_circo_resultats,low_memory=False)

    # i. Stats descriptives
circo_resultats_overview = df_resultats_circo_selected[['libCirco', 'Inscrits', 'Votants', '% Votants', 'Abstentions', '% Abstentions', 'Exprimés', '% Exprimés/inscrits', '% Exprimés/votants', 'Blancs', '% Blancs/inscrits', '% Blancs/votants', 'Nuls', '% Nuls/inscrits', '% Nuls/votants']]
circo_resultats_overview = circo_resultats_overview.drop_duplicates()
data_container3 = st.container()
with data_container3:
    st.write("Circonscriptions - Elections législatives:")
    st.dataframe(circo_resultats_overview,hide_index=True)

    # ii. Résultats (top10)
circo_resultats_details = df_resultats_circo_selected[['id_circo','libCirco','indicateur','valeur']]
circo_resultats_details['id_candidat'] = circo_resultats_details['indicateur'].str[-2:]
circo_resultats_details['id_candidat'] = circo_resultats_details['id_candidat'].str.strip()

circo_resultats_details['indicateur'] = circo_resultats_details['indicateur'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))
circo_resultats_details['indicateur']= circo_resultats_details['indicateur'].apply(lambda x: x[:-1] if isinstance(x, str) else x)

#circo_resultats_details

with st.expander("Circonscriptions - Résultats législatives (top10):"):
    groups = circo_resultats_details.groupby('id_circo')
    for name,group in groups:
        tmp_details_circo = group.pivot(index = ['id_circo','id_candidat'], columns='indicateur', values='valeur')
        tmp_details_circo = pd.DataFrame(tmp_details_circo.to_records())
        tmp_details_circo["Voix"] = tmp_details_circo["Voix"].fillna(0).astype(float).round().astype(int)
        tmp_details_circo = tmp_details_circo.nlargest(10, 'Voix')
        tmp_details_circo = tmp_details_circo[['Nuance candidat', 'Voix','% Voix/exprimés','% Voix/inscrits']]
        tmp_details_circo = tmp_details_circo.dropna(axis=0, subset=['Nuance candidat'])
        st.write(name)
        st.dataframe(tmp_details_circo,hide_index=True)   

# d.Liste des circonscriptions du département sélectionné
df_circo = df[df['id_dep'] == dpt_id_selected].drop(columns=['codeCommune','nomCommune','numeroBureauVote','codeBureauVote','id_bv','libBv']).drop_duplicates()
df_circo['id_circo'] = df_circo['id_circo'].astype(str)
df_circo.sort_values(by='id_circo',inplace=True)
df_circo['circo_lib'] = df_circo['id_circo'].str.cat(df_circo['libCirco'], sep = ' - ')

circo =  df_circo['circo_lib'].drop_duplicates().sort_values()
circo_selected = st.sidebar.selectbox('Sélection de la circonscription:', circo)
# ID circo
circo_id_selected = str(circo_selected).split(" - ")[0]

# 3.Bureaux de votes de la circonscription sélectionnée

# a.Carte
# Read the HTML content from the file
html_content2 = read_html_file('output/bv/map/map_' + circo_id_selected + '.html')
# Display the HTML content in Streamlit
map_container2 = st.container()
with map_container2:
    st.write("Bureaux de vote:")
    st.components.v1.html(html_content2,height=500)

# b.Résultats des circonscriptions du département sélectionné
file_path_bv_resultats = 'output/bv/data/resultats_' + circo_id_selected + '.csv'
df_resultats_bv_selected = pd.read_csv(file_path_bv_resultats,low_memory=False)

    # i. Stats descriptives
bv_resultats_overview = df_resultats_bv_selected[['libBv', 'Inscrits', 'Votants', '% Votants', 'Abstentions', '% Abstentions', 'Exprimés', '% Exprimés/inscrits', '% Exprimés/votants', 'Blancs', '% Blancs/inscrits', '% Blancs/votants', 'Nuls', '% Nuls/inscrits', '% Nuls/votants']]
bv_resultats_overview = bv_resultats_overview.drop_duplicates()
data_container3 = st.container()
with data_container3:
    st.write("Bureaux de votes - Elections législatives:")
    st.dataframe(bv_resultats_overview,hide_index=True)

    # ii. Résultats (top10)
bv_resultats_details = df_resultats_bv_selected[['id_bv','libBv','indicateur','valeur']]
bv_resultats_details['id_candidat'] = bv_resultats_details['indicateur'].str[-2:]
bv_resultats_details['id_candidat'] = bv_resultats_details['id_candidat'].str.strip()

bv_resultats_details['indicateur'] = bv_resultats_details['indicateur'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))
bv_resultats_details['indicateur']= bv_resultats_details['indicateur'].apply(lambda x: x[:-1] if isinstance(x, str) else x)

bv =  bv_resultats_details['libBv'].drop_duplicates().sort_values()
bv_selected = st.sidebar.selectbox('Sélection du bureau de vote:', bv)
# ID BV
bv_id_selected = bv_selected

df_bv = bv_resultats_details[bv_resultats_details['libBv'] == bv_id_selected]

tmp_details_bv = df_bv.pivot(index = ['libBv','id_candidat'], columns='indicateur', values='valeur')
tmp_details_bv = pd.DataFrame(tmp_details_bv.to_records())
tmp_details_bv["Voix"] = tmp_details_bv["Voix"].fillna(0).astype(float).round().astype(int)
tmp_details_bv = tmp_details_bv.nlargest(10, 'Voix')
tmp_details_bv = tmp_details_bv[['libBv','Nuance candidat', 'Voix','% Voix/exprimés','% Voix/inscrits']]
tmp_details_bv = tmp_details_bv.dropna(axis=0, subset=['Nuance candidat'])

data_container4 = st.container()
with data_container4:
    st.write("Bureau de vote sélectionné - Résultats législatives (top10):")
    st.dataframe(tmp_details_bv,hide_index=True)