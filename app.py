import streamlit as st
import pandas as pd
import json
import os
from dotenv import load_dotenv
from openai import OpenAI  
from pycaret.regression import load_model, predict_model
from halfmarathon_langfuse import Langfuse  


# Ładowanie zmiennych środowiskowych

load_dotenv()


# Inicjalizacja klientów

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL")
)


# Ładowanie modelu pycaret

model = load_model("models/halfmarathon_model")

st.title(":running_woman: Halfmarathon Finish Time Predictor")

user_text = st.text_area(
    ":raised_hand: Opisz siebie - podaj wiek, płeć i swój najlepszy czas na 5 km. Sztuczna inteligencja przeanalizuje twój opis i przewidzi czas na półmaraton!",
    placeholder="Mam 30 lat, jestem kobietą, 5 km biegnę w 25 minut"
)

if st.button("Przewiduj"):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Wyłuskaj dane z tekstu i zwróć tylko i wyłącznie JSON:
                    {{
                        "gender": 0,
                        "age": 0,
                        "time_5km_sec": 0
                    }}
                    Oznaczenie płci: kobieta 1, mężczyzna 0
                    Czas na 5 km zawsze zwróć w sekundach, niezależnie od formatu wejściowego.
                    Jeśli brakuje danych zwróć null dla danego pola.
                    Jeśli wiek powyżej 120 lat, to upewnij się o poprawność danych.

                    Tekst: {user_text}
                    """
                }
            ]
        )
        

        # Wyciągnięcie tekstu z odpowiedzi OpenAI

        ai_output = response.choices[0].message.content
        data = json.loads(ai_output)
        
        langfuse_client.event(
            name="runner-analysis",
            input=user_text,
            output=data
        )
        langfuse_client.flush()
        

        # Walidacja - obsługa wartości None/null z JSON-a

        if data.get("time_5km_sec") is None or data["time_5km_sec"] <= 0:
            st.error(":triangular_flag_on_post: Brakuje danych o czasie lub czas jest niepoprawny.")
            st.stop()

        if data.get("age") is None or data["age"] <= 0:
            st.error(":triangular_flag_on_post: Brakuje danych o wieku lub wiek jest niepoprawny.")
            st.stop()

        if data.get("gender") is None or data["gender"] not in [0, 1]:
            st.error(":triangular_flag_on_post: Brakuje danych o płci.")
            st.stop()


        # Przygotowanie danych dla PyCaret

        test_runner = pd.DataFrame({
            "gender": [data["gender"]],
            "age": [data["age"]],
            "time_5km_sec": [data["time_5km_sec"]]
        })


        # Predykcja modelu
        
        prediction = predict_model(
            model,
            data=test_runner
        )

        wynik = prediction["prediction_label"].iloc[0]


        # Konwersja sekund na format HH:MM:SS
        
        hours = int(wynik // 3600)
        minutes = int((wynik % 3600) // 60)
        seconds = int(wynik % 60)

        st.success(":tada: Predykcja wykonana.")

        st.write(
            f"Przewidywany czas półmaratonu: "
            f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )

        with st.expander("Dane odczytane przez AI"):
            st.json(data)

    except Exception as e:
        st.error(f"Błąd: {str(e)}")