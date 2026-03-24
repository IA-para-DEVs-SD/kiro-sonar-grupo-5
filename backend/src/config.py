"""Carregamento de regras de análise."""

import os

DEFAULT_RULES: str = """\
- Siga os princípios SOLID.
- Nomeie variáveis e funções de forma descritiva.
- Evite funções com mais de 20 linhas.
- Não use variáveis globais mutáveis.
- Trate todas as exceções de forma explícita.
- Use type hints em todas as assinaturas.
- Remova código morto e imports não utilizados.
- Evite duplicação de lógica (DRY).
- Mantenha complexidade ciclomática baixa.
- Documente funções públicas com docstrings.
"""


def load_rules(rules_path: str | None = None) -> str:
    """Carrega as regras de análise de um arquivo .md.

    Args:
        rules_path: Caminho para o arquivo de regras.
                    Se None, busca 'regras_empresa.md' no diretório atual.

    Returns:
        Conteúdo das regras ou DEFAULT_RULES se o arquivo não existir.
    """
    path = rules_path or "regras_empresa.md"
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return DEFAULT_RULES
