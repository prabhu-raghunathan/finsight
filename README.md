# FinSight — Setup Guide

FinSight is a microservices-based personal finance system with an AI insights layer. It consists of three independent backend services, a vanilla HTML/CSS/JS frontend, and uses Ollama to run a local LLM.

This guide covers setup on **Linux**, **macOS**, and **Windows**.

---

## What You're Running

| Service | Language | Port |
|---|---|---|
| User Service | Java / Spring Boot | 8081 |
| Transaction Service | Java / Spring Boot | 8082 |
| AI Insights Service | Python / FastAPI | 8083 |
| User Database | PostgreSQL (Docker) | 5432 |
| Transaction Database | PostgreSQL (Docker) | 5434 |
| Frontend | HTML / CSS / JS | 3000 |
| Ollama (LLM) | — | 11434 |

---

## Choose Your OS

- [Linux Setup](#linux-setup)
- [macOS Setup](#macos-setup)
- [Windows Setup](#windows-setup)
- [Steps Common to All Platforms](#steps-common-to-all-platforms)

---

## Linux Setup

### 1. Java 17

```bash
sudo apt install openjdk-17-jdk -y
java -version
# Should show: openjdk 17.x.x
```

### 2. Docker

```bash
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker
```

Fix permissions so you don't need `sudo` for every Docker command:

```bash
sudo chmod 666 /var/run/docker.sock
```

> **Note:** This permission resets on every reboot. Run it again each time you restart your machine.

### 3. Python 3.12+

```bash
sudo apt install python3 python3-pip python3-venv -y
python3 --version
```

### 4. Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

Configure Ollama to listen on all interfaces so Docker containers can reach it:

```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d

sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
EOF

sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Verify:

```bash
curl http://localhost:11434/api/tags
# Should return JSON with llama3.2 listed
```

### 5. Find Your Docker Bridge IP

On Linux, containers can't use `localhost` to reach the host machine. You need the Docker bridge IP:

```bash
ip addr show docker0 | grep "inet " | awk '{print $2}' | cut -d/ -f1
# Usually returns 172.17.0.1
```

Note this IP — you'll use it in the `.env` file later.

---

## macOS Setup

### 1. Homebrew

If you don't have Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Java 17

```bash
brew install openjdk@17
```

Add Java to your PATH. Add this to your `~/.zshrc`:

```bash
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
```

Then reload:

```bash
source ~/.zshrc
java -version
```

### 3. Docker Desktop

Download and install from: https://www.docker.com/products/docker-desktop/

Open Docker Desktop and make sure it's running (whale icon in menu bar).

> On macOS, Docker Desktop automatically provides `host.docker.internal` as a hostname that points to your machine. You'll use this in the `.env` file instead of an IP address.

### 4. Python 3.12+

```bash
brew install python@3.12
python3 --version
```

### 5. Ollama

Download and install from: https://ollama.com/download

Then pull the model:

```bash
ollama pull llama3.2
```

On macOS, Ollama runs as a desktop app and listens on all interfaces by default. No extra configuration needed.

Verify:

```bash
curl http://localhost:11434/api/tags
```

---

## Windows Setup

All commands below are for **PowerShell** unless stated otherwise.

### 1. Java 17

Download the installer from: https://adoptium.net/

Select **Java 17 (LTS)** and run the installer. Make sure to check **"Add to PATH"** during installation.

Verify:

```powershell
java -version
```

### 2. Docker Desktop

Download and install from: https://www.docker.com/products/docker-desktop/

During install, choose **WSL 2** as the backend when prompted.

Open Docker Desktop and wait for it to fully start (steady whale icon in system tray).

> On Windows, Docker Desktop automatically provides `host.docker.internal`. Use this in your `.env` file.

### 3. Python 3.12+

Download from: https://www.python.org/downloads/

During install, check **"Add Python to PATH"**.

Verify:

```powershell
python --version
```

### 4. Ollama

Download and install from: https://ollama.com/download

Pull the model:

```powershell
ollama pull llama3.2
```

Verify:

```powershell
curl http://localhost:11434/api/tags
```

### 5. Git

Download from: https://git-scm.com/download/win

During install, choose **"Git from the command line and also from 3rd-party software"**.

### 6. Fix PowerShell Execution Policy

Run this once to allow scripts to execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Steps Common to All Platforms

Once your prerequisites are done, the rest is the same on every OS (with minor differences noted).

### Step 1 — Clone the Repository

```bash
git clone https://github.com/prabhu-raghunathan/finsight.git
cd finsight
```

### Step 2 — Create the AI Service Environment File

The AI service reads secrets from a `.env` file that is not committed to the repo. Create it manually.

**Linux / macOS:**

```bash
cd ai-insights-service
cp .env.example .env
nano .env
```

**Windows:**

```powershell
cd ai-insights-service
Copy-Item .env.example .env
notepad .env
```

Fill in the values.

**Linux** — use the bridge IP from your Linux setup (Step 5):

```
JWT_SECRET=password-for-finserve-try-that-hacker
TRANSACTION_SERVICE_URL=http://172.17.0.1:8082
OLLAMA_BASE_URL=http://172.17.0.1:11434
OLLAMA_MODEL=llama3.2
```

**macOS and Windows** — use `host.docker.internal`:

```
JWT_SECRET=password-for-finserve-try-that-hacker
TRANSACTION_SERVICE_URL=http://host.docker.internal:8082
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2
```

> The `JWT_SECRET` must be identical in this file and in `application.properties` for both Java services. Don't change it unless you update all three places.

### Step 3 — Start the Databases and AI Service

From the root of the project:

```bash
docker-compose up -d
```

Verify all three containers are running:

```bash
docker ps
# Should show: user-db, transaction-db, ai-insights-service — all status Up
```

Check the AI service is healthy:

```bash
curl http://localhost:8083/health
# Expected: {"status":"UP","service":"ai-insights-service"}
```

If the AI service fails to start, check its logs:

```bash
docker logs ai-insights-service
```

### Step 4 — Start the User Service

Open a new terminal:

**Linux / macOS:**

```bash
cd finsight/user-service
./mvnw clean spring-boot:run
```

**Windows:**

```powershell
cd finsight\user-service
.\mvnw.cmd clean spring-boot:run
```

Wait until you see:

```
Started UserServiceApplication in X.XXX seconds
```

> The first run downloads Maven dependencies — this takes 2–3 minutes. Subsequent runs are much faster.

### Step 5 — Start the Transaction Service

Open another new terminal:

**Linux / macOS:**

```bash
cd finsight/transaction-service
./mvnw clean spring-boot:run
```

**Windows:**

```powershell
cd finsight\transaction-service
.\mvnw.cmd clean spring-boot:run
```

Wait until you see:

```
Started TransactionServiceApplication in X.XXX seconds
```

### Step 6 — Register a User

Before logging in, create an account. Run this once:

**Linux / macOS:**

```bash
curl -X POST http://localhost:8081/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","name":"Your Name","password":"yourpassword"}'
```

**Windows:**

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8081/api/auth/register" `
  -ContentType "application/json" `
  -Body '{"email":"you@example.com","name":"Your Name","password":"yourpassword"}'
```

You should get back a JWT token. This means registration worked.

> If you see `Email already registered`, the user already exists — skip to Step 8.

### Step 7 — Seed Transaction Data (Optional but Recommended)

The AI chat works best with real data to reason over. A seed script creates 70+ realistic transactions.

Set up the Python environment:

**Linux / macOS:**

```bash
cd finsight/ai-insights-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```powershell
cd finsight\ai-insights-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Open `seed_transactions.py` and make sure the email and password at the top match what you registered. Then run:

```bash
python seed_transactions.py
```

### Step 8 — Start the Frontend

**Linux / macOS:**

```bash
cd finsight/frontend
python3 -m http.server 3000
```

**Windows:**

```powershell
cd finsight\frontend
python -m http.server 3000
```

Open your browser and go to:

```
http://localhost:3000
```

Log in with the credentials from Step 6.

---

## Daily Startup Sequence

### Linux

```bash
sudo chmod 666 /var/run/docker.sock                                           # after every reboot
cd ~/finsight && docker-compose up -d                                          # terminal 1
cd ~/finsight/user-service && ./mvnw spring-boot:run                          # terminal 2
cd ~/finsight/transaction-service && ./mvnw spring-boot:run                   # terminal 3
cd ~/finsight/frontend && python3 -m http.server 3000                         # terminal 4
```

### macOS

```bash
# Open Docker Desktop first and wait for it to start
cd ~/finsight && docker-compose up -d                                          # terminal 1
cd ~/finsight/user-service && ./mvnw spring-boot:run                          # terminal 2
cd ~/finsight/transaction-service && ./mvnw spring-boot:run                   # terminal 3
cd ~/finsight/frontend && python3 -m http.server 3000                         # terminal 4
```

### Windows

```powershell
# Open Docker Desktop first and wait for it to start
cd ~\finsight; docker-compose up -d                                            # terminal 1
cd ~\finsight\user-service; .\mvnw.cmd spring-boot:run                        # terminal 2
cd ~\finsight\transaction-service; .\mvnw.cmd spring-boot:run                 # terminal 3
cd ~\finsight\frontend; python -m http.server 3000                            # terminal 4
```

Then open `http://localhost:3000`.

---

## Verify Everything is Running

```bash
# User Service — expects 400 (up, missing request body)
curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/api/auth/login

# Transaction Service — expects 401 (up, needs auth token)
curl -s -o /dev/null -w "%{http_code}" http://localhost:8082/api/transactions

# AI Service
curl http://localhost:8083/health
# Expected: {"status":"UP","service":"ai-insights-service"}

# Ollama
curl http://localhost:11434/api/tags
# Expected: JSON with llama3.2 listed
```

---

## Troubleshooting

**Port already in use**

Linux / macOS:

```bash
sudo kill -9 $(lsof -t -i:8081)
sudo kill -9 $(lsof -t -i:8082)
sudo kill -9 $(lsof -t -i:8083)
```

Windows:

```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8081).OwningProcess -Force
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8082).OwningProcess -Force
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8083).OwningProcess -Force
```

**Docker containers not starting**

```bash
sudo chmod 666 /var/run/docker.sock    # Linux only
docker-compose up -d
docker logs ai-insights-service        # see what failed
```

**AI service can't reach Ollama or Transaction Service (Linux only)**

The Docker bridge IP may have changed. Find the new one:

```bash
ip addr show docker0 | grep "inet " | awk '{print $2}' | cut -d/ -f1
```

Update `ai-insights-service/.env` with the new IP, then rebuild:

```bash
docker-compose up -d --build ai-insights-service
```

**JWT token expired**

Tokens expire after 24 hours. Open the browser console (`F12`) and run:

```javascript
localStorage.clear()
```

Then log in again.

**IntelliJ not picking up code changes**

Always do **Build → Rebuild Project** before clicking Run after any file change. Or use `./mvnw clean spring-boot:run` from the terminal — it's more reliable.

**Port 5433 conflict (Linux)**

If PostgreSQL is installed locally, it occupies port 5433. The transaction database is mapped to port 5434 in `docker-compose.yml` to avoid this — no changes needed.

**Windows PowerShell execution policy error**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Project Structure

```
finsight/
├── user-service/               <- Spring Boot, JWT auth, BCrypt
├── transaction-service/        <- Spring Boot, CRUD, ownership checks
├── ai-insights-service/        <- FastAPI, LangChain, Ollama, RAG
│   ├── main.py
│   ├── routers/insights.py
│   ├── services/insight_service.py
│   ├── clients/transaction_client.py
│   ├── models/schemas.py
│   ├── seed_transactions.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html              <- Login
│   ├── dashboard.html          <- Transaction list + summary
│   ├── transaction.html        <- Add / Edit form
│   ├── ai-chat.html            <- AI Q&A chat
│   ├── css/style.css
│   └── js/
│       ├── auth.js
│       ├── api.js
│       ├── login.js
│       ├── dashboard.js
│       ├── transaction.js
│       └── ai-chat.js
└── docker-compose.yml
```