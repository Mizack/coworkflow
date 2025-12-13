@echo off
cd /d %~dp0..
echo ========================================
echo Teste Rapido do Pipeline
echo ========================================
echo.

echo Instalando dependencias...
pip install -q pytest pytest-cov flake8 requests Flask werkzeug PyJWT flasgger

echo.
echo Executando lint...
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,.venv,htmlcov,.git

echo.
echo ========================================
echo Teste concluido!
echo.
echo Para testar no GitHub:
echo   git add .
echo   git commit -m "test: pipeline"
echo   git push origin develop
echo.
echo Depois veja em: GitHub -^> Actions
echo ========================================