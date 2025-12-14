#!/bin/bash
# Script simplificado para remover emojis do histórico Git usando git filter-branch

echo "=========================================="
echo "Removendo emojis do histórico do Git"
echo "=========================================="
echo ""
echo "ATENÇÃO: Esta operação reescreverá TODO o histórico!"
echo ""
read -p "Deseja continuar? (sim/não): " response

if [[ ! "$response" =~ ^(sim|s|yes|y)$ ]]; then
    echo "Operação cancelada."
    exit 0
fi

echo ""
echo "Criando backup da branch atual..."
git branch backup-before-emoji-removal

echo ""
echo "Reescrevendo histórico com git filter-branch..."
echo "Isso pode levar vários minutos..."

# Script Python para remover emojis
cat > /tmp/remove_emoji.py << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
import sys
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

content = sys.stdin.read()
print(EMOJI_PATTERN.sub('', content), end='')
PYTHON_SCRIPT

chmod +x /tmp/remove_emoji.py

# Reescreve o histórico removendo emojis de todos os arquivos
git filter-branch --force --tree-filter '
    find . -type f \( -name "*.py" -o -name "*.ipynb" -o -name "*.md" -o -name "*.txt" -o -name "*.sh" \) -exec sh -c '\''
        for file; do
            if [ -f "$file" ]; then
                python3 /tmp/remove_emoji.py < "$file" > "$file.tmp" && mv "$file.tmp" "$file"
            fi
        done
    '\'' sh {} +
' --msg-filter '
    python3 /tmp/remove_emoji.py
' --tag-name-filter cat -- --all

echo ""
echo "=========================================="
echo "Limpando referências antigas..."
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "=========================================="
echo "HISTÓRICO REESCRITO COM SUCESSO!"
echo "=========================================="
echo ""
echo "PRÓXIMOS PASSOS:"
echo ""
echo "1. Revise as mudanças:"
echo "   git log | head -50"
echo ""
echo "2. Se estiver satisfeito, force push:"
echo "   git push origin main --force"
echo ""
echo "3. Se algo deu errado, restaure o backup:"
echo "   git reset --hard backup-before-emoji-removal"
echo ""
echo "ATENÇÃO: Todos os colaboradores precisarão fazer:"
echo "   git fetch origin"
echo "   git reset --hard origin/main"
echo ""
