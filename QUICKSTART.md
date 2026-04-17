# Quick Start Guide

## 1. Install Prerequisites

### Option A: Windows
```bash
# Download & Install Ollama
# Go to: https://ollama.ai
# Run installer and create account
```

### Option B: macOS/Linux
```bash
# macOS with Homebrew
brew install ollama

# Or download from https://ollama.ai
```

## 2. Start Ollama

Open a new terminal and keep it running:
```bash
ollama serve
```

It will show: `Listening on 127.0.0.1:11434`

## 3. Pull a Model

In another terminal:
```bash
ollama pull llama2
```

This downloads the model (~5GB). Wait for completion.

## 4. Setup DevOps Agent

### Windows:
```bash
cd "d:\Devops Agent"
setup.bat
```

### macOS/Linux:
```bash
cd ~/Devops\ Agent
bash setup.sh
```

## 5. Configure Email

Edit `.env` file:
```ini
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECIPIENT=where-to-send@example.com
```

**Get Gmail App Password:**
1. Go to https://mail.google.com/mail/u/0/accounts/rescueaccount
2. Enable 2-factor authentication (if not enabled)
3. Generate App Password for "Mail" and "Windows Device"
4. Use this 16-char password in .env

## 6. Test Configuration

```bash
python main.py check-config
```

Should show:
- ✓ Email configured correctly
- ✓ Ollama is running

## 7. Run Pipeline Successfully

```bash
python main.py run
```

Expected output:
```
============================================================
Starting Pipeline Execution: 20260415_101530
============================================================
[STAGE] Build starting...
[STAGE] Build PASSED
[STAGE] Lint starting...
[STAGE] Lint PASSED
[STAGE] Test starting...
[STAGE] Test PASSED
============================================================
Pipeline Execution SUCCESSFUL ✓
============================================================
```

## 8. Test with Forced Failure

```bash
python main.py run --fail-at Test
```

This will:
1. Run Build ✓
2. Run Lint ✓
3. Fail at Test ✗
4. Analyze error with Ollama
5. Send email with AI recommendations

Check your email!

## Available Commands

```bash
# Run pipeline
python main.py run

# Force failure at specific stage
python main.py run --fail-at Build
python main.py run --fail-at Lint
python main.py run --fail-at Test

# Test email configuration
python main.py test-email

# Check system configuration
python main.py check-config

# See all commands
python main.py --help
```

## Logs

Pipeline logs are saved in `logs/` directory:
```
logs/
├── pipeline_20260415_101530.log
├── pipeline_20260415_101545.log
└── ...
```

## Troubleshooting

### "Ollama is not running"
```bash
# Terminal 1
ollama serve

# Terminal 2 (run commands here)
python main.py run
```

### "Email authentication failed"
- Double-check .env credentials
- Verify Gmail App Password (not regular password)
- Some Gmail accounts need settings changes

### "Connection refused" error
- Make sure Ollama is running in background
- Check firewall settings
- Try: http://127.0.0.1:11434 instead

