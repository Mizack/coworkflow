# Início Rápido - Pipeline CI/CD

## Opção 1: Teste Rápido (Recomendado)

```bash
cd coworkflow
scripts\quick-test.bat
```

Isso vai:
1. ✅ Instalar dependências automaticamente
2. ✅ Executar lint no código
3. ✅ Mostrar erros (se houver)

## Opção 2: Teste Completo

```bash
cd coworkflow
scripts\test-pipeline.bat
```

Isso vai:
1. ✅ Instalar dependências
2. ✅ Executar lint
3. ✅ Executar testes
4. ✅ Build Docker (se disponível)
5. ✅ Teste de integração (se disponível)

## Opção 3: Testar no GitHub (Mais Fácil)

### Passo 1: Fazer commit
```bash
git add .
git commit -m "test: pipeline ci/cd"
```

### Passo 2: Push
```bash
git push origin main
```

### Passo 3: Ver resultado
1. Ir para GitHub
2. Clicar em "Actions"
3. Ver o workflow executando
4. ✅ Verde = Passou
5. ❌ Vermelho = Falhou (clicar para ver detalhes)

## Resolver Problemas Comuns

### "flake8 não reconhecido"
```bash
pip install flake8
```

### "pytest não reconhecido"
```bash
pip install pytest
```

### "Docker não está rodando"
- Iniciar Docker Desktop
- Ou pular etapa Docker e testar só lint/test

## Comandos Úteis

```bash
# Instalar tudo
pip install pytest pytest-cov flake8 requests Flask werkzeug PyJWT flasgger

# Só lint
python -m flake8 . --exclude=venv,.venv,htmlcov,.git

# Só testes
python -m pytest tests/

# Docker
docker-compose up -d
docker-compose down
```

## Fluxo Recomendado

1. **Desenvolver localmente**
   ```bash
   scripts\quick-test.bat
   ```

2. **Corrigir erros** (se houver)

3. **Commit e push**
   ```bash
   git add .
   git commit -m "feat: nova funcionalidade"
   git push origin develop
   ```

4. **Ver no GitHub Actions**
   - Automático após push
   - Mostra todos os checks
   - Deploy automático se passar

## Exemplo Completo

```bash
# 1. Testar localmente
cd coworkflow
scripts\quick-test.bat

# 2. Se passou, fazer commit
git add .
git commit -m "feat: implementação completa"

# 3. Push para staging
git push origin develop
# Ver em: https://github.com/[usuario]/coworkflow/actions

# 4. Se passou em staging, merge para produção
git checkout main
git merge develop
git push origin main
# Deploy automático em produção
```

## Verificar Status

### Localmente
```bash
scripts\quick-test.bat
```

### GitHub
1. Ir para repositório
2. Clicar em "Actions"
3. Ver workflows
4. Clicar em execução para ver logs

## Próximos Passos

Após pipeline passar:
- ✅ Código validado
- ✅ Pronto para produção
- ✅ Deploy automático configurado