# Protein Electrophoresis Agent

> **Domain:** Computational Biology & AI Drug Discovery  
> **Reference Guidelines & Standards:** `wwPDB, IUPAC & CLSI Computational Guidelines`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Protein Electrophoresis Agent** is an advanced analytical and computational platform implementing Serum & Urine SPEP/UPEP M-Spike Densitometry Agent. It provides multi-agent consensus evaluation of protein electrophoresis data with enterprise-grade security features.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`Severity`** — dedicated module for severity evaluation and state verification.
- **`DomainKnowledgeRegistry`**: Enterprise domain rules, guideline matrices, and evidence benchmarks.
- **`AgentAlert`** — dedicated module for agent alert evaluation and state verification.
- **`MSpikeDensitometryAgent`**: Specialized Sub-Agent 1 for protein-electrophoresis-agent
- **`ImmunofixationMatcherAgent`**: Specialized Sub-Agent 2 for protein-electrophoresis-agent
- **`FreeLightChainAuditorAgent`**: Specialized Sub-Agent 3 for protein-electrophoresis-agent

---

## 💻 CLI Quickstart & Usage

### Installation

```bash
pip install -e .
```

### 1. Guided Interactive Mode
```bash
python cli.py
```

### 2. Direct Parameterized Evaluation
```bash
python cli.py --task-id <value> --target <value> --primary <value> --secondary <value>
```

### 3. Available Commands

| Command | Description |
|:--------|:------------|
| `audit` | Run single task evaluation |
| `chat` | System configuration query |
| `batch` | Batch process CSV records |
| `verify-audit` | Verify HMAC audit trail integrity |
| `serve` | Launch FastAPI REST server |

### Parameter Reference
- `--task-id`: Specifies input measurement or parameter value.
- `--target`: Specifies input measurement or parameter value.
- `--primary`: Specifies input measurement or parameter value.
- `--secondary`: Specifies input measurement or parameter value.
- `--critical`: Specifies input measurement or parameter value.
- `--status`: Specifies input measurement or parameter value.
- `--input`: Specifies input measurement or parameter value.
- `--output`: Specifies input measurement or parameter value.

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `case_id` | Parameter / observation metric | Required |
| `patient_synthetic_id` | Parameter / observation metric | Required |
| `metric_primary` | Parameter / observation metric | Required |
| `metric_secondary` | Parameter / observation metric | Required |
| `is_stat` | Parameter / observation metric | Required |
| `status_flag` | Parameter / observation metric | Required |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Configuration

Set the `AUDIT_SECRET_KEY` environment variable for persistent audit integrity across restarts:

```bash
export AUDIT_SECRET_KEY="your-secure-random-key"
```

If not set, a transient ephemeral key will be generated (with a warning).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py --tasks 1000 --concurrency 8
```

---

## 🐳 Container Deployment

```bash
docker build -t protein-electrophoresis-agent .
docker run -p 8000:8000 protein-electrophoresis-agent
```

---

## 📁 Project Structure

```
protein-electrophoresis-agent/
├── agents/                          # Core agent package
│   ├── __init__.py
│   ├── api.py                       # FastAPI REST API
│   ├── base.py                      # Security, PHI Guard, Audit Trail
│   ├── learning.py                  # Bayesian Calibration Engine
│   ├── llm_factory.py               # LLM Client Factory
│   ├── metrics.py                   # Prometheus Metrics
│   ├── models.py                    # Pydantic Data Models
│   ├── streamer.py                  # WebSocket Telemetry
│   ├── supervisor.py                # Supervisor Orchestrator
│   └── workers.py                   # Domain Worker Agents
├── protein_electrophoresis_agent/   # Clinical agent package
│   ├── __init__.py
│   ├── agents.py                    # Distributed Component Hierarchy
│   ├── cli.py                       # Clinical CLI
│   ├── engine.py                    # Clinical Algorithmic Engine
│   ├── models.py                    # Clinical Data Models
│   └── server.py                    # Clinical FastAPI Server
├── tests/                           # Test suite
│   ├── test_enrichment.py
│   ├── test_protein_electrophoresis_agent.py
│   └── test_protein_electrophoresis_agent_pkg.py
├── cli.py                           # Main CLI entry point
├── enrichment.py                    # Enrichment Feature Implementation
├── simulator.py                     # Traffic & Stress Testing Simulator
├── spep_mind.py                     # SpepMind CLI & API
├── pyproject.toml                   # Project configuration
├── Dockerfile                       # Container configuration
└── docker-compose.yml               # Docker Compose configuration
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
