#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Simple Mistral chat using Ollama - No complex dependencies
"""

import requests
import json
import sys

class SimpleMistralChat:
    """Simple chat interface with Mistral via Ollama API"""
    
    def __init__(self, base_url="http://localhost:11434", model="mistral:7b-instruct"):
        self.base_url = base_url
        self.model = model
        self.conversation_history = []
        
    def check_connection(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f" Connected to Ollama at {self.base_url}")
                print(f" Available models: {len(models)}")
                for m in models:
                    print(f"   • {m['name']} ({m['size'] / 1e9:.1f}GB)")
                return True
        except requests.exceptions.RequestException as e:
            print(f" Cannot connect to Ollama: {e}")
            print(" Make sure container is running: docker ps | grep mistral")
            return False
    
    def chat(self, prompt):
        """Send message to Mistral"""
        self.conversation_history.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=120
            )
            
            full_response = ""
            print("\n Mistral: ", end="", flush=True)
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'message' in data:
                        content = data['message'].get('content', '')
                        print(content, end="", flush=True)
                        full_response += content
                    
                    if data.get('done', False):
                        break
            
            print("\n")
            self.conversation_history.append({"role": "assistant", "content": full_response})
            return full_response
            
        except Exception as e:
            print(f"\n Error: {e}")
            return None
    
    def interactive(self):
        """Start interactive chat"""
        print("\n" + "="*70)
        print(" Mistral 7B Instruct - Quantum Cryptography Assistant")
        print("="*70)
        print("\n Ask about:")
        print("   • Quantum attacks (Shor, Grover)")
        print("   • Post-Quantum Cryptography (PQC)")
        print("   • RSA/ECC vulnerabilities")
        print("   • Migration strategies")
        print("\n Type 'quit' or 'exit' to stop")
        print("="*70 + "\n")
        
        if not self.check_connection():
            return
        
        print(f"\n Using model: {self.model}")
        print(" Start chatting...\n")
        
        # Initial system message
        self.conversation_history = [{
            "role": "system",
            "content": (
                "You are an expert in quantum cryptography and post-quantum security. "
                "Help users understand quantum computing threats to cryptography, "
                "including Shor's algorithm (RSA/ECC attacks) and Grover's algorithm "
                "(symmetric key attacks). Provide practical advice on PQC migration "
                "and security best practices. Be concise and technical."
            )
        }]
        
        while True:
            try:
                user_input = input(" You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n Goodbye!")
                    break
                
                self.chat(user_input)
                
            except KeyboardInterrupt:
                print("\n\n Chat interrupted. Goodbye!")
                break
            except EOFError:
                break

def main():
    """Main entry point"""
    chat = SimpleMistralChat()
    chat.interactive()

if __name__ == "__main__":
    main()
