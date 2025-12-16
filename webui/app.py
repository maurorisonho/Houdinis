#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Web interface for Houdinis Quantum Cryptography Testing Platform.
This is the ONLY component users interact with directly.
All operations execute inside Docker containers.
"""

import os
import json
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
from werkzeug.security import check_password_hash, generate_password_hash
import docker
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'houdinis-quantum-secret-key-change-me')
socketio = SocketIO(app, cors_allowed_origins="*")

# Docker client (lazy initialization)
docker_client = None

def get_docker_client():
    global docker_client
    if docker_client is None:
        try:
            docker_client = docker.from_env()
        except Exception as e:
            print(f"Warning: Could not connect to Docker: {e}")
            docker_client = None
    return docker_client

# Redis for session/cache
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

# Default admin credentials (change after first login!)
DEFAULT_USERS = {
    'admin': generate_password_hash('houdinis123')
}


# ============================================================================
# AUTHENTICATION
# ============================================================================

@app.route('/')
def index():
    """Landing page"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        stored_hash = DEFAULT_USERS.get(username)
        if stored_hash and check_password_hash(stored_hash, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.pop('user', None)
    return redirect(url_for('index'))


def login_required(f):
    """Decorator for protected routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# DASHBOARD
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get Docker container status
    containers = []
    try:
        client = get_docker_client()
        if client:
            for container in client.containers.list(all=True):
                containers.append({
                    'name': container.name,
                    'status': container.status,
                    'image': container.image.tags[0] if container.image.tags else 'unknown',
                    'id': container.short_id
                })
    except Exception as e:
        print(f"Error getting containers: {e}")
    
    return render_template('dashboard.html', 
                         user=session['user'],
                         containers=containers,
                         total_containers=len(containers),
                         running_containers=len([c for c in containers if c['status'] == 'running']))


# ============================================================================
# EXPLOITS
# ============================================================================

@app.route('/exploits')
@login_required
def exploits():
    """Exploit selection page"""
    exploits_list = [
        {
            'id': 'shor_rsa',
            'name': 'Shor\'s Algorithm - RSA Factorization',
            'description': 'Factor RSA keys using Shor\'s quantum algorithm',
            'difficulty': 'Medium',
            'category': 'Asymmetric Crypto'
        },
        {
            'id': 'grover_bruteforce',
            'name': 'Grover\'s Algorithm - Hash Bruteforce',
            'description': 'Accelerated bruteforce of symmetric keys and hashes',
            'difficulty': 'Easy',
            'category': 'Symmetric Crypto'
        },
        {
            'id': 'quantum_network_scan',
            'name': 'Quantum Vulnerability Scanner',
            'description': 'Scan network for quantum-vulnerable cryptography',
            'difficulty': 'Easy',
            'category': 'Reconnaissance'
        },
        {
            'id': 'tls_quantum_mitm',
            'name': 'TLS/SSL Quantum MITM',
            'description': 'Quantum-enabled man-in-the-middle on TLS',
            'difficulty': 'Hard',
            'category': 'Network Attack'
        },
        {
            'id': 'ssh_quantum_attack',
            'name': 'SSH Quantum Key Recovery',
            'description': 'Break SSH using quantum algorithms',
            'difficulty': 'Medium',
            'category': 'Network Attack'
        },
        {
            'id': 'pgp_quantum_crack',
            'name': 'PGP/GPG Quantum Cracking',
            'description': 'Crack PGP encrypted messages',
            'difficulty': 'Hard',
            'category': 'Encryption Breaking'
        }
    ]
    
    return render_template('exploits.html', exploits=exploits_list)


@app.route('/exploit/<exploit_id>')
@login_required
def exploit_detail(exploit_id):
    """Exploit configuration and execution page"""
    # Define exploit details with parameters
    exploits_data = {
        'shor_rsa': {
            'name': 'Shor\'s Algorithm - RSA Factorization',
            'description': 'Factor RSA keys using Shor\'s quantum algorithm on NVIDIA cuQuantum',
            'params': [
                {'name': 'target', 'label': 'Target IP/Hostname', 'type': 'text', 'default': '192.168.1.100', 'required': True},
                {'name': 'port', 'label': 'SSH Port', 'type': 'number', 'default': '22', 'required': True},
                {'name': 'bits', 'label': 'Key Size (bits)', 'type': 'number', 'default': '512', 'required': True}
            ]
        },
        'grover_bruteforce': {
            'name': 'Grover\'s Algorithm - Hash Bruteforce',
            'description': 'Accelerated bruteforce of symmetric keys using Grover\'s quantum search',
            'params': [
                {'name': 'hash', 'label': 'Target Hash', 'type': 'text', 'default': 'e99a18c428cb38d5f260853678922e03', 'required': True},
                {'name': 'algorithm', 'label': 'Hash Algorithm', 'type': 'text', 'default': 'md5', 'required': True},
                {'name': 'keyspace', 'label': 'Keyspace Size', 'type': 'number', 'default': '16', 'required': True}
            ]
        },
        'quantum_network_scan': {
            'name': 'Quantum Vulnerability Scanner',
            'description': 'Scan network for quantum-vulnerable cryptographic implementations',
            'params': [
                {'name': 'target', 'label': 'Target Network', 'type': 'text', 'default': '192.168.1.0/24', 'required': True},
                {'name': 'ports', 'label': 'Ports to Scan', 'type': 'text', 'default': '22,443,8443', 'required': True}
            ]
        },
        'tls_quantum_mitm': {
            'name': 'TLS/SSL Quantum MITM',
            'description': 'Quantum-enabled man-in-the-middle attack on TLS connections',
            'params': [
                {'name': 'target', 'label': 'Target Host', 'type': 'text', 'default': 'example.com', 'required': True},
                {'name': 'port', 'label': 'TLS Port', 'type': 'number', 'default': '443', 'required': True}
            ]
        },
        'ssh_quantum_attack': {
            'name': 'SSH Quantum Key Recovery',
            'description': 'Break SSH key exchange using quantum algorithms',
            'params': [
                {'name': 'target', 'label': 'SSH Server', 'type': 'text', 'default': '192.168.1.100', 'required': True},
                {'name': 'port', 'label': 'SSH Port', 'type': 'number', 'default': '22', 'required': True},
                {'name': 'username', 'label': 'Username', 'type': 'text', 'default': 'root', 'required': False}
            ]
        },
        'pgp_quantum_crack': {
            'name': 'PGP/GPG Quantum Cracking',
            'description': 'Crack PGP encrypted messages using quantum factorization',
            'params': [
                {'name': 'keyfile', 'label': 'Public Key File', 'type': 'text', 'default': '/tmp/target.asc', 'required': True},
                {'name': 'message', 'label': 'Encrypted Message', 'type': 'text', 'default': '/tmp/message.pgp', 'required': True}
            ]
        }
    }
    
    exploit = exploits_data.get(exploit_id)
    if not exploit:
        return render_template('404.html'), 404
    
    return render_template('exploit_detail.html', exploit_id=exploit_id, exploit=exploit)


@app.route('/api/exploit/execute', methods=['POST'])
@login_required
def execute_exploit():
    """Execute exploit in Docker container"""
    data = request.json
    exploit_id = data.get('exploit_id')
    params = data.get('params', {})
    
    # Map exploit to Docker command
    exploit_commands = {
        'shor_rsa': 'python3 -m exploits.rsa_shor',
        'grover_bruteforce': 'python3 -m exploits.grover_bruteforce',
        'quantum_network_scan': 'python3 -m scanners.quantum_vuln_scanner',
        'tls_quantum_mitm': 'python3 -m exploits.tls_sndl',
        'ssh_quantum_attack': 'python3 -m exploits.ssh_quantum_attack',
        'pgp_quantum_crack': 'python3 -m exploits.pgp_quantum_crack'
    }
    
    command = exploit_commands.get(exploit_id)
    if not command:
        return jsonify({'error': 'Unknown exploit'}), 400
    
    # Add parameters to command
    for key, value in params.items():
        command += f' --{key} {value}'
    
    # Execute in houdinis-core container
    try:
        client = get_docker_client()
        if not client:
            return jsonify({'status': 'error', 'message': 'Docker not available'}), 500
        container = client.containers.get('houdinis_core')
        
        # Create exec instance
        exec_instance = container.exec_run(
            command,
            detach=False,
            stream=True
        )
        
        # Store job ID for tracking
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store in Redis for real-time updates
        redis_client.hset(f'job:{job_id}', mapping={
            'exploit_id': exploit_id,
            'status': 'running',
            'started_at': datetime.now().isoformat(),
            'user': session['user']
        })
        
        return jsonify({
            'job_id': job_id,
            'status': 'started',
            'message': 'Exploit execution started in container'
        })
        
    except docker.errors.NotFound:
        return jsonify({'error': 'Houdinis container not found. Is it running?'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# AI ASSISTANT
# ============================================================================

@app.route('/ai-assistant')
@login_required
def ai_assistant():
    """AI-powered quantum crypto assistant"""
    return render_template('ai_assistant.html')


@app.route('/api/ai/chat', methods=['POST'])
@login_required
def ai_chat():
    """Chat with AI assistant"""
    data = request.json
    query = data.get('query')
    
    # Execute AI query in Mistral container
    try:
        client = get_docker_client()
        if not client:
            return jsonify({'error': 'Docker not available'}), 500
        container = client.containers.get('houdinis_mistral')
        
        command = f'python3 -m langchain_agents.mistral_local_agent --query "{query}"'
        
        exec_result = container.exec_run(command, detach=False)
        
        response = exec_result.output.decode('utf-8')
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except docker.errors.NotFound:
        return jsonify({'error': 'AI container not running. Enable AI profile.'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# BACKEND MANAGEMENT
# ============================================================================

@app.route('/backends')
@login_required
def backends():
    """Quantum computing backend management"""
    backends_list = [
        {
            'id': 'nvidia_cuquantum',
            'name': 'NVIDIA cuQuantum',
            'type': 'GPU Simulator',
            'status': 'available',
            'qubits': 40,
            'speed': 'Very Fast'
        },
        {
            'id': 'ibm_quantum',
            'name': 'IBM Quantum',
            'type': 'Real Quantum Hardware',
            'status': 'requires_token',
            'qubits': 127,
            'speed': 'Real Hardware'
        },
        {
            'id': 'aws_braket',
            'name': 'AWS Braket',
            'type': 'Cloud Quantum',
            'status': 'requires_credentials',
            'qubits': 'Varies',
            'speed': 'Fast'
        },
        {
            'id': 'azure_quantum',
            'name': 'Azure Quantum',
            'type': 'Cloud Quantum',
            'status': 'requires_credentials',
            'qubits': 'Varies',
            'speed': 'Fast'
        }
    ]
    
    return render_template('backends.html', backends=backends_list)


# ============================================================================
# SETTINGS
# ============================================================================

@app.route('/settings')
@login_required
def settings():
    """Settings page"""
    return render_template('settings.html')


@app.route('/api/settings/update', methods=['POST'])
@login_required
def update_settings():
    """Update settings"""
    data = request.json
    
    # Store settings in Redis
    for key, value in data.items():
        redis_client.hset(f'settings:{session["user"]}', key, value)
    
    return jsonify({'status': 'success', 'message': 'Settings updated'})


# ============================================================================
# WEBSOCKET FOR REAL-TIME UPDATES
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('status', {'message': 'Connected to Houdinis'})


@socketio.on('subscribe_job')
def handle_subscribe_job(data):
    """Subscribe to job updates"""
    job_id = data.get('job_id')
    # In production, implement proper job streaming
    emit('job_update', {
        'job_id': job_id,
        'status': 'running',
        'progress': 0
    })


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/status')
def api_status():
    """API status check"""
    return jsonify({
        'status': 'online',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/containers')
@login_required
def api_containers():
    """Get Docker container status"""
    containers = []
    try:
        client = get_docker_client()
        if not client:
            return jsonify({'containers': []})
        for container in client.containers.list(all=True):
            containers.append({
                'name': container.name,
                'status': container.status,
                'image': container.image.tags[0] if container.image.tags else 'unknown',
                'id': container.short_id,
                'ports': container.ports,
                'started': container.attrs.get('State', {}).get('StartedAt')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'containers': containers})


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Run in Docker container, exposed on port 8080
    socketio.run(
        app,
        host='0.0.0.0',
        port=8080,
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )
