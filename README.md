# Reviews-RAG-Analyzer-GCP
An end-to-end RAG application built on Google Cloud BigQuery ML and Gemini to analyze customer reviews in real-time.

# GCP BigQuery RAG Assistant 🚀

A complete, end-to-end Retrieval-Augmented Generation (RAG) web application built natively on Google Cloud Platform. This project utilizes BigQuery ML, Vertex AI Vector Search, and the Gemini model to intelligently answer user queries based on a customized dataset of customer reviews.

## 🌟 Features
*   **Fully Managed Backend:** Uses BigQuery ML to store data, generate embeddings, and perform Vector Search without exporting data to external databases.
*   **Native LLM Integration:** Directly invokes the Gemini model via BigQuery remote connections.
*   **Real-Time Retrieval:** Dynamically queries the vector index and passes context to the LLM in a single SQL execution.
*   **Interactive Web UI:** Provides a clean, user-friendly interface using Gradio.

## 🏗️ Architecture
1.  **Data Storage & Embeddings:** Customer reviews are stored in BigQuery. Text embeddings are generated using the `gemini-embedding-001` model.
2.  **Vector Search:** BigQuery ML's `VECTOR_SEARCH` is used to find the top-K reviews that are semantically similar to the user's query.
3.  **Prompt Generation:** The retrieved reviews are concatenated with the user's question.
4.  **LLM Response:** The augmented prompt is sent to `gemini-2.5-flash` to generate an accurate, hallucination-free response.
5.  **Frontend:** A Gradio app hosted on a Google Compute Engine (GCE) VM serves the application to the end user.

## 🚀 Deployment Prerequisites
*   A Google Cloud Project with Compute Engine, BigQuery, and Vertex AI APIs enabled.
*   A Service Account with `BigQuery User` and `BigQuery Data Viewer` roles attached to the VM.
*   VM Access Scope configured to `Allow full access to all Cloud APIs`.
*   A VPC Firewall rule allowing TCP ingress on port `7860`.
