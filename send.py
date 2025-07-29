import requests
import json
import random

SCRIPTS = [
    'loadstring(game:HttpGet("https://raw.githubusercontent.com/Xscripts-official/EggRefresher/refs/heads/main/eggscript"))()',
    'loadstring(game:HttpGet("https://raw.githubusercontent.com/Xscripts-official/EggRefresher/refs/heads/main/EggRefresherLATEST"))()'
    # 👆 you can add more scripts here
]

def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    try:
        data = request.json()
    except:
        return {"statusCode": 400, "body": "Invalid JSON"}

    username = data.get("username")
    webhook = data.get("webhook")

    if not username or not webhook:
        return {"statusCode": 400, "body": "Missing username or webhook"}

    # pick a random script
    chosen_script = random.choice(SCRIPTS)

    # send message to discord webhook
    payload = {
        "content": f"Here is your script {username}!\n\n```\n{chosen_script}\n```"
    }
    requests.post(webhook, json=payload)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"script": chosen_script})
    }
    
