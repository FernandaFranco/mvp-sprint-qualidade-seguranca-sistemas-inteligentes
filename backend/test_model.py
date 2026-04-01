import pickle
import pandas as pd
import numpy as np
import pytest
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score
from pathlib import Path
from app import app

BASE_DIR = Path(__file__).resolve().parent

# Carregar modelo e scaler
with open(BASE_DIR / "modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

with open(BASE_DIR / "scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Carregar e preparar os dados (mesmo processo do notebook)
url = "https://raw.githubusercontent.com/FernandaFranco/Gaming-Behavior/main/online_gaming_behavior_dataset.csv"
df = pd.read_csv(url)
df = df.drop("PlayerID", axis=1)
df["Gender"] = df["Gender"].map({"Female": 0, "Male": 1})
df["GameDifficulty"] = df["GameDifficulty"].map({"Easy": 0, "Medium": 1, "Hard": 2})
df = pd.get_dummies(df, columns=["Location"], dtype=int)
df = pd.get_dummies(df, columns=["GameGenre"], dtype=int)

X = df.drop("EngagementLevel", axis=1)
y = df["EngagementLevel"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
X_test_scaled = scaler.transform(X_test)
y_pred = modelo.predict(X_test_scaled)


# ===== TESTES DE MÉTRICAS DO MODELO =====


def test_acuracia():
    acc = accuracy_score(y_test, y_pred)
    assert acc >= 0.85, f"Acurácia {acc:.2f} abaixo do mínimo 0.85"


def test_f1_macro():
    f1 = f1_score(y_test, y_pred, average="macro")
    assert f1 >= 0.83, f"F1 Score {f1:.2f} abaixo do mínimo 0.83"


def test_recall_por_classe():
    recall = recall_score(
        y_test, y_pred, average=None, labels=["High", "Medium", "Low"]
    )
    assert (recall >= 0.80).all(), f"Recall por classe {recall} abaixo do mínimo 0.80"


# ===== TESTES DE API FLASK =====


@pytest.fixture
def client():
    """Fixture para cliente Flask de testes"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_api_home(client):
    """Testa rota home redirecionando para /docs"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/docs"


def test_api_predict_sucesso(client):
    """Testa predição com dados válidos"""
    data = {
        "Age": 25,
        "Gender": "Male",
        "PlayTimeHours": 100.5,
        "InGamePurchases": 50,
        "GameDifficulty": "Medium",
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "USA",
        "GameGenre": "Action",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert "prediction" in result
    assert result["prediction"] in ["High", "Medium", "Low"]


def test_api_predict_age_invalido(client):
    """Testa validação de idade fora do range"""
    data = {
        "Age": 150,  # Muito alto
        "Gender": "Male",
        "PlayTimeHours": 100,
        "InGamePurchases": 50,
        "GameDifficulty": "Medium",
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "USA",
        "GameGenre": "Action",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400
    assert "Age" in response.get_json()["error"]


def test_api_predict_age_muito_baixo(client):
    """Testa validação de idade muito baixa"""
    data = {
        "Age": 2,  # Abaixo do mínimo 5
        "Gender": "Male",
        "PlayTimeHours": 100,
        "InGamePurchases": 50,
        "GameDifficulty": "Medium",
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "USA",
        "GameGenre": "Action",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400


def test_api_predict_playtime_invalido(client):
    """Testa validação de PlayTimeHours"""
    data = {
        "Age": 25,
        "Gender": "Female",
        "PlayTimeHours": 15000,  # Acima do máximo
        "InGamePurchases": 50,
        "GameDifficulty": "Hard",
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "Europe",
        "GameGenre": "RPG",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400


def test_api_predict_sessoes_invalidas(client):
    """Testa validação de SessionsPerWeek (máx 168)"""
    data = {
        "Age": 25,
        "Gender": "Male",
        "PlayTimeHours": 100,
        "InGamePurchases": 50,
        "GameDifficulty": "Easy",
        "SessionsPerWeek": 200,  # Acima de 168
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "Asia",
        "GameGenre": "Strategy",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400


def test_api_predict_gender_invalido(client):
    """Testa validação de Gender"""
    data = {
        "Age": 25,
        "Gender": "Other",  # Inválido
        "PlayTimeHours": 100,
        "InGamePurchases": 50,
        "GameDifficulty": "Medium",
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "USA",
        "GameGenre": "Action",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400
    assert "Gênero" in response.get_json()["error"]


def test_api_predict_dificuldade_invalida(client):
    """Testa validação de GameDifficulty"""
    data = {
        "Age": 25,
        "Gender": "Male",
        "PlayTimeHours": 100,
        "InGamePurchases": 50,
        "GameDifficulty": "Impossible",  # Inválido
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "USA",
        "GameGenre": "Action",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400
    assert "Dificuldade" in response.get_json()["error"]


def test_api_predict_localizacao_invalida(client):
    """Testa validação de Location"""
    data = {
        "Age": 25,
        "Gender": "Male",
        "PlayTimeHours": 100,
        "InGamePurchases": 50,
        "GameDifficulty": "Medium",
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "Atlantida",  # Inválido
        "GameGenre": "Action",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400
    assert "Localização" in response.get_json()["error"]


def test_api_predict_genero_jogo_invalido(client):
    """Testa validação de GameGenre"""
    data = {
        "Age": 25,
        "Gender": "Male",
        "PlayTimeHours": 100,
        "InGamePurchases": 50,
        "GameDifficulty": "Medium",
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "USA",
        "GameGenre": "Horror",  # Inválido
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400
    assert "Gênero de jogo" in response.get_json()["error"]


def test_api_predict_valores_zerados(client):
    """Testa predição com valores mínimos válidos"""
    data = {
        "Age": 5,  # Mínimo
        "Gender": "Male",
        "PlayTimeHours": 0,  # Mínimo
        "InGamePurchases": 0,  # Mínimo
        "GameDifficulty": "Easy",
        "SessionsPerWeek": 0,  # Mínimo
        "AvgSessionDurationMinutes": 1,  # Mínimo
        "PlayerLevel": 1,  # Mínimo
        "AchievementsUnlocked": 0,  # Mínimo
        "Location": "USA",
        "GameGenre": "Action",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert "prediction" in response.get_json()


def test_api_predict_valores_maximos(client):
    """Testa predição com valores máximos válidos"""
    data = {
        "Age": 100,  # Máximo
        "Gender": "Female",
        "PlayTimeHours": 10000,  # Máximo
        "InGamePurchases": 100000,  # Máximo
        "GameDifficulty": "Hard",
        "SessionsPerWeek": 168,  # Máximo
        "AvgSessionDurationMinutes": 1440,  # Máximo (24h)
        "PlayerLevel": 999,  # Máximo
        "AchievementsUnlocked": 10000,  # Máximo
        "Location": "Europe",
        "GameGenre": "Strategy",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert "prediction" in response.get_json()


def test_api_predict_tipo_invalido(client):
    """Testa validação de tipo de dado"""
    data = {
        "Age": "vinte e cinco",  # String ao invés de int
        "Gender": "Male",
        "PlayTimeHours": 100,
        "InGamePurchases": 50,
        "GameDifficulty": "Medium",
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 60,
        "PlayerLevel": 50,
        "AchievementsUnlocked": 20,
        "Location": "USA",
        "GameGenre": "Action",
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 400
    assert "válido" in response.get_json()["error"]


# ===== TESTES DE DADOS E MODELO =====


def test_modelo_carregamento():
    """Verifica se modelo foi carregado corretamente"""
    assert modelo is not None
    assert hasattr(modelo, "predict")


def test_scaler_carregamento():
    """Verifica se scaler foi carregado corretamente"""
    assert scaler is not None
    assert hasattr(scaler, "transform")


def test_dataset_estrutura():
    """Verifica se dataset tem as colunas esperadas"""
    numeric_cols = [
        "Age",
        "Gender",
        "PlayTimeHours",
        "InGamePurchases",
        "GameDifficulty",
        "SessionsPerWeek",
        "AvgSessionDurationMinutes",
        "PlayerLevel",
        "AchievementsUnlocked",
    ]
    # Verificar colunas numéricas
    assert all(col in df.columns for col in numeric_cols)

    # Verificar se há colunas de Location (após get_dummies)
    location_cols = [col for col in df.columns if col.startswith("Location_")]
    assert len(location_cols) > 0, "Nenhuma coluna Location encontrada"

    # Verificar se há colunas de GameGenre (após get_dummies)
    genre_cols = [col for col in df.columns if col.startswith("GameGenre_")]
    assert len(genre_cols) > 0, "Nenhuma coluna GameGenre encontrada"
