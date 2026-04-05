# Education AI Assistant - Flask + MongoDB + OpenAI

A Python-based REST API service that processes educational queries using Mock AI, with support for both single and batch processing requests. Built with Flask for the backend and MongoDB for data persistence.

---

## 📋 Project Overview

This project implements an intelligent assistant that:

- Accepts educational queries via REST API endpoints
- Processes requests asynchronously to avoid blocking
- Returns mock AI responses for testing (without OpenAI API key required)
- Retrieves customizable prompt templates from MongoDB
- Maintains audit trail of all requests and responses in MongoDB
- Supports both single and batch query processing

**Note:** Currently running in **mock mode** - AI responses are simulated. The code structure is ready for real OpenAI API integration when needed.

---

## 📁 Folder Structure

```
Intrucate-assignment-py/
├── app.py                      # Main Flask application & route definitions
├── config.py                   # Configuration management (API keys, MongoDB URI)
├── db.py                       # Database initialization & connection setup
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (MONGO_URI, OPENAI_API_KEY)
│
└── services/                   # Business logic & API integrations
    ├── __init__.py
    ├── prompt_service.py       # Fetch & manage prompts from MongoDB
    ├── openai_service.py       # OpenAI API integration & async processing
    └── history_service.py      # Request/response logging to MongoDB
```

---

## 🗄️ Database Schema

### MongoDB Collections

#### **1. `prompts` Collection**

Stores reusable prompt templates for different domains.

```javascript
{
  "_id": "Education_Prompt",
  "template": "You are an expert in education domain. Answer the following: {{userInput}}",
  "created_at": ISODate("2025-01-15T10:30:00.000Z")
}
```

**Key Features:**

- Template placeholders (`{{userInput}}`) are replaced at runtime
- Easy to maintain & update without code changes
- Supports multiple prompt templates by using different `_id` values

---

#### **2. `history` Collection**

Audit trail of all requests and API responses.

```javascript
{
  "_id": ObjectId("..."),
  "timestamp": ISODate("2025-01-15T10:35:45.000Z"),
  "prompt_id": "Education_Prompt",
  "user_input": "How much should I score in each subject to pass CA final?",
  "ai_response": "You need minimum 40% in each subject...",
  "model": "gpt-4o-mini",
  "request_type": "single",
  "is_batch": false
}
```

**Key Features:**

- Immutable record of all interactions
- Timestamp for tracking & auditing
- Request type indicator (single vs batch)
- Model name for tracking API version changes

---

## 🔧 Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud - MongoDB Atlas)
- OpenAI API Key

### Step 1: Clone & Navigate to Project

```bash
cd d:\Assignment\Intrucate-assignment-py
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# MongoDB Connection String (Required)
MONGO_URI=mongodb://localhost:27017/education_db

# For MongoDB Atlas (cloud)
# MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/education_db

```

**Note:**

- **MongoDB is required** - stores prompts and history
- **OpenAI API Key is optional** - currently using mock responses for testing

**Get API Keys:**

- **MongoDB Atlas:** https://www.mongodb.com/cloud/atlas (free tier available)

---

## 🚀 How to Run

### 1. Ensure MongoDB is Running

```bash
# If using local MongoDB
mongod

# OR use MongoDB Atlas (no local setup needed)
```

### 2. Run the Flask Application

```bash
python app.py
```

**Expected Output:**

```
Server running on http://127.0.0.1:5001
 * Running on http://127.0.0.1:5001
 * Debug mode: on
```

**Available Endpoints:**

- `POST /api/prompt` - Single query processing
- `POST /api/batch_prompt` - Batch query processing

---

## 📡 API Endpoints Documentation

### Endpoint 1: Single Prompt Processing

**POST** `/api/prompt`
(returns mock response).

**Request Body:**

```json
{
  "userInput": "How much should I score in each subject to pass CA final?"
}
```

**Response (Success):**

```json
{
  "response": "[Mock AI Response for testing]\nQuestion: How much should I score in each subject to pass CA final?\n\nAs an education expert for CA Final:\n- You need minimum 40% in each subject and 50% aggregate to pass.\n- Solve at least 5 previous year papers.\n\n(This is mock response for testing purpose)
  "response": "As an education expert for CA Final:\n- You need minimum 40% in each subject and 50% aggregate to pass.\n- Focus heavily on DT, IDT, and practical problems.\n- Solve at least 5 previous year papers."
}
```

**Response (Error):**

```json
{
  "error": "Missing 'userInput' in request body"
}
```

**Status Codes:**

- `200` - Success
- `400` - Bad request (missing required fields)
- `500` - Server error (API key issues, DB connection, etc.)

---

### Endpoint 2: Batch Prompt Processing

**POST** `/api/batch_prompt`

Process multiple educational queries in a single request. Each query is processed asynchronously for better performance.

**Request Body:**

```json
{
  "userInputs": [
    "How much should I score in each subject to pass CA final?",
    "What are the best books for CA Advanced accounting?",
    "How to manage time during CA Final exam?"
  ]
}
```

**Response (Success):**

```json
{
  "responses": [
    "As an education expert for CA Final:\n- You need minimum 40% in each subject...",
    "For CA Advanced Accounting, recommended books are:\n- Mehra & Gupta's Advanced Accounting...",
    "Time management tips for CA Final:\n- Allocate 2-3 months for focused revision..."
  ]
}
```

