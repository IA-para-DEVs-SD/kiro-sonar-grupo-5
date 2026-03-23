# TASK-01: CLI Base, Entry Point e Configuração

## Branch
`feature/cli-base`

## Módulos a Criar
- `pyproject.toml` (raiz do projeto)
- `src/__init__.py`
- `src/cli.py`
- `src/config.py`

## Escopo Técnico

### 1. `pyproject.toml`
Configurar o empacotamento nativo com `console_scripts` para que o comando
`kirosonar` fique disponível no terminal após `pip install -e .`.

```toml
[project.scripts]
kirosonar = "src.cli:main"
```

### 2. `src/cli.py` — Entry Point
- Implementar verificação "Fail Fast" da versão do Python (>= 3.11).
  Se a versão for inferior, imprimir mensagem clara e sair com `sys.exit(1)`.
- Usar `argparse` para expor o subcomando `analyze` com as flags:
  - `--path <caminho>` (opcional): caminho de um arquivo específico para análise.
    Se omitido, o fluxo padrão usa `git diff`.
  - `--rules <caminho>` (opcional): caminho para um arquivo de regras customizado.
    Se omitido, busca `regras_empresa.md` na raiz do projeto analisado.
- A função `main()` deve montar um dicionário `args` e chamar as funções dos
  outros módulos **pelos seus contratos**, sem implementar lógica de negócio.

### 3. `src/config.py` — Carregamento de Regras
- Função principal:

```python
def load_rules(rules_path: str | None = None) -> str:
    """Carrega as regras de análise de um arquivo .md.

    Args:
        rules_path: Caminho para o arquivo de regras.
                    Se None, busca 'regras_empresa.md' no diretório atual.

    Returns:
        String com o conteúdo das regras. Se o arquivo não existir,
        retorna a string DEFAULT_RULES definida no módulo.
    """
```

- Definir uma constante `DEFAULT_RULES: str` com regras genéricas de fallback
  (boas práticas gerais de código limpo, ~10 linhas).

## Contratos que este módulo EXPÕE
| Função | Input | Output |
|---|---|---|
| `main()` | `None` (lê do `sys.argv`) | `None` (orquestra chamadas) |
| `load_rules(rules_path)` | `str \| None` | `str` (conteúdo das regras) |

## Contratos que este módulo CONSOME (usar mocks)
| Módulo | Função | Mock sugerido |
|---|---|---|
| `src/git_module.py` | `get_changed_files()` | Retornar `["src/exemplo.py"]` |
| `src/ai_service.py` | `analyze_code(prompt)` | Retornar string Markdown fixa |
| `src/report.py` | `save_report(content, path)` | Print no console |
| `src/autofix.py` | `apply_fix(ai_response, file)` | Print no console |

## Critérios de Aceite (Definition of Done)
- [ ] `pip install -e .` funciona sem erros no ambiente Conda (Python 3.11).
- [ ] Executar `kirosonar` no terminal exibe o help do argparse.
- [ ] Executar `kirosonar analyze` roda o fluxo completo com mocks sem erro.
- [ ] Executar com Python < 3.11 exibe mensagem de erro e sai com código 1.
- [ ] `load_rules()` sem arquivo presente retorna `DEFAULT_RULES`.
- [ ] `load_rules("regras_empresa.md")` com arquivo presente retorna seu conteúdo.
- [ ] Código segue PEP 8, tem type hints e docstrings em todas as funções.
