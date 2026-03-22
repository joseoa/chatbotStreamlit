import streamlit as st
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# CONFIG
# -----------------------------
DATA_PATH = "training_data.csv"

# -----------------------------
# DATASET INICIAL
# -----------------------------
def init_data():
    if not os.path.exists(DATA_PATH):
        data = pd.DataFrame({
            "text": [
                "hola", "buenos dias", "hi",
                "adios", "bye",
                "horario", "horas de atencion",
                "servicios", "que hacen",
                "donde estan", "ubicacion"
            ],
            "intent": [
                "saludo","saludo","saludo",
                "despedida","despedida",
                "horario","horario",
                "servicios","servicios",
                "ubicacion","ubicacion"
            ]
        })
        data.to_csv(DATA_PATH, index=False)

# -----------------------------
# RESPUESTAS
# -----------------------------
responses = {
    "saludo": "Hola, ¿en qué puedo ayudarte?",
    "despedida": "Hasta luego",
    "horario": "Nuestro horario es de 9am a 6pm",
    "servicios": "Ofrecemos desarrollo de software e IA",
    "ubicacion": "Estamos en Monterrey, México",
    "fallback": "No entendí tu pregunta"
}

# -----------------------------
# ENTRENAR MODELO
# -----------------------------
def train_model():
    df = pd.read_csv(DATA_PATH)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["text"])

    return vectorizer, X, df

# -----------------------------
# PREDECIR INTENCION
# -----------------------------
def predict_intent(user_input, vectorizer, X, df):
    user_vec = vectorizer.transform([user_input])

    similarity = cosine_similarity(user_vec, X)
    best_score = similarity.max()
    best_index = similarity.argmax()

    if best_score < 0.3:
        return "fallback", best_score

    return df.iloc[best_index]["intent"], best_score

# -----------------------------
# AGREGAR NUEVO EJEMPLO
# -----------------------------
def learn_new_example(text, intent):
    df = pd.read_csv(DATA_PATH)

    new_row = pd.DataFrame({
        "text": [text],
        "intent": [intent]
    })

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

# -----------------------------
# UI STREAMLIT
# -----------------------------
st.title("Chatbot con Machine Learning")

init_data()

# Estado
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

if "last_intent" not in st.session_state:
    st.session_state.last_intent = ""

# Entrenar modelo
vectorizer, X, df = train_model()

# -----------------------------
# FUNCION ENVIAR
# -----------------------------
def enviar():
    user_input = st.session_state.user_input

    intent, score = predict_intent(user_input, vectorizer, X, df)

    response = responses.get(intent, responses["fallback"])

    st.session_state.history.append(("Usuario", user_input))
    st.session_state.history.append(("Bot", f"{response} (confianza: {score:.2f})"))

    st.session_state.last_input = user_input
    st.session_state.last_intent = intent

    # limpiar input
    st.session_state.user_input = ""

# -----------------------------
# INPUT
# -----------------------------
st.text_input("Escribe tu mensaje:", key="user_input")
st.button("Enviar", on_click=enviar)

# -----------------------------
# HISTORIAL
# -----------------------------
st.subheader("Conversación")
for speaker, msg in st.session_state.history:
    st.write(f"**{speaker}:** {msg}")

# -----------------------------
# FEEDBACK
# -----------------------------
st.subheader("Evaluación")

rating = st.slider("¿La respuesta fue útil?", 1, 5)

correct_intent = st.selectbox(
    "¿Cuál era la intención correcta?",
    ["saludo", "despedida", "horario", "servicios", "ubicacion"]
)

if st.button("Enviar feedback"):

    if rating <= 2:
        st.warning("Aprendiendo de este error...")

        # aprender nuevo patrón
        learn_new_example(st.session_state.last_input, correct_intent)

    else:
        st.success("Gracias por tu feedback")