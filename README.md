# Sweet Crumbs Bakery — AI Support Chatbot

A custom AI chatbot that answers customer questions for a business — hours, orders, delivery, policies — using a business-specific knowledge prompt instead of generic answers. Runs **entirely locally**, no API keys, no per-message cost.

## What problem this solves

Small businesses lose time answering the same repetitive questions (hours, delivery fees, order process) over and over. This chatbot handles that automatically, in a natural conversational style, while being explicit about what it doesn't know rather than guessing.

## Tech stack

- **Streamlit** — chat UI
- **Ollama** — local LLM (llama3.2 or any model you pull)
- A business-specific **system prompt** that defines tone, facts, and boundaries

## Setup

1. Install [Ollama](https://ollama.com/download) and pull a model:
   ```bash
   ollama pull llama3.2
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run:
   ```bash
   streamlit run chatbot_app.py
   ```

## Customizing for a different business/client

Edit the `BUSINESS_NAME` and `SYSTEM_PROMPT` variables at the top of `chatbot_app.py` — swap in the client's actual hours, products, policies, and tone. That's the entire re-skinning process; no other code changes needed.

---

*This demonstrates the same pattern used for real client work: a conversational AI assistant trained on a business's own information, deployable on WhatsApp, a website widget, or any chat channel.*
