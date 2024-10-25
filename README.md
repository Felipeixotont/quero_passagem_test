# quero_passagem_test
## Processo Seletivo para empresa Quero Passagem - Vaga Desenvolvedor Python Pleno.

Esse teste foi desenvolvido por mim e todo o processo de criação foi feito no meu Gitlab: https://gitlab.com/felipeixotont/quero_passagem_test


Aqui no Github fiz somente a cópia do que desenvolvi para deixar de portfólio.

## Para rodar esse projeto você deve:

- Criar ambiente virtual: python3 -m venv venv

### No Linux
- Rodar ambiente virtual: source venv/bin/activate

### No Windows CMD
- Rodar ambiente virtual: venv\Scripts\activate

- Rodar no terminal: pip install -r requirements.txt

- Estar dentro do diretório '/src' e rodar no terminal o comando: python3 main.py


Ao rodar o arquivo 'main.py', um diretório chamado files será criado dentro de 'src' caso não exista ainda, nesse diretório os PDF gerados dos trechos e seus respectivos dias serão armazenados.

# TRELLO

Link do Trello que criei para organizar o teste e dividi-lo em tarefas: https://trello.com/b/yHO98AtX/quero-passagem-test
Cada tarefa contem a descrição da tarefa e o link do Merge Request no Gitlab.


# BIBLIOTECAS UTILIZADAS

As principais bibliotecas utilizadas foram: Requests, Json, Playwright (não foi necessário o uso da BeautifulSoup).
A escolha do Playwright ao invés do Selenium se deu pelo motivo de no Playwright ser capaz de adicionar Event Listener nas interações com o Browser de forma nativa (Selenium não tem suporte nativo para interceptação de requisições HTTP), permitindo a coleta dos tokens para fazer requisições na API antes desses tokens serem limpados pelo código Javascript que deletava o "access_token" do headers. Ao clicar no input de Origem do site, é feito uma requisição para o endpoint "https://api.jcatlm.com.br/place/v1/searchOrigin", o Event Listener que configurei no Playwright faz com que ao ser enviado a requisição para esse endpoint, antes de concluir essa requisição, armazena o "access_token" e também o "client_id" (mesmo esse aparentemente sendo fixo) em uma variável do tipo dict, para poder ser usada e autenticar nas chamadas desses endpoints da api da jcatlm.

A priori, a requisição para o endpoint "https://api.jcatlm.com.br/route/v1/getRoutes" trazia as viagens para os sete dias consecutivos, porém na quarta-feira esse endpoint passou por alterações. Foi necessário refatorar o método fetch_routes() da classe Trips de forma a fazer uma requisição para cada dia, aumentando a quantidade de requisições feitas para poder concluir a execução do Scraper. Antes da mudança, o Scraper estava fazendo somente onze requisições, uma para trazer todas as cidades disponíveis com seus respectivos IDs e um requisição para cada um dos top dez trechos. Após a mudança, foi necessário fazer sete requisições por cada um dos top dez trechos, aumentando assim a quantidade de requisições de onze para setenta e uma requisições.

# POR QUE ESCOLHI APRESENTAR OS DADOS EM PDF E CSV

Touxe os resultados em PDF e também em CSV. Fica a opção de utilizar uma das duas formas, ou utilizar as duas formas de uma vez. Optei por fazer das duas formas pois em PDF facilita a análise pra quem não for programador, em CSV pois caso seja necessário em um caso real pegar esses dados e fazer algo com eles, seria mais fácil manipular através de um CSV do que por um PDF.
Ao rodar o Scraper é criado uma pasta chamada "files" dentro de "src" onde é armazenado as informações de todos os dias e todas opções para cada um dos top dez trechos.

## Desafio de Web Scraping - Viação Cometa

Objetivo: Desenvolver um scraper que colete informações de passagens para
os top 10 trechos do site da viação Cometa.
Link para o site da Cometa: https://www.viacaocometa.com.br/

## Top 10 Trechos a serem coletados:
1. São Paulo - Tietê (SP) → Belo Horizonte - Terminal G. (MG)
2. Belo Horizonte - Terminal G. (MG) → São Paulo - Tietê (SP)
3. São Paulo - Tietê (SP) → Ribeirão Preto - Rodoviária (SP)
4. Ribeirão Preto - Rodoviária (SP) → São Paulo - Tietê (SP)
5. São Paulo - Tietê (SP) → Curitiba - Rodoviária (PR)
6. Rio de Janeiro - Novo Rio (RJ) → Belo Horizonte - Terminal G. (MG)
7. São Paulo - Barra Funda (SP) → São José do Rio Preto - Terminal (SP)
8. Curitiba - Rodoviária (PR) → São Paulo - Tietê (SP)
9. São José do Rio Preto - Terminal (SP) → São Paulo - Barra Funda (SP)
10. Rio de Janeiro - Novo Rio (RJ) → Campinas - Terminal Ramos (SP)


## Requisitos do desafio:
1. Linguagem: O scraper deve ser desenvolvido em Python.

2. Bibliotecas: É recomendado o uso de bibliotecas como Selenium ,
BeautifulSoup , e requests . O candidato está livre para escolher outras
Desafio de Web Scraping - Viação Cometa  Vaga de Desenvolvedor Python 2
ferramentas, desde que explique o motivo da escolha e sua justificativa
técnica.

3. Funcionalidade:
A aplicação deve acessar o site da viação diariamente e coletar
informações de passagens para os top 10 trechos mais populares.
Coletar dados para um período de 7 dias consecutivos, contando a
partir do dia em que a coleta é executada.
Exemplo: Se a coleta começar no dia 22/10/2024, os dados devem
ser coletados até o dia 28/10/2024.
As informações coletadas devem incluir:

- Origem
- Destino
- Classe (Cama, Semileito Premium, Executivo, Convencional DD) verificar e registrar as classes esgotadas e disponíveis.
- Quantidade de poltronas disponíveis
- Preço
- Horário de partida
- Horário de chegada

Os dados devem ser armazenados com timestamps para garantir a
organização e permitir análises temporais.
O scraper deve simular a navegação necessária para encontrar as
informações, incluindo, se necessário, o preenchimento de formulários
ou o uso de filtros.
O formato da apresentação dos resultados (ex.: CSV, JSON, relatório
em PDF, dashboard) fica a critério do candidato, desde que a escolha
seja justificada.

4. Relatórios de Erro:
O código deve capturar e reportar erros comuns que possam ocorrer
durante a execução, como problemas de conexão ou elementos não
encontrados.
É importante que sejam gerados logs claros e detalhados para ajudar
na depuração.

5. Código Limpo e Documentado:
O código deve ser bem estruturado e documentado para facilitar o
entendimento, manutenção e escalabilidade.


## Critérios de Avaliação:
- Eficiência do Código: Avaliação do desempenho do scraper em termos de
velocidade e uso eficiente de recursos.
- Manutenção: Facilidade de ajuste e manutenção do código, incluindo
clareza na estrutura e modularidade.
- Tratamento de Exceções: Como o candidato lida com possíveis erros e
falhas durante a execução, e se o tratamento é eficaz e bem implementado.
- Documentação e Estrutura: Qualidade da documentação e organização do
código, incluindo a clareza dos comentários e da lógica utilizada.

