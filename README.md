# 📚 Semantic Page Locator

**Find the exact page that answers your question.**

A lightweight desktop tool for students to search through course PDFs using natural language. Type a question like *"What is the Bellman equation?"* and instantly get the page numbers where it's explained.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

- **Hybrid Search** — Combines keyword matching (BM25) with meaning-based ranking
- **Works Offline** — No internet needed after initial setup
- **Lightweight** — Runs smoothly on 4GB laptops
- **Open PDF at Page** — Double-click a result to jump directly to that page
- **Adjustable Search Mode** — Slider to balance between semantic and literal matching

---

## 🚀 Quick Start

### 1. Install

```bash
# Clone the repo
git clone https://github.com/llk214/semantic-locator.git
cd semantic-locator

# Install dependencies
pip install -r requirements.txt
```

### 2. Run

```bash
python gui.py
```

### 3. Use

1. Click **Browse** and select a folder containing your PDFs
2. Click **Load/Rebuild Index** (first time takes ~30 seconds)
3. Type your question and hit **Search**
4. Double-click any result to open the PDF at that page

---

## 🎛️ Search Quality Options

Choose based on your hardware:

| Option | Download Size | RAM Needed | Best For |
|--------|---------------|------------|----------|
| ⚡ Fast | ~80MB | 4GB | Older laptops |
| ⚖️ Balanced | ~420MB | 8GB | Most users |
| 🎯 High Accuracy | ~440MB | 8GB | Better results |
| 🚀 Best | ~1.3GB | 16GB+ | Gaming PCs |

---

## 🎚️ Search Mode Slider

Adjust how search works:

```
🧠 Semantic ◀━━━━━━━━━━▶ 🔤 Literal
```

| Slide Left | Slide Right |
|------------|-------------|
| Understands meaning | Matches exact words |
| *"How does learning from experience work?"* | *"Bellman equation"* |

---

## 📁 Supported Files

- ✅ PDF (`.pdf`)

> **Tip:** Export your `.pptx` and `.docx` files to PDF for best results

---

## 🛠️ Requirements

- Python 3.8+
- ~500MB disk space (for models)
- PDF reader with command-line support (e.g., [SumatraPDF](https://www.sumatrapdfreader.org/))

---

## 📦 Dependencies

```
PyMuPDF          # PDF text extraction
rank-bm25        # Keyword search
sentence-transformers  # Semantic matching
```

---

## 💡 Tips for Better Results

1. **Add student notes** — Well-organized notes with clear headings improve search quality
2. **Use specific terms** — *"Q-learning update rule"* works better than *"how does it learn"*
3. **Adjust the slider** — Use literal mode for exact terms, semantic mode for concepts

---

## 🤔 FAQ

**Is this an AI/LLM?**  
No. It uses embedding models for similarity matching, not generative AI. It finds information — it doesn't generate answers.

**Can I use this during exams?**  
If "no LLM" is the rule, this tool is fine — it's just a smart search engine for your own materials.

**Why doesn't the page jump work?**  
Install [SumatraPDF](https://www.sumatrapdfreader.org/) — it has the best command-line page navigation support.

---

## 📄 License

MIT — free for personal and educational use.

---

<p align="center">
  Made for students, by students 📖
</p>
