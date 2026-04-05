from db import mongo
from datetime import datetime

def save_to_history(userInput, aiResponse, prompt_id="Education_Prompt", is_batch=False):

    history_record = {
        "timestamp": datetime.utcnow(),
        "prompt_id": prompt_id,
        "user_input": userInput,
        "ai_response": aiResponse,
        "model": "gpt-4o-mini",
        "request_type": "batch" if is_batch else "single",  
        "is_batch": is_batch
    }
    
    mongo.db.history.insert_one(history_record)
    print(f"History saved| Type: {'BATCH' if is_batch else 'SINGLE'} | Input: {userInput[:60]}...")