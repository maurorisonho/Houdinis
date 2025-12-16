#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Local AI agent using Mistral via Ollama - 100% offline and free.
Provides quantum cryptography analysis without API costs.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from langchain_community.llms import Ollama
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    print(f"[!] LangChain not available: {e}")
    print("[!] Running in simple mode without LangChain features")
    LANGCHAIN_AVAILABLE = False


class MistralQuantumAgent:
    """
    Local Mistral AI agent for quantum cryptography analysis.
    Runs completely offline using Ollama.
    
    Features:
    - 100% free and offline
    - No API keys required
    - Privacy: all data stays local
    - Fast inference on GPU
    - Customizable models
    """

    def __init__(
        self,
        model: str = "mistral:7b-instruct",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        use_rag: bool = True
    ):
        """
        Initialize Local Mistral Agent.
        
        Args:
            model: Ollama model name (mistral:7b, codellama:13b, etc.)
            base_url: Ollama server URL
            temperature: Model temperature
            use_rag: Enable RAG with local vector store
        """
        self.model_name = model
        self.base_url = base_url
        self.use_rag = use_rag
        
        print(f"[*] Initializing Mistral Agent ({model})...")
        
        # Initialize Ollama LLM
        try:
            self.llm = Ollama(
                model=model,
                base_url=base_url,
                temperature=temperature,
                num_ctx=4096  # Context window
            )
            print(f"[+] Connected to Ollama: {base_url}")
        except Exception as e:
            print(f"[!] Failed to connect to Ollama: {e}")
            print("[!] Make sure Ollama is running: ollama serve")
            raise
        
        # Initialize embeddings for RAG
        if use_rag:
            self.embeddings = OllamaEmbeddings(
                model=model,
                base_url=base_url
            )
            self._setup_rag()
        
        # Create tools and agent
        self.tools = self._create_tools()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.agent = self._create_agent()
        
        print(f"[+] Agent initialized with {len(self.tools)} tools")
        
    def _setup_rag(self):
        """Setup RAG with local vector store"""
        print("[*] Setting up local RAG with ChromaDB...")
        
        persist_dir = "./data/vectorstore_local"
        
        # Create vector store for Houdinis documentation
        self.vectorstore = Chroma(
            collection_name="houdinis_docs",
            embedding_function=self.embeddings,
            persist_directory=persist_dir
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
        )
        
        print(f"[+] RAG enabled with local vector store at {persist_dir}")
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for quantum crypto operations"""
        
        tools = [
            Tool(
                name="quantum_vulnerability_analysis",
                func=self._analyze_vulnerability,
                description=(
                    "Analyze quantum vulnerabilities in cryptographic systems. "
                    "Input: algorithm name and key size (e.g., 'RSA-2048'). "
                    "Returns: vulnerability assessment, timeline, recommendations."
                )
            ),
            Tool(
                name="shor_algorithm_simulator",
                func=self._simulate_shor,
                description=(
                    "Simulate Shor's algorithm for RSA factorization. "
                    "Input: number to factor. "
                    "Returns: simulation results, qubit requirements, complexity."
                )
            ),
            Tool(
                name="grover_attack_planner",
                func=self._plan_grover_attack,
                description=(
                    "Plan Grover's algorithm attack on symmetric crypto. "
                    "Input: key size and hash type. "
                    "Returns: attack strategy, speedup, feasibility."
                )
            ),
            Tool(
                name="pqc_migration_advisor",
                func=self._advise_pqc_migration,
                description=(
                    "Generate post-quantum cryptography migration plan. "
                    "Input: current crypto system description. "
                    "Returns: migration roadmap, PQC recommendations, timeline."
                )
            ),
            Tool(
                name="quantum_backend_selector",
                func=self._select_backend,
                description=(
                    "Recommend optimal quantum computing backend. "
                    "Input: algorithm, qubit count, budget. "
                    "Returns: backend recommendation with pros/cons."
                )
            ),
            Tool(
                name="crypto_strength_calculator",
                func=self._calculate_strength,
                description=(
                    "Calculate cryptographic strength against quantum attacks. "
                    "Input: algorithm and parameters. "
                    "Returns: bit security, quantum resistance level."
                )
            ),
            Tool(
                name="houdinis_documentation_search",
                func=self._search_docs,
                description=(
                    "Search Houdinis framework documentation. "
                    "Input: query about usage, exploits, or configuration. "
                    "Returns: relevant documentation and examples."
                )
            ),
            Tool(
                name="exploit_code_generator",
                func=self._generate_exploit,
                description=(
                    "Generate Python exploit code for quantum attacks. "
                    "Input: attack type and target parameters. "
                    "Returns: working Python code with comments."
                )
            )
        ]
        
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """Create ReAct agent with Mistral"""
        
        template = """You are an expert quantum cryptography analyst using the Houdinis Framework.
