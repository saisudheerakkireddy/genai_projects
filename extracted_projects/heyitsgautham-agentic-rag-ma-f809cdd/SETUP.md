# Quick Setup Guide - M&A Due Diligence Agentic RAG

This guide will help you get the system up and running in under 10 minutes.

---

## Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.8 or higher** installed
- ✅ **pip** package manager
- ✅ **VS Code** with Jupyter extension (or Jupyter Notebook)
- ✅ **Internet connection** for downloading dependencies and documents

---

## Step-by-Step Installation

### 1. Get Your Contextual AI API Key (3 minutes)

The system requires a Contextual AI API key. You can get a **free 30-day trial** account:

1. Visit [https://app.contextual.ai](https://app.contextual.ai)
2. Click **"Start Free"** and create an account
3. Navigate to **"API Keys"** in the left sidebar
4. Click **"Create API Key"** and copy it (save it somewhere safe!)

> ⚠️ **Important:** Keep your API key secure. Never commit it to Git.

---

### 2. Clone and Setup Environment (2 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/Group-J.git
cd Group-J

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Configure API Key (1 minute)

Create a `.env` file in the project root directory:

```bash
# On Windows:
echo CONTEXTUAL_API_KEY=your_api_key_here > .env

# On macOS/Linux:
echo "CONTEXTUAL_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual API key from Step 1.

**Example `.env` file:**
```
CONTEXTUAL_API_KEY=sk_live_abc123xyz789
```

---

### 4. Launch the Notebook (1 minute)

#### Option A: VS Code (Recommended)

1. Open VS Code
2. Open the project folder: `File > Open Folder > Select Group-J`
3. Open `Agentic_RAG.ipynb`
4. Select Python interpreter from your virtual environment
5. Click "Run All" or run cells individually

#### Option B: Jupyter Notebook

```bash
# Make sure virtual environment is activated
jupyter notebook Agentic_RAG.ipynb
```

Your browser will open with the notebook.

---

### 5. Run the Demo (5 minutes)

Execute the cells in order:

1. **Cells 1-7:** Setup and authentication (30 seconds)
2. **Cells 8-9:** Create datastore (10 seconds)
3. **Cells 10-13:** Upload documents (2-3 minutes)
   - Files will download automatically from GitHub
   - If download fails, follow the prompts to add files manually
4. **Cells 18:** Create RAG agent (10 seconds)
5. **Cells 20-23:** Query and get results! (30 seconds)

---

## Quick Troubleshooting

### Issue: API Key Not Found

**Error:** `API key not found` or `Authentication failed`

**Solution:**
1. Check that `.env` file exists in project root
2. Verify `.env` contains: `CONTEXTUAL_API_KEY=your_actual_key`
3. Restart the Jupyter kernel
4. Re-run cell 7 (API key loading)

---

### Issue: File Download Fails

**Error:** `✗ Download failed: Request timed out` or `HTTP Error 404`

**Solution:**
1. Check your internet connection
2. The system will prompt you with the file path
3. Download the file manually and place it in the `data/` folder
4. Re-run cell 13

**Manual download links:**
- [File 1](https://raw.githubusercontent.com/ContextualAI/examples/refs/heads/main/08-ai-workshop/data/A_Rev_by_Mkt_Qtrly_Trend_Q425.pdf)
- [File 2](https://raw.githubusercontent.com/ContextualAI/examples/refs/heads/main/08-ai-workshop/data/B_Q423-Qtrly-Revenue-by-Market-slide.pdf)
- [File 3](https://raw.githubusercontent.com/ContextualAI/examples/refs/heads/main/08-ai-workshop/data/C_Neptune.pdf)
- [File 4](https://raw.githubusercontent.com/ContextualAI/examples/refs/heads/main/08-ai-workshop/data/D_Unilever.pdf)

---

### Issue: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'contextual'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt

# If using Jupyter, install ipykernel
pip install ipykernel
python -m ipykernel install --user --name=venv
```

---

### Issue: Jupyter Kernel Dies

**Error:** Kernel crashes or "Dead kernel" message

**Solution:**
1. Restart kernel: `Kernel > Restart`
2. Check RAM usage (close other applications if needed)
3. Update Jupyter: `pip install --upgrade jupyter ipykernel`

---

## Testing Your Installation

Run this simple test to verify everything works:

```python
# Test cell - run this after completing setup
from contextual import ContextualAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("CONTEXTUAL_API_KEY")

if API_KEY:
    client = ContextualAI(api_key=API_KEY)
    print("✅ Authentication successful!")
    
    # List datastores
    datastores = client.datastores.list()
    print(f"✅ Connected to Contextual AI")
    print(f"📊 You have access to {len(datastores)} datastore(s)")
else:
    print("❌ API key not found. Check your .env file")
```

Expected output:
```
✅ Authentication successful!
✅ Connected to Contextual AI
📊 You have access to 0 datastore(s)
```

---

## Using Your Own Documents

To analyze your own financial documents:

1. Place PDF files in the `data/` directory
2. Use cell 15 (uncomment the code block)
3. Or modify cell 11 to add your own file URLs:

```python
files_to_upload = [
    ("your_document.pdf", "https://your-url.com/document.pdf"),
    # Add more files here
]
```

---

## Performance Tips

### Faster Setup
- Use a stable internet connection for initial downloads
- Pre-download sample documents to `data/` folder
- Keep your API key in `.env` for quick restarts

### Cost Optimization
- The free tier includes 30 days of usage
- Monitor your usage at [app.contextual.ai](https://app.contextual.ai)
- Use smaller document sets for testing

### Better Results
- Ask specific, well-formed questions
- Reference specific documents when known
- Use follow-up queries to drill down into details

---

## Next Steps

Once setup is complete:

1. **Try the suggested queries** (cell 18) to see the system in action
2. **Explore component demos** (cells 24-73) to understand how each piece works
3. **Upload your own documents** and test with real M&A scenarios
4. **Run evaluations** (cells 60-73) to assess performance
5. **Customize the system prompt** (cell 18) for your specific use case

---

## Resource Links

- 📖 [Full Documentation](README.md)
- 🌐 [Contextual AI Platform](https://app.contextual.ai)
- 📚 [API Documentation](https://docs.contextual.ai/)
- 💬 [GitHub Issues](https://github.com/yourusername/Group-J/issues)

---

## Getting Help

If you encounter issues not covered here:

1. Check the [README.md](README.md) for detailed documentation
2. Review [GUIDELINES.md](GUIDELINES.md) for hackathon requirements
3. Check [cursor-instructions.md](cursor-instructions.md) for implementation details
4. Open an issue on GitHub with:
   - Error message (full stack trace)
   - Steps to reproduce
   - Your Python version (`python --version`)
   - Your OS

---

**Happy Analyzing! 🚀**

Built by Group-J for GenAIVersity Hackathon

