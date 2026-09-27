import socket, os, sys, collections, threading
import pyperclip

host = os.environ.get("IP_SERVIDOR", "0.0.0.0")
porta = int(os.environ.get("PORTA", 9870))

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("Falha ao criar o socket")
    sys.exit()

try:
    s.bind((host, porta))
    s.listen(1)
except Exception as e:
    print(f"Falha ao abrir o servidor: {e}")
    sys.exit()

print(f"Servidor escutando na porta {porta}")
print("Aguardando conexão do cliente...")

conn, endereco_cliente = s.accept()
print(f"Cliente conectado: {endereco_cliente}")

historico = collections.deque(maxlen=5)

lock = threading.Lock()


def receber_tamanho_e_dados(conexao):
    """Lê primeiro 4 bytes com o tamanho da mensagem, depois a mensagem em si."""
    cabecalho = conexao.recv(4)
    if not cabecalho:
        return None
    tamanho = int.from_bytes(cabecalho, byteorder="big")

    dados = b""
    while len(dados) < tamanho:
        pedaco = conexao.recv(tamanho - len(dados))
        if not pedaco:
            break
        dados += pedaco
    return dados.decode("utf-8")


def thread_recebimento():
    """Roda em paralelo ao menu, sempre esperando novos textos do cliente."""
    while True:
        try:
            texto = receber_tamanho_e_dados(conn)
        except (ConnectionError, OSError):
            print("\nConexão com o cliente foi encerrada.")
            break

        if texto is None:
            print("\nCliente desconectou.")
            break

        if texto == "fim":
            print("\nCliente encerrou a sessão.")
            break

        with lock:
            historico.append(texto)
        print(f"\n[NOVO ITEM RECEBIDO] \"{texto}\" (histórico atualizado)")
        print("Digite uma opção e pressione Enter: ", end="", flush=True)


def listar_historico():
    with lock:
        if not historico:
            print("Histórico vazio. Aguardando o cliente copiar algo (Ctrl+C).")
            return
        print("Últimas cópias recebidas:")
        for i, item in enumerate(historico, start=1):
            print(f"  {i}. \"{item}\"")


def colar_item():
    with lock:
        if not historico:
            print("Histórico vazio, nada para colar.")
            return
        listar_local = list(historico)

    for i, item in enumerate(listar_local, start=1):
        print(f"  {i}. \"{item}\"")

    escolha = input("Digite o número do item que deseja colar: ").strip()
    if not escolha.isdigit() or not (1 <= int(escolha) <= len(listar_local)):
        print("Opção inválida.")
        return

    texto_escolhido = listar_local[int(escolha) - 1]
    pyperclip.copy(texto_escolhido)
    print(f"Copiado para a área de transferência do servidor: \"{texto_escolhido}\"")


def menu():
    print("=" * 60)
    print("OPÇÕES:")
    print("1. Listar itens do histórico")
    print("2. Colar (Ctrl+V) um item do histórico")
    print("3. Sair")
    print("=" * 60)

thread = threading.Thread(target=thread_recebimento, daemon=True)
thread.start()

while True:
    menu()
    inp = input("Escolha uma opção: ").strip()

    if inp == "1":
        listar_historico()
    elif inp == "2":
        colar_item()
    elif inp == "3":
        print("Encerrando servidor...")
        break
    else:
        print("Opção inválida, tente novamente.")

conn.close()
s.close()