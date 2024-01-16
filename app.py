import firebase_admin
from firebase_admin import credentials
from nordigen.nordigen import NordigenClient
from uuid import uuid4
import json
from flask import Flask, jsonify

cred = credentials.Certificate("/Users/suryaganesan/vscode/finance/guilty_re/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

client = NordigenClient(
    secret_id="b5314ee2-e221-4a84-96c0-ec97d252896c",
    secret_key="82380ff2da7d792baaa244062fb5538401397f1ec27f1e83c1b35da8e15c1ffb0e130d171f1c585e486d4ae72fb93abd049c480372aeed5daf48630bbd6e5e16"
)

app = Flask(__name__)

def get_banklist():
    token_data = client.generate_token()
    access_token = token_data["access"]

    institutions_dict = client.institution.get_institutions("GB")
    
    institutions = [d.get("name") for d in institutions_dict]

    return jsonify(institutions)

@app.route('/onboarding/get_banklist')
def get_banklist_route():
   inst = get_banklist()

   return inst, 200


#get_banklist()

#app.run(debug=True)