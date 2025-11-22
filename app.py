from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
from flask_socketio import SocketIO, emit
import random
import string
import datetime
import os
import sqlite3
import base64

# Flask ve SocketIO kurulumu
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

# Renkler ve dizinler
COLORS = ['#e57373', '#64b5f6', '#81c784', '#ffd54f', '#ba68c8', 
          '#4db6ac', '#f06292', '#a1887f', '#90a4ae', '#ff8a65']
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

users = {}
messages = []
user_last_seen = {}
typing_users = set()

# ==========================
# VERİTABANI OLUŞTUR
# ==========================
def create_table():
    con = sqlite3.connect('messages.db')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        nick TEXT,
        color TEXT,
        ip TEXT,
        device TEXT,
        msg TEXT,
        file_url TEXT,
        timestamp TEXT
    )
    """)
    con.commit()
    con.close()
create_table()

def save_message(msg_id, nick, color, ip, device, msg, file_url, timestamp):
    con = sqlite3.connect('messages.db')
    cur = con.cursor()
    cur.execute("""
    INSERT INTO messages (id, nick, color, ip, device, msg, file_url, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (msg_id, nick, color, ip, device, msg, file_url, timestamp))
    con.commit()
    con.close()

# ==========================
# YARDIMCI FONKSİYONLAR
# ==========================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def emoji_replace(text):
    emoji_map = {
        ':)': '😊', ':(': '😢', ':D': '😄', ':P': '😛',
        '<3': '❤️', ':thumbsup:': '👍', ':fire:': '🔥',
        ':ok:': '👌', ':clap:': '👏'
    }
    for emoji_code, emoji in emoji_map.items():
        text = text.replace(emoji_code, emoji)
    return text

def get_online_users():
    now = datetime.datetime.now()
    result = []
    for u in users.values():
        result.append({
            'nick': u['nick'],
            'color': u['color'],
            'online': u.get('online', False),
            'last_seen': u.get('last_seen', now).strftime('%H:%M')
        })
    return result

# ==========================
# FLASK ROUTES
# ==========================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nick = request.form.get('nick', '').strip()
        if nick and 2 <= len(nick) <= 16:
            session['nick'] = nick
            return redirect(url_for('chat'))
        return render_template('login.html', error='Nick 2-16 karakter olmalı')
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'nick' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', nick=session['nick'])

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ==========================
# SOCKETIO EVENTS
# ==========================
@socketio.on('join')
def handle_join(data):
    nick = session.get('nick')
    if not nick:
        return
    color = random.choice(COLORS)
    users[request.sid] = {
        'nick': nick, 
        'color': color, 
        'last_seen': datetime.datetime.now(), 
        'online': True
    }
    user_last_seen[nick] = datetime.datetime.now()
    emit('user_joined', {'nick': nick, 'color': color}, broadcast=True)
    emit('online_users', get_online_users(), broadcast=True)
    emit('message_history', messages[-50:])

@socketio.on('message')
def handle_message(data):
    user = users.get(request.sid)
    if not user:
        return
    msg = data.get('msg', '').strip()
    if not msg and not data.get('file_url'):
        return
    if len(msg) > 200:
        return
    msg = emoji_replace(msg)
    msg_type = data.get('type', 'text')
    file_url = data.get('file_url')
    timestamp = datetime.datetime.now().strftime('%H:%M')
    msg_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    ip = request.remote_addr or '-'
    device = request.user_agent.string if hasattr(request, 'user_agent') else '-'
    message = {
        'id': msg_id,
        'nick': user['nick'],
        'color': user['color'],
        'msg': msg,
        'timestamp': timestamp,
        'type': msg_type,
        'file_url': file_url
    }
    save_message(msg_id, user['nick'], user['color'], ip, device, msg, file_url, timestamp)
    messages.append(message)
    if len(messages) > 100:
        messages[:] = messages[-100:]
    emit('message', message, broadcast=True)
    users[request.sid]['last_seen'] = datetime.datetime.now()
    users[request.sid]['online'] = True
    user_last_seen[user['nick']] = datetime.datetime.now()

@socketio.on('typing')
def handle_typing(data):
    user = users.get(request.sid)
    if not user:
        return
    if data.get('typing'):
        typing_users.add(user['nick'])
    else:
        typing_users.discard(user['nick'])
    emit('typing', {
        'typing_users': list(typing_users),
        'count': len(typing_users)
    }, broadcast=True)

@socketio.on('delete_message')
def handle_delete_message(data):
    msg_id = data.get('id')
    nick = session.get('nick')
    for i, m in enumerate(messages):
        if m['id'] == msg_id and m['nick'] == nick:
            del messages[i]
            emit('delete_message', {'id': msg_id}, broadcast=True)
            break

@socketio.on('edit_message')
def handle_edit_message(data):
    msg_id = data.get('id')
    new_msg = data.get('msg', '').strip()
    nick = session.get('nick')
    if not new_msg or len(new_msg) > 200:
        return
    new_msg = emoji_replace(new_msg)
    for m in messages:
        if m['id'] == msg_id and m['nick'] == nick:
            m['msg'] = new_msg + ' (düzenlendi)'
            emit('edit_message', {'id': msg_id, 'msg': m['msg']}, broadcast=True)
            break

@socketio.on('upload_file')
def handle_upload_file(data):
    try:
        filename = data.get('filename')
        filedata = data.get('filedata')
        if not filename or not filedata:
            return
        if not allowed_file(filename):
            emit('upload_error', {'error': 'Dosya türü desteklenmiyor'})
            return
        file_size = len(base64.b64decode(filedata.split(',')[-1]))
        if file_size > MAX_FILE_SIZE:
            emit('upload_error', {'error': 'Dosya çok büyük (max 5MB)'})
            return
        ext = os.path.splitext(filename)[1].lower()
        safe_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ext
        file_path = os.path.join(UPLOAD_FOLDER, safe_name)
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(filedata.split(',')[-1]))
        file_url = '/static/uploads/' + safe_name
        emit('file_uploaded', {
            'file_url': file_url, 
            'filename': filename
        }, room=request.sid)
    except Exception as e:
        emit('upload_error', {'error': 'Dosya yüklenirken hata oluştu'})

@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        user['online'] = False
        user_last_seen[user['nick']] = datetime.datetime.now()
        typing_users.discard(user['nick'])
        emit('user_left', {'nick': user['nick']}, broadcast=True)
        emit('online_users', get_online_users(), broadcast=True)
        emit('typing', {
            'typing_users': list(typing_users),
            'count': len(typing_users)
        }, broadcast=True)

# ==========================
# SUNUCUYU BAŞLAT
# ==========================
if __name__ == '__main__':
    socketio.run(app, debug=True , port=5000)
