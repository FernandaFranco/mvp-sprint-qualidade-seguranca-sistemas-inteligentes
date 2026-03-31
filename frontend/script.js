const API_URL = "http://localhost:5000/predict";

function getFormData() {
  const fields = {
    Age: document.getElementById("age").value,
    Gender: document.getElementById("gender").value,
    PlayTimeHours: document.getElementById("playTimeHours").value,
    InGamePurchases: document.getElementById("inGamePurchases").value,
    GameDifficulty: document.getElementById("gameDifficulty").value,
    SessionsPerWeek: document.getElementById("sessionsPerWeek").value,
    AvgSessionDurationMinutes:
      document.getElementById("avgSessionDuration").value,
    PlayerLevel: document.getElementById("playerLevel").value,
    AchievementsUnlocked: document.getElementById("achievementsUnlocked")
      .value,
    Location: document.getElementById("location").value,
    GameGenre: document.getElementById("gameGenre").value,
  };

  // Validar se todos os campos foram preenchidos
  for (const [key, value] of Object.entries(fields)) {
    if (value === "" || value === null) {
      return null;
    }
  }

  // Converter valores numéricos
  fields.Age = parseInt(fields.Age);
  fields.PlayTimeHours = parseFloat(fields.PlayTimeHours);
  fields.InGamePurchases = parseInt(fields.InGamePurchases);
  fields.SessionsPerWeek = parseInt(fields.SessionsPerWeek);
  fields.AvgSessionDurationMinutes = parseInt(
    fields.AvgSessionDurationMinutes,
  );
  fields.PlayerLevel = parseInt(fields.PlayerLevel);
  fields.AchievementsUnlocked = parseInt(fields.AchievementsUnlocked);

  return fields;
}

async function predict() {
  const errorMsg = document.getElementById("errorMsg");
  const loading = document.getElementById("loading");
  const resultPanel = document.getElementById("resultPanel");

  // Esconder mensagens anteriores
  errorMsg.classList.remove("show");
  resultPanel.classList.remove("show");

  // Validar form
  const data = getFormData();
  if (!data) {
    errorMsg.textContent = "⚠ PREENCHA TODOS OS CAMPOS PARA CONTINUAR ⚠";
    errorMsg.classList.add("show");
    return;
  }

  // Mostrar loading
  loading.classList.add("show");
  document.getElementById("predictBtn").disabled = true;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error("Erro na API");
    }

    const result = await response.json();
    showResult(result.prediction);
  } catch (error) {
    errorMsg.textContent = "⚠ ERRO DE CONEXÃO COM O SERVIDOR ⚠";
    errorMsg.classList.add("show");
  } finally {
    loading.classList.remove("show");
    document.getElementById("predictBtn").disabled = false;
  }
}

function showResult(prediction) {
  const resultPanel = document.getElementById("resultPanel");
  const resultValue = document.getElementById("resultValue");
  const resultBar = document.getElementById("resultBar");

  // Traduzir resultado
  const translations = { High: "ALTO", Medium: "MÉDIO", Low: "BAIXO" };
  resultValue.textContent =
    translations[prediction] || prediction.toUpperCase();
  resultValue.className = "result-value " + prediction.toLowerCase();

  // Montar barra visual
  let bars = "";
  const totalBars = 10;
  let filledCount, colorClass;

  if (prediction === "High") {
    filledCount = 10;
    colorClass = "filled-green";
  } else if (prediction === "Medium") {
    filledCount = 6;
    colorClass = "filled-yellow";
  } else {
    filledCount = 3;
    colorClass = "filled-pink";
  }

  for (let i = 0; i < totalBars; i++) {
    bars += `<div class="bar-segment ${i < filledCount ? colorClass : ""}"></div>`;
  }
  resultBar.innerHTML = bars;

  resultPanel.classList.add("show");
  resultPanel.scrollIntoView({ behavior: "smooth" });
}

function resetForm() {
  // Limpar todos os inputs
  document
    .querySelectorAll("input")
    .forEach((input) => (input.value = ""));
  document
    .querySelectorAll("select")
    .forEach((select) => (select.selectedIndex = 0));

  // Esconder resultado
  document.getElementById("resultPanel").classList.remove("show");
  document.getElementById("errorMsg").classList.remove("show");

  // Scroll pro topo
  window.scrollTo({ top: 0, behavior: "smooth" });
}
