![Logo Datamining JUD](https://storage.googleapis.com/ueizejud/publica/logo.png)

# Bem-vindo ao app DATAmining JUD!

DATAmining JUD é um aplicativo do Time 7 do Hackaton CNJ Inova - Desafio 1 : Tempo e Produtividade.

Vídeo de apresentação da solução: [https://youtu.be/lNBJYAE4hgc](https://youtu.be/lNBJYAE4hgc)

A aplicação está disponível para testes em [https://storage.googleapis.com/ueizejud/index.html](https://storage.googleapis.com/ueizejud/index.html).

Se quiser ir direto às instruções de instalação [clique aqui](#instalação).

## O problema

Unidades judiciárias semelhantes possuem diferentes desempenhos.

Analisando relatórios elaborados pelo Conselho Nacional de Justiça - CNJ, como o Justiça em Números, nota-se desempenhos diferentes entre Tribunais considerados semelhantes dentre o mesmo ramo de atividade, sendo que a mesma situação acontece dentro do mesmo Tribunal quando comparando suas unidades judiciárias.

Algumas Varas do Trabalho apresentam melhores desempenhos em relação as demais, contudo a identificação da eficiência nem sempre é trivial. 


## O aplicativo

O app DATAmining JUD (Time 7) é uma ferramenta que utiliza técnicas de Process Mining para realizar a descoberta do fluxo de movimentos dos processos das unidades judiciárias, através dos dados disponibilizados do DATAJUD.

A ferramenta constrói dinamicamente modelos de tramitação de processos, a partir dos movimentos disponibilizados pelo Datajud, apresentando o fluxo de movimentos processuais de uma forma gráfica e visual, permitindo aos gestores a identificação de diferenças relevantes entre unidades judiciárias.

A partir da seleção de um órgão judiciário, uma classe processual e dois órgãos julgadores, são apresentados os grafos de fluxos (DFG - Directly-Follows Graph) dos modelos de processos dos movimentos processuais em cada órgão julgador selecionado, a frequência em que ocorrem e o tempo médio da transição entre movimentos processuais. Dessa forma, é possível comparar uma unidade que apresente desempenho acima da média com unidades que possuem indicadores considerados abaixo da meta com o intuito de identificar boas práticas.


## Roteiro da solução

### Importação dos dados

Para a importação e transformação dos dados foi utilizado o Notebook executado no ambiente Google Colaboratory, disponível no repositório com o nome "ExtratorDefinitivo.ipynb"

Inicialmente foram importados os dados disponibilizados, depois foram normalizados em um modelo relacional, gerados arquivos CSVs para cada uma das entidades relacionais do modelo, o que possibilitou que as análises exploratórias fossem feitas diretamente com os arquivos CSVs ou importadas para qualquer banco de dados.

Foram disponibilizados diversos dashboards MS-Power BI (https://powerbi.microsoft.com/pt-br/) e planilhas de dados para que todos pudessem compreender melhor os dados disponibilizados, suas limitações e potenciais. Após análises exploratórias nos dados, identificou-se diversas inconsistências e ausência de dados. Desta forma, foram aplicados correções e ajustes. Entre esses ajustes, pode-se citar a identificação e tratamento de datas em formatos incorretos, assim como exclusão daqueles registros cuja correção não era possível, entre outros. Restaram outras inúmeras inconsistências, mas como estava fora do escopo da proposta do Desafio 1 (Tempo e Produtividade), optou-se pelos ajustes mínimos que viabilizassem a solução final.

Para que todos pudessem trabalhar no mesmo conjunto de dados, foi criada uma base dados central Big Query do Google Cloud (https://cloud.google.com/bigquery) e os ajustes foram sendo aplicados nela. Conforme a necessidade, arquivos CSVs eram exportados para análises pudessem ser feitas em qualquer tecnologia que os integrantes da equipe achassem mais conveniente.

### Aplicação

Buscou-se, com foco nas técnicas de Process Mining, a descoberta de padrões de fluxo de movimentos processuais. Diversas ferramentas foram utilizadas, com destaque para:

* Fluxicon Disco : https://fluxicon.com/disco/

* ProM Tools : http://www.promtools.org/

* PM4PY: https://pm4py.fit.fraunhofer.de/

Enquanto o Fluxicon Disco e ProM Tools foram importantes para a fase de exploração de possibilidades, a biblioteca PM4PY foi eleita como nosso principal componente da aplicação, por se tratar de uma biblioteca de software (em contraste com as outras que eram aplicações) e fornecer um grau de flexibilidade e independência necessário para a construção de uma nova aplicação.

A biblioteca PM4PY possui um conjunto bem variado e rico de funcionalidades e, em um primeiro momento, foi necessário explorá-la à luz dos dados disponibilizados. Muito experimentos foram realizados com diversos resultados interessantes, mas devido aos prazos e escopo do desafio, a equipe teve que optar por um caminho minimamente viável. Logo percebeu-se que  os experimentos com descoberta de padrões específicos dentro dos modelos de processos descobertos e outras técnicas de predição mais avançadas teriam que ser deixadas para um outro momento, pois não seria possível estabelecer um processo mínimo que comportasse os ciclos de experimentação e validação necessários nesse tipo de projeto e equacioná-lo com o objeto final de avaliação do Hackaton que era uma aplicação completa. Além disso, a visível falta de qualidade dos dados aumentava a incerteza quanto aos resultados que seriam potencialmente possíveis, caso nos concentrássemos em identificação de padrões e predição.

Assim, a equipe optou pela construção de uma ferramenta que trouxesse uma compreensão mais simplificada e preferencialmente visual dos fluxos de movimentos processuais. Dentro da PM4PY a representação mais interessante e que mostrou expressar com mais propriedade as diversas situações possíveis nos fluxos de movimentação processual, segundo umaa avaliação qualitativa da equipe, foi o Directly-Follows Graph (DFG). Utilizou-se o DFG com ênfase no tempo e na frequência das transições entre os movimentos processuais.

Muitas das ferramentas citadas foram utilizadas somente internamente durante o processo de ideação e não fazem parte da solução final apresentada.

### Concepção da aplicação

Na disciplina de Process Mining um ponto de partida é o "log de eventos". A partir dele três tipos de Process Mining podem ser conduzidos: "Process Discovery", "Process Conformance" e "Process Enhancement". A aplicação desenvolvida focou no "Process Discovery" que é a descoberta de um modelo de processo que represente os eventos do log. 

Em um log, os eventos podem conter atributos e eles pertencem a um "case". Um log genérico pode conter:

caso, atributo1_caso, atributo2_caso, ..., evento, datahora, atributo1_evento, atributo2_evento, ...

Partimos da ideia de que os dados do Datajud disponibilizados representavam, principalmente do ponto de vista da dimensão dos movimentos processuais, um log de eventos e consideramos o seguinte:

* caso = ID do processo (um id artificial criado com os seguintes dados: número do processo, classe do processo, órgão julgador e tribunal

* evento = Código Movimento:Descrição Movimento (poderia ser somente o código e a descrição seria um atributo do evento, mas por simplificação unimos os dois)

* datahora = data hora do movimento

* Demais atributos do processo e evento

A partir de algum subconjunto de um log, gostaríamos de descobrir um modelo que o represente, assim como algumas métricas associadas (como duração entre dois eventos e frequência dos eventos) e compará-lo com outros modelos descobertos a partir de outros subconjuntos do log original. A aplicação foi concebida como um ambiente operacional mínimo para que análises comparativas, com foco em fluxo de movimentos processuais, sejam possíveis.

### Arquitetura da aplicação

Como a aplicação é mais uma prova de conceito, dado o prazo exíguo, optamos por utilizar o Streamlit.io que simplifica a criação da interface web gráfica de usuário (GUI) em Python.

No back-end utilizamos Python e as bibliotecas Pandas, PM4PY e Matplotlib/Seaborn.

Finalmente, como repositório de dados, para simplificar a distribuição e instalação optamos por utilizar um arquivo CSV previamente extraído e tratado (Script de extração e tratamento disponível no repositório). A substituição do CSV por uma tecnologia qualquer de banco de dados é simples.

* Front-end: Streamlit.io.

* Back-end: Python, Pandas, PM4PY, Matplotlib/Seaborn.

* Repositório de dados: arquivo CSV com subconjunto de dados de TRTs extraídos e transformados a partir do dataset disponibilizado.

#### Ferramentas utilizadas na aplicação final

* Streamlit (httpS://streamlit.io)

* PM4PY (PM4PY: https://pm4py.fit.fraunhofer.de/)

* Pandas (https://pandas.pydata.org/)

* Matplotlib/Seaborn (https://seaborn.pydata.org/)

## Considerações finais e trabalhos futuros

O app tem se mostrado útil para comparações de fluxo de movimentos entre órgãos julgadores, oferecendo diversos insights. Muitas questões foram levantadas no curto espaço de tempo em que o app pôde ser utilizado após ficar pronto. São questões que podem servir como ponto de partida para diversas outras análises mais dirigidas.

A qualidade dos dados fornecidos é um ponto importante e limitador das análises. Fizemos algumas tentativas de análise dos fluxos sob diferentes perspectivas, como a identificação das diversas fases processuais de acordo com os movimentos, cujo resultado foi inconclusivo, muito possivelmente por causa das inconsistências. Assim, não conseguimos identificar de maneira satisfatória os marcos de início e fim das fases processuais, nem mesmo os marcos de finalização do processo judicial como um todo, pois aparentemente faltam dados.

Outro aspecto é que as Tabelas Processuais Nacionais do CNJ, mesmo que fossem adotadas por todos os tribunais, muito possivelmente ainda teriam um conjunto limitado de informações e com uma modelagem de dados não muito propícia para alguns tipos de análises. Um exemplo disso é o uso de complementos (que não estavam disponíveis nos datasets) que dão diferentes significados a um mesmo movimento processual. Em outras palavras, no paradigma de "Process Mining", alguns complementos associados ao movimento representariam "eventos" distintos. Por outro lado, alguns complementos são muito específicos, como nomes de partes processuais, e configurariam apenas "atributos dos eventos" no paradigma de "Process Mining". Seria interessante uma reanálise dessas tabelas à luz dos desafios de Process Mining e de obtenção de estatísticas importantes que caracterizem aspectos importantes do processo judicial. Uma sugestão seria a criação de categorias de movimentos e complementos: uma básica e outra estendida. A primeira semelhante a que existe, mais focada nos eventos processuais previstos em lei e a segunda mais focada em questões estatísticas, de análise e algumas meramente informativas para os interessados.

Diversas melhorias futuras são possíveis, citamos algumas:

* Avaliação mais detalhada dos modelos gerados com relação às principais métricas de qualidade utilizadas para os modelos: 
  * (Fitness) The discovered model should allow for the behavior seen in the event
log.
  * (Precision) The discovered model should not allow for behavior completely unrelated
to what was seen in the event log.
  * (Generalization) The discovered model should generalize the example behavior
seen in the event log.
  * (Simplicity) The discovered model should be as simple as possible

* Utilização de técnicas de predição e detecção de anomalias.

* Simulações para prever tempos médios esperados para chegada do processo judicial nas suas diversas fases.

* Construção de painéis de monitoramento dos processos em relação a modelos previamente gerados, possibilitando a geração de alertas quando eles atingirem métricas e comportamentos destoantes.

São muitas as possibilidades e elas precisam ser exploradas, construídas e avaliadas com método. Os desafios também são grandes, começando pela qualidade e disponibilidade dos dados, passando pelo uso e avaliação das ferramentas e técnicas e por fim uma avaliação de qualidade e viabilidade da aplicação das técnicas.

## Instalação

O roteiro a seguir é baseado na instalação em um sistema Linux Ubunutu 18.04LTS.

### Instalar as dependências de SO

sudo apt-get install build-essential graphviz python3-dev python3-venv 


### Baixar o código do aplicativo 

git clone https://github.com/dataminingjud/time7.git

cd time7

### Criar environment venv para isolar as dependências python

python3 -m venv ./env

### Ativar environment recém criado

source ./env/bin/activate

### Instalar depedências python 

pip install -r ./requirements.txt

### Rodar aplicativo 

./roda.sh

O aplicativo vai rodar na porta 80. Caso já exista outra aplicação escutando na porta 80, edite o arquivo roda.sh para especificar outra porta.

### Acessar o aplicativo no navegador

Aponte o navegador para http://127.0.0.1/ (ou http://127.0.0.1:porta), caso tenha alterado a porta.

## Referências

* Wil van der Aalst - Process Mining Wil: Data Science in Action - Second Edition https://www.amazon.com.br/Process-Mining-Data-Science-Action/dp/3662498502

* Lars Reinkemeyer - Process Mining in Action Principles, Use Cases and Outlook : https://www.springer.com/gp/book/9783030401719

* Fluxicon Disco : https://fluxicon.com/disco/

* ProM Tools : http://www.promtools.org/

* PM4PY: https://pm4py.fit.fraunhofer.de/
