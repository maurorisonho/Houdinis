#!/usr/bin/env python3
"""
Script para reescrever o histórico do Git removendo emojis de todos os commits.
Usa git filter-repo para reescrever mensagens de commit e conteúdo de arquivos.
"""

import subprocess
import sys
import re

# Padrão regex para capturar todos os emojis Unicode
EMOJI_PATTERN = re.compile(
    "["
    "\U0001f1e0-\U0001f1ff"  # flags (iOS)
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f680-\U0001f6ff"  # transport & map symbols
    "\U0001f700-\U0001f77f"  # alchemical symbols
    "\U0001f780-\U0001f7ff"  # Geometric Shapes Extended
    "\U0001f800-\U0001f8ff"  # Supplemental Arrows-C
    "\U0001f900-\U0001f9ff"  # Supplemental Symbols and Pictographs
    "\U0001fa00-\U0001fa6f"  # Chess Symbols
    "\U0001fa70-\U0001faff"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027b0"  # Dingbats
    "\U000024c2-\U0001f251"
    "\U00002600-\U000026ff"  # Miscellaneous Symbols
    "\U00002700-\U000027bf"  # Dingbats
    "]+",
    flags=re.UNICODE,
)


def remove_emojis(text):
    """Remove todos os emojis de um texto."""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="ignore")
    return EMOJI_PATTERN.sub("", text)


print("=" * 80)
print("REESCREVENDO HISTÓRICO DO GIT - REMOVENDO EMOJIS")
print("=" * 80)
print()
print("ATENÇÃO: Esta operação irá reescrever TODO o histórico do repositório!")
print("Será criado um backup da branch atual antes de prosseguir.")
print()

# Pergunta ao usuário se deseja continuar
response = input("Deseja continuar? (sim/não): ").strip().lower()
if response not in ["sim", "s", "yes", "y"]:
    print("Operação cancelada.")
    sys.exit(0)

print()
print("Criando backup da branch atual...")
subprocess.run(["git", "branch", "backup-before-emoji-removal"], check=False)

print("Criando backup do remote...")
subprocess.run(["git", "remote", "rename", "origin", "origin-backup"], check=False)

print()
print("Reescrevendo histórico do Git...")
print("Isso pode levar alguns minutos dependendo do tamanho do repositório...")
print()

# Usa git filter-repo para reescrever o histórico
try:
    # Remove emojis das mensagens de commit
    subprocess.run(
        [
            "git",
            "filter-repo",
            "--force",
            "--commit-callback",
            f"""
import re
EMOJI_PATTERN = re.compile(
    "["
    "\\U0001F1E0-\\U0001F1FF"
    "\\U0001F300-\\U0001F5FF"
    "\\U0001F600-\\U0001F64F"
    "\\U0001F680-\\U0001F6FF"
    "\\U0001F700-\\U0001F77F"
    "\\U0001F780-\\U0001F7FF"
    "\\U0001F800-\\U0001F8FF"
    "\\U0001F900-\\U0001F9FF"
    "\\U0001FA00-\\U0001FA6F"
    "\\U0001FA70-\\U0001FAFF"
    "\\U00002702-\\U000027B0"
    "\\U000024C2-\\U0001F251"
    "\\U00002600-\\U000026FF"
    "\\U00002700-\\U000027BF"
    "]+",
    flags=re.UNICODE
)
commit.message = EMOJI_PATTERN.sub(b"", commit.message)
        """,
            "--blob-callback",
            f"""
import re
EMOJI_PATTERN = re.compile(
    "["
    "\\U0001F1E0-\\U0001F1FF"
    "\\U0001F300-\\U0001F5FF"
    "\\U0001F600-\\U0001F64F"
    "\\U0001F680-\\U0001F6FF"
    "\\U0001F700-\\U0001F77F"
    "\\U0001F780-\\U0001F7FF"
    "\\U0001F800-\\U0001F8FF"
    "\\U0001F900-\\U0001F9FF"
    "\\U0001FA00-\\U0001FA6F"
    "\\U0001FA70-\\U0001FAFF"
    "\\U00002702-\\U000027B0"
    "\\U000024C2-\\U0001F251"
    "\\U00002600-\\U000026FF"
    "\\U00002700-\\U000027BF"
    "]+",
    flags=re.UNICODE
)
try:
    text = blob.data.decode("utf-8")
    blob.data = EMOJI_PATTERN.sub("", text).encode("utf-8")
except:
    pass
        """,
        ],
        check=True,
    )

    print()
    print("=" * 80)
    print("HISTÓRICO REESCRITO COM SUCESSO!")
    print("=" * 80)
    print()
    print("PRÓXIMOS PASSOS:")
    print()
    print("1. Revise as mudanças:")
    print("   git log")
    print()
    print("2. Restaure o remote:")
    print("   git remote rename origin-backup origin")
    print()
    print("3. Se estiver satisfeito, force push:")
    print("   git push origin main --force")
    print()
    print("4. Se algo deu errado, restaure o backup:")
    print("   git checkout backup-before-emoji-removal")
    print()
    print("ATENÇÃO: Todos os colaboradores precisarão fazer:")
    print("   git fetch origin")
    print("   git reset --hard origin/main")
    print()

except subprocess.CalledProcessError as e:
    print(f"\nERRO ao reescrever histórico: {e}")
    print("\nRestaurando remote...")
    subprocess.run(["git", "remote", "rename", "origin-backup", "origin"], check=False)
    print("Para restaurar o backup, execute:")
    print("   git checkout backup-before-emoji-removal")
    sys.exit(1)
