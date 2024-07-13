import requests
import json
import time
from flask import Flask, jsonify, request
import os
from pyngrok import ngrok
port_no = 5000
app = Flask(__name__)
ngrok.set_auth_token("2j9RbOId8SNWHjrfbYtSBTE7DmH_7VtTzKAz5KkLPvXD4TQ1J")
public_url =  ngrok.connect(port_no).public_url
def process_hwid(hwid):
    code = "rinx"
    payload = {
    "captcha": "",
    "type": "Turnstile"
}
    hwid = hwid.replace('https://gateway.platoboost.com/a/8?id=', '')
    session = requests.Session()
    session.post(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{hwid}", json=payload)
    time.sleep(5)
    session.put(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{hwid}/{code}")
    response = session.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{hwid}")
    if response.text:
        try:
            response_json = json.loads(response.text)
            key_value = response_json.get('key', 'No key found in response')
        except json.JSONDecodeError:
            key_value = 'Response is not in JSON format'
    else:
                key_value = 'No response received'
    return f'{key_value}'

@app.route('/', methods=['GET'])
def delta():
    user_hwid = request.args.get('hwid')
    if not user_hwid or not user_hwid.isalnum():
        return jsonify({"error": "Invalid or missing 'hwid' parameter."}), 400
    key_value = process_hwid(user_hwid)
    return {"KEY" : key_value}
print(f'{public_url}')
app.run(port=port_no)
