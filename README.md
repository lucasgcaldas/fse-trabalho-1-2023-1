[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/OJtG4ZlI)
# Trabalho 1 (2023-1) - Controle de Estacionamentos

Trabalho 1 da disciplina de Fundamentos de Sistemas Embarcados (2023/1)

**Aluno:** Lucas Gomes Caldas

**Matrícula:** 212005426

## Como rodar o projeto

- Necessário ```Python3```
- É necessário escolher algum dos dashboards do estacionamento.
- Em cada servidor distribuido há uma pasta de configuração, em que dependendo do dashboard, as GPIO são diferentes, ou seja, é necessário escolher o JSON de acordo com o dashboard. 
- A referencia é ```estacionamento_x```, em que **x** corresponde ao dashboard escolhido, caso seja o 2, entao o JSON de configuração é estacionamento_2.
- Para entrar na Raspberry Pi: ```ssh <primeiro_nome><ultimo_nome>@<ip> -p 13508``` e a senha é a ```<matricula>```
- Sugestão de configuração de ambiente:
    - ```$ python3 -m venv venv```
    - ```$ source venv/bin/activate```
    - ```$ pip install -r requirements.txt```

### Servidor central

- ```$ cd servidor_central```
- ```$ python3 main.py```

### Servidor distribuido 1

- ```$ cd servidor_distribuido_p1```
- ```$ python3 main.py estacionamento_x```

### Servidor distribuido 2

- ```$ cd servidor_distribuido_p2```
- ```$ python3 main.py estacionamento_x```

## Vídeo de entrega

[<img src="https://i.ytimg.com/vi/BXVQolGnPwM/maxresdefault.jpg">](https://www.youtube.com/watch?v=BXVQolGnPwM "FSE - Controle de Estacionamentos")