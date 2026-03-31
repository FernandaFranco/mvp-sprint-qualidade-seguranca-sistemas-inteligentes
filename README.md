# Classificação: Engajamento de Jogadores Online

MVP da pós-graduação em Engenharia de Software da PUC-Rio. O projeto utiliza modelos de machine learning para prever o nível de engajamento (Alto, Médio ou Baixo) de jogadores online, com base em dados demográficos e métricas de jogo.

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

### Frontend

Com o backend rodando, abra o arquivo `frontend/index.html` diretamente no navegador (duplo clique no arquivo).

### Testes

Com o ambiente virtual ativo na pasta backend:

    pytest test_model.py -v

## Notebook

O notebook `MVP_Qualidade_Software_Segurança_Sistemas_Inteligentes.ipynb` contém todo o processo de criação do modelo de machine learning. Pode ser aberto e executado no Google Colab sem necessidade de configuração adicional.

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