**Response (Error):**

```json
{
  "error": "Missing 'userInputs' in request body"
}
```

**Key Features:**

- Maintains order of responses (response[0] corresponds to userInputs[0])
- Uses `asyncio.gather()` to run all queries **concurrently** - all tasks execute in parallel
- Each request is processed independently with its own async context
- Prevents request blocking during long OpenAI API calls
- **Performance:** Much faster than processing queries sequentially

---

## 💡 Design Decisions & Architecture

### 1. **Asynchronous Processing with asyncio.gather()**

**Single Request:**

```python
# Why: Prevents request blocking during API calls
# Implementation: Using asyncio.run() for simple async execution
aiResponse = asyncio.run(get_ai_response(userInput))
```

**Batch Requests:**

```python
async def process_batch():
    # Create list of async tasks
    tasks = [get_ai_response(userInput) for userInput in inputs]
    # asyncio.gather() runs all tasks concurrently and waits for all to complete
    return await asyncio.gather(*tasks)

responses = asyncio.run(process_batch())
```

**Benefit:**

- Single requests: Handles async AI response without blocking
- Batch requests: `asyncio.gather()` runs multiple queries in parallel (not sequentially), significantly improving performance for large batches

---

### 2. **Prompt Template Separation**

**Architecture:**

- Prompts stored in MongoDB, not hardcoded in code
- Template system with placeholder replacement

**Benefit:**

- Easy to change prompts without redeploying code
- Supports multiple prompt templates
- Domain expert can update prompts independently

---

### 3. **Service Layer Separation**

```
app.py → Routes & Request Handling
    ↓
services/
  ├── prompt_service.py → DB Queries & Template Management
  ├── openai_service.py → AI API Integration & Logic
  └── history_service.py → Audit Trail & Logging
```

**Benefits:**

- Clear separation of concerns
- Easy to test individual components
- Maintainable & scalable code

---

### 4. **History Tracking**

Every request-response pair is saved with:

- Timestamp for analytics
- Request type (single vs batch) for monitoring
- User input & AI response for debugging
- Model name for version tracking

**Use Cases:**

- Debug failed requests
- Track usage patterns
- Analyze frequently asked questions

---

### 5. **Error Handling**

```python
try:
    # Process request
except Exception as e:
    return jsonify({"error": str(e)}), 500
```

**Handles:**

- Missing OpenAI API key → 500 error
- MongoDB connection failure → 500 error
- Invalid request format → 400 error

---

## 🧪 Testing the API

### Using cURL

**Single Query:**

```bash
curl -X POST http://127.0.0.1:5000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"userInput":"How much should I score in each subject to pass CA final?"}'
```

**Batch Queries:**

```bash
curl -X POST http://127.0.0.1:5000/api/batch_prompt \
  -H "Content-Type: application/json" \
  -d '{"userInputs":["Question 1?","Question 2?","Question 3?"]}'
```

### Using Postman

1. Open Postman
2. Create new POST request to `http://127.0.0.1:5000/api/prompt`
3. Set Headers: `Content-Type: application/json`
4. Set Body (JSON):

```json
{
  "userInput": "Your question here"
}
```

5. Click Send

---

## 🔍 Verifying MongoDB Setup

### Check if Prompts Collection is Created

```bash
# Connect to MongoDB (if local)
mongosh

# Switch to database
use education_db

# View prompts collection
db.prompts.find().pretty()

# View history collection
db.history.find().pretty()
```

---

## 📦 Dependencies & Versions

| Package       | Version | Purpose                         |
| ------------- | ------- | ------------------------------- |
| Flask         | 3.0.3   | Web framework for REST API      |
| Flask-PyMongo | 2.3.0   | MongoDB integration             |
| python-dotenv | 1.0.1   | Environment variable management |

---

## ⚠️ Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'openai'"

**Solution:** Ensure virtual environment is activated and dependencies installed.

```bash
pip install -r requirements.txt
```

### Issue 2: "Failed to connect to MongoDB"

**Solution:**

- Check MongoDB is running: `mongod` (for local)
- Verify MONGO_URI in `.env` is correct
- For MongoDB Atlas, ensure IP whitelist includes your IP

### Issue 3: "Invalid OpenAI API Key"

**Solution:**

- Verify OPENAI_API_KEY in `.env`
- Check key hasn't been revoked at https://platform.openai.com/api-keys
- Ensure key has required permissions

### Issue 4: Returns Mock Response Instead of Real OpenAI Response

**Solution:**
Currently configured for mock responses (safe testing). To enable real OpenAI:

Edit [services/openai_service.py](services/openai_service.py) to replace:

```python
# Mock response logic
```

With actual API call:

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": final_prompt}]
)
return response.choices[0].message.content
```

---

## 📚 Code Flow Diagram

```
Client Request
    ↓
[app.py - Route Handler]
    ↓
[services/prompt_service.py - Fetch Template]
    ↓
[services/openai_service.py - Process with AI]
    ↓
[services/history_service.py - Save to MongoDB]
    ↓
Response to Client
```

---

**Last Updated:** January 2025  
**Python Version:** 3.8+  
**License:** Open Source
