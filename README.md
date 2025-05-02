# 🧠 Elycia: A Local Second Brain

Elycia is a lightweight, privacy-first second brain for developers, powered by your IDE, LlamaIndex, and Markdown. It supports secure, structured, and obfuscated note-taking with natural language search — without relying on cloud services.

---

## ✅ Features Implemented

- **Note capture via IDE tab**
  - Run `make note` to open a new markdown note in your IDE
  - Stored in `notes/YYYY-MM-DD/HH-MM-SS.md`
- **Automatic obfuscation**
  - Notes are obfuscated on every save using a `.env` file for sensitive mappings
  - Output saved to `obfuscated/YYYY-MM-DD/HH-MM-SS.md`
- **Secure, human-readable token format**
  - Tokens like `🔐PROJECT_ab12🔐`, `🔐PERSON_9fc3🔐` created using a short hash
- **Manual indexing**
  - Run `make index` to embed and index all obfuscated notes using LlamaIndex + Chroma
  - Recursively processes all files under `./obfuscated/`
- **No cloud dependency for core flow**
  - Embedding uses OpenAI only if enabled via `.env` with `OPENAI_API_KEY`

---

## 📁 Directory Structure

```bash
elycia/
├── notes/                  # Raw notes organized by date
│   └── 2025-04-30/14-12-33.md
├── obfuscated/            # Obfuscated versions of notes
│   └── 2025-04-30/14-12-33.md
├── brain/                 # Chroma vector store (persisted index)
├── scripts/
│   ├── new_note.py        # Opens IDE, watches file, obfuscates on save
│   ├── index_notes.py     # Indexes obfuscated notes with LlamaIndex
├── .env                   # Stores SENSITIVE_ tokens for obfuscation
├── Makefile               # Simplified command entry points
└── README.md
```

---

## 🚀 Usage

### 📓 Create a new note
```bash
make note
```
- Opens IDE (auto-detected: VSCode, PyCharm, nano)
- On save, content is obfuscated and saved to `obfuscated/`

### 🔍 Index your brain
```bash
make index
```
- Embeds all obfuscated notes under `./obfuscated/`
- Saves to Chroma database in `./brain/`

---

## 🔐 Obfuscation Configuration

Add sensitive terms to your `.env` like this:
```env
SENSITIVE_CompanyX=COMPANY_a1f3
SENSITIVE_ProjectZeus=PROJECT_7c2e
SENSITIVE_Maya=PERSON_b819
```

Token values are generated using a deterministic short hash.

---

## 🛠 Dependencies

- [Poetry](https://python-poetry.org/) for dependency management
- [LlamaIndex](https://github.com/jerryjliu/llama_index) for semantic search
- [Chroma](https://github.com/chroma-core/chroma) for local vector storage
- [watchexec](https://github.com/watchexec/watchexec) to watch notes on save

To install `watchexec`:
```bash
brew install watchexec  # macOS
# or
cargo install watchexec-cli
```

---

## 🧪 Local Testing

- Run `make note` and type some semicolon-separated thoughts
- Save the file in your IDE
- Observe the corresponding obfuscated note in `./obfuscated/`
- Run `make index` to update the semantic index

---

## 📦 Future Plans
- Add querying support
- Integrate OpenAI/Claude as optional summarizers
- Build an Electron UI for conversational recall

---
