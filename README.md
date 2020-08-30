# Teste Confitec - Desenvolvedor Pyyhon

## Introdução
Projeto Desafio Noverde foi desenvolvido em Python (Flask, DynamoDB e Redis. O projeto foi concluído conforme todas as expecificações determinadas em https://github.com/noverde/challenge. Desenvolvido por Gabriel Marcolino Rampazo.

## Instalação
Para que esse projeto execute é necessário instalar:

* Python (3.8.3) 
* Redis Server

Linux (Ubuntu):
```
 sudo apt install redis-server
```

Após a instalação do Python, instale os componentes que já estão no arquivo requirements.txt na pasta raiz do projeto.

```
 pip install -r requirements.txt
```

Dica: é interessante fazer um *virtual environment* com o Python 3.8.3, assim pode-se instalar todos os componentes Python sem ocasionar problemas com os demais instalados.
## Configuração

Para configurar o banco de dados DynamoDB coloque os parametros da AWS em `config.py`.

## Execução
Para o processo de execução há dois processos que precisam ser executados:

* Criação do DB no DynamoDB (Na pasta raiz do projeto):

```
 python create_table.py
```

* Rodando a Aplicaćão em Flask (Na pasta raiz do projeto):

```
 python app.py
```

Rodando este processo já é possível fazer as requisições GET, para isso use o endereço `http://127.0.0.1:5000/artist/<nome_do_artista>`. 

## Como Funciona

Tudo se inicia por uma requisição do tipo GET feita no endereço `http://127.0.0.1:5000/artist/<nome_do_artista>`.

Caso seja enviado `cache=False` como parametro do GET, é a opção de escolha que não utiliza o recurso em cache.

O retorno será em com as 10 músicas mais famosas do artista pesquisado.