import streamlit as st
import pandas as pd
import altair as alt
import datetime
import graphviz as graphviz
import pm4py
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.algo.filtering.log.attributes import attributes_filter    
from pm4py.visualization.dfg import visualizer as dfg_visualizer
import seaborn as sns
import matplotlib.pyplot as plt


st.beta_set_page_config(
    page_title="DATAminingJUD",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    )

@st.cache(allow_output_mutation=True)
def get_dataset():
  df = pd.read_csv("dataset.csv", sep=",",parse_dates=["movimentoDataHora","dataAjuizamentoOK"])
  df.columns = ['org:siglaTribunal', 'case:concept:name', 'org:numero', 'org:dataAjuizamento',
        'org:orgaoJulgador_nomeOrgao', 'time:timestamp', 'concept:name',
        'tipoResponsavelMovimento','org:codigoClasse','org:Classe','org:orgaoJulgador_codigoOrgao']
  df.sort_values(by=['time:timestamp'], inplace=True)

  return df


@st.cache(allow_output_mutation=True)
def get_log(df):
  print("get_log")
  #df = get_dataset()
  from pm4py.objects.conversion.log import converter as log_converter
  
  log_x = log_converter.apply(df)
  return log_x

@st.cache(allow_output_mutation=True)
def get_opcoes(df):
  list_tribs = list(df["org:siglaTribunal"].unique())
  list_tribs.sort()

  list_ojs = list(df["org:orgaoJulgador_nomeOrgao"].unique())
  list_ojs.sort()
  list_ojs_cod = list(df["org:orgaoJulgador_codigoOrgao"].unique())
  list_ojs_cod.sort()

  list_classes = list(df["org:Classe"].unique())
  list_classes.sort()
  list_classes_cod = list(df["org:codigoClasse"].unique())
  list_classes_cod.sort()
  
  return list_tribs, list_ojs, list_classes, list_ojs_cod, list_classes_cod
  

df = get_dataset()
list_tribs, list_ojs, list_classes, list_ojs_cod, list_classes_cod = get_opcoes(df)
log = get_log(df)

def render_svg(svg,width, height):
  import base64
  b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
  html = f'<img  width="{width}" height="{height}" src="data:image/svg+xml;base64,{b64}"/>'
  return html

def filtra_classe(classe):
  #list_classes = list(df[df['org:siglaTribunal'] == tribunal]['org:Classe'].unique())
  #list_classes.sort()
  list_ojs = list(df[df['org:Classe'] == classe]['org:orgaoJulgador_nomeOrgao'].unique())
  list_ojs.sort()
  return list_ojs


def filtra_tribunal(tribunal):
  df_tribunal=df[df['org:siglaTribunal'] == tribunal]
  list_classes = list(df_tribunal['org:Classe'].unique())
  list_classes.sort()
  list_classes_cod = list(df_tribunal['org:codigoClasse'].unique())
  list_classes_cod.sort()
  list_ojs = list(df_tribunal['org:orgaoJulgador_nomeOrgao'].unique())
  list_ojs.sort()
  list_ojs_cod = list(df_tribunal['org:orgaoJulgador_codigoOrgao'].unique())
  list_ojs_cod.sort()
  return list_ojs, list_classes, list_ojs_cod, list_classes_cod



#pagina_slider_data1 = st.sidebar.slider("2When do you start?",value=datetime.datetime(2020, 1, 1, 9, 30), format="MM/DD/YY - hh:mm")
with st.sidebar:

    st.write('<center><a href="https://storage.googleapis.com/ueizejud/index.html"><img width="150" src="https://storage.googleapis.com/ueizejud/publica/logo.png" /></a></center>',  unsafe_allow_html=True)
    #st.write("[![](https://storage.googleapis.com/ueizejud/publica/logo.png)](https://storage.googleapis.com/ueizejud/index.html)")
    #st.image("https://storage.googleapis.com/ueizejud/publica/logo.png",width=20, use_column_width=True)
    #st.sidebar.title("DATAminingJUD")
    
    sb_1_trib = st.selectbox("Tribunal", list_tribs, 2)
    if sb_1_trib:
      list_ojs, list_classes, list_ojs_cod, list_classes_cod = filtra_tribunal(sb_1_trib)
    sb_1_classes = st.selectbox("Classe", list_classes, 2)
    sb_1_OJ = st.selectbox("Órgão Julgador 1", list_ojs, 0 )
    sb_2_OJ = st.selectbox("Órgão Julgador 2", list_ojs, 1)

    rd_metrica =st.radio("Métrica",('Frequência', 'Tempo'))



