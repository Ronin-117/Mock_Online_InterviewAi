from transformers import BertTokenizer, BertForSequenceClassification
import torch

def set_sentance_complete(results_path):
    print(f"{results_path =}")
    # 1. Load the tokenizer and model
    tokenizer = BertTokenizer.from_pretrained(results_path,local_files_only=True) # same folder that the pretrained values are
    model = BertForSequenceClassification.from_pretrained(results_path,local_files_only=True) # same folder that the pretrained values are

    # 2. Define the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device) #Move model to the active device.
    model.eval() #put model in evaluation mode
    return tokenizer, model, device


# 3. Define the is_complete function
def is_complete(text, tokenizer, model, device): #now passes arguments
    """
    Classifies if the given text is complete or incomplete using a pre-trained DistilBERT model.
    """
    if not text:
        return 1
    model.eval()  # Set the model to evaluation mode
    model.to(device) #move model to device

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device) # Move inputs to device
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(probabilities).item()  # Use item() to get the Python number
    return predicted_class
# 4. Example usage

if __name__ == "__main__":
    tokenizer, model, device = set_sentance_complete("results") #now we pass the training and test objects in here
    text_to_test = "hello my name is neil joseph and i am a data scientist. i like to "  #@param {type:"string"}
    # Run the check
    prediction = is_complete(text_to_test, tokenizer, model, device) #now we pass the training and test objects in here, we also pass the text string

    # Convert numerical values to what we defined before (label2id = {"complete": 0, "incomplete": 1}
    labels= {0: "complete", 1: "incomplete"}
    predicted_label=labels[prediction] #Here we get the label from the dictionary with key values

    # 5. Output the result.
    print(f"The sentence '{text_to_test}' is predicted as: {predicted_label}")
