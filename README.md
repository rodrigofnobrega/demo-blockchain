## Descrição

A API precisará implementa 6 *end-points*:

- **[POST]** `/transactions/create` para criar uma nova transação a ser incluída no próximo bloco. No corpo da requisicão HTTP, usando POST, inclua as informações necessárias para criação de uma nova transação.
- **[GET]** `/transactions/mempool` para retornar a *memory pool* do nó.
- **[GET]** `/mine` para informar o nó para criar e minerar um novo bloco. Ou seja, um nó que for requisitado a partir desse end-point deve pegar todas as transações incluídas em seu memory pool, montar um bloco e minera-lo.
- **[GET]** `/chain` para retornar o blockchain completo daquele nó.
- **[POST]** `/nodes/register` para aceitar uma lista de novos nós no formato de URLs. Note que já existe uma variável do tipo conjunto (*set*) chamado `nodes` para armazenar os nós registrados.
- **[GET]** `/nodes/resolve` para executar o modelo de consenso, resolvendo conflitos e garantindo que contém a cadeia de blocos correta. Basicamente o que deve ser feito pelo nó é solicitar a todos os seus nós registrados os seus respectivos blockchains. Então deve-se conferir se o blockchain é válido, e, se for maior (mais longo) que o atual, deve substitui-lo.


## Teste

Para testar, será necessário executar no mínimo dois nós simultaneamente, e no caso de ser na mesma máquina, as instâncias em execução devem usar portas diferentes (por exemplo, porta 5000 e 5001). Você pode testar no seu navegador, usando _curl_, ou então usando o [Postman](https://www.postman.com/) ou [Insomnia](https://insomnia.rest/).

## Roteiro da apresentação

Para a apresentação, já se organize para realizar os seguintes passos:

```
[  ] Sobe um primeiro nó (ex: porta 5001)
[  ] Sobe um segundo nó (ex: porta 5002)
[  ] Cria uma nova transação (tx) no nó #1
[  ] Confere o mempool do nó #1
[  ] Cria e minera um novo bloco no nó #1
[  ] Cria e minera outro bloco (sem transações) no nó #1
[  ] Confere a atual chain do nó #1
[  ] Registra o nó #2 no nó #1
[  ] Resolve (consenso) o nó #1 (o blockchain não deve mudar)
[  ] Cria e minera um único bloco (sem transações) no nó #2
[  ] Confere a atual chain do nó #2
[  ] Registra o nó #1 no nó #2
[  ] Resolve (consenso) o nó #2 (o blockchain deve mudar para a chain do nó #1)
[  ] Confere a atual chain do nó #2
```


## Licença
[MIT](https://choosealicense.com/licenses/mit/)
