"""
Simple Customer Support Chatbot — powered by a local LLM via Ollama.

No embeddings, no vector database — just a clean, fast chat interface
with a business-specific system prompt, so it stays on-topic and answers
like a real support agent for one business.
"""

import streamlit as st
import ollama

st.set_page_config(page_title="Support Chatbot", page_icon="🧁", layout="centered")

# ---------------------------------------------------------------------------
# Business info — edit this block to re-skin the bot for any business
# ---------------------------------------------------------------------------
BUSINESS_NAME = "Sweet Crumbs Bakery"
SYSTEM_PROMPT = f"""You are a friendly, helpful customer support assistant for {BUSINESS_NAME}, a bakery.

Business facts you know:
- Hours: Tuesday–Sunday, 8 AM – 6 PM. Closed Mondays.
- Location: 42 Baker Street, Lahore.
- Popular items: custom birthday cakes, croissants, sourdough bread, cupcakes.
- Custom cake orders need 48 hours notice.
- Delivery available within 10km for a flat PKR 300 fee; free pickup in-store.
- Payment: cash, card, and bank transfer on delivery.
- Allergen note: all baked goods are made in a kitchen that also processes nuts and dairy.

Rules:
- Be warm, concise, and helpful — like a real staff member, not a generic bot.
- If you don't know something specific (e.g. exact pricing for a custom design), say so
  and suggest the customer call the bakery directly rather than guessing.
- Never make up facts that aren't listed above.
"""

LLM_MODEL = "llama3.2"  # change to llama3.2:1b for a faster, lighter model

st.title(f"🧁 {BUSINESS_NAME} — Support Chat")
st.caption("Ask about hours, orders, delivery, or anything else — runs on a local AI model, no API costs.")

# ---------------------------------------------------------------------------
# Chat state
# ---------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": f"Hi! Welcome to {BUSINESS_NAME} 👋 How can I help you today?"}
    ]

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your question...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🤔 Thinking...")
        full_response = ""

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history
        ]

        try:
            stream = ollama.chat(
                model=LLM_MODEL,
                messages=messages,
                options={"num_predict": 300, "temperature": 0.4},
                stream=True,
            )
            for part in stream:
                token = part["message"]["content"]
                if token:
                    full_response += token
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            full_response = (
                "⚠️ Couldn't reach the local model. Make sure Ollama is running "
                f"(`ollama serve`) and the model is pulled with `ollama pull {LLM_MODEL}`.\n\nError: {e}"
            )
            placeholder.markdown(full_response)

    st.session_state.chat_history.append({"role": "assistant", "content": full_response})

with st.sidebar:
    st.header("About this demo")
    st.markdown(
        f"This is a **custom AI support chatbot** built for {BUSINESS_NAME}. "
        "It runs entirely on a local AI model — no per-message API cost — "
        "and can be re-skinned for any business by editing the system prompt."
    )
    if st.button("Clear conversation"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": f"Hi! Welcome to {BUSINESS_NAME} 👋 How can I help you today?"}
        ]
        st.rerun()
