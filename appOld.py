import streamlit as st

# -----------------------
# INTENCIONES
# -----------------------
intents = {
    "saludo": {
        "patterns": ["hola", "buenos días", "hi"],
        "responses": ["Hola, ¿en qué puedo ayudarte?"]
    },
    "despedida": {
        "patterns": ["adiós", "bye"],
        "responses": ["Hasta luego, que tengas un buen día"]
    },
    "horario": {
        "patterns": ["horario", "horas", "abren"],
        "responses": ["Nuestro horario es de 9am a 6pm"]
    },
    "servicios": {
        "patterns": ["servicios", "qué hacen"],
        "responses": ["Ofrecemos soporte técnico y desarrollo de software"]
    },
    "ubicacion": {
        "patterns": ["dónde están", "ubicación"],
        "responses": ["Estamos ubicados en Monterrey, México"]
    }
}

fallback_response = "Lo siento, no entendí tu pregunta. ¿Puedes reformularla?"

# -----------------------
# FUNCIONES NLP
# -----------------------
def match_intent(user_input):
    user_input = user_input.lower()
    for intent, data in intents.items():
        for pattern in data["patterns"]:
            if pattern in user_input:
                return intent
    return "fallback"

# -----------------------
# STREAMLIT UI
# -----------------------
st.title("Chatbot IA ")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Escribe tu mensaje:")

if st.button("Enviar"):
    intent = match_intent(user_input)

    if intent != "fallback":
        response = intents[intent]["responses"][0]
    else:
        response = fallback_response

    st.session_state.history.append(("Usuario", user_input))
    st.session_state.history.append(("Bot", response))

# Mostrar historial
for speaker, msg in st.session_state.history:
    st.write(f"**{speaker}:** {msg}")

# Evaluación
st.subheader("Evaluación")
rating = st.slider("¿Qué tan útil fue la respuesta?", 1, 5)

if st.button("Enviar evaluación"):
    st.success("Gracias por tu feedback")