import numpy as np
import faiss
from model2vec import StaticModel

# Load the model
model = StaticModel.from_pretrained("minishlab/potion-base-2M")

# Get the embedding dimension by encoding a sample text
sample_embedding = model.encode(["sample text"])
embedding_dimension = sample_embedding.shape[1] #Shape of (1,64)
print(f"Embedding dimension: {embedding_dimension}")

# Function to extract embeddings
def extract_embeddings(texts):
    embeddings = model.encode(texts)
    return embeddings

# Load data from files
def load_texts_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f]
    return texts

complete_texts = load_texts_from_file("complete.txt")  # Replace with your file paths
incomplete_texts = load_texts_from_file("incomplete.txt")

# Extract embeddings
complete_embeddings = extract_embeddings(complete_texts)
incomplete_embeddings = extract_embeddings(incomplete_texts)

# Combine embeddings and labels
all_embeddings = np.concatenate([complete_embeddings, incomplete_embeddings])
labels = np.array([1] * len(complete_texts) + [0] * len(incomplete_texts)) # 1 for complete, 0 for incomplete

# Build FAISS index
index = faiss.IndexFlatL2(embedding_dimension)  # L2 distance for similarity
index.add(all_embeddings)

# Save index and labels (for later use)
faiss.write_index(index, "completeness.index")
np.save("completeness_labels.npy", labels)

print("Embeddings extracted and FAISS index built.")