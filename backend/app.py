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
