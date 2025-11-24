# Lab API 

Bem-vindo! Este README foi reescrito de forma curta, clara e criativa para explicar o projeto e, em especial, o propósito dos testes automatizados.

### O que é este projeto?

Uma pequena API em Flask usada como laboratório para práticas de DevOps: conteiners com Docker, pipeline CI/CD, deploy em Render e testes automatizados. O código principal está em `app.py` e os testes na pasta `testes/`.

### Principais funcionalidades

- Endpoints básicos: `/`, `/login`, `/protected` (exemplo de rota protegida).
- Documentação Swagger em `static/swagger.json`.
- Dockerfile e `docker-compose.yml` para facilitar execução local e deploy.

## Testes — para que servem (explicação simples)

Testes automatizados servem para garantir que mudanças no código não quebrem o comportamento esperado. Eles funcionam como uma rede de segurança:

- Detectam regressões quando alteramos rotas ou lógica de autenticação.
- Permitem que a pipeline CI falhe rapidamente se algo estiver quebrado, evitando deploys com bugs.
- Documentam (indiretamente) o comportamento esperado das rotas.

No projeto há testes usando `unittest` em `testes/test_app.py`. Em termos simples, estes testes verificam:

- Que `/login` retorna um JSON com a chave `access_token` (uma string não vazia).
- Que `/protected` devolve HTTP 200 quando acessada com um token válido.
- Que `/protected` devolve HTTP 401 quando acessada sem token.

Esses cenários cobrem autenticação básica e proteção de rota — pontos críticos para a API.

## Como executar o projeto (rápido)

1) (Opcional, recomendado) Crie e ative um virtualenv:

```bash
python3 -m venv venv
source venv/bin/activate
```

2) Instale dependências:

```bash
pip install -r requirements.txt
```

3) Rode a API localmente:

```bash
python app.py
# Acesse: http://127.0.0.1:1313/ (dependendo da porta configurada)
```

## Como rodar os testes (passo a passo)

Execute a suíte de testes com o comando abaixo (ele procura por testes na pasta `testes`):

```bash
python -m unittest discover -s testes -v
```

O que esperar:
- Todos os testes devem passar (OK). Caso algum falhe, o output mostrará qual teste e o motivo.

Dica: se usar Docker/Compose, você também pode executar os testes dentro do container conforme sua configuração de `docker-compose.yml`.

## Boas práticas rápidas

- Rode os testes localmente antes de abrir PRs.
- Mantenha os testes pequenos e focados (cada teste valida uma única responsabilidade).
- Ao adicionar uma nova rota, adicione um teste cobrindo o comportamento principal.

## Contribuindo

1. Fork e branch.
2. Execute os testes localmente.
3. Abra um PR com uma descrição clara do que mudou.

---

Se quiser, eu posso também:

- Rodar os testes aqui e reportar o resultado.
- Adicionar badges no topo do README mostrando status do build/testes.
- Escrever testes adicionais (ex.: casos de erro, tokens expirados, etc.).

Diga o que prefere que eu faça a seguir.

# Desafio_DevOps
# Desafio_DevOps
