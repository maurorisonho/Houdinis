#!/usr/bin/env python3
"""
Build Monitor ULTRA-DETALHADO para Houdinis Mistral AI
Com SUB-BARRAS DE PROGRESSO para cada processo
"""

import subprocess
import sys
import re
import time
import threading
from datetime import datetime
from collections import defaultdict, OrderedDict

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    MAGENTA = '\033[35m'

class MicroProgress:
    """Gerencia micro-barra para uma dependência individual"""
    def __init__(self, name, status='waiting'):
        self.name = name
        self.status = status  # waiting, downloading, installing, complete
        self.progress = 0
        self.size = None
        self.version = None
        
    def get_micro_bar(self, width=15):
        icons = {
            'waiting': ('⏸', Colors.DIM),
            'resolving': ('', Colors.YELLOW),
            'downloading': ('', Colors.CYAN),
            'installing': ('', Colors.BLUE),
            'complete': ('', Colors.GREEN)
        }
        
        icon, color = icons.get(self.status, ('', Colors.CYAN))
        
        if self.status == 'complete':
            bar = '' * width
            percentage = 100.0
        elif self.status == 'downloading':
            filled = int(width * self.progress / 100) if self.progress else 0
            bar = '' * filled + '' * (width - filled)
            percentage = self.progress
        elif self.status == 'installing':
            filled = int(width * 0.8)  # 80% durante instalação
            bar = '' * filled + '' * (width - filled)
            percentage = 80.0
        elif self.status == 'resolving':
            filled = int(width * 0.3)  # 30% durante resolução
            bar = '' * filled + '' * (width - filled)
            percentage = 30.0
        else:
            bar = '' * width
            percentage = 0.0
        
        # Formatação do nome com versão
        display_name = self.name
        if self.version:
            display_name = f"{self.name}-{self.version}"
        if self.size:
            display_name = f"{display_name} ({self.size})"
        
        return f"      {color}{icon} [{bar}] {percentage:5.1f}% {display_name[:40]:<40}{Colors.ENDC}"

class SubProgress:
    """Gerencia uma sub-barra de progresso individual"""
    def __init__(self, name, total, icon, color):
        self.name = name
        self.current = 0
        self.total = total
        self.icon = icon
        self.color = color
        self.items = []
        self.completed = False
        self.micro_bars = OrderedDict()  # Micro-barras para deps individuais
        
    def add_micro_bar(self, dep_name, status='waiting'):
        """Adiciona micro-barra para uma dependência"""
        if dep_name not in self.micro_bars:
            self.micro_bars[dep_name] = MicroProgress(dep_name, status)
    
    def update_micro_bar(self, dep_name, status=None, progress=None, version=None, size=None):
        """Atualiza micro-barra de uma dependência"""
        if dep_name in self.micro_bars:
            if status:
                self.micro_bars[dep_name].status = status
            if progress is not None:
                self.micro_bars[dep_name].progress = progress
            if version:
                self.micro_bars[dep_name].version = version
            if size:
                self.micro_bars[dep_name].size = size
    
    def update(self, current, item=None):
        self.current = current
        if item and item not in self.items:
            self.items.append(item)
        if current >= self.total:
            self.completed = True
    
    def get_bar(self, width=30):
        if self.total == 0:
            filled = width if self.completed else 0
        else:
            filled = int(width * self.current / self.total)
        bar = '' * filled + '' * (width - filled)
        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        
        status = "" if self.completed else ""
        color = Colors.GREEN if self.completed else self.color
        
        return f"{color}{status} {self.icon} {self.name:<20} [{bar}] {self.current:>3}/{self.total:<3} ({percentage:5.1f}%){Colors.ENDC}"

