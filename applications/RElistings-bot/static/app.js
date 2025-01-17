const startBotButton = document.getElementById("start-bot");
const stopBotButton = document.getElementById("stop-bot");
const logsDiv = document.getElementById("logs");

// Start the bot
startBotButton.addEventListener("click", async () => {
  const startTime = document.getElementById("start-time").value;
  const interval = document.getElementById("interval").value;

  const response = await fetch("/start-bot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start_time: startTime, interval: parseInt(interval) }),
  });

  const data = await response.json();
  alert(data.message);
});

// Stop the bot
stopBotButton.addEventListener("click", async () => {
  const response = await fetch("/stop-bot", {
    method: "POST",
  });
  const data = await response.json();
  alert(data.message);
});

// Fetch logs periodically
setInterval(async () => {
  const response = await fetch("/logs");
  const data = await response.json();

  if (data.status === "success") {
    logsDiv.innerHTML = data.logs.map(log => `<div>${log}</div>`).join("");
  }
}, 4000);