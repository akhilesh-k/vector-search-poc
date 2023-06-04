from sentence_transformers import SentenceTransformer

# Example query
sentences = ["women shirt red color"]

# Load or create a SentenceTransformer model.
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Compute sentence embeddings.
embeddings = model.encode(sentences)

# Create a list object, comma separated.
vector_embeddings = list(embeddings)
print(vector_embeddings)