requireAuth();

document.getElementById("logoutBtn").addEventListener("click", (e) => { e.preventDefault(); logout(); });

// Set today's date as default
document.getElementById("date").value = new Date().toISOString().split("T")[0];

const params = new URLSearchParams(window.location.search);
const editId = params.get("id");

if (editId) {
  document.getElementById("pageTitle").textContent = "Edit Transaction";
  document.getElementById("submitBtn").textContent = "Save Changes";
  loadTransaction(editId);
}

async function loadTransaction(id) {
  try {
    const transactions = await getTransactions();
    const t = transactions.find(t => String(t.id) === String(id));
    if (!t) return;
    document.getElementById("description").value = t.description;
    document.getElementById("amount").value      = t.amount;
    document.getElementById("type").value        = t.type;
    document.getElementById("category").value    = t.category;
    document.getElementById("date").value        = t.date;
  } catch (error) {
    console.error("Failed to load transaction", error);
  }
}

document.getElementById("submitBtn").addEventListener("click", async () => {
  const errorMsg   = document.getElementById("errorMsg");
  const successMsg = document.getElementById("successMsg");
  const submitBtn  = document.getElementById("submitBtn");

  errorMsg.style.display   = "none";
  successMsg.style.display = "none";

  const data = {
    description: document.getElementById("description").value.trim(),
    amount:      document.getElementById("amount").value,
    type:        document.getElementById("type").value,
    category:    document.getElementById("category").value.trim(),
    date:        document.getElementById("date").value,
  };

  if (!data.description || !data.amount || !data.category || !data.date) {
    errorMsg.textContent   = "Please fill in all fields.";
    errorMsg.style.display = "block";
    return;
  }

  submitBtn.textContent = "Saving...";
  submitBtn.disabled    = true;

  try {
    if (editId) {
      await updateTransaction(editId, data);
    } else {
      await createTransaction(data);
    }
    window.location.href = "dashboard.html";
  } catch (error) {
    errorMsg.textContent   = "Something went wrong. Please try again.";
    errorMsg.style.display = "block";
    submitBtn.textContent  = editId ? "Save Changes" : "Save Transaction";
    submitBtn.disabled     = false;
  }
});