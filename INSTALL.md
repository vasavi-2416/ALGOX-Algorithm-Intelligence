# ALGOX — Installation & Quick Start Guide (macOS)

## Option 1: One-Click Launch (Easiest)
1. Double-click **`start.command`** in Finder.
2. Terminal will open, install any missing dependencies, and launch ALGOX in your browser at `http://localhost:8052`.
3. Default login credentials:
   - **Username:** `admin`
   - **Password:** `algox`

---

## Option 2: Terminal Manual Installation

### Step 1: Open Terminal and navigate to the project directory
```bash
cd "path/to/ALGOX DAA PROJECT"
```

### Step 2: (Recommended) Create & activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

*Required packages:*
- `streamlit>=1.28.0`
- `plotly>=5.18.0`
- `pandas>=2.0.0`
- `numpy>=1.24.0`

### Step 4: Run ALGOX
```bash
streamlit run app.py --server.port 8052
```
or simply:
```bash
./run.sh
```

---

## Access the Application
Open your web browser and navigate to:
**http://localhost:8052**

Login with:
- **Username:** `admin`
- **Password:** `algox`
