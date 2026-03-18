"""Módulo de infraestrutura Git para o KiroSonar.

Responsável por interagir com o Git via subprocess para descobrir
arquivos alterados no working tree e ler seus conteúdos.
"""

import subprocess
import sys


def get_changed_files() -> list[str]:
    """Executa 'git diff --name-only' e retorna a lista de arquivos alterados.

    Returns:
        Lista de caminhos relativos dos arquivos modificados.
        Retorna lista vazia se não houver alterações.

    Raises:
        SystemExit: Se o diretório atual não for um repositório Git.
    """
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True,
    )

    # returncode != 0 indica que não é um repositório Git válido
    if result.returncode != 0:
        print(
            "Erro: o diretório atual não é um repositório Git válido.\n"
            f"Detalhes: {result.stderr.strip()}"
        )
        sys.exit(1)

    # Filtra linhas vazias geradas pelo split do output
    changed_files = [line for line in result.stdout.splitlines() if line.strip()]

    return changed_files


def read_file_content(file_path: str) -> str:
    """Lê e retorna o conteúdo completo de um arquivo.

    Args:
        file_path: Caminho relativo ou absoluto do arquivo.

    Returns:
        Conteúdo do arquivo como string.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
