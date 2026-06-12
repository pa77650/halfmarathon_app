🏃‍♀️Kalkulator czasu półmaratonu "Halfmarathon Finish Time Predictor"

Aplikacja pozwala biegaczowi wpisać naturalnym językiem podstawowe informacje o sobie (np. "Mam 30 lat, jestem kobietą, 5 km biegam w 22 minuty"). 

:point_right:Cel aplikacji

System automatycznie wyciąga z tego tekstu wpisanego przez użytkownika kluczowe parametry, a następnie precyzyjnie oblicza prognozowany czas ukończenia półmaratonu. Model ML wytrenowane na podstawie danych z Półmaratonu Wrocławskiego 2023 i 2024 (ok. 21 000 wyników).

:point_right:Technologia

Python - główny język programowania projektu.
Streamlit - framework do szybkiego tworzenia aplikacji webowej bezpośrednio w Pythonie.
OpenAI API (GPT-4o-mini) - model językowy (LLM) odpowiedzialny za przetwarzanie tekstu naturalnego i wyciąganie z niego ustrukturyzowanych danych do formatu JSON.
PyCaret - biblioteka Machine Learning typu AutoML. Służy do załadowania wcześniej wytrenowanego modelu regresyjnego (halfmarathon_model) i generowania predykcji.
Pandas - biblioteka do manipulacji danymi, służąca do konwersji danych z JSON na tabelę (DataFrame) akceptowaną przez model ML.
Langfuse - narzędzie klasy LLMOps do monitorowania, śledzenia kosztów tokenów oraz debugowania zapytań wysyłanych do OpenAI.
Dotenv (python-dotenv) - biblioteka do bezpiecznego zarządzania kluczami API i zmiennymi środowiskowymi z pliku .env.
