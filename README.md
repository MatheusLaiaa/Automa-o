#                        Automação Temperatura
------------------------------------------------

Esse projeto tem o intuito de colher as informçãoes do controlador que vem diretamente do Robo Kawasaki, informações tais como, temperatura de cada encoder localizado atrás do motor, de forma sincronizada entre quatro robos.
Nesse projeto eu utilizei a liguagem Python para a programação, onde atualmente a mesma está sendo altamente utilizada na area de automação, a mesma me deu versatilidade para a comunicação de rede e realizar atividades sincronizadas. 

Configuração

Define conexões Telnet (hosts, port, username, TIMEOUT).

Configura o InfluxDB (url, token, org, bucket).

Função conectar_e_obter(host, nome, write_api)

Estabelece conexão Telnet com o robô.

Envia login e comando WHERE 43 a cada 2 segundos.

Recebe e processa resposta: extrai nomes de eixos e valores de temperatura, converte para float e monta dicionário.

Envia cada temperatura como métrica para o InfluxDB (temperatura_eixo), com tags host, nome, eixo, valor e timestamp UTC.

Em caso de erro de leitura ou conexão, faz log e aguarda 30 segundos para reconectar.

Função main()

Cria cliente InfluxDBClient e abre write_api.

Executa tarefas paralelas (asyncio.gather) para cada host.

Fecha conexão após parada.

Execução

asyncio.run(main()) inicia todo o monitoramento em loop contínuo.

 # Programação 
<img width="867" height="842" alt="image" src="https://github.com/user-attachments/assets/8c1b8a05-0900-403d-8a8c-70e475fa9ede" />
<img width="882" height="778" alt="image" src="https://github.com/user-attachments/assets/ec43927c-6959-43aa-8236-47060be213c8" />
<img width="755" height="358" alt="image" src="https://github.com/user-attachments/assets/c38cd5aa-6dbf-4ad4-a60a-0c2489f8dc0f" />



# Intuito do programa 

Conecta aos robôs via Telnet para coletar as temperaturas dos eixos (ex.: J1, J2, J3...).

Envia as temperaturas para o InfluxDB, armazenando-as com a hora exata, o IP do robô e o eixo.

Repete o processo continuamente a cada 10 segundos, tentando se reconectar se houver falhas.

Registra erros e sucessos no log para monitoramento.

Um sistema automatizado de monitoramento e registro de temperatura dos eixos de robôs, com armazenamento em um banco de dados.
