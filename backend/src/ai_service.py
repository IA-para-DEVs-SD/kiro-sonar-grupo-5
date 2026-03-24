"""Serviço de chamada à LLM via subprocesso kiro-cli."""

import os
import subprocess

MOCK_RESPONSE: str = """\
## Bugs
- Nenhum bug encontrado.

## Vulnerabilidades
- Nenhuma vulnerabilidade encontrada.

## Code Smells
- Variável com nome não descritivo (linha 10).

## Hotspots de Segurança
- Nenhum hotspot encontrado.

## Código Refatorado
[START]
def calcular_total(valor: float) -> float:
    return valor * 1.1
[END]
"""


def call_llm(prompt: str) -> str:
    """Envia um prompt para a LLM via kiro-cli e retorna a resposta.

    Args:
        prompt: String completa do prompt a ser enviado.

    Returns:
        Resposta da LLM (stdout).

    Raises:
        RuntimeError: Se o subprocesso falhar.
    """
    if os.environ.get("KIROSONAR_MOCK") == "1":
        return MOCK_RESPONSE

    result = subprocess.run(
        ["kiro-cli", "chat", "--message", prompt],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Erro ao chamar kiro-cli: {result.stderr}")
    return result.stdout.strip()
