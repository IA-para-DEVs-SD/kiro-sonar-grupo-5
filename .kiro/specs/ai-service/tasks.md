# Plano de Implementação

## Tarefas

- [x] 1. Criar módulo `src/ai_service.py`
  - [x] 1.1 Definir constante `MOCK_RESPONSE: str` com Markdown completo contendo as 5 seções e as tags `[START]`/`[END]`
  - [x] 1.2 Implementar função `call_llm(prompt: str) -> str` com verificação de `KIROSONAR_MOCK`
  - [x] 1.3 Implementar chamada via `subprocess.run` com `capture_output=True` e `text=True`
  - [x] 1.4 Implementar verificação de `returncode` e levantamento de `RuntimeError` com `stderr`
  - [x] 1.5 Adicionar type hints e docstring com `Args`, `Returns` e `Raises`

- [x] 2. Criar módulo `src/prompt_builder.py`
  - [x] 2.1 Implementar função `build_prompt(code: str, rules: str, file_path: str) -> str`
  - [x] 2.2 Incluir no prompt as regras da empresa, o código do arquivo e o `file_path`
  - [x] 2.3 Incluir no prompt o Template_Fixo com as 5 seções e as tags `[START]`/`[END]`
  - [x] 2.4 Adicionar type hints e docstring com `Args` e `Returns`
