import asyncio
from openai import AsyncOpenAI
from config import Config

async def get_ai_response(userInput: str, prompt_id="Education_Prompt"):
    from services.prompt_service import get_prompt_template
    
    template = get_prompt_template(prompt_id)
    final_prompt = template.replace("{{userInput}}", userInput)

    # client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
    
    # response = await client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": final_prompt}]
    # )
    
    # return response.choices[0].message.content
    
    print(f"Final Prompt: {final_prompt[:100]}...")
    
    await asyncio.sleep(0.7)   # delay
    
    mockResponse = f"""[Mock AI Response for testing]
Question: {userInput}

As an education expert for CA Final:
- You need minimum 40% in each subject and 50% aggregate to pass.
- Solve at least 5 previous year papers.

(This is mock response for testing purpose)
"""
    return mockResponse.strip()