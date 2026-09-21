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
### Rotas para manipulação de dados de clientes
/building/clients

    /register
    /update/{client_id}
    /list-all

### Rotas para manipulação de dados de membros de clientes
/building/clients/members

    /register
    /update/{member_id}
