# Collections Postman - CoworkFlow

Collections para testar todos os microsserviços do sistema CoworkFlow.

## Como Usar

1. **Importar no Postman:**
   - Abra o Postman
   - Clique em "Import"
   - Selecione os arquivos `.json` desta pasta

2. **Configurar Variáveis:**
   - Cada collection tem suas próprias variáveis
   - Para API Gateway, configure o `token` após fazer login

## Collections Disponíveis

### Microsserviços Individuais
- `MS-Usuarios.postman_collection.json` - Porta 5001
- `MS-Espacos.postman_collection.json` - Porta 5002  
- `MS-Reservas.postman_collection.json` - Porta 5003
- `MS-Pagamentos.postman_collection.json` - Porta 5004
- `MS-Precos.postman_collection.json` - Porta 5005
- `MS-Checkin.postman_collection.json` - Porta 5006
- `MS-Notificacoes.postman_collection.json` - Porta 5007
- `MS-Financeiro.postman_collection.json` - Porta 5008
- `MS-Analytics.postman_collection.json` - Porta 5009

### API Gateway
- `API-Gateway.postman_collection.json` - Porta 8000 (Recomendado)

## Fluxo de Teste Recomendado

1. **Cadastro e Login** (via API Gateway)
2. **Criar Espaços**
3. **Calcular Preços**
4. **Criar Reservas**
5. **Processar Pagamentos**
6. **Fazer Check-in/Check-out**
7. **Enviar Notificações**
8. **Consultar Analytics e Financeiro**

## Variáveis Importantes

- `{{gateway_url}}` = http://localhost:8000
- `{{token}}` = JWT obtido no login
- `{{base_url}}` = URL específica de cada microsserviço

## Exemplos de Dados

### Usuário de Teste
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123",
  "name": "João Silva"
}
```

### Espaço de Teste
```json
{
  "name": "Sala de Reunião A",
  "description": "Sala equipada com projetor",
  "capacity": 8,
  "price_per_hour": 25.0
}
```

### Reserva de Teste
```json
{
  "user_id": 1,
  "space_id": 1,
  "start_time": "2024-01-15T09:00:00",
  "end_time": "2024-01-15T11:00:00",
  "total_price": 50.0
}
```