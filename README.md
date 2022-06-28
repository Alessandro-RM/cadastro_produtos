# Cadastro de produtos

Sistema que é  utilizado para criar uma lista de produtos que salva tudo juntamente no banco de dados. Nesse caso, foi utilizado o MySQL !! 

<img src="./prints/001.png">

Na aba lista de produtos, é possível excluir, gerar um PDF e editar o produto juntamente ao banco de dados !!

<img src="./prints/002.png">

<img src="./prints/003.png">


## need to run 

- docker
- python 3.9.2

## How to Run

Install libs

```bash
  pip install -r requirements.txt
```


Run Docker
```bash
  docker-compose up -d
```

Run Project
```bash
  python3 controle.py
  OR
  python controle.py
```