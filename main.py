from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

@app.get("/")
def root():
    return {"status": "ok", "service": "piggybank-backend"}


app = FastAPI()

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"child1": {"balance": 0, "history": []},
                "child2": {"balance": 0, "history": []}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


class Transaction(BaseModel):
    amount: float
    description: str | None = None


@app.get("/balance/{child}")
def get_balance(child: str):
    data = load_data()
    return data.get(child, {"balance": 0, "history": []})


@app.post("/deposit/{child}")
def deposit(child: str, t: Transaction):
    data = load_data()
    data[child]["balance"] += t.amount
    data[child]["history"].append(
        {"type": "deposit", "amount": t.amount, "description": t.description}
    )
    save_data(data)
    return {"status": "ok", "balance": data[child]["balance"]}


@app.post("/withdraw/{child}")
def withdraw(child: str, t: Transaction):
    data = load_data()
    data[child]["balance"] -= t.amount
    data[child]["history"].append(
        {"type": "withdraw", "amount": t.amount, "description": t.description}
    )
    save_data(data)
    return {"status": "ok", "balance": data[child]["balance"]}


@app.get("/history/{child}")
def get_history(child: str):
    data = load_data()
    return data[child]["history"]

