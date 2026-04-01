# Classificação: Engajamento de Jogadores Online

[![Python CI](https://github.com/FernandaFranco/mvp-sprint-qualidade-seguranca-sistemas-inteligentes/actions/workflows/python-app.yml/badge.svg)](https://github.com/FernandaFranco/mvp-sprint-qualidade-seguranca-sistemas-inteligentes/actions/workflows/python-app.yml)

MVP da pós-graduação em Engenharia de Software da PUC-Rio. O projeto utiliza modelos de machine learning para prever o nível de engajamento (Alto, Médio ou Baixo) de jogadores online, com base em dados demográficos e métricas de jogo.

## Links

- [Notebook no Google Colab](https://colab.research.google.com/drive/1TdLTwHil_aeLKGLA_u4ADDnOixhQv9rc?usp=sharing)
- [Vídeo de apresentação](https://youtube.com/seu-link-aqui)

## Tecnologias

- **Machine Learning:** Python, Scikit-Learn, Pandas, NumPy
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

### API

- Endpoint: `POST /predict`
- Content-Type: `application/json`
- Corpo esperado:

```json
{
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
  "GameGenre": "Action"
}
```

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

### Frontend

Com o backend rodando, abra o terminal na pasta `frontend` e execute um servidor local:

```bash
cd frontend
python3 -m http.server 8000
```

Em seguida, abra `http://localhost:8000` no navegador.

> O backend restringe CORS apenas para origens confiáveis durante o desenvolvimento.

### Testes

Com o ambiente virtual ativo na pasta backend:

    pytest test_model.py -v

### Integração contínua

O repositório agora inclui um workflow GitHub Actions em `.github/workflows/python-app.yml` que executa `pytest` em cada push e pull request para `main`.

## Notebook

O notebook `MVP_Qualidade_Software_Seguranca_Sistemas_Inteligentes.ipynb` contém todo o processo de criação do modelo de machine learning. Pode ser aberto e executado no Google Colab sem necessidade de configuração adicional. Se preferir, use a URL acima.

## Dataset

Fonte: [Predict Online Gaming Behavior Dataset](https://www.kaggle.com/datasets/rabieelkharoua/predict-online-gaming-behavior-dataset) (Kaggle)

O dataset contém 40.034 registros com métricas de jogadores online. O modelo escolhido (Árvore de Classificação otimizada) atingiu 90% de acurácia.

## Estrutura do projeto

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
    └── MVP_Qualidade_Software_Segurança_Sistemas_Inteligentes.ipynb
