# 🚀 Adobe India Hackathon 2025 – Connecting the Dots  
## Rethink Reading. Rediscover Knowledge.

What if every PDF you opened wasn't just a document—but a **living, thinking companion**?  
What if it could **summarize**, **connect**, and **guide** you through your ideas?

We’re building that future. This is our solution to Adobe’s **"Connecting the Dots"** Challenge.

---

## 🔍 Problem Statement

In a world of static documents, the challenge is no longer more content—it’s **more context**.  
Our mission is to transform PDFs into intelligent, interactive companions that:

- 🧠 Understand and extract structured outlines  
- 🔗 Link related content across collections  
- 📚 Provide insight tailored to user intent/persona

---

## 💡 Project Structure

```

Adobe-Hackathon-2025/
│
├── Adobe\_1A/               # Challenge 1A: PDF Structuring & Extraction
│   ├── process\_pdfs.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── Adobe\_1B/               # Challenge 1B: Multi-PDF Contextual Linking
│   ├── analyze\_persona.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── .gitignore

````

---

## 📂 Challenge Breakdown

### 🔹 Challenge 1A: PDF Structuring Engine

Builds the core of the system — processes PDFs and outputs structured data like titles, subtitles, and hierarchy.

- ✅ Fast and accurate extraction using PyMuPDF & pdfminer.six  
- ✅ Outputs clean JSON structures  
- ✅ Fully containerized using Docker  

### 🔹 Challenge 1B: Persona-Based Insight Engine

Analyzes multiple documents and links ideas contextually based on target user personas.

- 🔍 Cross-document idea mapping  
- 🧭 Persona-aware question answering  
- 🔗 Connects concepts across unrelated files  

---

## 🐳 Run Using Docker

Make sure Docker is installed.

### For Challenge 1A:

```bash
cd Adobe_1A
docker build -t adobe_1a .
docker run -v $(pwd)/pdfs:/app/pdfs adobe_1a
````

### For Challenge 1B:

```bash
cd Adobe_1B
docker build -t adobe_1b .
docker run -v $(pwd)/pdfs:/app/pdfs adobe_1b
```

---

## 🧠 Tech Stack

| Domain            | Tools / Libraries                   |
| ----------------- | ----------------------------------- |
| Language          | Python                              |
| PDF Parsing       | PyMuPDF, pdfminer.six               |
| Data Handling     | json                                |
| Containerization  | Docker                              |
| NLP Layer         | Custom heuristics + keyword mapping |
| Round 2 (Planned) | Adobe PDF Embed API, Web Frontend   |

---

## ✨ Round 2 Vision

In the next phase, we'll create a smart webapp using Adobe PDF Embed API that allows:

* 📖 Interactive PDF viewing
* 🧭 Outline-based navigation
* 🧠 Real-time summarization and linking
* 🔍 Contextual persona recommendations

---

## 📌 Status

| Challenge | Status         |
| --------- | -------------- |
| 1A        | ✅ Completed    |
| 1B        | ✅ Completed    |


---

