@echo off
cd /d %~dp0..
echo Instalando dependencias...
pip install -r ms-usuarios\requirements.txt
pip install -r api-gateway\requirements.txt
pip install -r frontend\requirements.txt
pip install pytest pytest-cov flake8
echo Dependencias instaladas com sucesso!