tracefilter_log_pos = log
if sb_1_trib:
  tracefilter_log_pos =  attributes_filter.apply(tracefilter_log_pos, 
                                            sb_1_trib, 
                                          parameters={
                                              #attributes_filter.Parameters.CASE_ID_KEY: 'case:concept:name',
                                              attributes_filter.Parameters.ATTRIBUTE_KEY: "org:siglaTribunal",
                                              attributes_filter.Parameters.POSITIVE: True
                                              }
                                          )
print("trib",sb_1_trib,len(tracefilter_log_pos))
if sb_1_classes:
  tracefilter_log_pos =  attributes_filter.apply(tracefilter_log_pos, 
                                            sb_1_classes, 
                                          parameters={
                                              #attributes_filter.Parameters.CASE_ID_KEY: 'case:concept:name',
                                              attributes_filter.Parameters.ATTRIBUTE_KEY: "org:Classe",
                                              attributes_filter.Parameters.POSITIVE: True
                                              }
                                          )
print("classes",sb_1_classes,len(tracefilter_log_pos))
if sb_1_OJ:
  tracefilter_log_pos_oj1 =  attributes_filter.apply(tracefilter_log_pos, 
                                            sb_1_OJ, 
                                          parameters={
                                              #attributes_filter.Parameters.CASE_ID_KEY: 'case:concept:name',
                                              attributes_filter.Parameters.ATTRIBUTE_KEY: "org:orgaoJulgador_nomeOrgao",
                                              attributes_filter.Parameters.POSITIVE: True
                                              }
                                          )
  print("oj1",sb_1_OJ,len(tracefilter_log_pos_oj1))

if sb_2_OJ:
  tracefilter_log_pos_oj2 =  attributes_filter.apply(tracefilter_log_pos, 
                                            sb_2_OJ, 
                                          parameters={
                                              attributes_filter.Parameters.CASE_ID_KEY: 'case:concept:name',
                                              attributes_filter.Parameters.ATTRIBUTE_KEY: "org:orgaoJulgador_nomeOrgao",
                                              attributes_filter.Parameters.POSITIVE: True
                                              }
                                          )
  print("oj2",sb_2_OJ,len(tracefilter_log_pos_oj2))


print("1:",len(tracefilter_log_pos_oj1))    
print("2:",len(tracefilter_log_pos_oj2))

parameters = {dfg_visualization.Variants.PERFORMANCE.value.Parameters.FORMAT: "svg"}
#gviz = dfg_visualization.apply(dfg, log=tracefilter_log_pos, variant=dfg_visualization.Variants.PERFORMANCE, parameters=parameters)
if rd_metrica=="Frequência":
  dfg_metrica = dfg_visualization.Variants.FREQUENCY
  disc_metrica = dfg_discovery.Variants.FREQUENCY
else:
  dfg_metrica = dfg_visualization.Variants.PERFORMANCE
  disc_metrica = dfg_discovery.Variants.PERFORMANCE

dfg_oj1 = dfg_discovery.apply(tracefilter_log_pos_oj1, variant=disc_metrica)
dfg_oj2 = dfg_discovery.apply(tracefilter_log_pos_oj2, variant=disc_metrica)



#activities_freq = dict(df["concept:name"].value_counts())

#gviz = dfg_visualizer.apply(dfg, variant=dfg_visualizer.Variants.FREQUENCY, activities_count=activities_freq, parameters={"format": "svg"})
#gviz_perf = dfg_visualizer.apply(performance_dfg, variant=dfg_visualizer.Variants.PERFORMANCE, activities_count=activities_freq, parameters={"format": "svg"})

