import gradio as gr
from google.cloud import bigquery

# Initialize BigQuery client
client = bigquery.Client()

def ask_rag(question):
    """
    Executes a real-time RAG workflow using BigQuery ML.
    It embeds the user question, performs a vector search against customer reviews,
    and prompts the Gemini model with the retrieved context.
    """
    # Sanitize input to prevent SQL syntax errors (Unclosed string literal)
    safe_question = question.replace("'", " ").replace('"', " ").replace('\n', ' ').strip()
    
    # Combined SQL Query for Embedding -> Vector Search -> LLM Generation
    sql = f"""
    SELECT ml_generate_text_llm_result AS answer
    FROM ML.GENERATE_TEXT(
        MODEL `CustomerReview.Gemini`,
        (
            SELECT CONCAT('User Question: {safe_question}\\nContext:\\n', 
            STRING_AGG(content, '\\n')) AS prompt
            FROM VECTOR_SEARCH(
                TABLE `CustomerReview.customer_reviews_embedded`,
                'ml_generate_embedding_result',
                (SELECT ml_generate_embedding_result FROM ML.GENERATE_EMBEDDING(
                    MODEL `CustomerReview.Embeddings`, (SELECT '{safe_question}' AS content))),
                top_k => 3
            )
        ),
        STRUCT(0.4 AS temperature)
    );
    """
    try:
        query_job = client.query(sql)
        result = list(query_job.result())
        return result[0].answer if result else "No relevant information found in the database."
    except Exception as e:
        return f"System Error: {str(e)}"

# Build the Gradio Web Interface
demo = gr.Interface(
    fn=ask_rag,
    inputs=gr.Textbox(lines=2, placeholder="Ask about customer service, coffee quality, etc...", label="User Query"),
    outputs=gr.Textbox(label="RAG-Powered AI Response"),
    title="Customer Reviews AI Assistant",
    description="Ask the AI about customer feedback. The system uses Vector Search on BigQuery to retrieve relevant context before generating a highly accurate answer.",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
