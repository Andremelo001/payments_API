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

#### 6. **Comunicação Assíncrona com Message Broker**
- Utiliza **RabbitMQ** para comunicação desacoplada entre microserviços
- Eventos de pagamento são publicados em exchange do tipo **fanout**
- Permite que múltiplos consumidores recebam notificações de mudança de status
- Elimina acoplamento direto entre serviços (não precisa conhecer URLs dos consumidores)
- Garante entrega confiável de mensagens mesmo se consumidores estiverem offline

#### 7. **Tecnologia Heterogênea**
- Liberdade para escolher a stack mais adequada (Python/FastAPI neste caso)
- Enquanto a API principal pode usar outras tecnologias
- Cada microserviço pode evoluir tecnologicamente de forma independente
 

## 🚀 Tecnologias Utilizadas

- **Python 3.13+**
- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM para interação com banco de dados
- **PostgreSQL 15** - Banco de dados relacional
- **RabbitMQ** - Message broker para comunicação assíncrona entre microserviços
- **Pika** - Cliente Python para RabbitMQ
- **Mercado Pago SDK** - Integração para pagamentos PIX
- **Docker & Docker Compose** - Containerização e orquestração
- **Databases** - Suporte assíncrono para PostgreSQL
- **asyncpg** - Driver assíncrono para PostgreSQL
- **uv** - Gerenciador de pacotes Python moderno e rápido

## 📁 Arquitetura do Projeto

O projeto segue uma **arquitetura limpa (Clean Architecture)** organizada em camadas:

```
src/
├── drivers/           # Drivers externos (QR Code, Messaging)
│   ├── messaging/     # RabbitMQ publisher para eventos de pagamento
│   └── qrCode/        # Geração de QR Codes
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
- ✅ Webhook para notificação de mudança de status com validação HMAC-SHA256
- ✅ Consulta de status de pagamentos
- ✅ **Publicação de eventos de pagamento via RabbitMQ** (comunicação assíncrona)
- ✅ Persistência de transações em PostgreSQL
- ✅ API RESTful com FastAPI
- ✅ Suporte completo a operações assíncronas
- ✅ Padrão Singleton para conexão RabbitMQ (otimização de recursos)
- ✅ Context Manager para gerenciamento automático de sessões de banco de dados

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
MERCADOPAGO_WEBHOOK_SECRET=seu_webhook_secret_do_mercado_pago

# RabbitMQ
RABBITMQ_URL=amqps://usuario:senha@host/vhost
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
```

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

A comunicação ocorre de forma **híbrida** combinando requisições HTTP síncronas e mensageria assíncrona:

**1. Geração de Pagamento (HTTP Síncrono):**
- API principal recebe solicitação de pagamento do cliente
- Faz requisição POST para `/payments/generate_payment`
- Recebe QR Code e dados de pagamento
- Retorna informações para o cliente finalizar o pagamento

**2. Notificação de Status (Webhook + RabbitMQ Assíncrono):**
- Mercado Pago notifica este microserviço via POST em `/webhook/mercadopago`
- Webhook valida autenticidade da requisição via **HMAC-SHA256**
- Microserviço atualiza status do pagamento no banco de dados PostgreSQL
- **Publica evento de pagamento no RabbitMQ** (exchange fanout)
- API principal consome mensagem da fila e processa mudança de status
- **Vantagem**: Desacoplamento total - se API principal estiver offline, mensagem fica na fila

**3. Consulta de Pagamento (HTTP Síncrono):**
- API principal ou cliente podem consultar status via GET em `/payments/finder_payment`
- Retorna informações atualizadas do pagamento



#### 🐰 RabbitMQ (CloudAMQP)
- **Exchange**: `payment_events` (tipo fanout)
- **Pattern**: Publish/Subscribe
- **Garantias**: Persistência de mensagens (`delivery_mode=2`)
- **Otimização**: Singleton pattern para reutilização de conexão
- **Benefícios**: 
  - Comunicação assíncrona e desacoplada
  - Tolerância a falhas (mensagens persistidas)
  - Múltiplos consumidores podem receber eventos
  - Redução de latência (~90% mais rápido que criar nova conexão a cada webhook)

## 📚 Aprendizados e Boas Práticas

Este projeto demonstra:

- ✅ Separação de responsabilidades (Single Responsibility Principle)
- ✅ Inversão de dependências (Dependency Inversion Principle)
- ✅ Uso de interfaces para desacoplamento
- ✅ Arquitetura limpa e organizada
- ✅ Padrão de composição de dependências
- ✅ Padrões de otimização (Singleton, Connection Pooling, Context Manager)
- ✅ Message Broker para comunicação assíncrona entre microserviços
- ✅ Async/Await para operações não-bloqueantes
- ✅ Containerização com Docker
- ✅ Segurança em webhooks com validação criptográfica

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
