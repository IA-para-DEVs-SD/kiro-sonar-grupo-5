# TASK-02: Módulo Git Diff

## Branch
`feature/git-diff`

## Módulos a Criar
- `src/git_module.py`

## Escopo Técnico

### `src/git_module.py` — Descoberta de Arquivos Alterados
Responsável por interagir com o Git via `subprocess` para descobrir quais
arquivos foram alterados no working tree.

- Função principal:

```python
def get_changed_files() -> list[str]:
    """Executa 'git diff --name-only' e retorna a lista de arquivos alterados.

    Returns:
        Lista de caminhos relativos dos arquivos modificados.
        Retorna lista vazia se não houver alterações.

    Raises:
        SystemExit: Se o diretório atual não for um repositório Git.
    """
```

- Função auxiliar para ler o conteúdo de um arquivo descoberto:

```python
def read_file_content(file_path: str) -> str:
    """Lê e retorna o conteúdo completo de um arquivo.

    Args:
        file_path: Caminho relativo ou absoluto do arquivo.

    Returns:
        Conteúdo do arquivo como string.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
```

### Regras de Implementação
- Usar `subprocess.run(["git", "diff", "--name-only"], ...)` com
  `capture_output=True` e `text=True`.
- Verificar `returncode != 0` para detectar se não é um repo Git.
  Nesse caso, imprimir mensagem amigável e `sys.exit(1)`.
- Filtrar linhas vazias do output do `git diff`.
- Tratar o caso de nenhum arquivo alterado: retornar lista vazia e
  permitir que o chamador (CLI) exiba mensagem "Nenhum arquivo alterado".

## Contratos que este módulo EXPÕE
| Função | Input | Output |
|---|---|---|
| `get_changed_files()` | `None` | `list[str]` (paths relativos) |
| `read_file_content(file_path)` | `str` | `str` (conteúdo do arquivo) |

## Contratos que este módulo CONSOME
Nenhum. Este módulo é independente (camada de infraestrutura).

## Critérios de Aceite (Definition of Done)
- [ ] Dentro de um repo Git com arquivos modificados, `get_changed_files()`
      retorna a lista correta de paths.
- [ ] Dentro de um repo Git sem alterações, retorna `[]`.
- [ ] Fora de um repo Git, exibe mensagem de erro e sai com código 1.
- [ ] `read_file_content()` lê corretamente um arquivo existente.
- [ ] `read_file_content()` levanta `FileNotFoundError` para arquivo inexistente.
- [ ] Código segue PEP 8, tem type hints e docstrings em todas as funções.
