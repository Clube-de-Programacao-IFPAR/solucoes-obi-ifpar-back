# Como executar o sandbox em Docker

Use este passo a passo quando quiser testar a execução das submissões dentro do container.

## 1. Abrir o Docker Desktop

Antes de rodar qualquer comando, abra o Docker Desktop no Windows e espere ele ficar com o estado `Running`.

## 2. Estar na raiz do projeto

Abra um terminal no diretório raiz do repositório:

```powershell
cd ./solucoes-obi-ifpar-back
```

## 3. Construir a imagem do sandbox

Essa imagem é a que o backend usa para compilar e executar as submissões dentro do Docker:

```powershell
docker build -t obi-judge-runner -f docker/Dockerfile .
```
(isso pode demorar um pouco)

Se quiser conferir se a imagem foi criada:

```powershell
docker images obi-judge-runner
```

## 4. Ativar o uso do Docker no backend

Defina as variáveis de ambiente para usar o sandbox em Docker:

(./.env)
```text
USE_DOCKER_SANDBOX = "true"
```

Se o projeto ainda não tiver dependências instaladas, faça isso antes de subir a aplicação:

```powershell
pip install -r requirements.txt
```

## 5. Iniciar o backend

Com a imagem pronta e as variáveis definidas, inicie a API Flask:

```powershell
flask --app app.py run --debug
```

## 6. Testar a funcionalidade

Com o backend rodando, envie uma submissão normalmente pela API. Quando `USE_DOCKER_SANDBOX=true`, a execução vai acontecer dentro do container criado em `obi-judge-runner`.

## 7. Limpar a imagem quando quiser

Se precisar remover a imagem criada localmente:

```powershell
docker rmi obi-judge-runner
```
