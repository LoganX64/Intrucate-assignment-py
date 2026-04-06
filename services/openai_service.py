# import asyncio
import os
from openai import AsyncOpenAI
from config import Config

# Global client
_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = getattr(Config, 'OPENAI_API_KEY', None) 
        
        if not api_key or api_key.strip() == "":
            raise ValueError("OPENAI_API_KEY is not configured in Config")
        
        _client = AsyncOpenAI(
            base_url="https://api.fireworks.ai/inference/v1",
            api_key=api_key
        )
    return _client

async def get_ai_response(userInput: str, prompt_id="Education_Prompt"):
    from services.prompt_service import get_prompt_template
    
    template = get_prompt_template(prompt_id)
    final_prompt = template.replace("{{userInput}}", userInput)
    
    print(f"Final Prompt: {final_prompt[:150]}...")

    client = AsyncOpenAI(
        base_url="https://api.fireworks.ai/inference/v1",
        api_key=Config.OPENAI_API_KEY   
    )

    try:
        client = _get_client()
        response = await client.chat.completions.create(
            model="accounts/fireworks/models/deepseek-v3p2",
            messages=[{"role": "user", "content": final_prompt}],
            max_tokens=1024, # Adjust as needed 1024,2048
            temperature=0.7,
            top_p=0.95
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise

    # client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
    
    # response = await client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": final_prompt}]
    # )
    
    # return response.choices[0].message.content
    
    
#     await asyncio.sleep(0.7)   # delay
    
#     mockResponse = f"""[Mock AI Response for testing]
# Question: {userInput}

# As an education expert for CA Final:
# - You need minimum 40% in each subject and 50% aggregate to pass.
# - Solve at least 5 previous year papers.

# (This is mock response for testing purpose)
# """
#     # return mockResponse.strip()