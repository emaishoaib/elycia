# 🧠 Elycia: AI-Powered Local Second Brain

Elycia is a privacy-focused second brain that lets you:
- Write notes in Markdown via your IDE
- Obfuscate sensitive content using `.env` mappings
- Search your notes using local embeddings + Chroma
- Query in natural language without sending data to the cloud
- Keep full versioned control using Git + Markdown

---

## 🛠 Tech Stack
- **GUI (IDE)**: PyCharm or VSCode (invoked by script)
- **Note Parsing**: Python 3.12
- **Embedding & Indexing**: LlamaIndex
- **Vector DB**: Chroma (local, using `chromadb`)
- **LLM API (optional)**: OpenAI / Claude
- **Package Management**: Poetry
- **Automation**: Makefile + Scripts
- **Linting & Hooks**: Ruff + Pre-commit

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
poetry install
```

### 2. Setup pre-commit hooks
```bash
poetry run pre-commit install
```

### 3. Configure `.env`
Define obfuscation mappings like:
```dotenv
SENSITIVE_Project_Zeus=🔐PROJECT_abcd🔐
SENSITIVE_John_Doe=🔐PERSON_1234🔐
```

---

## ✍️ Adding Notes
```bash
make note
```
- Opens your IDE with a blank markdown file
- When you close the file, it is saved to `notes/YYYY-MM-DD/HH-MM-SS.md`
- It is automatically obfuscated to `obfuscated/YYYY-MM-DD/HH-MM-SS.md`

---

## 🔐 Obfuscating Notes (manually)
```bash
make sync
```
- Re-obfuscates all notes using current `.env`

---

## 🧠 Indexing Notes
```bash
make index
```
- Scans `obfuscated/**/*.md`
- Embeds the content using LlamaIndex
- Stores to Chroma vector store in `./brain`

---

## 🔎 Querying Your Brain
```bash
make query
```
- Prompts for your question in the terminal
- Writes the result to `__query_preview__.md`
- Opens that file in your configured editor (via `EDITOR_APP` in `.env`)
- Deletes the file when closed

---

## ✅ Pre-commit Checks

Elycia uses [pre-commit](https://pre-commit.com/) to auto-check code style, linting, and config:

- Ruff (`ruff` + `ruff-format`)
- Poetry config validation
- No large files, private keys, debug prints, etc.

### Run manually:
```bash
poetry run pre-commit run --all-files
```

---

## 📂 Directory Structure
```txt
notes/               # Raw notes written by you
obfuscated/          # Obfuscated copies with sensitive info replaced
brain/               # Chroma vector store index
scripts/             # Python scripts for adding, syncing, querying
.env                 # Your obfuscation mappings (not committed)
```

---

## 🔒 Privacy Note
No data leaves your machine. Obfuscation ensures even local embeddings don’t include sensitive terms.

