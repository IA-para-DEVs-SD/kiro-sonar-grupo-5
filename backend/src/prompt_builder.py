"""Montagem do prompt para envio à LLM."""


def build_prompt(code: str, rules: str, file_path: str) -> str:
    """Monta o prompt completo para envio à LLM.

    Args:
        code: Conteúdo do arquivo a ser analisado.
        rules: String com as regras da empresa.
        file_path: Nome/caminho do arquivo para contexto.

    Returns:
        Prompt formatado instruindo a LLM a retornar o relatório no template fixo.
    """
    return (
        f"Você é um auditor de código sênior. Analise o arquivo '{file_path}' "
        f"com base nas regras abaixo e retorne EXATAMENTE no template indicado.\n\n"
        f"## Regras da Empresa\n{rules}\n\n"
        f"## Código para Análise\n```\n{code}\n```\n\n"
        f"## Template de Resposta (siga exatamente)\n"
        f"## Bugs\n(lista)\n\n"
        f"## Vulnerabilidades\n(lista)\n\n"
        f"## Code Smells\n(lista)\n\n"
        f"## Hotspots de Segurança\n(lista)\n\n"
        f"## Código Refatorado\n[START]\n(código refatorado completo)\n[END]"
    )