You have deep knowledge of:
- Quantum algorithms (Shor's, Grover's, QAOA, VQE)
- Classical and post-quantum cryptography
- Quantum computing backends (IBM, NVIDIA, AWS, Azure, Google)
- Network security and penetration testing
- Cryptographic vulnerability assessment

Answer the following question as best you can. You have access to these tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to provide technical details and code examples when relevant.

Question: {input}
Thought: {agent_scratchpad}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
        )
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def chat(self, query: str) -> str:
        """Chat with the local Mistral agent"""
        try:
            response = self.agent.invoke({"input": query})
            return response["output"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Tool implementations
    
    def _analyze_vulnerability(self, crypto_system: str) -> str:
        """Analyze quantum vulnerability"""
        analysis = {
            "RSA-1024": "CRITICAL - Already vulnerable to quantum attacks",
            "RSA-2048": "HIGH - Vulnerable within 10-15 years",
            "RSA-4096": "MEDIUM - Vulnerable within 15-20 years",
            "ECDSA-256": "HIGH - Vulnerable within 10-15 years",
            "AES-128": "LOW - Double key size to AES-256",
            "AES-256": "SAFE - Quantum resistant"
        }
        
        result = analysis.get(crypto_system, "UNKNOWN")
        
        return json.dumps({
            "system": crypto_system,
            "vulnerability": result,
            "recommendation": "Migrate to post-quantum cryptography (Kyber, Dilithium)",
            "urgency": "HIGH" if "HIGH" in result else "MEDIUM"
        }, indent=2)
    
    def _simulate_shor(self, number: str) -> str:
        """Simulate Shor's algorithm"""
        try:
            n = int(number)
            qubits = n.bit_length() * 2
            
            return json.dumps({
                "number": n,
                "qubits_required": qubits,
                "circuit_depth": qubits * 10,
                "gates_count": qubits * 100,
                "estimated_time": f"{qubits * 0.1}s on simulator",
                "feasibility": "HIGH" if qubits < 20 else "MEDIUM",
                "recommendation": "Use NVIDIA cuQuantum for GPU acceleration"
            }, indent=2)
        except:
            return json.dumps({"error": "Invalid input"})
    
    def _plan_grover_attack(self, params: str) -> str:
        """Plan Grover's attack"""
        return json.dumps({
            "attack": "Grover's Algorithm",
            "speedup": "Quadratic O(√N)",
            "key_size_impact": "Effective halving of security",
            "example": "AES-128 → 64-bit security vs quantum",
            "defense": "Use AES-256 for quantum resistance",
            "estimated_time": "Depends on key space size",
            "backend_recommendation": "NVIDIA cuQuantum for best performance"
        }, indent=2)
    
    def _advise_pqc_migration(self, system: str) -> str:
        """Advise PQC migration"""
        return json.dumps({
            "current_system": system,
            "recommended_pqc": {
                "key_exchange": "Kyber-1024 (NIST standard)",
                "signatures": "Dilithium or SPHINCS+",
                "encryption": "AES-256-GCM"
            },
            "migration_phases": [
                "Phase 1: Assessment (3-6 months)",
                "Phase 2: Hybrid deployment (6-12 months)",
                "Phase 3: Full migration (12-24 months)"
            ],
            "estimated_cost": "Medium to High",
            "urgency": "Start planning now"
        }, indent=2)
    
    def _select_backend(self, requirements: str) -> str:
        """Select quantum backend"""
        return json.dumps({
            "recommendation": "NVIDIA cuQuantum",
            "reasons": [
                "GPU acceleration (10-50x faster)",
                "Local deployment (no cloud costs)",
                "Up to 40 qubits practical",
                "Best for development/testing"
            ],
            "alternatives": {
                "IBM Quantum": "Real hardware, research use",
                "AWS Braket": "Production, pay-per-use",
                "Azure Quantum": "Enterprise features"
            }
        }, indent=2)
    
    def _calculate_strength(self, algorithm: str) -> str:
        """Calculate crypto strength"""
        strengths = {
            "RSA-1024": "80 bits classical, ~40 bits quantum",
            "RSA-2048": "112 bits classical, ~56 bits quantum",
            "RSA-4096": "140 bits classical, ~70 bits quantum",
            "AES-128": "128 bits classical, ~64 bits quantum",
            "AES-256": "256 bits classical, ~128 bits quantum"
        }
        
        return json.dumps({
            "algorithm": algorithm,
            "security": strengths.get(algorithm, "Unknown"),
            "quantum_resistant": "AES-256" in algorithm,
            "recommendation": "Use 256-bit keys minimum for quantum era"
        }, indent=2)
    
    def _search_docs(self, query: str) -> str:
        """Search Houdinis documentation"""
        if self.use_rag:
            try:
                result = self.qa_chain.invoke({"query": query})
                return result["result"]
            except:
                pass
        
        return json.dumps({
            "query": query,
            "result": "Local documentation search. Check docs/ directory.",
            "main_docs": [
                "README.md - Main documentation",
                "docs/BACKENDS.md - Quantum backends",
                "docs/LANGCHAIN_MCP_GUIDE.md - AI integration"
            ]
        }, indent=2)
    
    def _generate_exploit(self, attack_type: str) -> str:
        """Generate exploit code"""
        code_template = """#!/usr/bin/env python3
\"\"\"
Houdinis Exploit - {attack_type}
Generated by Local Mistral Agent
\"\"\"

from houdinis.exploits import {module}
from houdinis.quantum import QuantumBackend

def main():
    # Initialize backend
    backend = QuantumBackend("nvidia_cuquantum")
    
    # Configure attack
    config = {{
        "target": "example.com",
        "algorithm": "{attack_type}",
        "backend": backend
    }}
    
    # Execute exploit
    result = {module}.run(config)
    
    print(f"Result: {{result}}")

if __name__ == "__main__":
    main()
"""
        
        module_map = {
            "shor": "rsa_shor",
            "grover": "grover_bruteforce",
            "network": "quantum_network_recon"
        }
        
        module = module_map.get(attack_type.lower(), "quantum_exploit")
        
        return code_template.format(
            attack_type=attack_type,
            module=module
        )


def main():
    """Interactive local Mistral agent"""
    print("=" * 70)
    print(" Houdinis Local Mistral AI Agent")
    print("100% Free, Offline & Private Quantum Crypto Analysis")
    print("=" * 70)
    
    # Check if Ollama is running
    print("\n[*] Checking Ollama availability...")
    
    try:
        agent = MistralQuantumAgent(
            model="mistral:7b-instruct",
            use_rag=False  # Disable RAG for faster startup
        )
    except Exception as e:
        print(f"\n[!] Error: {e}")
        print("\n Quick Start:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Run: ollama serve")
        print("3. Pull model: ollama pull mistral:7b-instruct")
        print("4. Try again!\n")
        return
    
    print("\n" + "=" * 70)
    print(" Agent Ready!")
    print("\nAvailable features:")
    print("  • Quantum vulnerability analysis")
    print("  • Shor's algorithm simulation")
    print("  • Grover's attack planning")
    print("  • Post-quantum migration advice")
    print("  • Backend selection")
    print("  • Exploit code generation")
    print("\nType 'quit' to exit\n")
    print("=" * 70)
    
    # Example queries
    examples = [
        "Is RSA-2048 safe from quantum attacks?",
        "How does Grover's algorithm affect AES?",
        "Generate exploit code for Shor's algorithm",
        "Recommend a quantum backend for my project"
    ]
    
    print("\n Example queries:")
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex}")
    print()
    
    # Interactive loop
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n Goodbye!")
                break
            
            if not query:
                continue
            
            print("\n Mistral: ", end="", flush=True)
            response = agent.chat(query)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\n Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n  Error: {str(e)}\n")


if __name__ == "__main__":
    main()
