# Código do cliente
# Código do cliente
import socket, os, sys, time
import pyperclip
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("IP_SERVIDOR", "127.0.0.1")
porta = int(os.environ.get("PORTA", 9870))

INTERVALO_VERIFICACAO = 0.5  # segundos entre checagens da área de transferência


def enviar_tamanho_e_dados(conexao, texto):
    """Envia primeiro 4 bytes com o tamanho da mensagem, depois a mensagem em si.
    Espelha o receber_tamanho_e_dados do servidor."""
    dados = texto.encode("utf-8")
    tamanho = len(dados)
    conexao.sendall(tamanho.to_bytes(4, byteorder="big"))
    conexao.sendall(dados)


def conectar():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError:
        print("Falha ao criar o socket")
        sys.exit()

    try:
        s.connect((host, porta))
    except Exception as e:
        print(f"Falha ao conectar ao servidor em {host}:{porta} -> {e}")
        sys.exit()

    print(f"Conectado ao servidor {host}:{porta}")
    return s


def monitorar_area_de_transferencia(conexao):
    print("Monitorando a área de transferência (Ctrl+C).")
    print("Pressione Ctrl+C no TERMINAL (não na área de transferência) para encerrar a sessão.\n")

    ultimo_texto = pyperclip.paste()

    while True:
        texto_atual = pyperclip.paste()

        if texto_atual != ultimo_texto and texto_atual.strip() != "":
            ultimo_texto = texto_atual
            try:
                enviar_tamanho_e_dados(conexao, texto_atual)
                print(f'[ENVIADO] "{texto_atual}"')
            except (ConnectionError, OSError) as e:
                print(f"Conexão perdida ao enviar dados: {e}")
                break

        time.sleep(INTERVALO_VERIFICACAO)


def main():
    conexao = conectar()

    try:
        monitorar_area_de_transferencia(conexao)
    except KeyboardInterrupt:
        print("\nEncerrando cliente...")
    finally:
        try:
            enviar_tamanho_e_dados(conexao, "fim")
        except (ConnectionError, OSError):
            pass
        conexao.close()
        print("Conexão encerrada.")


if __name__ == "__main__":
    main()