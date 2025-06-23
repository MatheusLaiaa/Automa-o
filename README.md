#                        Automação Temperatura
------------------------------------------------

Esse projeto tem o intuito de colher as informçãoes do controlador que vem diretamente do Robo Kawasaki, informações tais como, temperatura de cada encoder localizado atrás do motor, de forma sincronizada entre quatro robos.
Nesse projeto eu utilizei a liguagem Python para a programação, onde atualmente a mesma está sendo altamente utilizada na area de automação, a mesma me deu versatilidade para a comunicação de rede e realizar atividades sincronizadas. 

 # Programação 

 ![image](https://github.com/user-attachments/assets/666d6c90-1486-41b3-8334-4c31eda1b809)
![image](https://github.com/user-attachments/assets/582a4104-9051-416b-80e4-08c59856c4d8)

# Intuito do programa 

Conecta aos robôs via Telnet para coletar as temperaturas dos eixos (ex.: J1, J2, J3...).

Envia as temperaturas para o InfluxDB, armazenando-as com a hora exata, o IP do robô e o eixo.

Repete o processo continuamente a cada 10 segundos, tentando se reconectar se houver falhas.

Registra erros e sucessos no log para monitoramento.

Um sistema automatizado de monitoramento e registro de temperatura dos eixos de robôs, com armazenamento em um banco de dados.
