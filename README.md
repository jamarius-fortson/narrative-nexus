# 🚀 NarrativeNexus
### *The Enterprise-Grade Multi-Agent Editorial Engine*

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/nadir-sheikh09)
[![Framework](https://img.shields.io/badge/Orchestration-CrewAI-purple?style=for-the-badge)](https://www.crewai.com/)
[![LLM](https://img.shields.io/badge/Intelligence-DeepSeek--V3%20%7C%20GPT--4o%20%7C%20Claude--3.5-orange?style=for-the-badge)](https://www.deepseek.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Decentralized%20Agents-blue?style=for-the-badge)](#-the-intelligence-nexus)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## ✒️ Executive Summary
**NarrativeNexus** is a production-ready, decentralized multi-agent system designed to mirror the workflow of a high-performance digital newsroom. Built on a foundation of **Sequential Reasoning** and **Strategic Context Handoffs**, NarrativeNexus orchestrates five specialized AI agents to transform raw topics into publication-ready, SEO-optimized, and fact-verified intelligence reports.

Unlike traditional LLM wrappers, NarrativeNexus employs a **Modular Agentic Architecture**, ensuring each piece of content undergoes rigorous research, drafting, executive editing, and integrity verification before final delivery.

---

## 🏗️ Technical Architecture: The Intelligence Pipeline
NarrativeNexus utilizes a sequential process where each agent serves as a node in a professional editorial graph. The output of one agent becomes the foundational context for the next, minimizing hallucinations and maximizing depth.

```mermaid
graph TD
    User([📝 User Input]) --> R1[🔍 Strategic Researcher]
    R1 -->|Structured Research Data| A1[✍️ Narrative Architect]
    A1 -->|Initial Manuscript| E1[📝 Executive Editor]
    E1 -->|Refined Narrative| F1[✅ Integrity Scout]
    F1 -->|Verified Content| S1[📈 Growth Strategist]
    S1 --> Final([🎯 Production-Ready Article])

    subgraph "Core Orchestration (CrewAI)"
    R1
    A1
    E1
    F1
    S1
    end

    style R1 fill:#4f46e5,stroke:#fff,color:#fff
    style A1 fill:#7c3aed,stroke:#fff,color:#fff
    style E1 fill:#db2777,stroke:#fff,color:#fff
    style F1 fill:#059669,stroke:#fff,color:#fff
    style S1 fill:#ea580c,stroke:#fff,color:#fff
    style User fill:#334155,stroke:#fff,color:#fff
    style Final fill:#334155,stroke:#fff,color:#fff
```

---

## 🛠️ The Intelligence Nexus: Agent Personas
| Agent | Role | Strategic Objective |
| :--- | :--- | :--- |
| **Strategic Researcher** | Data Acquisition | Discover high-authority sources and cross-reference real-time statistics. |
| **Narrative Architect** | Synthesis & Writing | Construct compelling narratives using proven storytelling frameworks. |
| **Executive Editor** | Quality Governance | Refine tone, improve structural flow, and ensure brand voice consistency. |
| **Integrity Scout** | Verification | Rigorous fact-checking against external search tools to ensure 100% accuracy. |
| **Growth Strategist** | SEO & Engagement | Optimize for search intent, keyword density, and strategic distribution. |

---

## 🌟 Premium Features
- **🎯 Dynamic Neural Engine Selection**: Switch between **DeepSeek-V3**, **GPT-4o**, and **Claude 3.5 Sonnet** directly from the UI.
- **💎 Glassmorphism Dashboard**: A premium, high-end Streamlit interface designed for modern enterprise workflows.
- **📊 Production Analytics**: Real-time metrics on word velocity, agent sequential steps, and production duration.
- **⭐ Governance Module**: Integrated quality scoring system with linguistic clarity and logical structure metrics.
- **📜 Version Ledger**: Immutable SQLite-backed history tracking for all generated narratives.
- **🛡️ Enterprise Security**: Built-in authentication layer and secure environment variable management.

---

## 🚀 Quick Start & Deployment

### 📋 Prerequisites
- Python 3.12+
- Docker (Optional)
- DeepSeek / OpenAI / Anthropic API Keys

### 🛠️ Local Installation
```bash
# 1. Clone the repository
git clone https://github.com/nadir-sheikh09/NarrativeNexus.git
cd NarrativeNexus

# 2. Virtual Environment Setup
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 3. Dependencies
pip install -r requirements.txt
```

### ⚙️ Configuration
Create a `.env` file in the root directory:
```env
# Multi-Model Support
DEEPSEEK_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Application Settings
ENABLE_AUTH=true
APP_USERNAME=admin
APP_PASSWORD=admin
APP_SECRET_KEY=your_secure_random_string
```

### 🏃 Execution
```bash
streamlit run app.py
```

---

## 🗺️ Product Roadmap
- [ ] **Multi-Modal Integration**: Automated image generation for articles via Flux.1 / DALL-E 3.
- [ ] **Vector Memory (RAG)**: Integration with Pinecone to allow agents to "remember" brand-specific style guides.
- [ ] **CMS Gateways**: One-click deployment to WordPress, Ghost, and Substack APIs.
- [ ] **Real-time Collaboration**: WebSocket integration for multi-user editorial sessions.

---

## 🤝 Contribution Guidelines
We follow a strict **Feature-Branch** workflow. Professional PRs with unit tests are prioritized.
1. Fork the repo.
2. Create your feature branch (`git checkout -b feature/ScaleEnhancement`).
3. Commit follows Conventional Commits specification.
4. Push and open a PR.

---

## 📄 License & Attribution
Distributed under the MIT License.
*Check out my other agentic frameworks on [GitHub](https://github.com/nadir-sheikh09).*

⭐ **Star NarrativeNexus if it powers your content strategy!**
