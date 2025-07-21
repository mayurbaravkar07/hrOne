# HROne Backend API

This is a simple backend API built using **FastAPI** and **MongoDB**.
It allows users to create and list products and place orders.

## Live URL
**Base URL:** https://hronebackend-qvky.onrender.com  
**Docs:** https://hronebackend-qvky.onrender.com/docs

## Features
- Create and list products
- Filter products by name or size
- Create orders
- List orders by user with total price
- Pagination support

## How to Run Locally
```bash
# Clone the repository
git clone https://github.com/mayurbaravkar07/hrOne.git
cd hrOneBackend

# Create virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
```
Visit http://localhost:8000/docs to test the API.

## Environment Variable
Create a `.env` file with:
```
MONGODB_URI=your_mongo_connection_string
```

## Author
**Mayur Baravkar**  
📧 mayurbaravkar24@gmail.com  
🔗 https://github.com/mayurbaravkar07
