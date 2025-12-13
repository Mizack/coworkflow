@echo off
cd /d %~dp0..
echo Parando servicos...
docker-compose down
echo Servicos parados!