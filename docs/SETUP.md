# Installation Guide

Complete step-by-step setup instructions for iTrip on Windows, macOS, and Linux.

## Prerequisites Checklist

- [ ] Python 3.10 or higher
- [ ] Node.js 18.x or higher
- [ ] Git
- [ ] Docker & Docker Compose (optional, for Qdrant/PostgreSQL)
- [ ] Text editor or IDE (VS Code recommended)
- [ ] API key from OpenAI, Anthropic, or Google Gemini
- [ ] 2GB free disk space minimum

---

## Windows Setup

### Step 1: Install Prerequisites

#### Python 3.10+
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.11" (or newer)
3. **Important**: Check "Add Python to PATH"
4. Click "Install Now"
5. Wait for installation to complete

**Verify installation:**
```powershell
python --version
pip --version
```

#### Node.js 18+
1. Go to https://nodejs.org/
2. Download LTS version (18.x or newer)
3. Run the installer
4. Accept all defaults
5. Click "Install"

**Verify installation:**
```powershell
node --version
npm --version
```

#### Git
1. Go to https://git-scm.com/download/win
2. Download the installer
3. Run the installer and accept all defaults
4. Restart your computer

### Step 2: Clone the Repository

1. Open PowerShell or Command Prompt
2. Navigate to where you want the project:
   ```powershell
   cd Desktop
   ```
3. Clone the repository:
   ```powershell
   git clone https://github.com/kemperdesign/iTrip.git
   cd iTrip
   ```

### Step 3: Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
Copy-Item .env.example .env

# Open .env in editor and fill in API keys
notepad .env
```

Edit `.env`:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
SECRET_KEY=your-generated-key
```

To generate SECRET_KEY:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Frontend Setup

```powershell
# Open new PowerShell window
cd iTrip\frontend

# Install dependencies
npm install
```

### Step 5: Docker (Optional)

If you want to use Qdrant vector database and PostgreSQL:

1. Install Docker Desktop: https://www.docker.com/products/docker-desktop
2. Start Docker Desktop
3. In PowerShell:
   ```powershell
   cd iTrip
   docker-compose up -d
   ```

### Step 6: Start Services

**Terminal 1 - Backend:**
```powershell
cd iTrip\backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd iTrip\frontend
npm run dev
```

### Step 7: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Login: `test@example.com` / `password`

---

## macOS Setup

### Step 1: Install Prerequisites

#### Using Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install Node
brew install node

# Install Git (usually pre-installed)
brew install git
```

**Without Homebrew:**
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Git: https://git-scm.com/

### Step 2: Clone Repository

```bash
cd ~/Desktop
git clone https://github.com/kemperdesign/iTrip.git
cd iTrip
```

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Or open in text editor:
```bash
open -a TextEdit .env
```

Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

### Step 5: Docker (Optional)

```bash
# Install Docker
brew install --cask docker

# Or download from https://www.docker.com/products/docker-desktop

# Start services
docker-compose up -d
```

### Step 6: Start Services

**Terminal 1 - Backend:**
```bash
cd iTrip/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd iTrip/frontend
npm run dev
```

### Step 7: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Linux Setup

### Step 1: Install Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv python3-pip nodejs git curl
```

**Fedora/RHEL:**
```bash
sudo dnf install python3.10 python3.10-pip nodejs git curl
```

**Arch:**
```bash
sudo pacman -S python nodejs git
```

### Step 2: Clone Repository

```bash
cd ~/Desktop
git clone https://github.com/kemperdesign/iTrip.git
cd iTrip
```

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env
nano .env
```

Generate SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Frontend Setup

```bash
cd ../frontend
npm install
```

### Step 5: Docker (Optional)

**Ubuntu/Debian:**
```bash
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER
```

**Start services:**
```bash
docker-compose up -d
```

### Step 6: Start Services

**Terminal 1 - Backend:**
```bash
cd iTrip/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd iTrip/frontend
npm run dev
```

### Step 7: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Verifying Installation

### Backend Verification

```bash
# Test backend API
curl http://localhost:8000/docs

