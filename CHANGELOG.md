# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-03-27

### Rebranding & Major Upgrades
- Project rebranded to **NarrativeNexus**.
- Overhauled UI with a **Premium Glassmorphism Design System** (Outfit & Inter fonts).
- Implemented **Dynamic Neural Engine Selection** (DeepSeek-V3, GPT-4o, Claude 3.5 Sonnet).
- Integrated **langchain-anthropic** for native Claude 3.5 support.
- Enhanced Agent backstories and task expectations for enterprise-grade output.
- Upgraded Content Versioning to track production analytics (word count, step velocity).

### Fixed
- Improved error handling for search tool timeouts.
- Resolved session state persistence issues in Streamlit during long generation cycles.

## [1.0.0] - 2026-01-29

### Added
- Initial release of AI Content Generation Pipeline
- Multi-agent orchestration with CrewAI
- Integration with DeepSeek-V3 LLM
- Premium Streamlit UI with dark mode
- DuckDuckGo search integration for research
- Quality scoring system for generated content
- Content versioning and history tracking
- Comprehensive documentation (README, DEPLOYMENT, CONTRIBUTING)
- Docker and docker-compose support
- GitHub Actions CI/CD pipeline
- MIT License

### Features
- 5 specialized AI agents (Researcher, Writer, Editor, Fact Checker, SEO Specialist)
- Sequential workflow with context passing
- Real-time progress monitoring
- Markdown export functionality
- Environment variable configuration

### Documentation
- Professional README with badges
- Deployment guide for multiple platforms
- Contributing guidelines
- Code of Conduct
- Example environment file

### DevOps
- Automated CI/CD with GitHub Actions
- Docker containerization
- Security scanning with Bandit
- Code quality checks with flake8 and black

---

For more details, see the [GitHub Releases](https://github.com/nadir-sheikh09/NarrativeNexus/releases) page.
