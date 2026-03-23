"""Módulo de integração com Git via subprocess."""

import subprocess
import sys


def get_changed_files() -> list[str]:
    """Executa 'git diff --name-only' e retorna a lista de arquivos alterados.

    Returns:
        Lista de caminhos relativos dos arquivos modificados.

    Raises:
        SystemExit: Se o diretório atual não for um repositório Git.
    """
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Erro: O diretório atual não é um repositório Git.")
        sys.exit(1)
    return [line for line in result.stdout.strip().splitlines() if line]


def read_file_content(file_path: str) -> str:
    """Lê e retorna o conteúdo completo de um arquivo.

    Args:
        file_path: Caminho relativo ou absoluto do arquivo.

    Returns:
        Conteúdo do arquivo como string.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    with open(file_path, encoding="utf-8") as f:
        return f.read()
