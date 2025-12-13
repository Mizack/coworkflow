@echo off
cd /d %~dp0..
echo Construindo imagens Docker...
docker-compose build
echo Build concluido!