class BuildMonitor:
    def __init__(self):
        self.current_step = 0
        self.total_steps = 14
        self.packages = defaultdict(list)
        self.current_operation = ""
        self.start_time = time.time()
        self.lock = threading.Lock()
        
        # Sub-processos ativos
        self.sub_processes = OrderedDict()
        self.last_line_count = 0
        
        # Contadores por tipo
        self.apt_total = 0
        self.apt_current = 0
        self.pip_total = 0
        self.pip_current = 0
        self.download_total = 0
        self.download_current = 0
        
    def print_header(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}   HOUDINIS MISTRAL AI - BUILD MONITOR DETALHADO{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}\n")
        print(f"{Colors.YELLOW}⏱  Estimativa: 10-15 minutos{Colors.ENDC}")
        print(f"{Colors.DIM}   Componentes: NVIDIA CUDA 12.4 + Ollama + Python 3.11 + LangChain + cuQuantum{Colors.ENDC}\n")
    
    def clear_lines(self, count):
        """Limpa N linhas anteriores"""
        for _ in range(count):
            print(f"\033[F\033[K", end='')
    
    def render_full_display(self):
        """Renderiza display completo com barra principal + sub-barras"""
        with self.lock:
            # Limpar linhas anteriores
            if self.last_line_count > 0:
                self.clear_lines(self.last_line_count)
            
            lines = []
            
            # Barra principal
            percentage = (self.current_step / self.total_steps) * 100
            bar_length = 60
            filled = int(bar_length * self.current_step / self.total_steps)
            bar = '' * filled + '' * (bar_length - filled)
            
            elapsed = time.time() - self.start_time
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            
            status = "" if self.current_step >= self.total_steps else "⏳"
            
            lines.append(f"\n{Colors.BOLD}{Colors.CYAN}{''*100}{Colors.ENDC}")
            lines.append(f"{Colors.BOLD}{status} [{bar}] {percentage:5.1f}%{Colors.ENDC} | "
                        f"{Colors.CYAN}STEP {self.current_step}/{self.total_steps}{Colors.ENDC}: "
                        f"{self.current_operation[:50]:<50} | "
                        f"{Colors.DIM}⏱ {mins:02d}:{secs:02d}{Colors.ENDC}")
            lines.append(f"{Colors.CYAN}{''*100}{Colors.ENDC}")
            
            # Sub-barras de progresso
            if self.sub_processes:
                lines.append(f"{Colors.BOLD}   Processos Ativos:{Colors.ENDC}")
                for key, sub_proc in self.sub_processes.items():
                    lines.append(f"    {sub_proc.get_bar()}")
                    
                    # MICRO-BARS: Show individual progress for each dependency
                    if sub_proc.micro_bars:
                        # Show up to 10 most recent micro-bars
                        visible_micros = list(sub_proc.micro_bars.items())[-10:]
                        for dep_name, micro in visible_micros:
                            # Only show if not complete or one of the last 3
                            if micro.status != 'complete' or dep_name in list(sub_proc.micro_bars.keys())[-3:]:
                                lines.append(micro.get_micro_bar())
                    
                    # Fallback: Show last 3 items if no micro-bars
                    elif sub_proc.items and not sub_proc.completed:
                        recent = sub_proc.items[-3:]
                        for item in recent:
                            lines.append(f"      {Colors.DIM} {item}{Colors.ENDC}")
            
            lines.append(f"{Colors.CYAN}{''*100}{Colors.ENDC}\n")
            
            # Imprimir tudo
            output = '\n'.join(lines)
            print(output, end='', flush=True)
            
            # Salvar contagem de linhas para próxima limpeza
            self.last_line_count = len(lines)
    
    def add_subprocess(self, key, name, total, icon, color):
        """Adiciona novo sub-processo"""
        self.sub_processes[key] = SubProgress(name, total, icon, color)
    
    def update_subprocess(self, key, current, item=None):
        """Atualiza sub-processo"""
        if key in self.sub_processes:
            self.sub_processes[key].update(current, item)
            # Remover se completo após 1 segundo
            if self.sub_processes[key].completed:
                threading.Timer(1.0, lambda: self.sub_processes.pop(key, None)).start()
    
    def complete_subprocess(self, key):
        """Marca sub-processo como completo"""
        if key in self.sub_processes:
            total = self.sub_processes[key].total
            self.sub_processes[key].update(total)
            self.sub_processes[key].completed = True
    
    def parse_line(self, line):
        """Analisa linha e extrai informações relevantes"""
        
        # Detectar step atual
        step_match = re.search(r'#(\d+)\s+\[\s*(\d+)/(\d+)\]', line)
        if step_match:
            self.current_step = int(step_match.group(2))
            self.total_steps = int(step_match.group(3))
            
            # Limpar sub-processos ao mudar de step
            self.sub_processes.clear()
            
            # Identificar operação
            if 'FROM' in line:
                self.current_operation = " Baixando imagem base NVIDIA CUDA 12.4"
                self.add_subprocess('download', 'Pulling layers', 10, '', Colors.BLUE)
            
            elif 'RUN apt-get update' in line:
                self.current_operation = " Atualizando repositórios APT"
                self.add_subprocess('apt-update', 'Fetching packages', 1, '', Colors.YELLOW)
            
            elif 'RUN apt-get install' in line:
                self.current_operation = " Instalando dependências do sistema"
                # Contar pacotes no comando
                pkgs = re.findall(r'(python3\.11|git|wget|curl|cmake|ttyd|vim|libgomp1|software-properties-common)', line)
                self.apt_total = len(pkgs) if pkgs else 10
                self.apt_current = 0
                self.add_subprocess('apt-install', 'APT packages', self.apt_total, '', Colors.GREEN)
            
            elif 'RUN curl' in line and 'ollama' in line:
                self.current_operation = " Instalando Ollama AI Framework"
                self.add_subprocess('ollama', 'Downloading Ollama', 1, '', Colors.MAGENTA)
            
            elif 'WORKDIR' in line:
                workdir = re.search(r'WORKDIR\s+(.+)', line)
                if workdir:
                    self.current_operation = f" Configurando workspace: {workdir.group(1)}"
            
            elif 'COPY requirements' in line:
                self.current_operation = " Copying Python dependency files"
            
            elif 'RUN pip3 install' in line:
                if 'requirements.txt' in line and 'langchain' not in line:
                    self.current_operation = " Installing base Python packages (Qiskit, NumPy, Pandas...)"
                    self.pip_total = 200  # Estimativa
                    self.pip_current = 0
                    self.download_total = 50
                    self.download_current = 0
                    self.add_subprocess('pip-collect', 'Resolving deps', self.pip_total, '', Colors.YELLOW)
                    self.add_subprocess('pip-download', 'Downloading', self.download_total, '', Colors.CYAN)
                    self.add_subprocess('pip-install', 'Installing', self.pip_total, '', Colors.GREEN)
                
                elif 'langchain' in line.lower():
                    self.current_operation = " Installing LangChain ecosystem"
                    self.pip_total = 50
                    self.pip_current = 0
                    self.add_subprocess('langchain-collect', 'LangChain deps', 50, '', Colors.BLUE)
                    self.add_subprocess('langchain-download', 'Downloading', 15, '', Colors.CYAN)
                    self.add_subprocess('langchain-install', 'Installing', 50, '', Colors.GREEN)
                
                elif 'chromadb' in line.lower():
                    self.current_operation = " Installing Vector Stores (ChromaDB + FAISS)"
                    self.add_subprocess('vectordb-collect', 'Vector store deps', 30, '', Colors.BLUE)
                    self.add_subprocess('vectordb-download', 'Downloading', 10, '', Colors.CYAN)
                    self.add_subprocess('vectordb-install', 'Installing', 30, '', Colors.GREEN)
                
                elif 'cuquantum' in line.lower():
                    self.current_operation = " Installing NVIDIA cuQuantum (GPU acceleration)"
                    self.add_subprocess('cuquantum', 'cuQuantum package', 5, '', Colors.MAGENTA)
            
            elif 'COPY .' in line:
                self.current_operation = " Copying Houdinis source code"
                self.add_subprocess('copy-files', 'Copying files', 100, '', Colors.CYAN)
            
            elif 'RUN mkdir' in line:
                self.current_operation = " Creating persistent data directories"
            
            elif 'RUN useradd' in line:
                self.current_operation = " Configuring non-root user (security)"
            
            elif 'EXPOSE' in line:
                self.current_operation = " Exposing ports (Ollama 11434, ttyd 7681, API 8001)"
            
            elif 'HEALTHCHECK' in line:
                self.current_operation = " Configurando health check (Ollama API)"
            
            self.render_full_display()
        
        # ===== MONITORAMENTO DE SUB-PROCESSOS =====
        
        # APT: Unpacking (primeiro estágio)
        if 'Unpacking' in line:
            pkg = re.search(r'Unpacking\s+([^\s]+)', line)
            if pkg and 'apt-install' in self.sub_processes:
                pkg_name = pkg.group(1)
                self.sub_processes['apt-install'].add_micro_bar(pkg_name, 'downloading')
                self.sub_processes['apt-install'].update_micro_bar(pkg_name, 'downloading', 40)
                self.render_full_display()
        
        # APT: Setting up (instalação)
        if 'Setting up' in line:
            pkg = re.search(r'Setting up\s+([^\s]+)', line)
            if pkg and 'apt-install' in self.sub_processes:
                pkg_name = pkg.group(1)
                self.apt_current += 1
                self.update_subprocess('apt-install', self.apt_current, pkg_name)
                self.sub_processes['apt-install'].update_micro_bar(pkg_name, 'installing', 80)
                self.render_full_display()
        
        # APT: Configurando (finalização)
        if 'Processing triggers' in line or 'ldconfig deferred' in line:
            # Marcar últimos pacotes APT como completos
            if 'apt-install' in self.sub_processes:
                for pkg_name in list(self.sub_processes['apt-install'].micro_bars.keys())[-3:]:
                    self.sub_processes['apt-install'].update_micro_bar(pkg_name, 'complete', 100)
                self.render_full_display()
        
        # PIP: Collecting
        collecting = re.search(r'Collecting\s+([a-zA-Z0-9_\[\]-]+)', line)
        if collecting:
            pkg_name = collecting.group(1)
            self.packages['collecting'].append(pkg_name)
            
            # Determinar qual sub-processo usar e adicionar micro-barra
            for key in ['pip-collect', 'langchain-collect', 'vectordb-collect', 'cuquantum']:
                if key in self.sub_processes:
                    self.pip_current += 1
                    self.update_subprocess(key, self.pip_current, pkg_name)
                    # Adicionar micro-barra para este pacote
                    self.sub_processes[key].add_micro_bar(pkg_name, 'resolving')
                    self.render_full_display()
                    break
                    self.pip_current += 1
                    self.update_subprocess(key, self.pip_current, pkg_name)
                    self.render_full_display()
        # PIP: Downloading
        downloading = re.search(r'Downloading\s+([a-zA-Z0-9_-]+)-([0-9\.]+).*?\(([0-9\.]+\s*[kMG]?B)\)', line)
        if downloading:
            pkg_name = downloading.group(1)
            version = downloading.group(2)
            size = downloading.group(3)
            item = f"{pkg_name}-{version} ({size})"
            self.packages['downloading'].append(item)
            
            # Atualizar downloads e micro-barra
            for key in ['pip-download', 'langchain-download', 'vectordb-download']:
                if key in self.sub_processes:
                    self.download_current += 1
                    self.update_subprocess(key, self.download_current, item)
                    # Atualizar micro-barra para downloading
                    self.sub_processes[key].add_micro_bar(pkg_name, 'downloading')
                    self.sub_processes[key].update_micro_bar(pkg_name, 'downloading', 50, version, size)
                    self.render_full_display()
                    break
        # PIP: Installing collected packages
        if 'Installing collected packages:' in line:
            # Extrair lista de pacotes que serão instalados
            pkgs_match = re.search(r'Installing collected packages:\s+(.+)', line)
            if pkgs_match:
                pkgs = [p.strip() for p in pkgs_match.group(1).split(',')]
                for key in ['pip-install', 'langchain-install', 'vectordb-install']:
                    if key in self.sub_processes:
                        for pkg in pkgs[:10]:  # First 10 to avoid overload
                            self.sub_processes[key].add_micro_bar(pkg, 'installing')
        
        # PIP: Successfully installed
        installed = re.search(r'Successfully installed\s+(.+)', line)
        if installed:
            pkgs = installed.group(1).split()
            self.packages['installed'].extend(pkgs)
            
            # Marcar todas as micro-barras como completas
            for pkg_full in pkgs:
                pkg_name = pkg_full.split('-')[0]  # Extrair nome sem versão
                for key in ['pip-collect', 'langchain-collect', 'vectordb-collect', 
                           'pip-download', 'langchain-download', 'vectordb-download',
                           'pip-install', 'langchain-install', 'vectordb-install']:
                    if key in self.sub_processes:
                        self.sub_processes[key].update_micro_bar(pkg_name, 'complete', 100)
            
            # Completar instalação
            for key in ['pip-install', 'langchain-install', 'vectordb-install', 'cuquantum']:
                if key in self.sub_processes:
                    self.complete_subprocess(key)
                    self.render_full_display()
                    breakled.group(1).split()
            self.packages['installed'].extend(pkgs)
            
            # Completar instalação
            for key in ['pip-install', 'langchain-install', 'vectordb-install', 'cuquantum']:
                if key in self.sub_processes:
                    self.complete_subprocess(key)
                    self.render_full_display()
                    break
        
        # Ollama installation
        if 'install.sh' in line and 'ollama' in line.lower():
            if 'ollama' in self.sub_processes:
                self.complete_subprocess('ollama')
                self.render_full_display()
        
        # Docker export/finalize
        if 'exporting layers' in line.lower():
            self.current_operation = " Exportando layers da imagem"
            self.add_subprocess('export', 'Exporting layers', 10, '', Colors.CYAN)
            self.render_full_display()
        
        if 'exporting manifest' in line.lower():
            self.current_operation = " Finalizando build"
            if 'export' in self.sub_processes:
                self.complete_subprocess('export')
            self.render_full_display()
        
        if 'writing image sha256' in line.lower():
            self.sub_processes.clear()
            self.render_full_display()
        
        # Erros
        if 'ERROR' in line or ('error' in line.lower() and 'failed' in line.lower()):
            print(f"\n{Colors.RED} ERRO: {line[:100]}{Colors.ENDC}\n")
        
        # Warnings importantes
        if 'WARNING' in line and 'Running pip as the' not in line and 'DEPRECATION' not in line:
            print(f"\n{Colors.YELLOW}  {line[:100]}{Colors.ENDC}\n")

