from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Patient
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_ai_remarks(name, glucose, haemoglobin, cholesterol):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    prompt = (
        f"A patient named {name} has the following blood test results:\n"
        f"- Glucose: {glucose} mg/dL\n"
        f"- Haemoglobin: {haemoglobin} g/dL\n"
        f"- Cholesterol: {cholesterol} mg/dL\n\n"
        f"Provide a brief 2-3 sentence health prediction mentioning possible risks. Keep it professional and concise."
    )
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        print("AI RESPONSE:", data)
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI prediction unavailable: {str(e)}"

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    remarks = get_ai_remarks(data['full_name'], data['glucose'], data['haemoglobin'], data['cholesterol'])
    patient = Patient(full_name=data['full_name'], dob=data['dob'], email=data['email'],
        glucose=data['glucose'], haemoglobin=data['haemoglobin'], cholesterol=data['cholesterol'], remarks=remarks)
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    return jsonify([p.to_dict() for p in Patient.query.all()])

@app.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    return jsonify(Patient.query.get_or_404(id).to_dict())

@app.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    data = request.json
    patient.full_name = data['full_name']
    patient.dob = data['dob']
    patient.email = data['email']
    patient.glucose = data['glucose']
    patient.haemoglobin = data['haemoglobin']
    patient.cholesterol = data['cholesterol']
    patient.remarks = get_ai_remarks(data['full_name'], data['glucose'], data['haemoglobin'], data['cholesterol'])
    db.session.commit()
    return jsonify(patient.to_dict())

@app.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)