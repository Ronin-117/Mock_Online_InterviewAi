from transformers import BertTokenizer, BertForSequenceClassification
import torch

def set_sentance_complete(results_path):
    print(f"{results_path =}")
    # 1. Load the tokenizer and model
    tokenizer = BertTokenizer.from_pretrained(results_path,local_files_only=True)
    model = BertForSequenceClassification.from_pretrained(results_path,local_files_only=True) 

    # 2. Define the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device) 
    model.eval() 
    return tokenizer, model, device


# 3. Define the is_complete function
def is_complete(text, tokenizer, model, device): 
    """
    Classifies if the given text is complete or incomplete using a pre-trained DistilBERT model.
    """
    if not text:
        return 1
    model.eval() 
    model.to(device)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(probabilities).item()  
    return predicted_class
# 4. Example usage

if __name__ == "__main__":
    tokenizer, model, device = set_sentance_complete("results") 
    text_to_test = "hello my name is neil joseph and i am a data scientist. i like to "  
    # Run the check
    prediction = is_complete(text_to_test, tokenizer, model, device)

    # Convert numerical values to what we defined before (label2id = {"complete": 0, "incomplete": 1}
    labels= {0: "complete", 1: "incomplete"}
    predicted_label=labels[prediction] 

    # 5. Output the result.
    print(f"The sentence '{text_to_test}' is predicted as: {predicted_label}")
