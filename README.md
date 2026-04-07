# Classificação: Engajamento de Jogadores Online

[![Python CI](https://github.com/FernandaFranco/mvp-sprint-qualidade-seguranca-sistemas-inteligentes/actions/workflows/python-app.yml/badge.svg)](https://github.com/FernandaFranco/mvp-sprint-qualidade-seguranca-sistemas-inteligentes/actions/workflows/python-app.yml)

```
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ░                                       ░
  ░     PREDITOR DE ENGAJAMENTO GAMER     ░
  ░                                       ░
  ░        ▶  INSIRA UMA MOEDA  ◀         ░
  ░                                       ░
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

MVP da sprint de Qualidade de Software, Segurança e Sistemas Inteligentes da pós-graduação em Engenharia de Software da PUC-Rio. O projeto utiliza modelos de machine learning para prever o nível de engajamento (Alto, Médio ou Baixo) de jogadores online, com base em dados demográficos e métricas de jogo.

## Links

- [Notebook no Google Colab](https://colab.research.google.com/github/FernandaFranco/mvp-sprint-qualidade-seguranca-sistemas-inteligentes/blob/main/MVP_Qualidade_Software_Seguranca_Sistemas_Inteligentes.ipynb)
- [Vídeo de apresentação](https://youtube.com/seu-link-aqui)

## Tecnologias

- **Machine Learning:** Python, Scikit-Learn, Pandas
- **Backend:** Flask, Flask-CORS
- **Frontend:** HTML, CSS, JavaScript
- **Testes:** PyTest

## Como executar

### Backend

No terminal, navegue até a pasta do backend, crie o ambiente virtual, instale as dependências e inicie o servidor:

    cd backend
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python app.py

O servidor será iniciado em http://localhost:5000

### Frontend

Com o backend rodando, abra o terminal na pasta `frontend` e execute um servidor local:

```bash
cd frontend
python3 -m http.server 8000
```

Em seguida, abra `http://localhost:8000` no navegador.

> O backend restringe CORS apenas para origens confiáveis durante o desenvolvimento.

### API

- Endpoint: `POST /predict`
- Content-Type: `application/json`
- Corpo esperado:

```json
{
  "Age": 25,
  "Gender": "Male",
  "PlayTimeHours": 10.5,
  "InGamePurchases": 1,
  "GameDifficulty": "Medium",
  "SessionsPerWeek": 5,
  "AvgSessionDurationMinutes": 60,
  "PlayerLevel": 50,
  "AchievementsUnlocked": 20,
  "Location": "USA",
  "GameGenre": "Action"
}
```

Ranges aceitos por campo numérico:

| Campo | Tipo | Valores aceitos |
|---|---|---|
| Age | inteiro | 10–80 |
| PlayTimeHours | decimal | 0–24 |
| InGamePurchases | binário | 0 ou 1 |
| SessionsPerWeek | inteiro | 0–28 |
| AvgSessionDurationMinutes | inteiro | 1–240 |
| PlayerLevel | inteiro | 1–100 |
| AchievementsUnlocked | inteiro | 0–100 |

- Resposta de sucesso:

```json
{ "prediction": "High" }
```

- Respostas de erro possíveis:

```json
{ "error": "Campos obrigatórios faltando: Age" }
{ "error": "Age deve ser um número válido" }
{ "error": "Gênero inválido" }
{ "error": "Erro ao processar predição" }
```

- Documentação interativa disponível em `http://localhost:5000/docs`
- A raiz `http://localhost:5000/` redireciona automaticamente para a documentação Swagger UI.

### Testes

Na raiz do projeto, ative o ambiente virtual e execute os testes:

    source backend/env/bin/activate
    pytest backend/test_model.py -v

## Integração contínua

O repositório inclui um workflow GitHub Actions em `.github/workflows/python-app.yml` que executa `pytest` em cada push e pull request para `main`.

## Dataset

Fonte: [Predict Online Gaming Behavior Dataset](https://www.kaggle.com/datasets/rabieelkharoua/predict-online-gaming-behavior-dataset) (Kaggle)

O dataset contém 40.034 registros com métricas de jogadores online. O modelo escolhido (Árvore de Classificação otimizada) atingiu 90% de acurácia.

## Notebook

O notebook `MVP_Qualidade_Software_Seguranca_Sistemas_Inteligentes.ipynb` contém todo o processo de criação do modelo de machine learning. Pode ser aberto e executado no Google Colab sem necessidade de configuração adicional.

[Abrir no Google Colab](https://colab.research.google.com/github/FernandaFranco/mvp-sprint-qualidade-seguranca-sistemas-inteligentes/blob/main/MVP_Qualidade_Software_Seguranca_Sistemas_Inteligentes.ipynb)

## Estrutura do projeto

    ├── .github/
    │   └── workflows/
    │       └── python-app.yml    # Workflow de CI
    ├── backend/
    │   ├── app.py                # API Flask
    │   ├── modelo.pkl            # Modelo treinado
    │   ├── scaler.pkl            # Scaler para normalização
    │   ├── test_model.py         # Testes automatizados
    │   └── requirements.txt      # Dependências Python
    ├── frontend/
    │   ├── index.html            # Página principal
    │   ├── style.css             # Estilos (tema 8-bit)
    │   └── script.js             # Lógica do frontend
    └── MVP_Qualidade_Software_Seguranca_Sistemas_Inteligentes.ipynb
