# FinVerse

**Event-Driven Finance, Investing, and Commerce Platform**

FinVerse is a **distributed, event-driven financial platform** that unifies **personal banking**, **investment analytics**, and **light e-commerce insights** into a single system.

The project is designed to demonstrate **backend systems engineering, data pipelines, and scalable architecture** using modern industry tools such as **Kafka, Databricks / Delta Lake, and FastAPI**.

> ⚠️ This is a **simulation platform** (no real money movement). It focuses on system design, correctness, and scalability rather than financial compliance.

---

## 🚀 Motivation / Use Case

Modern financial products are no longer isolated:

- Banking apps track spending
- Brokerages track portfolios
- Commerce platforms track purchases

**FinVerse unifies these domains** and treats all user activity as **immutable events** flowing through a central log, enabling reliable analytics, alerts, and predictions.

---

## 🧠 Core Concepts

- Event-driven architecture (append-only, immutable events)
- Separation of concerns:
  - OLTP (commands, authentication, metadata)
  - OLAP (analytics, aggregates, ML)
- Bronze → Silver → Gold lakehouse pattern
- Eventual consistency
- Replayable data pipelines

---

## 🏗️ High-Level Architecture

```
Client (Web)
↓
FastAPI (API Gateway)
↓
Kafka (Event Log / Source of Truth)
↓
Spark / Databricks
↓
Delta Lake (Bronze → Silver → Gold)
↓
Analytics APIs / Alerts / ML Models
```

---

## 🔧 Tech Stack

### Backend & Systems

- FastAPI (async API gateway)
- Apache Kafka (event streaming)
- PostgreSQL (users, metadata, idempotency)
- Redis (optional caching)

### Data & Analytics

- Apache Spark / Databricks
- Delta Lake
- MLflow (model tracking)

### Infra & Tooling

- Docker & Docker Compose
- GitHub Actions (CI)
- Terraform (optional IaC)

---

## 📦 Domain Features

### 1️⃣ Banking (FinTech)

- Multi-account support (checking, savings, credit)
- Ledger-style transactions (append-only)
- Budget tracking by category
- Spending alerts

### 2️⃣ Investing (Stocks)

- Portfolio holdings (paper trading)
- Market price ingestion
- Portfolio analytics (ROI, allocation, volatility)
- Price and risk alerts

### 3️⃣ Light E-Commerce

- Purchase tracking
- Merchant-level analytics
- Cashback / reward calculation
- Subscription detection

---

## 📊 Data Engineering Pipeline

### Bronze (Raw)

- Raw Kafka events
- No validation or mutation
- Append-only JSON / Delta

### Silver (Cleaned)

- Schema validation
- Normalized timestamps
- Enriched categories and merchants

### Gold (Analytics)

- Daily balances
- Spend by category
- Portfolio value over time
- Cashback summaries

---

## 👤 User Use Cases

### 🧑‍💼 Use Case 1: User Login & Dashboard

1. User logs in via the web app
2. FastAPI authenticates the user (JWT)
3. Dashboard requests:
   - Current balances
   - Portfolio value
   - Month-to-date spending
4. Backend serves data from **Gold tables**

---

### 💳 Use Case 2: User Makes a Purchase

1. User records a purchase (e.g. `$120` at _Amazon_)
2. FastAPI validates the request
3. A `transaction_created` event is published to Kafka
4. Consumers:
   - Persist raw data to **Bronze**
   - Transform data into **Silver**
   - Update aggregates in **Gold**
5. Budget service emits an alert if thresholds are exceeded

---

### 📈 Use Case 3: User Buys a Stock (Paper Trade)

1. User submits a buy order (e.g. `AAPL`, `5` shares)
2. FastAPI emits a `portfolio_trade_executed` event
3. Market price events are ingested independently
4. Spark jobs join trades with prices
5. Portfolio value is recomputed in **Gold**
6. Dashboard updates asynchronously

---

### 🛒 Use Case 4: Cashback & Merchant Analytics

1. Purchase event enters the system
2. Silver layer assigns merchant category
3. Gold aggregation computes cashback
4. User views:
   - Cashback earned this month
   - Top merchants by spend

---

### 🚨 Use Case 5: Alerts & Anomaly Detection

1. Transaction events are scored by rules or ML
2. Suspicious activity emits an `alert_created` event
3. Alert service stores alert metadata
4. User receives a dashboard notification

---

## 🧪 Local Development

```bash
docker-compose up --build
```

- API: http://localhost:8000
- Kafka UI (optional): http://localhost:8080

## 📁 Repository Structure

```
finverse/
  backend/        # FastAPI services
  kafka/          # Producers & consumers
  databricks/     # Spark jobs & pipelines
  data/
    bronze/
    silver/
    gold/
  infra/          # Docker / Terraform
  docs/           # Architecture & tradeoffs
```

## 📈 What This Project Demonstrates

- Event-driven system design
- Financial data correctness over time
- Separation of read and write paths
- Scalable analytics architecture
- Real-world engineering tradeoffs

## 🧠 Design Tradeoffs

- Kafka as source of truth: replayability and decoupling
- Append-only data model: auditability and correctness
- Eventual consistency: scalability over synchronous writes
- Lakehouse architecture: unified batch and streaming analytics

## ⚠️ Disclaimer

FinVerse is a simulation platform built for learning and portfolio demonstration purposes only.
It does not move real money or integrate with real financial institutions.
