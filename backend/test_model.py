import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score

# Carregar modelo e scaler
with open("modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

with open("scaler.pkl", "rb") as f:
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
