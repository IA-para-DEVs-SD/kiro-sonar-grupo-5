# Documento de Requisitos

## Introdução

Este documento descreve os requisitos do módulo de serviço de IA do KiroSonar (TASK-03).
O módulo é composto por dois arquivos: `ai_service.py`, responsável por enviar prompts à LLM
via subprocesso `kiro-cli`, e `prompt_builder.py`, responsável por montar o prompt estruturado
que será enviado à LLM. Ambos os módulos já estão implementados e este spec documenta o
comportamento existente.

## Glossário

- **AI_Service**: Módulo `src/ai_service.py` — responsável por invocar a LLM via subprocesso.
- **Prompt_Builder**: Módulo `src/prompt_builder.py` — responsável por montar o prompt completo.
- **LLM**: Modelo de linguagem grande acessado via `kiro-cli`.
- **MOCK_RESPONSE**: Constante string definida em `ai_service.py` com um relatório Markdown de exemplo.
- **kiro-cli**: Ferramenta de linha de comando que serve como interface com a LLM.
- **Template_Fixo**: Estrutura de resposta com 5 seções obrigatórias que a LLM deve seguir.

## Requisitos

### Requisito 1: Chamada à LLM via subprocesso

**User Story:** Como desenvolvedor, quero que o sistema envie prompts à LLM via `kiro-cli`,
para que a análise de código seja executada sem dependências externas além da Standard Library.

#### Critérios de Aceite

1. WHEN um prompt é fornecido e `KIROSONAR_MOCK` não está definido como `"1"`, THE AI_Service SHALL invocar `kiro-cli chat --message <prompt>` via `subprocess.run` com `capture_output=True` e `text=True`.
2. WHEN o subprocesso `kiro-cli` retorna `returncode` igual a `0`, THE AI_Service SHALL retornar o conteúdo de `stdout` com espaços em branco removidos das extremidades.
3. IF o subprocesso `kiro-cli` retorna `returncode` diferente de `0`, THEN THE AI_Service SHALL levantar `RuntimeError` contendo o conteúdo de `stderr`.
4. WHEN a variável de ambiente `KIROSONAR_MOCK` está definida como `"1"`, THE AI_Service SHALL retornar `MOCK_RESPONSE` sem invocar o subprocesso.

### Requisito 2: Resposta mock para testes offline

**User Story:** Como desenvolvedor, quero uma resposta mock completa disponível via variável de ambiente,
para que os testes possam ser executados sem acesso à LLM real.

#### Critérios de Aceite

1. THE AI_Service SHALL definir a constante `MOCK_RESPONSE` do tipo `str` contendo um relatório Markdown com as seções: `## Bugs`, `## Vulnerabilidades`, `## Code Smells`, `## Hotspots de Segurança` e `## Código Refatorado`.
2. THE AI_Service SHALL incluir em `MOCK_RESPONSE` um bloco de código refatorado delimitado pelas tags `[START]` e `[END]`.
3. WHILE `KIROSONAR_MOCK` está definido como `"1"`, THE AI_Service SHALL retornar `MOCK_RESPONSE` em todas as chamadas a `call_llm`, independentemente do prompt recebido.

### Requisito 3: Montagem do prompt estruturado

**User Story:** Como desenvolvedor, quero que o prompt enviado à LLM contenha o código, as regras
da empresa e o template de resposta esperado, para que a LLM produza relatórios no formato correto.

#### Critérios de Aceite

1. WHEN `build_prompt` é chamado com `code`, `rules` e `file_path`, THE Prompt_Builder SHALL retornar uma string contendo o conteúdo de `code`.
2. WHEN `build_prompt` é chamado com `code`, `rules` e `file_path`, THE Prompt_Builder SHALL retornar uma string contendo o conteúdo de `rules`.
3. WHEN `build_prompt` é chamado com `code`, `rules` e `file_path`, THE Prompt_Builder SHALL retornar uma string contendo o Template_Fixo com as 5 seções: `## Bugs`, `## Vulnerabilidades`, `## Code Smells`, `## Hotspots de Segurança` e `## Código Refatorado`.
4. WHEN `build_prompt` é chamado com `code`, `rules` e `file_path`, THE Prompt_Builder SHALL incluir no prompt as tags `[START]` e `[END]` para delimitar o bloco de código refatorado esperado na resposta.
5. WHEN `build_prompt` é chamado com `code`, `rules` e `file_path`, THE Prompt_Builder SHALL incluir `file_path` no prompt para fornecer contexto à LLM sobre o arquivo sendo analisado.

### Requisito 4: Conformidade com padrões de código

**User Story:** Como tech lead, quero que todos os módulos sigam os padrões definidos no PRD,
para que o código seja legível, tipado e documentado de forma consistente.

#### Critérios de Aceite

1. THE AI_Service SHALL implementar a função `call_llm` com type hint `prompt: str` no parâmetro e `-> str` no retorno.
2. THE Prompt_Builder SHALL implementar a função `build_prompt` com type hints `code: str`, `rules: str`, `file_path: str` nos parâmetros e `-> str` no retorno.
3. THE AI_Service SHALL conter docstring na função `call_llm` documentando `Args`, `Returns` e `Raises`.
4. THE Prompt_Builder SHALL conter docstring na função `build_prompt` documentando `Args` e `Returns`.
5. THE AI_Service SHALL utilizar apenas módulos da Standard Library do Python (`os`, `subprocess`).
