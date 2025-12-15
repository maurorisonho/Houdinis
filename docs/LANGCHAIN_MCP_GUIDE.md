#  LangChain + MCP Integration Guide

**Houdinis Framework - AI-Enhanced Quantum Cryptography Testing**

> **Developed by:** Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)

##  Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [MCP Server](#mcp-server)
- [LangChain Agent](#langchain-agent)
- [Docker Deployment](#docker-deployment)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

##  Overview

This integration adds **AI-powered intelligence** to the Houdinis Framework using:

- **LangChain**: Orchestrates AI agents for quantum crypto analysis
- **MCP (Model Context Protocol)**: Provides tools and context to AI models
- **Vector Databases**: Enables RAG (Retrieval-Augmented Generation)
- **Multi-Backend Support**: IBM Quantum, NVIDIA cuQuantum, AWS Braket, etc.

### Key Features

 **Intelligent Analysis**: AI agents that understand quantum cryptography  
 **Automated Exploitation**: Smart selection of attack vectors  
 **Threat Assessment**: Timeline predictions for quantum threats  
 **PQC Migration**: Automated post-quantum migration planning  
 **Multi-Backend**: Benchmarking across quantum platforms  

---

##  Architecture

```

                    User Interface                           
            (CLI / Web / API / Chat)                         

              

              LangChain Agent Layer                          
      
    Quantum Crypto Agent                                  
    - Shor's Algorithm                                    
    - Grover's Algorithm                                  
    - Vulnerability Scanning                              
    - PQC Migration Analysis                              
      

                

              MCP Server (Tools)                             
          
   shor_factor     grover_bf       network_scan     
          
          
   threat_time     pq_migration    benchmark        
          

                

           Houdinis Core Framework                           
          
   Exploits    Scanners    Quantum     Payloads   
          

                

          Quantum Backends                                   
          
     IBM        NVIDIA       AWS        Azure     
   Quantum     cuQuantum    Braket     Quantum    
          

```

---

##  Quick Start

### Prerequisites

1. **API Keys**:
   - OpenAI API key (GPT-4) or Anthropic API key (Claude)
   - Optional: IBM Quantum, AWS, Azure credentials

2. **System Requirements**:
   - Docker & Docker Compose
   - NVIDIA GPU (optional, for cuQuantum)
   - 8GB+ RAM

### Installation

```bash
# 1. Clone repository
cd /path/to/Houdinis

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env and add your API keys
nano .env  # or vim, code, etc.

# 4. Build and run with Docker Compose
cd docker/
docker-compose -f docker-compose-langchain.yml up --build

# 5. Access the services
# - Web Terminal: http://localhost:7681
# - MCP Server: http://localhost:8000
# - LangChain API: http://localhost:8001
```

### Local Development (Without Docker)

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install -r requirements-langchain.txt

# 2. Set environment variables
export OPENAI_API_KEY="your-key-here"
# or
export ANTHROPIC_API_KEY="your-key-here"

# 3. Run MCP server (in one terminal)
python -m mcp_servers.quantum_mcp_server

# 4. Run LangChain agent (in another terminal)
python -m langchain_agents.quantum_agent
```

---

##  MCP Server

The MCP server provides tools that AI agents can use to interact with Houdinis.

### Available Tools

| Tool | Description |
|------|-------------|
| `shor_factorize` | Factor RSA keys using Shor's algorithm |
| `grover_bruteforce` | Quantum-accelerated hash cracking |
| `scan_network` | Identify quantum-vulnerable systems |
| `analyze_quantum_threat` | Calculate threat timelines |
| `benchmark_backends` | Compare quantum backend performance |

### Running the MCP Server

```bash
# Start MCP server
python -m mcp_servers.quantum_mcp_server

# Test with MCP client
echo '{"method": "tools/list"}' | python -m mcp_servers.quantum_mcp_server
```

### MCP Server API

```python
from mcp.client import ClientSession

async with ClientSession() as session:
    # List available tools
    tools = await session.list_tools()
    
    # Call a tool
    result = await session.call_tool(
        "shor_factorize",
        {"number": 15, "backend": "qiskit_simulator"}
    )
```

---

##  LangChain Agent

The LangChain agent provides natural language interface to quantum crypto operations.

### Starting the Agent

```bash
# Interactive mode
python -m langchain_agents.quantum_agent

# Or with specific model
python -c "
from langchain_agents.quantum_agent import QuantumCryptoAgent
agent = QuantumCryptoAgent(model='gpt-4')
response = agent.chat('Analyze quantum threats to RSA-2048')
print(response)
"
```

### Example Queries

```python
from langchain_agents.quantum_agent import QuantumCryptoAgent

agent = QuantumCryptoAgent(model="gpt-4")

# Threat analysis
response = agent.chat("""
What is the quantum threat timeline for systems using:
- RSA-2048 for key exchange
- ECDSA P-256 for signatures
- AES-128 for encryption
""")

# Exploitation guidance
response = agent.chat("""
I want to test a target system at 192.168.1.100. 
What quantum attacks are applicable and how should I proceed?
""")

# Migration planning
response = agent.chat("""
Create a post-quantum migration plan for an enterprise 
using RSA-2048 TLS certificates expiring in 2 years.
""")
```

---

##  Docker Deployment

### Using Docker Compose

```bash
# Start all services
docker-compose -f docker/docker-compose-langchain.yml up -d

# View logs
docker-compose -f docker/docker-compose-langchain.yml logs -f

# Stop services
docker-compose -f docker/docker-compose-langchain.yml down

# Rebuild after changes
docker-compose -f docker/docker-compose-langchain.yml up --build
```

### Service Endpoints

| Service | Port | Description |
|---------|------|-------------|
| Houdinis | 7681 | Web terminal (ttyd) |
| MCP Server | 8000 | Model Context Protocol API |
| LangChain API | 8001 | Agent REST API |
| WebSocket | 8765 | Real-time communication |
| ChromaDB | 8080 | Vector database |
| Redis | 6379 | Cache & sessions |
| Nginx | 80/443 | Reverse proxy |

### Environment Configuration

Edit `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...

# Optional - Quantum backends
IBM_QUANTUM_TOKEN=...
AWS_ACCESS_KEY_ID=...
AZURE_QUANTUM_RESOURCE_ID=...

# Optional - Monitoring
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true
```

---

##  API Reference

### REST API

```bash
# Health check
curl http://localhost:8000/health

# List tools
curl http://localhost:8000/tools

# Execute tool
curl -X POST http://localhost:8000/tools/shor_factorize \
  -H "Content-Type: application/json" \
  -d '{"number": 15, "backend": "qiskit"}'

# Chat with agent
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze quantum threats to RSA-2048"}'
```

### Python SDK

```python
from langchain_agents.quantum_agent import QuantumCryptoAgent
from mcp_servers.quantum_mcp_server import QuantumMCPServer

# Initialize agent
agent = QuantumCryptoAgent(
    model="gpt-4",
    temperature=0.7
)

# Natural language query
response = agent.chat("What is Shor's algorithm?")

# Use specific tools
result = agent.agent.invoke({
    "input": "Factor 15 using Shor's algorithm",
    "tool": "shor_algorithm"
})
```

---

##  Examples

### Example 1: Automated Threat Assessment

```python
from langchain_agents.quantum_agent import QuantumCryptoAgent

agent = QuantumCryptoAgent()

# Analyze complete system
query = """
Perform a comprehensive quantum threat assessment for:

Target: example.com
Services:
- HTTPS (RSA-2048, ECDSA P-256)
- SSH (RSA-2048)
- Email (AES-128)

Provide:
1. Current vulnerabilities
2. Timeline for quantum threats
3. Migration recommendations
4. Cost estimates
"""

response = agent.chat(query)
print(response)
```

### Example 2: Benchmark Quantum Backends

```python
# Compare performance across backends
query = """
Benchmark Shor's algorithm for factoring a 15-bit number across:
- IBM Quantum simulator
- NVIDIA cuQuantum (GPU)
- AWS Braket simulator
- Local Qiskit Aer

Compare: execution time, accuracy, cost
"""

response = agent.chat(query)
```

### Example 3: Interactive Security Audit

```python
# Multi-turn conversation
agent = QuantumCryptoAgent()

# Step 1: Initial scan
agent.chat("Scan 192.168.1.100 for quantum vulnerabilities")

# Step 2: Deep analysis
agent.chat("Analyze the RSA key found. How long until it's broken?")

# Step 3: Recommendations
agent.chat("Generate a migration plan with timeline and costs")
```

---

##  Troubleshooting

### Common Issues

**1. "No API key found"**
```bash
# Solution: Set environment variable
export OPENAI_API_KEY="your-key"
# or edit .env file
```

**2. "MCP server not responding"**
```bash
# Check if server is running
docker ps | grep mcp

# View logs
docker logs houdinis_langchain

# Restart service
docker-compose restart houdinis-langchain
```

**3. "CUDA not available"**
```bash
# Verify GPU
nvidia-smi

# Check Docker GPU support
docker run --gpus all nvidia/cuda:12.4.1-base nvidia-smi
```

**4. "Import errors"**
```bash
# Install dependencies
pip install -r requirements-langchain.txt

# Verify installation
python -c "import langchain; print(langchain.__version__)"
```

### Debug Mode

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
export DEBUG=true

# Run with debugging
python -m pdb -m langchain_agents.quantum_agent
```

---

##  Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Houdinis Main Documentation](../README.md)
- [Quantum Computing Backends](../docs/BACKENDS.md)

---

##  Contributing

Contributions are welcome! Please:

1. Test thoroughly with multiple LLM providers
2. Add unit tests for new MCP tools
3. Update documentation
4. Follow security best practices

---

##  License

MIT License - See [LICENSE](../LICENSE) for details

---

**Houdinis Framework** - Making quantum cryptography testing accessible with AI  
*Powered by LangChain + Claude Sonnet 4.5* 