def run_build():
    monitor = BuildMonitor()
    monitor.print_header()
    
    # Verificar requisitos
    print(f"{Colors.BOLD} Verificando requisitos...{Colors.ENDC}\n")
    
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        print(f"   Docker: {result.stdout.strip()}")
    except:
        print(f"  {Colors.RED} Docker not found{Colors.ENDC}")
        return False
    
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            print(f"   GPU: {result.stdout.strip()}")
    except:
        print(f"  {Colors.YELLOW}  NVIDIA GPU not detected (build will continue without GPU){Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Iniciar build com SUB-BARRAS DE PROGRESSO? [S/n]{Colors.ENDC} ", end='', flush=True)
    response = input().strip().lower()
    if response and response not in ['s', 'sim', 'y', 'yes', '']:
        print(f"\n{Colors.YELLOW}Build cancelado{Colors.ENDC}")
        return False
    
    print(f"\n{Colors.CYAN}{'='*100}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}   Iniciando build ULTRA-DETALHADO...{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*100}{Colors.ENDC}")
    
    cmd = [
        'docker', 'buildx', 'build',
        '--progress=plain',
        '--file', 'docker/Dockerfile.mistral',
        '--tag', 'houdinis-mistral:latest',
        '.'
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    try:
        for line in process.stdout:
            monitor.parse_line(line.strip())
        
        process.wait()
        
        # Limpar display de progresso
        if monitor.last_line_count > 0:
            monitor.clear_lines(monitor.last_line_count)
        
        elapsed = time.time() - monitor.start_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        
        if process.returncode == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*100}{Colors.ENDC}")
            print(f"{Colors.GREEN}{Colors.BOLD}   BUILD CONCLUÍDO COM SUCESSO!{Colors.ENDC}")
            print(f"{Colors.GREEN}{Colors.BOLD}{'='*100}{Colors.ENDC}\n")
            
            print(f"  ⏱  Tempo total: {Colors.BOLD}{mins}m {secs}s{Colors.ENDC}")
            print(f"   Pacotes Python instalados: {Colors.BOLD}{len(monitor.packages['installed'])}+{Colors.ENDC}")
            
            # Mostrar tamanho da imagem
            result = subprocess.run(['docker', 'images', 'houdinis-mistral:latest', '--format', '{{.Size}}'],
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print(f"   Tamanho da imagem: {Colors.BOLD}{result.stdout.strip()}{Colors.ENDC}\n")
            
            # Estatísticas detalhadas
            print(f"{Colors.CYAN}{''*100}{Colors.ENDC}")
            print(f"{Colors.BOLD} Estatísticas:{Colors.ENDC}\n")
            print(f"  • Pacotes coletados: {len(monitor.packages['collecting'])}")
            print(f"  • Pacotes baixados: {len(monitor.packages['downloading'])}")
            print(f"  • Pacotes instalados: {len(monitor.packages['installed'])}")
            
            print(f"\n{Colors.CYAN}{''*100}{Colors.ENDC}")
            print(f"{Colors.BOLD} Próximos passos:{Colors.ENDC}\n")
            print(f"  1. {Colors.CYAN}docker compose -f docker/docker-compose-lite.yml up -d mistral{Colors.ENDC}")
            print(f"      Inicia container Mistral com Ollama")
            print(f"\n  2. {Colors.CYAN}docker logs houdinis_mistral -f{Colors.ENDC}")
            print(f"      Monitora download do modelo Mistral 7B (~4.1GB)")
            print(f"\n  3. {Colors.CYAN}curl http://localhost:11434/api/tags{Colors.ENDC}")
            print(f"      Verifica modelos disponíveis no Ollama")
            print(f"\n  4. Acesse http://localhost:8080/ai-assistant")
            print(f"      Teste o AI Assistant com Mistral")
            
            print(f"\n{Colors.GREEN}{'='*100}{Colors.ENDC}\n")
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}{'='*100}{Colors.ENDC}")
            print(f"{Colors.RED}{Colors.BOLD}   Build falhou (exit code {process.returncode}){Colors.ENDC}")
            print(f"{Colors.RED}{Colors.BOLD}{'='*100}{Colors.ENDC}\n")
            return False
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}{'='*100}{Colors.ENDC}")
        print(f"{Colors.YELLOW}    Build interrupted by user{Colors.ENDC}")
        print(f"{Colors.YELLOW}{'='*100}{Colors.ENDC}\n")
        process.terminate()
        return False

if __name__ == '__main__':
    success = run_build()
    sys.exit(0 if success else 1)
