# Imagem base
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala uv via pip
RUN pip install uv

# Copia arquivos de configuração do projeto
COPY pyproject.toml uv.lock ./

# Instala dependências usando o uv
RUN uv sync --frozen --no-dev

# Copia o restante da aplicação
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar a aplicação usando uv run
CMD ["uv", "run", "uvicorn", "src.main.server.server:app", "--host", "0.0.0.0", "--port", "8000"]