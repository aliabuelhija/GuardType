import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, Dataset
import pandas as pd


# Define the dataset class
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Load data
train_data = pd.read_csv('C:/Users/ali12/PycharmProjects/guardtype_server/training_data_1000.csv')
val_data = pd.read_csv('C:/Users/ali12/PycharmProjects/guardtype_server/validation_data_separate.csv')

# Prepare datasets
train_dataset = TextDataset(train_data['text'].tolist(), train_data['label'].tolist(), tokenizer)
val_dataset = TextDataset(val_data['text'].tolist(), val_data['label'].tolist(), tokenizer)

# DataLoaders
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

# Move model to GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
print(device)

# Optimizer
optimizer = AdamW(model.parameters(), lr=5e-5)


# Training and validation function
def train_and_evaluate(model, train_loader, val_loader, optimizer, epochs=3):
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        total_batches = len(train_loader)
        for i, batch in enumerate(train_loader):
            optimizer.zero_grad()
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            if (i + 1) % 10 == 0:  # Print loss every 10 batches
                print(f'Epoch {epoch + 1}, Batch {i + 1}/{total_batches}, Training Loss: {loss.item()}')

        avg_train_loss = total_loss / total_batches

        # Validation phase
        model.eval()
        total_eval_accuracy = 0
        total_eval_loss = 0
        total_eval_batches = len(val_loader)
        for batch in val_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            with torch.no_grad():
                outputs = model(**batch)
                loss = outputs.loss
                total_eval_loss += loss.item()

                logits = outputs.logits
                predictions = torch.argmax(logits, dim=1)
                correct_predictions = (predictions == batch['labels']).float().sum()
                total_eval_accuracy += correct_predictions

        avg_val_accuracy = total_eval_accuracy / len(val_dataset)
        avg_val_loss = total_eval_loss / total_eval_batches

        print(f'Epoch {epoch + 1} Completed.')
        print(f'Training Loss Average: {avg_train_loss}')
        print(f'Validation Loss Average: {avg_val_loss}')
        print(f'Validation Accuracy: {avg_val_accuracy:.4f}')


# Train the model
train_and_evaluate(model, train_loader, val_loader, optimizer)
# Save the model and tokenizer after training
model.save_pretrained('C:/Users/ali12/PycharmProjects/guardtype_server/saved_model')
tokenizer.save_pretrained('C:/Users/ali12/PycharmProjects/guardtype_server/saved_model')
