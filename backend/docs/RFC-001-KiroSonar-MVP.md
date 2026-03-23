# RFC 001: Arquitetura KiroSonar MVPd
**Status:** Em rascunho (Draft)
**Data:** [Data de Hoje]

## 1. O Problema
Atualmente, a esteira padrão de análise de código (como o SonarQube) é passiva e gera alta fricção. O desenvolvedor comete um erro de arquitetura, a ferramenta aponta a falha em um dashboard externo, e o desenvolvedor gasta horas mudando de contexto para entender e reescrever o código manualmente.

## 2. A Solução Proposta (KiroSonar)
Criar uma CLI em Python ("KiroSonar") que integre análise estática baseada em IA e refatoração automática (Auto-Fix) diretamente no terminal do desenvolvedor. A ferramenta deve operar idealmente lendo o `git diff` para aplicar a análise apenas nos arquivos alterados ("Clean as You Code").

## 3. Arquitetura e Fluxo (High Level)
1. **Input:** O usuário executa `kirosonar analyze`.
2. **Descoberta:** O módulo de Git executa `git diff --name-only` e lista os arquivos alterados.
3. **Análise (LLM):** Para cada arquivo, O código é encapsulado com as regras da empresa (injetadas a partir de um arquivo externo configurável de regras, ex: regras_empresa.md) e enviado para a IA.
4. **Output (Relatório):** A IA retorna um relatório nos moldes do SonarQube (Bugs, Smells, Hotspots), que é salvo em `.md` na pasta `/relatorios`.
5. **Auto-Fix:** A CLI extrai o código refatorado da resposta da IA e pergunta no terminal: "Deseja aplicar o fix? (s/n)". Se sim, sobrescreve o arquivo original.

# Stack Tecnológica e Padrões
- Linguagem: Python 3.11+ (Implementar mecanismo de "Fail Fast" verificando a versão no início da execução).
- Distribuição e Execução: A ferramenta deve operar como um executável de sistema. O desenvolvedor deve conseguir rodar `kirosonar analyze` sem o prefixo `python`. Para isso, utilize empacotamento nativo via `pyproject.toml` (usando `console_scripts`).
- Bibliotecas Principais: Apenas bibliotecas nativas (Standard Library) para o core da aplicação (`argparse`, `subprocess`, `os`, `re`, `sys`). Evite dependências externas para a ferramenta em si, mantendo-a leve.
- Padrões de Código: 
  - Siga a PEP 8 estritamente.
  - Uso obrigatório de Type Hinting.
  - Uso de Docstrings em módulos e funções explicando parâmetros e retornos.
  - Princípios SOLID e Clean Architecture.

## 5. Fora do Escopo (O que NÃO Faremos Agora)
- Integração com CI/CD na nuvem (GitHub Actions/GitLab CI).
- Dashboard Web.
- Análise de repositórios inteiros sem uso de `git diff` ou indicação de arquivo específico.

## 6. Riscos e Mitigações
- **Custo/Tokens:** Mitigado pelo uso exclusivo do `git diff` (analisa poucas linhas/arquivos).
- **Alucinação da IA:** Mitigado por prompts estritos e aprovação humana explícita `(y/n)` antes de aplicar o Auto-Fix.