# Trabalho_Sistemas_Distribuidos
Repositório criado para um trabaho da matéria de Sistemas Distribuídos. 

---

## Tema: Envio da área de transferência (Ctrl + C) com histórico

Enviar ao servidor a área de transferência de texto do cliente e acumular no servidor
as últimas cinco cópias de textos (Ctrl+C) recebidas do cliente. Deve ser dada a
opção ao servidor de qual das últimas cinco cópias de texto será colada quando o
lado do servidor pressionar colar (Ctrl+V).

---

## Estrutura do projeto

```
.
├── README.md
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── .env.example
├── .python-version
└── src/
    ├── cliente.py
    └── servidor.py
```

---

## Configuração

1. Copie o arquivo de exemplo de variáveis de ambiente:

   ```bash
   cp .env.example .env
   ```

2. Edite o `.env` conforme o seu cenário:

   ```
   IP_SERVIDOR=0.0.0.0
   PORTA=9870
   ```

   - No **servidor**, `IP_SERVIDOR` é o endereço em que ele vai escutar (`0.0.0.0` escuta em todas as interfaces).
   - No **cliente**, `IP_SERVIDOR` deve ser o IP real da máquina onde o servidor está rodando (ex: `192.168.0.10` ou `127.0.0.1` se for no mesmo computador).
   - `PORTA` deve ser a mesma nos dois lados.

Requer Python **3.14+** (ver `.python-version`).

---

## Como executar

### Opção 1 — usando `uv` (recomendado)

O projeto já vem com `pyproject.toml` e `uv.lock`, então o `uv` resolve e instala as dependências automaticamente.

1. Instale o [uv](https://docs.astral.sh/uv/getting-started/installation/) (caso ainda não tenha):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Sincronize o ambiente (cria a `.venv` e instala as dependências do `uv.lock`):

   ```bash
   uv sync
   ```

3. Em um terminal, rode o **servidor**:

   ```bash
   uv run src/servidor.py
   ```

4. Em outro terminal (ou outra máquina, apontando `IP_SERVIDOR` para o servidor), rode o **cliente**:

   ```bash
   uv run src/cliente.py
   ```

### Opção 2 — sem `uv` (pip + venv)

1. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Linux/macOS
   .venv\Scripts\activate         # Windows
   ```

2. Instale as dependências a partir do `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. Em um terminal, rode o **servidor**:

   ```bash
   python src/servidor.py
   ```

4. Em outro terminal (ou outra máquina), rode o **cliente**:

   ```bash
   python src/cliente.py
   ```

---

## Uso

- O **cliente** monitora a área de transferência local e envia automaticamente ao servidor todo novo texto copiado (Ctrl+C). Para encerrar, pressione `Ctrl+C` no terminal do cliente (isso avisa o servidor e fecha a conexão).
- O **servidor** acumula as últimas 5 cópias recebidas e exibe um menu interativo:
  1. Listar itens do histórico
  2. Colar (Ctrl+V) um item do histórico — copia o item escolhido para a área de transferência do servidor
  3. Sair

---

## Integrantes:

- Kaique Silva Sousa
- Vinícius Nunes de Andrade