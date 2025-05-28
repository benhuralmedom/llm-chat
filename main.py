import streamlit as st
import ollama  # pip install ollama streamlit

def main():
    st.set_page_config(page_title="Ollama Chat", page_icon="🤖")
    st.title("Chat with Ollama")

    # Initialize conversation with a system persona prompt
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are an SEP-licensing consultant with deep experience in FRAND negotiations, "
                    "alternative dispute resolution, and collective-bargaining intermediaries (e.g. patent pools "
                    "and licensee negotiation groups). Provide guidance on how an LNG (Licensee Negotiation Group) "
                    "and a facilitator like LINGA operate, how counter-offers and escrow mechanisms work, "
                    "and what risks arise if a licensor insists on litigation instead of ADR."
                )
            }
        ]

    # Render the existing chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Capture user input
    user_input = st.chat_input("Type your question here…")
    if not user_input:
        return

    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Invoke Ollama's chat API
    try:
        response = ollama.chat(
            model="llama3.1",
            messages=st.session_state.messages
        )
        assistant_reply = response.message.content
    except Exception as e:
        assistant_reply = f"Error: {e}"

    # Append and rerun to display assistant reply
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.rerun()

if __name__ == "__main__":
    main()
