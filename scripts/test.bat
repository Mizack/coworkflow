@echo off
cd /d %~dp0..
echo Executando testes...
pytest tests\ --cov=. --cov-report=html
echo Testes concluidos! Veja o relatorio em htmlcov\index.html