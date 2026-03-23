# TASK-04: Módulo de Geração de Relatório

## Branch
`feature/report`

## Módulos a Criar
- `src/report.py`

## Escopo Técnico

### `src/report.py` — Salvamento do Relatório em Markdown
Responsável por receber a resposta da LLM e persistir como arquivo `.md`
na pasta `relatorios/` do projeto analisado.

- Função principal:

```python
def save_report(content: str, file_path: str) -> str:
    """Salva o relatório da análise em um arquivo Markdown.

    Args:
        content: String Markdown retornada pela LLM.
        file_path: Caminho do arquivo original analisado (usado para
                   gerar o nome do relatório).

    Returns:
        Caminho absoluto do arquivo de relatório salvo.
    """
```

- Função auxiliar para gerar o nome do relatório:

```python
def generate_report_name(file_path: str) -> str:
    """Gera o nome do arquivo de relatório baseado no arquivo analisado.

    Args:
        file_path: Caminho do arquivo original (ex: 'src/app.py').

    Returns:
        Nome do relatório (ex: 'relatorios/src_app_py_20260318_173000.md').
    """
```

### Regras de Implementação
- Criar a pasta `relatorios/` automaticamente se não existir (`os.makedirs`).
- O nome do relatório deve conter o nome do arquivo analisado (com `/`
  substituído por `_`) + timestamp (`YYYYMMDD_HHMMSS`) para evitar colisões.
- Usar encoding `utf-8` na escrita.
- Imprimir no terminal o caminho do relatório salvo para feedback ao usuário.

## Contratos que este módulo EXPÕE
| Função | Input | Output |
|---|---|---|
| `save_report(content, file_path)` | `str, str` | `str` (caminho do relatório salvo) |
| `generate_report_name(file_path)` | `str` | `str` (nome do arquivo .md) |

## Contratos que este módulo CONSOME
Nenhum. Recebe dados prontos do orquestrador (CLI).

## Mock para Desenvolvimento Independente
Para testar sem depender da LLM, usar uma string Markdown fixa como input:

```python
MOCK_CONTENT = """## Bugs
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
- [ ] `save_report()` cria a pasta `relatorios/` se não existir.
- [ ] `save_report()` salva o arquivo `.md` com encoding UTF-8.
- [ ] O nome do relatório contém o nome do arquivo analisado e um timestamp.
- [ ] `save_report()` retorna o caminho absoluto do arquivo salvo.
- [ ] Relatórios de arquivos diferentes não colidem (nomes únicos).
- [ ] Funciona com o `MOCK_CONTENT` sem depender de nenhum outro módulo.
- [ ] Código segue PEP 8, tem type hints e docstrings em todas as funções.
