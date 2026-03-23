# TASK-03: Módulo Serviço de IA (LLM via Subprocesso)

## Branch
`feature/ai-service`

## Módulos a Criar
- `src/ai_service.py`
- `src/prompt_builder.py`

## Escopo Técnico

### 1. `src/ai_service.py` — Chamada à LLM
Responsável por enviar o prompt montado para o `kiro-cli` via subprocesso
e capturar a resposta.

- Função principal:

```python
def call_llm(prompt: str) -> str:
    """Envia um prompt para a LLM via kiro-cli e retorna a resposta.

    Args:
        prompt: String completa do prompt a ser enviado.

    Returns:
        String com a resposta da LLM (stdout).

    Raises:
        RuntimeError: Se o subprocesso falhar (returncode != 0).
    """
```

### Regras de Implementação
- Usar `subprocess.run(["kiro-cli", "chat", "--message", prompt], capture_output=True, text=True)`.
- Verificar `returncode`. Se != 0, levantar `RuntimeError` com o stderr.
- Retornar `stdout.strip()`.
- **Mock obrigatório para desbloquear a equipe:** Criar uma constante
  `MOCK_RESPONSE: str` no módulo com um Markdown de exemplo completo
  seguindo o template fixo (seções Bugs, Vulnerabilidades, Code Smells,
  Hotspots, Código Refatorado com tags `[START]`/`[END]`).
  Expor uma flag ou variável de ambiente `KIROSONAR_MOCK=1` que, quando
  ativa, retorna o mock em vez de chamar o subprocesso real.

### 2. `src/prompt_builder.py` — Montagem do Prompt
Responsável por montar o prompt completo que será enviado à LLM,
combinando as regras da empresa + o código do arquivo.

```python
def build_prompt(code: str, rules: str, file_path: str) -> str:
    """Monta o prompt completo para envio à LLM.

    Args:
        code: Conteúdo do arquivo a ser analisado.
        rules: String com as regras da empresa.
        file_path: Nome/caminho do arquivo (para contexto no prompt).

    Returns:
        String do prompt formatado, instruindo a LLM a retornar
        o relatório no template fixo com as 5 seções e as tags
        [START]/[END] para o código refatorado.
    """
```

### Template que o Prompt deve FORÇAR na resposta da LLM:
```
## Bugs
(lista de bugs encontrados)

## Vulnerabilidades
(lista de vulnerabilidades)

## Code Smells
(lista de code smells)

## Hotspots de Segurança
(lista de hotspots)

## Código Refatorado
[START]
(código refatorado completo do arquivo)
[END]
```

## Contratos que este módulo EXPÕE
| Função | Input | Output |
|---|---|---|
| `call_llm(prompt)` | `str` | `str` (Markdown da LLM) |
| `build_prompt(code, rules, file_path)` | `str, str, str` | `str` (prompt montado) |

## Contratos que este módulo CONSOME
Nenhum diretamente. Recebe dados prontos do orquestrador (CLI).

## Critérios de Aceite (Definition of Done)
- [ ] `call_llm()` com `KIROSONAR_MOCK=1` retorna o Markdown mock completo.
- [ ] `call_llm()` sem mock chama `kiro-cli` e retorna stdout.
- [ ] `call_llm()` levanta `RuntimeError` se o subprocesso falhar.
- [ ] `build_prompt()` retorna um prompt que contém o código, as regras e
      as instruções do template fixo com as 5 seções.
- [ ] O mock `MOCK_RESPONSE` contém todas as 5 seções e as tags `[START]`/`[END]`.
- [ ] Código segue PEP 8, tem type hints e docstrings em todas as funções.
