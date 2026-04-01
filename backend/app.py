from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]}})

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Predictor de Engajamento Gamer",
        "version": "1.0.0",
        "description": "API para prever nível de engajamento de jogadores baseado em dados de uso e perfil.",
    },
    "paths": {
        "/predict": {
            "post": {
                "summary": "Faz uma predição de engajamento",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "Age": {
                                        "type": "integer",
                                        "minimum": 5,
                                        "maximum": 100,
                                    },
                                    "Gender": {
                                        "type": "string",
                                        "enum": ["Male", "Female"],
                                    },
                                    "PlayTimeHours": {"type": "number", "minimum": 0},
                                    "InGamePurchases": {
                                        "type": "integer",
                                        "minimum": 0,
                                    },
                                    "GameDifficulty": {
                                        "type": "string",
                                        "enum": ["Easy", "Medium", "Hard"],
                                    },
                                    "SessionsPerWeek": {
                                        "type": "integer",
                                        "minimum": 0,
                                        "maximum": 168,
                                    },
                                    "AvgSessionDurationMinutes": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 1440,
                                    },
                                    "PlayerLevel": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 999,
                                    },
                                    "AchievementsUnlocked": {
                                        "type": "integer",
                                        "minimum": 0,
                                    },
                                    "Location": {
                                        "type": "string",
                                        "enum": ["USA", "Europe", "Asia", "Other"],
                                    },
                                    "GameGenre": {
                                        "type": "string",
                                        "enum": [
                                            "Action",
                                            "Sports",
                                            "RPG",
                                            "Strategy",
                                            "Simulation",
                                        ],
                                    },
                                },
                                "required": [
                                    "Age",
                                    "Gender",
                                    "PlayTimeHours",
                                    "InGamePurchases",
                                    "GameDifficulty",
                                    "SessionsPerWeek",
                                    "AvgSessionDurationMinutes",
                                    "PlayerLevel",
                                    "AchievementsUnlocked",
                                    "Location",
                                    "GameGenre",
                                ],
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Predição de engajamento realizada com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "prediction": {
                                            "type": "string",
                                            "enum": ["High", "Medium", "Low"],
                                        }
                                    },
                                }
                            }
                        },
                    },
                    "400": {
                        "description": "Requisição inválida",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {"error": {"type": "string"}},
                                }
                            }
                        },
                    },
                    "500": {
                        "description": "Erro interno no servidor",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {"error": {"type": "string"}},
                                }
                            }
                        },
                    },
                },
            }
        }
    },
}

with open(BASE_DIR / "modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

with open(BASE_DIR / "scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


@app.route("/")
def home():
    return redirect("/docs")


@app.route("/openapi.json")
def openapi_spec():
    return jsonify(OPENAPI_SPEC)


@app.route("/docs")
def swagger_ui():
    return """<!doctype html>
<html lang=\"pt-BR\">
  <head>
    <meta charset=\"utf-8\" />
    <title>Swagger UI - API de Engajamento Gamer</title>
    <link rel=\"stylesheet\" href=\"https://unpkg.com/swagger-ui-dist/swagger-ui.css\" />
    <style>body { margin:0; padding:0; }</n    </style>
  </head>
  <body>
    <div id=\"swagger-ui\"></div>
    <script src=\"https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js\"></script>
    <script src=\"https://unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js\"></script>
    <script>
      window.onload = function() {
        SwaggerUIBundle({
          url: '/openapi.json',
          dom_id: '#swagger-ui',
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset
          ],
          layout: 'StandaloneLayout'
        });
      };
    </script>
  </body>
</html>"""


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Validar se JSON foi enviado
        if not request.is_json:
            return jsonify({"error": "Requisição deve conter JSON"}), 400

        data = request.get_json()
        if data is None:
            return jsonify({"error": "JSON vazio recebido"}), 400

        # Validar campos obrigatórios
        required_fields = [
            "Age",
            "Gender",
            "PlayTimeHours",
            "InGamePurchases",
            "GameDifficulty",
            "SessionsPerWeek",
            "AvgSessionDurationMinutes",
            "PlayerLevel",
            "AchievementsUnlocked",
            "Location",
            "GameGenre",
        ]
        missing_fields = [
            f for f in required_fields if f not in data or data[f] is None
        ]
        if missing_fields:
            return (
                jsonify(
                    {
                        "error": f"Campos obrigatórios faltando: {', '.join(missing_fields)}"
                    }
                ),
                400,
            )

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
                    return (
                        jsonify(
                            {
                                "error": f"{field} deve estar entre {range_limits['min']} e {range_limits['max']}"
                            }
                        ),
                        400,
                    )
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
        df["GameDifficulty"] = df["GameDifficulty"].map(
            {"Easy": 0, "Medium": 1, "Hard": 2}
        )
        df = pd.get_dummies(df, columns=["Location"], dtype=int)
        df = pd.get_dummies(df, columns=["GameGenre"], dtype=int)

        # Garantir que todas as colunas existam
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

        return jsonify({"prediction": prediction[0]}), 200

    except KeyError:
        return jsonify({"error": "Campo esperado não encontrado"}), 400
    except Exception:
        return jsonify({"error": "Erro ao processar predição"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Rota não encontrada"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Método HTTP não permitido"}), 405


if __name__ == "__main__":
    app.run(debug=False)
