from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

with open("modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


@app.route("/")
def home():
    return "API rodando!"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Validar ranges dos valores numéricos
    validations = {
        "Age": {"min": 5, "max": 100},
        "PlayTimeHours": {"min": 0, "max": 10000},
        "InGamePurchases": {"min": 0, "max": 100000},
        "SessionsPerWeek": {"min": 0, "max": 168},
        "AvgSessionDurationMinutes": {"min": 1, "max": 1440},
        "PlayerLevel": {"min": 1, "max": 999},
        "AchievementsUnlocked": {"min": 0, "max": 10000},
    }

    # Validar cada campo numérico
    for field, range_limits in validations.items():
        try:
            value = float(data.get(field, -1))
            if value < range_limits["min"] or value > range_limits["max"]:
                return jsonify(
                    {"error": f"{field} deve estar entre {range_limits['min']} e {range_limits['max']}"}
                ), 400
        except (ValueError, TypeError):
            return jsonify({"error": f"{field} deve ser um número válido"}), 400

    # Validar campos categóricos
    valid_genders = {"Male", "Female"}
    valid_difficulties = {"Easy", "Medium", "Hard"}
    valid_locations = {"USA", "Europe", "Asia", "Other"}
    valid_genres = {"Action", "Sports", "RPG", "Strategy", "Simulation"}

    if data.get("Gender") not in valid_genders:
        return jsonify({"error": "Gênero inválido"}), 400
    if data.get("GameDifficulty") not in valid_difficulties:
        return jsonify({"error": "Dificuldade inválida"}), 400
    if data.get("Location") not in valid_locations:
        return jsonify({"error": "Localização inválida"}), 400
    if data.get("GameGenre") not in valid_genres:
        return jsonify({"error": "Gênero de jogo inválido"}), 400

    # Montar DataFrame com os mesmos nomes do notebook
    df = pd.DataFrame(
        [
            {
                "Age": data["Age"],
                "Gender": data["Gender"],
                "PlayTimeHours": data["PlayTimeHours"],
                "InGamePurchases": data["InGamePurchases"],
                "GameDifficulty": data["GameDifficulty"],
                "SessionsPerWeek": data["SessionsPerWeek"],
                "AvgSessionDurationMinutes": data["AvgSessionDurationMinutes"],
                "PlayerLevel": data["PlayerLevel"],
                "AchievementsUnlocked": data["AchievementsUnlocked"],
                "Location": data["Location"],
                "GameGenre": data["GameGenre"],
            }
        ]
    )

    # Mesmo encoding do notebook
    df["Gender"] = df["Gender"].map({"Female": 0, "Male": 1})
    df["GameDifficulty"] = df["GameDifficulty"].map({"Easy": 0, "Medium": 1, "Hard": 2})
    df = pd.get_dummies(df, columns=["Location"], dtype=int)
    df = pd.get_dummies(df, columns=["GameGenre"], dtype=int)

    # Garantir que todas as colunas existam (mesmo que o usuário
    # não tenha escolhido todas as categorias, as colunas one-hot
    # precisam existir com valor 0)
    expected_columns = [
        "Age",
        "Gender",
        "PlayTimeHours",
        "InGamePurchases",
        "GameDifficulty",
        "SessionsPerWeek",
        "AvgSessionDurationMinutes",
        "PlayerLevel",
        "AchievementsUnlocked",
        "Location_Asia",
        "Location_Europe",
        "Location_Other",
        "Location_USA",
        "GameGenre_Action",
        "GameGenre_RPG",
        "GameGenre_Simulation",
        "GameGenre_Sports",
        "GameGenre_Strategy",
    ]

    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_columns]

    # Escalar e prever
    df_scaled = scaler.transform(df)
    prediction = modelo.predict(df_scaled)

    return jsonify({"prediction": prediction[0]})


if __name__ == "__main__":
    app.run(debug=True)
