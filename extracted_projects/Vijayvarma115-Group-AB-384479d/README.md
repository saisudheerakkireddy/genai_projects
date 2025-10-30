***

# RAG-Enabled Agentic AI Conversational Assistant for Intelligent Customer Support

## Overview

This project delivers an open-source conversational AI assistant designed for modern customer support, combining Retrieval-Augmented Generation (RAG), agentic workflows, and seamless human handoff. It integrates with leading open-source tools like Chatwoot (for customer messaging and live agent handoff), n8n (for workflow automation), Pipecat (for voice AI pipelines), and LiveKit (for real-time voice transport), delivering scalable, cost-effective intelligent support across text and, eventually, voice channels.

***

## Problem Statement

Most customer service bots fail to provide personalized, human-like support for complex queries, and often lack seamless escalation to human agents. Voice support and hybrid automation–human workflows are rarely efficiently combined in current open platforms. This project solves these challenges by building a modular, agentic system that:

- Autonomously resolves customer queries with RAG-based, contextual AI.
- Seamlessly transfers conversations to human agents on Chatwoot based on configurable triggers, and returns to automation when human intervention is complete.
- Is designed for future extension to real-time voice interactions using ultra-low-latency streaming and speech technologies.

***

## Project Objectives

- **Autonomous Query Resolution:** RAG-powered LLM chatbot delivers accurate, contextually grounded responses.
- **Intelligent Human Handoff:** Automated detection and routing for complex, sentiment-driven, or user-requested escalations to human agents.
- **Workflow Continuity:** Automated return to bot after human resolution, closing the loop and ensuring complete customer journey coverage.
- **Voice Agent Extension (Planned):** Voice pipeline integration for real-time speech support, with the same agentic handoff and RAG context.

***

## Architecture

### Phase 1: RAG-Based Text Chatbot with Human Handoff

| Layer         | Tool/Technology                                   |
|---------------|---------------------------------------------------|
| Messaging     | Chatwoot                                          |
| Orchestration | n8n                                               |
| RAG/Vector DB | FAISS / Pinecone / ChromaDB                       |
| LLM           | GPT-4 / Llama 3 / Mistral                         |

- **Chatwoot:** Multichannel messaging, agent dashboards, and agent routing.
- **n8n:** Modular, no-code workflows for RAG, API integration, and agent handoff logic.
- **RAG Layer:** Semantic search over knowledge base (FAQs/tickets/policies).
- **Agentic AI:** Multi-step planning, validation, and tool-augmented actions.
- **Human Handoff:** Triggered by low confidence, keywords, sentiment, or unresolved intent—automatically assigning to agents via Chatwoot.

### Phase 2: Voice Agent Integration (Planned)

| Layer           | Tool/Technology                          |
|-----------------|------------------------------------------|
| Voice Pipeline  | Pipecat                                  |
| Real-time Voice | LiveKit                                  |
| STT             | Whisper / AssemblyAI / Deepgram          |
| TTS             | Cartesia / ElevenLabs / Coqui TTS        |
| NLU/DM          | Rasa / spaCy (optional)                  |

- Real-time speech pipeline for customer calls, with RAG-powered conversational context and automated handoff to live agents when needed.

***

## Key Features

- Modular open-source architecture (cloud or on-premise).
- Scalable vector database for fast RAG context.
- Seamless, configurable escalation to human support.
- Future-proof: Designed for easy extension to full voice agent flows.
- Cost-effective: All core components are open-source, licensing optional for advanced LLMs/APIs.

***

## Setup & Installation

### Prerequisites

- Docker & Docker Compose (for easy deployment)
- Accounts/Keys for any cloud APIs or LLM providers (if not using only open-source LLMs)
- Node.js and npm/yarn (for n8n workflows if running from source)
- Optional: Python for FAISS/ChromaDB indexing scripts

### Core Services Used

- [Chatwoot](https://www.chatwoot.com/) – Customer conversation & agent management.
- [n8n](https://n8n.io/) – Workflow orchestration and RAG logic.
- [FAISS](https://github.com/facebookresearch/faiss), [Pinecone](https://www.pinecone.io/), or [ChromaDB](https://www.trychroma.com/) – Vector DB for semantic document retrieval.
- [OpenAI GPT-4](https://openai.com/), [Llama 3](https://llama.meta.com/llama3/), [Mistral](https://mistral.ai/) – LLM backends.
- Vapi.ai [Pipecat](https://github.com/pipecat-ai/pipecat), [LiveKit](https://livekit.io/) for real-time voice support.

### Quick Start (Docker Compose)

1. **Clone the Repository**
   ```sh
   git clone <your-repo-url>
   cd <your-repo>
   ```

2. **Configure Environment Variables**
   - Copy `file.env` to `.env`
   - Set Chatwoot, n8n, LLM, and vector DB keys as needed.

3. **Start the Core Services**
   ```sh
   docker-compose up -d
   ```

4. **Import/Configure n8n Workflows**
   - Open n8n dashboard
   - Import prebuilt RAG and handoff workflows, configure endpoints for Chatwoot/LLM/vector DB.

5. **Configure Chatwoot**
   - Add channels (web, WhatsApp, email, etc.)
   - Set up your agent teams and automation triggers.

6. **Test Locally**
   - Use the included `index.html` local test page to trigger chatbot via Chatwoot widget.
   - Confirm handoff triggers and full workflow execution.

### Extending to Voice (Phase 2)

- Add Pipecat and LiveKit services to the Docker Compose stack.
- Configure integration with n8n for voice event triggers.

***

## Example Workflow

1. **User Message:** Enters via Chatwoot widget/channel.
2. **n8n Workflow:** Receives webhook, preprocesses query, triggers semantic document retrieval.
3. **LLM:** Consumes RAG-augmented prompt; generates grounded response.
4. **Human Handoff (if needed):** Triggered by confidence score, keywords, user request, or sentiment.
5. **Agent Handles Conversation:** Chatwoot routes to live agent.
6. **Return to Bot:** After agent resolution, bot follows up if needed.
7. **(Planned) Voice Conversion:** All logic above extended to real-time speech interaction.

***

## Contributing

Contributions, feature requests, and feedback are welcome via Issues/PRs!

- To add a new vector DB, LLM, or channel, follow the modular guidelines in `n8n` workflow examples.
- Document new workflow patterns or voice extensions in `/docs`.

***

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

***

## Acknowledgements

- Open-source communities of Chatwoot, n8n, Pipecat, LiveKit, FAISS, Pinecone, ChromaDB, OpenAI, Meta AI, Mistral.
- Inspiration from pioneering hybrid AI-human customer service architectures.

***

## Project Status

- **Phase 1:** RAG chatbot with human handoff via Chatwoot and n8n — functional.
- **Phase 2:** Voice support via Pipecat + LiveKit — in progress/planned.

***

## Short Description

"This project builds an open-source RAG-enabled agentic AI chatbot with intelligent human handoff using Chatwoot and n8n, extending to real-time voice agents via Pipecat and LiveKit. The system autonomously resolves customer queries, seamlessly transfers complex cases to human agents, and provides voice-based conversational support for scalable, accessible customer service."

---
Screenshot's:

<img width="1919" height="971" alt="image" src="https://github.com/user-attachments/assets/468f2b8a-886e-48fd-95fa-6176a00c21f4" />



<img width="1919" height="970" alt="image" src="https://github.com/user-attachments/assets/b8a1a39d-f0ac-44a6-af13-15a1b04678b9" />


<img width="1549" height="548" alt="image" src="https://github.com/user-attachments/assets/5f2dd9a8-44d2-4eb2-b266-60909aac4f20" />



