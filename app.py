import firebase_admin
from firebase_admin import credentials
from nordigen import NordigenClient
from uuid import uuid4
import json
from flask import Flask, jsonify, request

path_linux = "/home/guilty_re/serviceAccountKey.json"
path_mac = "/Users/suryaganesan/vscode/finance/guilty_re/serviceAccountKey.json"

cred = credentials.Certificate(path_linux)
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
    error = None   

    try:
        institutions = [d.get("name") for d in institutions_dict]

    except Exception as e:
        error = {"error": e}
        pass

    if not error:
       return jsonify(institutions), 200

    else:
        return jsonify(error), 400
    

@app.route('/onboarding/get_banklist')
def get_banklist_route():
   response = get_banklist()

   return response

def init_link(inst):
    token_data = client.generate_token()

    institution_id = client.institution.get_institution_id_by_name(
        country="GB",
        institution=inst
    )

    init = client.initialize_session(
        institution_id=institution_id,
        redirect_uri="https://suryagg925.bubbleapps.io/version-test/init_success_redirect?debug_mode=true",
        reference_id=str(uuid4())
    )
    
    try:
       link = init.link
       req_id = init.requisition_id
       print("link: "+link)
       print("req id: "+req_id)

       return jsonify({"link": link, "requisition_id": req_id, "institution_id": institution_id}), 200

    except Exception as e:
       return jsonify({"error": e}), 400

@app.route("/onboarding/initialize_link")
def init_link_route():
    inst_selected = request.args.get('institution')
    print(inst_selected)
    response = init_link(inst_selected)

    return response

def check_connection(requisition_id, institution_id):

    init = client.initialize_session(
        institution_id=institution_id,
        redirect_uri="https://suryagg925.bubbleapps.io/version-test/init_success_redirect?debug_mode=true",
        reference_id=str(uuid4())
    )

    accounts = client.requisition.get_requisition_by_id(
        requisition_id=requisition_id
    )
    
    try:
       account_id = accounts["accounts"][0]
    
    except Exception as e:
        return jsonify({"error": e}), 400

    else:
        return jsonify({"account_id": account_id}), 200

@app.route("/onboarding/check_connection")
def check_connection_route():

    req_id = request.args.get("requisition_id")
    inst_id = request.args.get("institution_id")

    response = check_connection(req_id, inst_id)
    
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)