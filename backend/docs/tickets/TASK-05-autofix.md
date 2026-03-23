# TASK-05: Módulo Auto-Fix (Parser + Aplicação)

## Branch
`feature/autofix`

## Módulos a Criar
- `src/autofix.py`

## Escopo Técnico

### `src/autofix.py` — Extração e Aplicação do Código Refatorado
Responsável por parsear a resposta da LLM, extrair o código entre as tags
`[START]` e `[END]`, e sobrescrever o arquivo original após confirmação
explícita do usuário.

- Função de extração:

```python
def extract_refactored_code(ai_response: str) -> str | None:
    """Extrai o código refatorado da resposta da LLM.

    Busca o conteúdo entre as tags [START] e [END] usando Regex.

    Args:
        ai_response: String Markdown completa retornada pela LLM.

    Returns:
        String com o código refatorado, ou None se as tags não forem
        encontradas.
    """
```

- Função de aplicação:

```python
def apply_fix(ai_response: str, file_path: str) -> bool:
    """Aplica o código refatorado ao arquivo original.

    Extrai o código via extract_refactored_code(), exibe um preview
    no terminal, pergunta ao usuário 'Deseja aplicar o fix? (s/n)',
    e sobrescreve o arquivo se confirmado.

    Args:
        ai_response: String Markdown completa retornada pela LLM.
        file_path: Caminho do arquivo original a ser sobrescrito.

    Returns:
        True se o fix foi aplicado, False se o usuário recusou
        ou se não havia código refatorado.
    """
```

### Regras de Implementação
- Regex para extração: `r'\[START\]\s*\n(.*?)\n\s*\[END\]'` com flag
  `re.DOTALL` para capturar múltiplas linhas.
- Antes de sobrescrever, exibir no terminal:
  - O caminho do arquivo que será alterado.
  - Um preview das primeiras 20 linhas do código refatorado.
  - O prompt interativo: `Deseja aplicar o fix em '<file_path>'? (s/n): `
- Só sobrescrever se o input for `s` ou `S`.
- Usar encoding `utf-8` na escrita.

## Contratos que este módulo EXPÕE
| Função | Input | Output |
|---|---|---|
| `extract_refactored_code(ai_response)` | `str` | `str \| None` |
| `apply_fix(ai_response, file_path)` | `str, str` | `bool` |

## Contratos que este módulo CONSOME
Nenhum. Recebe dados prontos do orquestrador (CLI).

## Mock para Desenvolvimento Independente
Usar a mesma string `MOCK_CONTENT` da TASK-04 como input para testar
a extração e aplicação:

```python
MOCK_AI_RESPONSE = """## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Variável 'x' com nome não descritivo (linha 10).

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
def calcular_total(valor: float) -> float:
    return valor * 1.1
[END]
"""
```

## Critérios de Aceite (Definition of Done)
- [ ] `extract_refactored_code()` extrai corretamente o código entre `[START]` e `[END]`.
- [ ] `extract_refactored_code()` retorna `None` se as tags não existirem.
- [ ] `apply_fix()` exibe preview e prompt interativo antes de sobrescrever.
- [ ] `apply_fix()` sobrescreve o arquivo apenas se o usuário digitar `s`/`S`.
- [ ] `apply_fix()` retorna `False` se o usuário recusar ou não houver código.
- [ ] `apply_fix()` retorna `True` após aplicar o fix com sucesso.
- [ ] Funciona com o `MOCK_AI_RESPONSE` sem depender de nenhum outro módulo.
- [ ] Código segue PEP 8, tem type hints e docstrings em todas as funções.
