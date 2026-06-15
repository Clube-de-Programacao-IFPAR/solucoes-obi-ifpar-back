# 💡 Soluções OBI IFPAR - Backend

Projeto desenvolvido pelo **Clube de Programação do IFPAR** (Instituto Federal do Rio Grande do Norte — Campus Parnamirim).

O objetivo do projeto é criar uma plataforma web onde estudantes possam **resolver e testar automaticamente questões da Olimpíada Brasileira de Informática (OBI)**.

A ideia surgiu a partir da necessidade de uma ferramenta que permita aos alunos praticar problemas da OBI e naveguem pela plataforma com facilidade.

Este é o **primeiro projeto oficial do clube**.

## 📍 Objetivo

Criar uma plataforma que permita aos estudantes:

- acessar problemas da OBI
- navegar entre listas, enunciados e páginas de apoio
- enviar códigos como solução
- testar automaticamente as respostas
- visualizar informações de forma clara e organizada
- receber feedback sobre a execução
- utilizar a plataforma como ferramenta de estudo para olimpíadas de programação

Além disso, o projeto também funciona como **um ambiente de aprendizado colaborativo**, permitindo que estudantes participem do desenvolvimento de uma aplicação real.

## 💡 Sobre a OBI

A [**Olimpíada Brasileira de Informática (OBI)**](https://olimpiada.ic.unicamp.br/) é uma competição nacional que busca estimular o estudo de algoritmos, lógica e programação entre estudantes brasileiros.

As provas são compostas por desafios que exigem a implementação de **algoritmos eficientes para resolver problemas computacionais**.

Este projeto busca facilitar o treinamento para a OBI reunindo diversos problemas em uma única plataforma.

## 📚 Tecnologias utilizadas

O projeto utiliza tecnologias modernas de desenvolvimento web.

### Backend

- Python
- Flask

### Ferramentas

- Git
- Git Flow
- GitHub

### Documentação

- Sphinx

## 🔧 Como rodar o backend do projeto

Siga os passos abaixo para executar o projeto localmente.

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/Clube-de-Programacao-IFPAR/solucoes-obi-ifpar-back.git
cd solucoes-obi-ifpar-back
```

### 2️⃣ Rodar o projeto

Copie o .env e coloque as credenciais
```bash
cp .env.example .env
```

Instale as dependências do Python:
```bash
pip install -r requirements.txt
```

Atualize os dados das questões:
```bash
python scripts/get_urls.py
```

Baixe os gabaritos de todas as questões (opcional):
```bash
python scripts/download_answers.py
```
Ou baixe e extraia cada gabarito manualmente para a pasta ```questions/answers/<nome_do_zip>```.

Inicie o servidor Flask:
```bash
flask --app app.py run
```

O backend estará disponível em:
```
http://127.0.0.1:5000
```

## Documentação

Você pode acessar a documentação oficial compilando ela com os dados do proprio projeto.

### Compilar a documentação
1. Baixe as dependências do Sphinx em `docs/requirements.txt` e as dependências do projeto em `requirements.txt` com o `pip`:
``` console
   $ pip install -r docs/requirements.txt -r requirements.txt
```

2. Rode o comando ``rm -r docs/build/html && sphinx-build docs/source/ docs/build/html``:
``` console
   $ rm -r docs/build/html && sphinx-build docs/source/ docs/build/html
```

3. A documentação estara disponível em `docs/build/html/`, use seu navegador preferido para acessar o arquivo `docs/build/html/index.html`.

## 👥 Contribuição

Este é um projeto **aberto aos estudantes do Clube de Programação do IFPAR**.

Os participantes podem contribuir de diversas formas:

- desenvolvimento frontend
- desenvolvimento backend
- design de interface
- testes
- revisão de código
- organização do projeto

Mesmo quem ainda está aprendendo pode participar acompanhando o desenvolvimento e contribuindo gradualmente.

### 👨‍💻 Participantes

- [Alanderson Lima](https://github.com/Alanderson-LS) — Estudante Aprendiz
- [Brasilicio Henrique](https://github.com/brasilicioh) — Coordenador e Dev Fullstack
- [Bruno Gustavo](https://github.com/brunoficial) — Dev Backend
- [Cauã de Lima](https://github.com/CauaLima18) — Dev Backend
- [Douglas Ryan](https://github.com/Douglas-Mesquita) — Estudante Aprendiz
- [Emanuele Rafaela](https://github.com/ManulSilva) — Estudante Aprendiz
- [Gabriel Nascimento](https://github.com/GGGabriell) — Estudante Aprendiz
- [Guilherme Aleixo](https://github.com/G-aleixo) — Dev Backend
- [Gustavo Andrey](https://github.com/GustavoAndreyIF) — Dev Frontend
- [Júlio César](https://github.com/JCOAlves) — Dev Fullstack
- [Kaio Henrique](https://github.com/pc123456789n) — Dev Frontend
- [Leonardo Kauffman](https://github.com/Leonardo1234321) — Dev Backend
- [Rita de Cássia](https://github.com/Ritinha-tari) — Estudante Aprendiz
- [Thiago Freitas](https://github.com/thifre09) — Dev Frontend

## ⚙️ Status do projeto

MVP finalizado. Primeira versão entregue. Aos poucos são desenvolvidas mais recursos.

Este repositório contém o código da aplicação do backend que está sendo construída colaborativamente pelos membros do clube.
