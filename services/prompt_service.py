from db import mongo
from datetime import datetime

def get_prompt_template(prompt_id="Education_Prompt"):

    prompt_doc = mongo.db.prompts.find_one({"_id": prompt_id})

    if not prompt_doc:
        prompt_doc = {
            "_id": prompt_id,
            "template": "You are an expert in education domain. Answer the following: {{userInput}}",
            "created_at": datetime.utcnow()
        }
        mongo.db.prompts.insert_one(prompt_doc)

    return prompt_doc.get("template")