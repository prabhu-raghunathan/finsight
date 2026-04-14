requireAuth();

document.getElementById("logoutBtn").addEventListener("click", (e) => { e.preventDefault(); logout(); });

const sendBtn       = document.getElementById("sendBtn");
const questionInput = document.getElementById("questionInput");

sendBtn.addEventListener("click", sendMessage);

questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) sendMessage();
});

// Suggestion chip clicks
document.querySelectorAll(".suggestion").forEach(btn => {
  btn.addEventListener("click", () => {
    questionInput.value = btn.textContent;
    sendMessage();
  });
});

let isWaiting = false;

async function sendMessage() {
  if (isWaiting) return;

  const question = questionInput.value.trim();
  if (!question) return;

  // Hide the hint/suggestions once first message is sent
  const hint = document.getElementById("chatHint");
  if (hint) hint.remove();

  questionInput.value  = "";
  sendBtn.textContent  = "...";
  sendBtn.disabled     = true;
  isWaiting            = true;

  appendMessage("user", question);
  const loadingId = appendThinking();

  try {
    const data = await askAI(question);
    replaceThinking(loadingId, data.answer);
  } catch (error) {
    replaceThinking(loadingId, "Sorry, I couldn't reach the AI service. Please try again.");
  } finally {
    sendBtn.textContent = "Ask";
    sendBtn.disabled    = false;
    isWaiting           = false;
  }
}

function appendMessage(sender, text) {
  const chatBody = document.getElementById("chatBody");
  const id  = "msg-" + Date.now() + "-" + Math.random();
  const div = document.createElement("div");
  div.className = "message " + sender + " fade-in";
  div.id = id;
  div.innerHTML = "<p>" + escapeHtml(text) + "</p>";
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
  return id;
}

function appendThinking() {
  const chatBody = document.getElementById("chatBody");
  const id  = "msg-" + Date.now() + "-thinking";
  const div = document.createElement("div");
  div.className = "message ai thinking fade-in";
  div.id = id;
  div.innerHTML = "<p>Thinking...</p>";
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
  return id;
}

function replaceThinking(id, text) {
  const div = document.getElementById(id);
  if (!div) return;
  div.className = "message ai fade-in";
  div.querySelector("p").textContent = text;
  document.getElementById("chatBody").scrollTop = document.getElementById("chatBody").scrollHeight;
}

function escapeHtml(text) {
  return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
}