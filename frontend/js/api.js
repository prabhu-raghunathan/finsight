const API = {
  USER_SERVICE:        "http://localhost:8081",
  TRANSACTION_SERVICE: "http://localhost:8082",
  AI_SERVICE:          "http://localhost:8083",
};

function authHeader() {
  return { Authorization: "Bearer " + getToken() };
}

function handleError(error) {
  if (error.response && error.response.status === 401) logout();
  throw error;
}

async function login(email, password) {
  const response = await axios.post(API.USER_SERVICE + "/api/auth/login", { email, password });
  return response.data;
}

async function getTransactions() {
  const response = await axios.get(API.TRANSACTION_SERVICE + "/api/transactions", { headers: authHeader() });
  return response.data;
}

async function createTransaction(data) {
  const response = await axios.post(API.TRANSACTION_SERVICE + "/api/transactions", data, { headers: authHeader() });
  return response.data;
}

async function updateTransaction(id, data) {
  const response = await axios.put(API.TRANSACTION_SERVICE + "/api/transactions/" + id, data, { headers: authHeader() });
  return response.data;
}

async function deleteTransaction(id) {
  await axios.delete(API.TRANSACTION_SERVICE + "/api/transactions/" + id, { headers: authHeader() });
}

async function askAI(question) {
  const response = await axios.post(API.AI_SERVICE + "/api/insights/ask", { question }, { headers: authHeader() });
  return response.data;
}