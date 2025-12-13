@echo off
cd /d %~dp0..
echo Iniciando servicos...
docker-compose up -d
echo Servicos iniciados!
echo Frontend: http://localhost:3000
echo API Gateway: http://localhost:8000