st.header(f"Órgão Julgador 1 - {sb_1_OJ}")
with st.beta_expander("Ajuda"):        
  st.write("Trib: "+sb_1_trib) 
  st.write("Classes: "+sb_1_classes)
  st.write("Órgão: "+sb_1_OJ)
  st.write("")
  st.write("Os movimentos estão no seguinte formato:")
  st.write("* CódigoNacionalCNJ:Descrição do Movimento")
  st.write("")
  st.write('Quando a métrica selecionada é o "Tempo" são utilizadas as seguintes unidades:' )
  st.write('* D = Days/Dias' )
  st.write('* MO = Months/Meses' )
  st.write('* Y = Years/Anos' )
  st.write('' )
  st.write('Ex: 5D = 5 Dias, 2Y = 2 anos.' )
    
st.write("")   
sl_grafo_oj1 = st.empty()
with st.spinner('Só mais 1 segundo...'):
  
  gviz_oj1 = dfg_visualization.apply(dfg_oj1, log=tracefilter_log_pos_oj1, variant=dfg_metrica, parameters=parameters)
  html = render_svg(gviz_oj1.pipe().decode('utf-8'), 1200, 500)
  sl_grafo_oj1.write(html, unsafe_allow_html=True)

    
st.header(f"Órgão Julgador 2 - {sb_2_OJ}")
with st.beta_expander("Ajuda"):        
  st.write("Trib: "+sb_1_trib) 
  st.write("Classes: "+sb_1_classes)
  st.write("Órgão: "+sb_2_OJ)
  st.write("")
  st.write("Os movimentos estão no seguinte formato:")
  st.write("* CódigoNacionalCNJ:Descrição do Movimento")
  st.write("")
  st.write('Quando a métrica selecionada é o "Tempo" são utilizadas as seguintes unidades:' )
  st.write('* D = Days/Dias' )
  st.write('* MO = Months/Meses' )
  st.write('* Y = Years/Anos' )
  st.write('' )
  st.write('Ex: 5D = 5 Dias, 2Y = 2 anos.' )
    
st.write("")   
sl_grafo_oj2 = st.empty()
with st.spinner('Só mais 1 segundo...'):
  gviz_oj2 = dfg_visualization.apply(dfg_oj2, log=tracefilter_log_pos_oj2, variant=dfg_metrica, parameters=parameters)
  html = render_svg(gviz_oj2.pipe().decode('utf-8'), 1200, 500)
  sl_grafo_oj2.write(html, unsafe_allow_html=True)



def diferenca_metricas(dfg1, dfg2):
    resultado = []
    #Cria conjunto com transições dos dois dfgs
    set_transicoes = set([t for t in dfg1])
    set_transicoes.update([t for t in dfg2])
    #percorre transicoes obtendo diferenca na metrica
    for t in set_transicoes:
        metrica1 = 0
        metrica2 = 0
        if t in dfg1:     
            metrica1 = dfg1[t]
        if t in dfg2:     
            metrica2 = dfg2[t]
        diferenca = abs(metrica1 - metrica2)
        resultado.append([ t[0], t[1], diferenca ])        
    return resultado

df_trans = pd.DataFrame(diferenca_metricas(dfg_oj1,dfg_oj2))
df_trans.columns = ['origem','destino','metrica']

if rd_metrica=="Tempo":
  # converte a duração para dias
  df_trans['metrica'] = round(df_trans['metrica']/(24*3600*360), 2)

mapa_calor = df_trans.pivot('origem','destino','metrica')
plt.figure(figsize = (12,8))
ax = sns.heatmap(mapa_calor,annot=True, cbar_kws={'fraction' : 0.01}, # shrink colour bar
    cmap='OrRd', fmt="g")

if rd_metrica=="Tempo":
  st.header(f"Diferença nas Transições entre Órgãos Julgadores (unidade = anos)")
else:
  st.header(f"Diferença nas Transições entre Órgãos Julgadores")
  
st.pyplot(plt)


if rd_metrica=="Tempo":
  st.header(f"Maiores diferenças (unidade = anos)")
else:
  st.header(f"Maiores diferenças (unidade = frequência)")
st.write(df_trans.nlargest(10,'metrica'))