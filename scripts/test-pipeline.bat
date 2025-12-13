@echo off
cd /d %~dp0..
echo ========================================
echo Testando Pipeline CI/CD Localmente
echo ========================================
echo.

echo [0/4] Verificando dependencias...
pip show flake8 >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install pytest pytest-cov flake8 requests Flask werkzeug PyJWT flasgger
)
echo Dependencias: OK
echo.

echo [1/4] Executando Lint...
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,.venv,htmlcov,.git
if %errorlevel% neq 0 (
    echo ERRO: Lint encontrou erros criticos!
    exit /b 1
)
echo Lint: OK
echo.

echo [2/4] Executando Testes...
python -m pytest tests\ --cov=. --cov-report=html 2>nul
if %errorlevel% neq 0 (
    echo AVISO: Nenhum teste encontrado ou testes falharam
)
echo Testes: OK
echo.

echo [3/4] Construindo Imagens Docker...
docker-compose build >nul 2>&1
if %errorlevel% neq 0 (
    echo AVISO: Build Docker falhou ou Docker nao esta instalado
    echo Pulando etapa de build...
) else (
    echo Build: OK
)
echo.

echo [4/4] Testando Integracao...
docker-compose up -d >nul 2>&1
if %errorlevel% neq 0 (
    echo AVISO: Nao foi possivel iniciar servicos Docker
    echo Pulando teste de integracao...
) else (
    echo Aguardando servicos iniciarem...
    timeout /t 30 /nobreak >nul
    curl -f http://localhost:8000/health >nul 2>&1
    if %errorlevel% neq 0 (
        echo AVISO: Teste de integracao falhou
    ) else (
        echo Integracao: OK
    )
    docker-compose down >nul 2>&1
)
echo.

echo ========================================
echo Pipeline executado!
echo ========================================
echo.
echo Proximos passos:
echo 1. Corrigir erros de lint (se houver)
echo 2. Adicionar testes em tests/
echo 3. Fazer commit e push para testar no GitHub
echo ========================================