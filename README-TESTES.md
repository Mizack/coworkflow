# 🧪 Guia de Testes - CoworkFlow

## Estrutura de Testes

```
tests/
├── unit/                    # Testes unitários
│   ├── test_ms_usuarios.py
│   ├── test_ms_espacos.py
│   ├── test_ms_reservas.py
│   ├── test_ms_pagamentos.py
│   ├── test_ms_precos.py
│   ├── test_ms_checkin.py
│   ├── test_ms_notificacoes.py
│   ├── test_ms_financeiro.py
│   └── test_ms_analytics.py
├── integration/             # Testes de integração
│   ├── test_reservation_flow.py
│   ├── test_api_gateway.py
│   └── conftest.py
├── ui/                      # Testes de interface (Selenium)
│   ├── test_user_registration.py
│   ├── test_space_booking.py
│   ├── test_payment_flow.py
│   └── conftest.py
├── e2e/                     # Testes end-to-end
│   └── test_complete_user_journey.py
├── performance/             # Testes de performance
│   └── load_test.py
└── conftest.py             # Configuração global
```

## Tipos de Testes

### 1. Testes Unitários
- **Objetivo**: Testar funções e métodos isoladamente
- **Cobertura**: Cada microsserviço individualmente
- **Execução**: `pytest tests/unit/`

### 2. Testes de Integração
- **Objetivo**: Testar comunicação entre microsserviços
- **Cobertura**: Fluxos completos de negócio
- **Execução**: `pytest tests/integration/`

### 3. Testes de UI
- **Objetivo**: Testar interface do usuário
- **Ferramenta**: Selenium WebDriver
- **Execução**: `pytest tests/ui/`

### 4. Testes E2E
- **Objetivo**: Testar jornadas completas do usuário
- **Cobertura**: Do cadastro ao checkout
- **Execução**: `pytest tests/e2e/`

### 5. Testes de Performance
- **Objetivo**: Testar carga e performance
- **Ferramenta**: Locust
- **Execução**: `locust -f tests/performance/load_test.py`

## Comandos de Execução

### Executar Todos os Testes
```bash
scripts\run-tests.bat all
```

### Executar por Categoria
```bash
# Testes unitários
scripts\run-tests.bat unit

# Testes de integração
scripts\run-tests.bat integration

# Testes de UI
scripts\run-tests.bat ui

# Testes E2E
scripts\run-tests.bat e2e

# Testes de performance
scripts\run-tests.bat performance
```

### Executar com Pytest Diretamente
```bash
# Testes unitários com cobertura
pytest tests/unit/ -v --cov=. --cov-report=html

# Testes específicos
pytest tests/unit/test_ms_usuarios.py -v

# Testes com marcadores
pytest -m "unit" -v
pytest -m "integration" -v
```

## Configuração do Ambiente

### Instalar Dependências
```bash
pip install -r requirements-test.txt
```

### Configurar WebDriver (Chrome)
```bash
# Instalar ChromeDriver automaticamente
pip install webdriver-manager
```

### Variáveis de Ambiente
```bash
# Para testes
export TESTING=true
export DATABASE_URL=postgresql://test:test@localhost/coworkflow_test
```

## Relatórios de Cobertura

### Gerar Relatório HTML
```bash
pytest tests/unit/ --cov=. --cov-report=html
# Relatório em: htmlcov/index.html
```

### Gerar Relatório XML (CI/CD)
```bash
pytest tests/unit/ --cov=. --cov-report=xml
```

## Testes Automatizados (CI/CD)

### GitHub Actions
- **Trigger**: Push, PR, agendamento diário
- **Matriz**: Python 3.9, 3.10, 3.11
- **Stages**: Unit → Integration → UI → E2E → Performance

### Pipeline de Testes
1. **Unit Tests**: Execução rápida, sem dependências
2. **Integration Tests**: Com Docker containers
3. **UI Tests**: Com Chrome headless
4. **E2E Tests**: Cenários completos
5. **Performance Tests**: Apenas agendado/manual

## Boas Práticas

### Nomenclatura
- Arquivos: `test_*.py`
- Classes: `Test*`
- Métodos: `test_*`

### Estrutura de Teste
```python
def test_should_do_something_when_condition():
    # Arrange
    setup_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

### Fixtures
```python
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

### Mocking
```python
@pytest.fixture
def mock_external_api(mocker):
    return mocker.patch('module.external_api_call')
```

## Dados de Teste

### Usuários de Teste
- **Regular**: `test@example.com` / `test123`
- **Admin**: `admin@coworkflow.com` / `admin123`
- **Load Test**: `loadtest{id}@example.com` / `loadtest123`

### Espaços de Teste
- **Meeting Room**: Capacidade 8, R$ 25/hora
- **Executive Room**: Capacidade 12, R$ 45/hora
- **Open Space**: Capacidade 20, R$ 15/hora

## Troubleshooting

### Testes Falhando
```bash
# Ver logs detalhados
pytest tests/unit/test_ms_usuarios.py -v -s

# Debug específico
pytest tests/unit/test_ms_usuarios.py::test_login_success -v -s
```

### Selenium Issues
```bash
# Verificar Chrome/ChromeDriver
google-chrome --version
chromedriver --version

# Executar com interface (debug)
# Remover --headless do conftest.py
```

### Performance Issues
```bash
# Executar com menos usuários
locust -f tests/performance/load_test.py --users=5 --spawn-rate=1
```

## Métricas de Qualidade

### Cobertura de Código
- **Meta**: 80% mínimo
- **Atual**: Verificar em `htmlcov/index.html`

### Performance
- **Response Time**: < 500ms (95%)
- **Throughput**: > 100 req/s
- **Error Rate**: < 1%

### Disponibilidade
- **Uptime**: > 99.9%
- **Health Checks**: Todos os microsserviços

## Integração com IDEs

### VS Code
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "python.testing.cwd": "${workspaceFolder}"
}
```

### PyCharm
- Configurar pytest como test runner
- Adicionar `tests/` como source root
- Configurar coverage.py para relatórios