# Expected: Swagger UI page loads
```

### Frontend Verification

```bash
# Frontend should be running
# Navigate to http://localhost:3000
# Should see login page
```

### Database Verification

```bash
# Check SQLite database created
ls -la backend/itrip.db

# Or on Windows:
dir backend\itrip.db
```

### Qdrant Verification (if using Docker)

```bash
# Check Qdrant health
curl http://localhost:6333/health

# Expected: {"status":"ok"}
```

---

## First Run Walkthrough

### 1. Login
1. Open http://localhost:3000
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `password`
3. Click "Login"

### 2. Upload Sample Data
1. Navigate to "Imports" page
2. Upload the sample data files:
   - `example of internal property data.docx`
   - `NEW common responses doc.docx`
   - `Copy of Historical data 2025.xlsx`
3. Wait for files to process (green checkmark)

### 3. Test Property Brain
1. Go to "Property Brain" page
2. Ask a question: "What is the WiFi password?"
3. View the answer and source documents

### 4. Generate a Quote
1. Go to "Quote Builder" page
2. Fill in form:
   - Property: Select from dropdown
   - Dates: Pick check-in and check-out
   - Guest count: 4
   - Guest type: Family
3. Click "Generate Quote"
4. View three-tier pricing recommendation

### 5. View Analytics
1. Go to "Revenue Analysis" page
2. View "Top Properties" report
3. Select property to see monthly trends

---

## Troubleshooting Installation

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Use different port
uvicorn app.main:app --reload --port 8001
```

### Python Not Found

```bash
# Windows: Try python3
python3 --version

# macOS/Linux
python3 --version
alias python=python3
```

### npm: command not found

1. Restart terminal/PowerShell
2. Verify Node installation: `node --version`
3. Reinstall Node if needed

### Virtual Environment Won't Activate

```bash
# Recreate virtual environment
rm -rf backend/venv
python -m venv backend/venv

# Windows
backend\venv\Scripts\activate

# macOS/Linux
source backend/venv/bin/activate
```

### API Key Issues

1. Verify key is correct: https://platform.openai.com/account/api-keys
2. Check API key has credits
3. Verify format: `sk-proj-...` for OpenAI
4. For Anthropic: `sk-ant-...`
5. For Gemini: `AIza...`

### Database Locked

```bash
# Delete database and restart
rm backend/itrip.db

# Windows
del backend\itrip.db

# Restart backend server
```

### Docker Issues

```bash
# Ensure Docker is running
docker ps

# Restart containers
docker-compose restart

# View logs
docker-compose logs -f

# Reset everything
docker-compose down -v
docker-compose up -d
```

---

## Getting Help

- **Documentation**: Read [README.md](../README.md) and [DEVELOPMENT.md](../DEVELOPMENT.md)
- **Issues**: Check [GitHub Issues](https://github.com/kemperdesign/iTrip/issues)
- **Email**: kemperdesignservices@gmail.com
- **API Docs**: http://localhost:8000/docs (interactive API testing)

---

## Next Steps

After successful installation:

1. Read [FEATURES.md](./FEATURES.md) for feature guides
2. Read [API.md](./API.md) for API reference
3. Check [DEVELOPMENT.md](../DEVELOPMENT.md) for development tips
4. Upload your actual property data
5. Customize templates and settings

---

## Uninstallation

To completely remove iTrip:

```bash
# Remove project directory
rm -rf iTrip

# Windows: use File Explorer to delete folder

# Remove database
rm ~/iTrip/backend/itrip.db

# Docker cleanup (if used)
docker-compose down -v
docker rmi itrip-backend itrip-frontend
```

---

For more detailed information, see [DEVELOPMENT.md](../DEVELOPMENT.md).
