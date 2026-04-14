requireAuth();

document.getElementById("logoutBtn").addEventListener("click", (e) => { e.preventDefault(); logout(); });

window.addEventListener("load", async () => {
  try {
    const transactions = await getTransactions();
    renderSummary(transactions);
    renderTransactions(transactions);
    document.getElementById("subheading").textContent =
        transactions.length + " transaction" + (transactions.length !== 1 ? "s" : "") + " found";
  } catch (error) {
    document.getElementById("loadingMsg").textContent = "Failed to load transactions.";
  }
});

function renderSummary(transactions) {
  let income = 0, expense = 0;

  transactions.forEach(t => {
    if (t.type === "INCOME") income  += parseFloat(t.amount);
    else                     expense += parseFloat(t.amount);
  });

  const net = income - expense;

  document.getElementById("totalIncome").textContent  = "₹" + income.toLocaleString("en-IN", { maximumFractionDigits: 0 });
  document.getElementById("totalExpense").textContent = "₹" + expense.toLocaleString("en-IN", { maximumFractionDigits: 0 });
  document.getElementById("netBalance").textContent   = "₹" + net.toLocaleString("en-IN", { maximumFractionDigits: 0 });
  document.getElementById("netBalance").style.color   = net >= 0 ? "var(--income)" : "var(--expense)";
}

function renderTransactions(transactions) {
  const container = document.getElementById("transactionList");

  if (transactions.length === 0) {
    container.innerHTML = `
      <div class="empty">
        <p>No transactions yet.</p>
        <a href="transaction.html" class="btn">Add your first transaction</a>
      </div>`;
    return;
  }

  // Sort newest first
  const sorted = [...transactions].sort((a, b) => new Date(b.date) - new Date(a.date));

  container.innerHTML = sorted.map(t => {
    const isIncome = t.type === "INCOME";
    const sign     = isIncome ? "+" : "−";
    const amount   = parseFloat(t.amount).toLocaleString("en-IN", { maximumFractionDigits: 0 });
    const date     = new Date(t.date).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });

    return `
      <div class="transaction-row">
        <div class="tx-left">
          <div class="type-dot ${isIncome ? 'income' : 'expense'}"></div>
          <div>
            <div class="tx-desc">${t.description}</div>
            <div class="tx-meta">${t.category} &middot; ${date}</div>
          </div>
        </div>
        <div class="tx-right">
          <div class="tx-amount ${isIncome ? 'income' : 'expense'}">${sign} ₹${amount}</div>
          <button class="edit-btn" onclick="window.location.href='transaction.html?id=${t.id}'">Edit</button>
        </div>
      </div>`;
  }).join("");
}