import firebase_admin
from firebase_admin import credentials
from flask import Flask
from pyngrok import ngrok
from flask_ngrok import run_with_ngrok

cred = credentials.Certificate("/Users/suryaganesan/vscode/finance/guilty_re/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

#initializing flask server
ngrok.set_auth_token("ak_2azm3M9tC6lbHmGDtmLlpNUh0vP")

app = Flask(__name__) 
#run_with_ngrok(app) 
port = 5000


#Onboarding

# 1) Send institution list for dropdown
def banklist():
    pass

@app.route('/onboarding/banklist')
def banklist_route():
    return "None"

# 2) Take institution name, find inst. id, return requisition id and authorization link

#Homepage

# 1) Take in pay date, budget amount, requisition id and return day spend, budget health, budget left nad days to pay date


app.run()