# skill.md - Padrao de Engenharia do Projeto

Documento oficial de boas praticas. Toda contribuicao (humana ou via IA) deve
seguir estas regras. Este arquivo serve de base para o planejamento e a
implementacao do projeto.

## 1. Gerenciamento de ambiente e pacotes

- Usar **Poetry** para gerenciar dependencias e o ambiente virtual.
- O virtualenv fica dentro do projeto (`virtualenvs.in-project = true`).
- A versao do Python e fixada localmente (`.python-version`).
- **Nunca** usar `pip` diretamente para instalar dependencias do projeto.

## 2. Estrutura e arquitetura

- Layout `src/` (`src/f1/...`).
- Projeto **modular**, dividido por responsabilidade:
  - `ingestion/` - acesso a dados externos (cliente HTTP da OpenF1);
  - `domain/` - modelos (Pydantic), repositorios e servicos (regra de negocio);
  - `processing/` - transformacao e analise dos dados;
  - `utils/` - configuracao, logger e apoio.
- `dashboard.py` apenas orquestra: chama servicos, nao concentra regra de negocio.
- Funcoes pequenas, com responsabilidade unica. Evitar scripts monoliticos.
- Camadas de dominio nao devem depender de detalhes de infraestrutura.

## 3. Estilo de codigo, lint e format

- **ruff** para lint, format e organizacao de imports (inclui isort).
- Seguir a PEP 8.
- Type hints em funcoes publicas.

## 4. Testes

- **pytest** para testes unitarios.
- Cobertura minima de **50%** do projeto.
- A chamada HTTP externa e mockada nos testes (nao bater na API de verdade).

## 5. Documentacao

- **mkdocs-material** para a documentacao.
- Documentacao publicavel via GitHub Pages.

## 6. Seguranca

- Segredos ficam em `.env` (nunca commitado).
- `.gitignore` cobrindo `.env`, caches, coverage e artefatos.
