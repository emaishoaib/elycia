# 🧠 Personal Second Brain Assistant (Desktop App)

This project aims to build a **cross-platform desktop app** (macOS + Windows) that acts as a personal "second brain": capturing knowledge snippets, organizing them, protecting sensitive content, and enabling retrieval and LLM-powered conversations.

---

## ✅ Goal

Create a keyboard-activated app that:
- Opens a lightweight input window for quick notes
- Records those notes (date-aware)
- Obfuscates sensitive content using a user-defined mapping
- Stores both raw and obfuscated versions
- Indexes the obfuscated notes using LLM embeddings
- Allows natural language queries and ChatGPT-style conversations
- Can store conversations into the second brain on command

---

## 📦 Feature Breakdown

### 1. **Quick-Capture Input App (Desktop GUI)**
- Cross-platform (Electron)
- Opens via keyboard shortcut
- Text input field
- "Submit" triggers save + obfuscation + indexing

### 2. **Note Recording and Organization**
- Raw note saved as `.md` file under `notes/YYYY-MM-DD.md`
- Each entry timestamped and separated
- Obfuscated version saved in parallel (`obfuscated/YYYY-MM-DD.md`)
- Obfuscation uses predefined dictionary (configurable)

### 3. **Sensitive Info Obfuscation**
- Custom mapping file (YAML or JSON)
- Words like company name, project names, or people obfuscated
- Stored as constants or user-editable config file

### 4. **Indexing System**
- Uses LlamaIndex for embedding
- Stores vector index using **Chroma**
- Works entirely offline, private, and local

### 5. **Natural Language Query Interface**
- Input box for asking questions like:
    - "What do I know about requisition IDs?"
    - "How many Lucidchart links exist for [company]?"
    - "Is there a Lucidchart on test ID mapping?"
- Returns answers based on indexed obfuscated notes
- De-obfuscates tokens in final output

### 6. **LLM Querying (ChatGPT / Claude)**
- Option to forward user prompt to external LLM API
- Allow follow-up conversation
- Option to "Record this chat" → saves to notes + indexes like normal

---

## 🔐 Privacy Model
- Only obfuscated notes are indexed
- Raw notes never sent to LLM
- Decryption only happens client-side at display time
- Sensitive mapping never leaves your machine

---

## 🛠️ Tech Stack

| Concern        | Selected Option             |
| -------------- | --------------------------- |
| GUI            | Electron                    |
| Note Parsing   | Python                      |
| Embedding      | LlamaIndex                  |
| Vector Storage | Chroma                      |
| LLM API        | OpenAI / Anthropic (Claude) |
| Packaging      | Poetry                      |

---

## 📁 Proposed Project Structure

```
my-second-brain/
├── app/                  # GUI app frontend (Electron)
├── notes/                # Raw markdown notes
├── obfuscated/           # Obfuscated version of notes
├── brain/                # Vector indexes (Chroma)
├── config/
│   └── sensitive_terms.json
├── scripts/
│   ├── obfuscate.py
│   ├── index_notes.py
│   ├── query_brain.py
│   └── send_to_llm.py
├── README.md
└── pyproject.toml        # Poetry package config
```

---

## 📌 Next Steps
1. Define the sensitive term obfuscation format (JSON/YAML)
2. Scaffold Electron app for note capture
3. Hook Electron frontend to Python backend via IPC or local API
4. Build obfuscator and Chroma-compatible indexing system
5. Implement querying and de-obfuscation
6. Add OpenAI/Claude integration and record-to-notes feature

---