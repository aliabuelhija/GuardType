import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
import logging
from sqlalchemy.orm import Session
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import roc_auc_score

from db.models import OffensiveEntry, SourceEnum, Users
from db.database import get_db
from schemas.offensive_entry import RecognizeWordEntryResponse, RecognizeWordEntryRequest, CheckSentenceResponse, \
    CheckSentenceRequest
from services.notification_service import notify_offensive_word

# Create FastAPI app and router
router = APIRouter(prefix='/recognize_word', tags=['recognize_word'])

#Load tokenizer and model
model_path = 'C:/Users/ali12/PycharmProjects/guardtype_server/saved_model'
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=2)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

y_true = [0, 1, 0, 1]
y_scores = [0.1, 0.4, 0.35, 0.8]

auc = roc_auc_score(y_true, y_scores)
print(f"The AUC is: {auc}")


def is_offensive(text, model, tokenizer, device):
    print("Tokenizing text")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    print(f"Inputs: {inputs}")

    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        print(f"Outputs: {outputs.logits}")
        prediction = outputs.logits.argmax(dim=-1).item()

    print(f"Prediction: {prediction}")
    return bool(prediction)


@router.post('/entry', response_model=RecognizeWordEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_recognize_word_entry(request: RecognizeWordEntryRequest, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    notify_offensive_word(user.email, user.username, request.text)

    new_entry = OffensiveEntry(username=request.username, text=request.text, source=SourceEnum.ROOM_SQL)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.post('/check', response_model=CheckSentenceResponse, status_code=status.HTTP_200_OK)
async def check_sentence(request: CheckSentenceRequest, db: Session = Depends(get_db)):
    print(f"Received request: {request.text}")
    logger.info(f"Received request: {request.text}")  # Using logger instead of print
    if not request or not request.text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request text cannot be null or empty")
    offensive = is_offensive(request.text, model, tokenizer, device)
    current_date = datetime.datetime.utcnow()
    user = db.query(Users).filter(Users.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if offensive:
        new_entry = OffensiveEntry(username=request.username, text=request.text, source=SourceEnum.SERVER,
                                   date=current_date)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        notify_offensive_word(user.email,user.username, request.text)
        return {
            "id": new_entry.id,
            "username": new_entry.username,
            "text": new_entry.text,
            "date": new_entry.date,
            "source": new_entry.source,
            "offensive": offensive
        }
    else:
        return {
            "id": None,
            "username": request.username,
            "text": request.text,
            "date": current_date,
            "source": None,
            "offensive": offensive
        }
@router.get('/entries', response_model=List[RecognizeWordEntryResponse], status_code=status.HTTP_200_OK)
async def get_all_recognize_word_entries(db: Session = Depends(get_db)):
    entries = db.query(OffensiveEntry).all()
    return entries
