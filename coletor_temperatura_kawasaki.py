
import asyncio
import telnetlib3
import logging
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# -------- CONFIGURAÇÃO DO LOG --------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)

# -------- CONFIGURAÇÃO DO INFLUXDB --------
influx_url = "http://20.19.224.248:8086"  # Coloque seu IP/URL do InfluxDB
influx_token = "SEU_TOKEN_AQUI"            # Substituir pelo token do InfluxDB
influx_org = "TDB"                         # Nome da organização no InfluxDB
influx_bucket = "Kawasaki_robots"          # Nome do bucket

# -------- CONFIGURAÇÃO DOS ROBÔS --------
hosts = {
    '192.168.5.3': 'UMR5-3',
    '192.168.5.4': 'UMR5-4',
    '192.168.5.5': 'UMR5-5',
    '192.168.5.6': 'UMR5-6'
}

port = 23           # Porta do Telnet
username = "as"     # Login do robô (Telnet)
TIMEOUT = 5         # Timeout para respostas Telnet


# -------- FUNÇÃO PARA CONECTAR E COLETAR DADOS --------
async def conectar_e_obter(host: str, nome: str, write_api):
    while True:
        try:
            reader, writer = await telnetlib3.open_connection(host=host, port=port, encoding='utf8')
            logging.info(f"[{nome}] Conectado! Enviando login...")
            writer.write(username + "\r\n")
            await asyncio.sleep(1)

            while True:
                writer.write("WHERE 43\r\n")
                await asyncio.sleep(2)

                resposta = await asyncio.wait_for(reader.read(4096), timeout=TIMEOUT)
                logging.info(f"[{nome}] Resposta recebida")

                linhas = resposta.splitlines()
                nomes_eixos, valores_temp = [], []

                for i, linha in enumerate(linhas):
                    if "J" in linha:
                        nomes_eixos = linha.split()
                        if i + 1 < len(linhas):
                            valores_temp = linhas[i + 1].split()
                        break

                if not nomes_eixos or not valores_temp:
                    logging.warning(f"[{nome}] Dados incompletos, tentando novamente...")
                    continue

                try:
                    valores_temp = [float(temp) for temp in valores_temp]
                except ValueError as e:
                    logging.warning(f"[{nome}] Erro ao converter temperaturas: {e}")
                    continue

                temperaturas = dict(zip(nomes_eixos, valores_temp))

                for eixo, temperatura in temperaturas.items():
                    ponto = (
                        Point("temperatura_eixo")
                        .tag("host", host)
                        .tag("nome", nome)
                        .tag("eixo", eixo)
                        .field("valor", temperatura)
                        .time(datetime.utcnow())
                    )
                    try:
                        write_api.write(bucket=influx_bucket, org=influx_org, record=ponto)
                    except Exception as e:
                        logging.error(f"[{nome}] Erro ao enviar temperatura do eixo {eixo}: {e}")

                logging.info(f"[{nome}] Temperaturas enviadas: {temperaturas}")
                await asyncio.sleep(10)

        except Exception as e:
            logging.error(f"[{nome}] Erro de conexão ou leitura: {e}")
            logging.info(f"[{nome}] Tentando reconectar em 30 segundos...")
            await asyncio.sleep(30)


# -------- FUNÇÃO PRINCIPAL --------
async def main():
    client_influx = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
    with client_influx.write_api(write_options=SYNCHRONOUS) as write_api:
        tarefas = [conectar_e_obter(host, nome, write_api) for host, nome in hosts.items()]
        await asyncio.gather(*tarefas)
    client_influx.close()


# -------- EXECUTA O PROGRAMA --------
if __name__ == "__main__":
    asyncio.run(main())
