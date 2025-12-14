#!/bin/bash
# Script para reescrever o histórico do Git removendo emojis de mensagens de commit e conteúdo de arquivos

echo "=========================================="
echo "Reescrevendo histórico do Git"
echo "Removendo emojis de commits e arquivos"
echo "=========================================="
echo ""

# Backup do repositório antes de reescrever
echo "Criando backup da branch atual..."
git branch backup-before-emoji-removal

# Função para remover emojis de texto
remove_emojis() {
    python3 -c "
import sys
import re

EMOJI_PATTERN = re.compile(
    '['
    '\U0001F1E0-\U0001F1FF'
    '\U0001F300-\U0001F5FF'
    '\U0001F600-\U0001F64F'
    '\U0001F680-\U0001F6FF'
    '\U0001F700-\U0001F77F'
    '\U0001F780-\U0001F7FF'
    '\U0001F800-\U0001F8FF'
    '\U0001F900-\U0001F9FF'
    '\U0001FA00-\U0001FA6F'
    '\U0001FA70-\U0001FAFF'
    '\U00002702-\U000027B0'
    '\U000024C2-\U0001F251'
    '\U00002600-\U000026FF'
    '\U00002700-\U000027BF'
    ']+',
    flags=re.UNICODE
)

text = sys.stdin.read()
print(EMOJI_PATTERN.sub('', text), end='')
"
}

echo "Reescrevendo histórico do Git..."
echo "ATENÇÃO: Isso reescreverá TODOS os commits!"
echo ""

# Usa git filter-repo (mais seguro e rápido que filter-branch)
# Verifica se git-filter-repo está instalado
if ! command -v git-filter-repo &> /dev/null; then
    echo "git-filter-repo não encontrado. Instalando..."
    pip3 install git-filter-repo
fi

# Cria um script Python para remover emojis dos arquivos
cat > /tmp/remove_emojis_filter.py << 'EOF'
#!/usr/bin/env python3
import re
import sys

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "]+",
    flags=re.UNICODE
)

for line in sys.stdin:
    sys.stdout.write(EMOJI_PATTERN.sub('', line))
EOF

chmod +x /tmp/remove_emojis_filter.py

echo "Reescrevendo histórico usando git filter-repo..."
git filter-repo --force \
    --commit-callback '
import re
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "]+",
    flags=re.UNICODE
)
commit.message = EMOJI_PATTERN.sub(b"", commit.message)
' \
    --blob-callback '
import re
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "]+",
    flags=re.UNICODE
)
try:
    text = blob.data.decode("utf-8")
    blob.data = EMOJI_PATTERN.sub("", text).encode("utf-8")
except:
    pass
'

echo ""
echo "=========================================="
echo "Histórico reescrito com sucesso!"
echo "=========================================="
echo ""
echo "PRÓXIMOS PASSOS:"
echo "1. Revise as mudanças: git log"
echo "2. Se estiver satisfeito, force push: git push origin main --force"
echo "3. Se algo deu errado, restaure o backup: git checkout backup-before-emoji-removal"
echo ""
echo "ATENÇÃO: Todos os colaboradores precisarão clonar novamente o repositório!"
echo "         ou executar: git fetch origin && git reset --hard origin/main"
