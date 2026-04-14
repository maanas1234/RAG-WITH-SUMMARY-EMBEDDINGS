# 📚 Multi-Vector RAG with LangChain + Chroma

## 🚀 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline using a **multi-vector retrieval strategy**.

Instead of embedding full documents, it:

* Embeds **summaries** for better semantic search
* Stores **original chunks separately**
* Retrieves **high-quality context** efficiently

---

## 🧠 Core Idea

Traditional RAG:

* Embed full text → noisy + slower

This approach:

* Summaries → used for embedding (clean + fast)
* Original chunks → stored separately (no info loss)

👉 Result: Better retrieval + better answers

---

## 🏗️ Tech Stack

* LangChain
* ChromaDB
* OpenRouter (LLM API)
* HuggingFace Embeddings
* Python

---

## 📁 Project Structure

```
.
├── chroma_db/                  # Vector DB storage
├── BOOKS AND PAPERS FOR AI/   # Input PDFs
├── main.py                     # Main script
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone Repository

```
git clone <your-repo-url>
cd <repo-name>
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Set API Key

#### Linux / Mac

```
export OPENROUTER_API_KEY=your_key_here
```

#### Windows (PowerShell)

```
setx OPENROUTER_API_KEY "your_key_here"
```

---

## ▶️ How It Works

### 1. Load Documents

* Loads PDFs using `DirectoryLoader`

### 2. Split Documents

* Uses `RecursiveCharacterTextSplitter`
* Chunk size = 300

### 3. Generate Summaries

* Each chunk is summarized using an LLM

### 4. Store Data

* Summaries → stored in **Chroma (vector DB)**
* Original chunks → stored in **InMemoryByteStore**

### 5. Retrieval

#### MultiVectorRetriever

* Searches summaries
* Returns full original chunk

#### Similarity Search

* Searches summaries only
* Returns short summaries

---

## 🔍 Example Usage

```python
result = multi_vector_retriever.invoke("Tell me about concept mapper?")
print(result[0])

result2 = summaries_collection.similarity_search("What is concept mapper?")
print(result2)
```

---

## ⚠️ Bug Fix

❌ Incorrect:

```python
doc_id = [str(uuid.uuid4() for _ in chunks)]
```

✅ Correct:

```python
doc_id = [str(uuid.uuid4()) for _ in chunks]
```

---

## ⚠️ Notes

* `reset_collection()` clears DB on every run
* `InMemoryByteStore` is not persistent
* Free OpenRouter models may be slow

---

## 🔥 Future Improvements

* Persistent storage (Redis / disk)
* FastAPI backend
* UI for querying
* Streaming responses
* Embedding visualization (3D)

---

## 💡 Why This Matters

This setup is closer to **production-grade RAG systems**:

* Better semantic retrieval
* Reduced noise
* Scalable for large datasets

---

## ⭐ Contribute

Feel free to fork, improve, and build on top of this.

---

## 📌 Tags

#RAG #LangChain #ChromaDB #LLM #AI #OpenRouter #VectorSearch #MachineLearning
