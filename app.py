from flask import Flask, render_template, request, jsonify
import time
from datetime import datetime
import random

app = Flask(__name__)

# Mule account database - fake
MULE_ACCOUNTS = ["123456789012", "987654321098", "112233445566"]

def calculate_risk(data):
    hold_avg = data.get('hold_avg', 80)
    flight_avg = data.get('flight_avg', 120)
    wpm = data.get('wpm', 40)
    is_paste = data.get('is_paste', False)
    is_foreign = data.get('is_foreign', False)
    device_new = data.get('device_new', False)
    
    risk = 10 # base
    
    # Rule 1: Fast typing = Mule gang
    if hold_avg < 50: risk += 40
    elif hold_avg < 70: risk += 20
    
    # Rule 2: Very low flight time = Copy paste gang
    if flight_avg < 60: risk += 35
    
    # Rule 3: Paste detected
    if is_paste: risk += 30
    
    # Rule 4: WPM too high
    if wpm > 90: risk += 25
    
    # Rule 5: Foreign + Fast = 99% Fraud
    if is_foreign and hold_avg < 60: risk += 50
    
    # Rule 6: New Device
    if device_new: risk += 30
    
    # Rule 7: Mule account number
    if data.get('account') in MULE_ACCOUNTS: risk += 60
    
    risk = min(risk, 99)
    
    if risk < 30: status = "SAFE"
    elif risk < 70: status = "SUSPICIOUS"
    else: status = "FRAUD"
    
    return risk, status

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    risk, status = calculate_risk(data)
    
    response = {
        "risk_score": risk,
        "status": status,
        "hold_avg": data.get('hold_avg'),
        "flight_avg": data.get('flight_avg'),
        "wpm": data.get('wpm'),
        "time": datetime.now().strftime("%d %b %I:%M %p"),
        "transaction_id": f"BBSTXN{random.randint(100000,999999)}"
    }
    
    if status == "SAFE":
        response["action"] = "ALLOW"
        response["message"] = "Typing behaviour matched. Transaction