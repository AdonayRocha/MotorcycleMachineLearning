import os
import subprocess
import sys

# Caminho do Python 3.12 (ajuste se necessário)
python_exe = "python"  # ou o caminho completo do python 3.12 se houver mais de uma versão instalada

# Cria o ambiente virtual
subprocess.run([python_exe, "-m", "venv", ".venv"])

# Instala as dependências
subprocess.run([os.path.join(".venv", "Scripts", "pip"), "install", "--upgrade", "pip"])

# Instala oracledb explicitamente (garante instalação mesmo se não estiver no requirements)
subprocess.run([os.path.join(".venv", "Scripts", "pip"), "install", "-r", "requirements.txt"])
subprocess.run([os.path.join(".venv", "Scripts", "pip"), "install", "oracledb"])

print("Ambiente virtual criado e dependências instaladas!")