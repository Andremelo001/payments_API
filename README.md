# 💳 Payments API - Microserviço de Pagamentos

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.118+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![Status](https://img.shields.io/badge/Status-Em%20Produção-success.svg)

## 📋 Sobre o Projeto

Este projeto é um **microserviço de pagamentos** desenvolvido com o objetivo principal de **compreender e aplicar os conceitos fundamentais da arquitetura de microserviços**. O serviço é responsável por processar pagamentos via PIX utilizando a integração com o Mercado Pago, gerando QR Codes, persistindo informações de transações e processando webhooks de notificação de pagamento.

**🚀 Este microserviço está atualmente rodando em produção**, processando pagamentos reais via PIX através da integração com o Mercado Pago.

Este microserviço é consumido pela API principal de gerenciamento de pet shops, disponível em: [schedule-pet-shop](https://github.com/Andremelo001/schedule-pet-shop) **(também em produção)**

## 🎯 Objetivo Educacional

O foco principal deste projeto é **explorar e demonstrar os conceitos de microserviços** através de uma aplicação prática e funcional. Não se trata apenas de construir uma API de pagamentos, mas de entender como os microserviços se comunicam, se isolam e colaboram em uma arquitetura distribuída.

## 🏗️ Conceitos Fundamentais de Microserviços

### O que são Microserviços?

Microserviços são uma abordagem arquitetural para desenvolvimento de software onde uma aplicação é construída como um conjunto de **serviços pequenos e independentes**, cada um executando em seu próprio processo e comunicando-se através de mecanismos leves (geralmente HTTP/REST).

### Princípios Aplicados neste Projeto

#### 1. **Responsabilidade Única**
- Este microserviço tem **uma única responsabilidade**: gerenciar pagamentos
- Não gerencia agendamentos, clientes ou outros domínios do pet shop
- Foco exclusivo em processamento de pagamentos PIX e geração de QR Codes

#### 2. **Independência e Autonomia**
- Possui seu **próprio banco de dados** (PostgreSQL independente)
- Pode ser desenvolvido, testado e implantado **independentemente** da API principal
- Tem seu próprio ciclo de vida e versionamento

#### 3. **Comunicação via API**
- Expõe endpoints REST bem definidos (`/payments/generate_payment`)
- Comunicação assíncrona e desacoplada com outros serviços
- Contratos claros através de interfaces HTTP

#### 4. **Isolamento de Falhas**
- Se este serviço falhar, não afeta diretamente outras funcionalidades do pet shop
- Erros são contidos dentro do contexto de pagamentos
- Permite implementar estratégias de fallback e circuit breaker

#### 5. **Escalabilidade Independente**
- Pode ser escalado horizontalmente de acordo com a demanda de pagamentos
- Não precisa escalar toda a aplicação, apenas o serviço de pagamentos
- Otimização de recursos baseada em necessidades específicas

#### 6. **Tecnologia Heterogênea**
- Liberdade para escolher a stack mais adequada (Python/FastAPI neste caso)
- Enquanto a API principal pode usar outras tecnologias
- Cada microserviço pode evoluir tecnologicamente de forma independente
 

## 🚀 Tecnologias Utilizadas

- **Python 3.13+**
- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM para interação com banco de dados
- **PostgreSQL 15** - Banco de dados relacional
- **Mercado Pago SDK** - Integração para pagamentos PIX
- **Docker & Docker Compose** - Containerização e orquestração
- **Databases** - Suporte assíncrono para PostgreSQL
- **asyncpg** - Driver assíncrono para PostgreSQL
- **uv** - Gerenciador de pacotes Python moderno e rápido

## 📁 Arquitetura do Projeto

O projeto segue uma **arquitetura limpa (Clean Architecture)** organizada em camadas:

```
src/
├── drivers/           # Drivers externos (QR Code, APIs)
├── infra/            # Infraestrutura (DB, Entities, Repositories)
├── main/             # Configurações principais (Routes, Composers, Server)
├── modules/          # Módulos de negócio
│   └── payment/      # Domínio de pagamentos
│       ├── data/     # Casos de uso e interfaces
│       └── domain/   # Regras de negócio
└── presentation/     # Controllers e tipos HTTP
```

### Camadas

- **Presentation**: Controllers e adaptadores HTTP
- **Domain**: Regras de negócio e interfaces de casos de uso
- **Data**: Implementação dos casos de uso
- **Infra**: Acesso a dados e integrações externas
- **Drivers**: Integrações com serviços externos (Mercado Pago)
- **Main**: Composição de dependências e configuração de rotas

### Responsabilidades
- ✅ Geração de pagamentos PIX via Mercado Pago
- ✅ Criação de QR Codes para pagamento (texto e base64)
- ✅ Webhook para notificação de mudança de status
- ✅ Consulta de status de pagamentos
- ✅ Notificação para API principal sobre mudanças de status
- ✅ Persistência de transações em PostgreSQL
- ✅ API RESTful com FastAPI
- ✅ Suporte completo a operações assíncronas
- ✅ Comunicação entre microserviços via rede Docker compartilhadaentos
- ✅ API RESTful com FastAPI
- ✅ Suporte a operações assíncronas

## 📦 Instalação e Execução

### Pré-requisitos

- Python 3.13+
- Docker e Docker Compose
- Conta no Mercado Pago (para credenciais de API)

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Database
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=db_petshop
DATABASE_URL=postgresql://usuario:senha@localhost:5433/db_petshop
DATABASE_URL_DOCKER=postgresql://usuario:senha@db:5432/db_petshop

# Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN=seu_token_mercado_pago

API_MAIN_URL_DEVELOPMENT="http://schedule_pet_shop_app:8000"
```

### Usando Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/Andremelo001/payments_API.git
cd payments_API

# Crie a rede compartilhada (se ainda não existir)
docker network create shared_network

# Suba os containers
docker-compose up -d

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/Andremelo001/payments_API.git
cd payments_API

# Instale o uv (gerenciador de pacotes)
pip install uv

# Instale as dependências usando uv
uv sync

# Execute a aplicação
uv run uvicorn src.main.server.server:app --reload --port 8000
```

## 🔌 API Endpoints

### 1. Gerar Pagamento

```

```http
POST /payments/generate_payment
Content-Type: application/json

{
  "amount": 100.00,
  "description": "Pagamento de serviço pet shop",
  "email": "cliente@email.com"
}
```

**Resposta de Sucesso:**

```json
{
  "status": "pending",
  "qr_code": "00020126580014br.gov.bcb.pix...",
  "qr_code_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "transaction_id": "123456789"
}
```

### 2. Buscar Pagamento

```http
GET /payments/finder_payment?transaction_id=123456789
```

**Resposta de Sucesso:**

```json
{
  "transaction_id": "123456789",
  "status": "approved",
  "amount": 100.00,
  "description": "Pagamento de serviço pet shop"
}
```

### 3. Webhook Mercado Pago

```http
POST /webhook/mercadopago
Content-Type: application/json

{
  "action": "payment.updated",
  "data": {
    "id": "123456789"
  }
}
```

**Resposta de Sucesso:**

```json
{
  "message": "Webhook processed successfully"
}
```

## 🔗 Integração com API Principal

Este microserviço é consumido pela API de gerenciamento de pet shops:

🔗 [schedule-pet-shop](https://github.com/Andremelo001/schedule-pet-shop)

### Fluxo de Comunicação

A comunicação ocorre através de requisições HTTP em uma arquitetura de microserviços:

**1. Geração de Pagamento:**
- API principal recebe solicitação de pagamento do cliente
- Faz requisição POST para `/payments/generate_payment`
- Recebe QR Code e dados de pagamento
- Retorna informações para o cliente finalizar o pagamento

**2. Notificação de Status (Webhook):**
- Mercado Pago notifica este microserviço via POST em `/webhook/mercadopago`
- Microserviço atualiza status do pagamento no banco de dados
- Microserviço notifica a API principal sobre mudança de status

**3. Consulta de Pagamento:**
- API principal ou cliente podem consultar status via GET em `/payments/finder_payment`
- Retorna informações atualizadas do pagamento

### Comunicação entre Serviços

Os serviços se comunicam através de uma **rede Docker compartilhada** (`shared_network`), permitindo que os containers se comuniquem de forma isolada e segura. A variável `API_MAIN_URL_DEVELOPMENT` define a URL da API principal para notificações de webhook.
3. Recebe QR Code e dados de pagamento
4. Retorna informações para o cliente finalizar o pagamento

## 📚 Aprendizados e Boas Práticas

Este projeto demonstra:

- ✅ Separação de responsabilidades (Single Responsibility Principle)
- ✅ Inversão de dependências (Dependency Inversion Principle)
- ✅ Uso de interfaces para desacoplamento
- ✅ Arquitetura limpa e organizada
- ✅ Padrão de composição de dependências
- ✅ Async/Await para operações não-bloqueantes
- ✅ Containerização com Docker
- ✅ Comunicação entre microserviços

## 👤 Autor

**André Melo**

- GitHub: [@Andremelo001](https://github.com/Andremelo001)
- Projeto Principal: [schedule-pet-shop](https://github.com/Andremelo001/schedule-pet-shop)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!

## 📖 Recursos Adicionais sobre Microserviços

Para aprofundar seus conhecimentos sobre microserviços:

- [Microservices Pattern](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/articles/microservices.html)
- [The Twelve-Factor App](https://12factor.net/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
