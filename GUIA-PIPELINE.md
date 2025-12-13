# Guia de Testes do Pipeline CI/CD

## Scripts Disponíveis (Windows)

Todos os scripts estão na pasta `scripts/`:

### Comandos Individuais

```bash
# Instalar dependências
scripts\install.bat

# Executar testes
scripts\test.bat

# Executar lint
scripts\lint.bat

# Build Docker
scripts\build.bat

# Iniciar serviços
scripts\up.bat

# Parar serviços
scripts\down.bat
```

### Testar Pipeline Completo

```bash
# Executa todo o pipeline localmente
scripts\test-pipeline.bat
```

## Como Testar o Pipeline Localmente

### Passo 1: Instalar Dependências

```bash
cd coworkflow
scripts\install.bat
```

### Passo 2: Executar Lint

```bash
scripts\lint.bat
```

**O que verifica:**
- Erros de sintaxe Python
- Complexidade do código
- Padrões de código

**Resultado esperado:**
```
0 errors found
```

### Passo 3: Executar Testes

```bash
scripts\test.bat
```

**O que verifica:**
- Testes unitários
- Cobertura de código

**Resultado esperado:**
```
===== X passed in X.XXs =====
Coverage report: htmlcov\index.html
```

### Passo 4: Build Docker

```bash
scripts\build.bat
```

**O que faz:**
- Build de todas as imagens Docker
- Valida Dockerfiles

**Resultado esperado:**
```
Successfully built [image-id]
Successfully tagged coworkflow/[service]:latest
```

### Passo 5: Teste de Integração

```bash
scripts\up.bat
# Aguardar 30 segundos
curl http://localhost:8000/health
curl http://localhost:3000
scripts\down.bat
```

**Resultado esperado:**
```json
{"status": "healthy"}
```

## Como Testar o Pipeline no GitHub

### Método 1: Push para Branch

```bash
# Criar branch de teste
git checkout -b test/pipeline

# Fazer uma mudança
echo "# Test" >> README.md

# Commit e push
git add .
git commit -m "test: pipeline test"
git push origin test/pipeline
```

**Verificar:**
1. Ir para GitHub → Actions
2. Ver workflow "CI/CD Pipeline" executando
3. Verificar cada job (Lint → Test → Build → Integration Test)

### Método 2: Pull Request

```bash
# Criar PR no GitHub
gh pr create --title "Test Pipeline" --body "Testing CI/CD"
```

**Verificar:**
1. PR mostra checks do CI/CD
2. Todos os checks devem passar (✓)
3. Ver detalhes clicando em "Details"

### Método 3: Executar Manualmente

```bash
# Via GitHub CLI
gh workflow run ci-cd.yml

# Verificar status
gh run list
gh run view [run-id]
```

**Ou via interface:**
1. GitHub → Actions
2. Selecionar workflow "CI/CD Pipeline"
3. Clicar em "Run workflow"
4. Escolher branch
5. Clicar em "Run workflow"

## Estrutura do Pipeline

```
┌─────────────┐
│    Lint     │ ← Valida código
└──────┬──────┘
       │
┌──────▼──────┐
│    Test     │ ← Executa testes
└──────┬──────┘
       │
┌──────▼──────┐
│    Build    │ ← Build Docker
└──────┬──────┘
       │
┌──────▼──────┐
│ Integration │ ← Testa integração
└──────┬──────┘
       │
   ┌───▼───┐
   │Deploy │ ← Deploy automático
   └───────┘
```

## Verificar Resultados

### Localmente

```bash
# Ver relatório de testes
start htmlcov\index.html

# Ver logs Docker
docker-compose logs

# Ver status dos containers
docker-compose ps
```

### No GitHub

1. **Actions Tab:**
   - Ver todos os workflows
   - Status de cada execução
   - Logs detalhados

2. **Pull Request:**
   - Checks automáticos
   - Status de cada job
   - Comentários automáticos

3. **Security Tab:**
   - Vulnerabilidades encontradas
   - Dependências desatualizadas
   - Alertas de segurança

## Troubleshooting

### Lint Falhou

```bash
# Ver erros
scripts\lint.bat

# Corrigir automaticamente (alguns casos)
autopep8 --in-place --aggressive --aggressive [arquivo.py]
```

### Testes Falharam

```bash
# Ver detalhes
scripts\test.bat

# Executar teste específico
pytest tests\test_api_gateway.py -v
```

### Build Falhou

```bash
# Ver logs
docker-compose build --no-cache [service]

# Verificar Dockerfile
type ms-usuarios\Dockerfile
```

### Integração Falhou

```bash
# Ver logs dos serviços
docker-compose logs api-gateway
docker-compose logs ms-usuarios

# Verificar conectividade
curl -v http://localhost:8000/health
```

## Exemplo Completo

```bash
# 1. Preparar ambiente
cd coworkflow
scripts\install.bat

# 2. Testar pipeline completo
scripts\test-pipeline.bat

# 3. Se tudo passou, fazer commit
git add .
git commit -m "feat: nova funcionalidade"
git push origin develop

# 4. Verificar no GitHub
# Ir para: https://github.com/[seu-usuario]/coworkflow/actions

# 5. Ver deploy automático em staging
# URL: https://staging.coworkflow.com (exemplo)
```

## Métricas de Sucesso

✅ **Pipeline OK se:**
- Lint: 0 erros
- Testes: 100% passando
- Build: Todas as imagens criadas
- Integração: Health check retorna 200
- Deploy: Serviços acessíveis

❌ **Pipeline FALHOU se:**
- Qualquer job retornar erro
- Timeout em algum serviço
- Health check falhar
- Testes com falhas

## Próximos Passos

Após pipeline passar:
1. ✅ Código validado
2. ✅ Testes passando
3. ✅ Build funcionando
4. ✅ Pronto para merge
5. ✅ Deploy automático