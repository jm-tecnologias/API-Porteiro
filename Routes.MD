# Rotas da API
As rotas aqui apresentadas serão divididas em categorias

## Rotas de autenticação
### Rotas de cliente
building/auth/user/client

      /login
      /dashboard/get/{token}

### Rotas de Staff
building/auth/user/employee

    /login
    /update/{client_id}

## Rotas de CRUD
### Rotas para manupulação de dados de clientes
/building/clients

    /register
    /update/{client_id}
    /list-all
