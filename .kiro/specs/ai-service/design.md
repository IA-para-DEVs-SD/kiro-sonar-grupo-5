# Documento de Design

## Visão Geral

O módulo de serviço de IA do KiroSonar é composto por dois arquivos Python que formam
a camada de integração com a LLM. O `ai_service.py` encapsula a comunicação com o
`kiro-cli` via subprocesso, e o `prompt_builder.py` monta o prompt estruturado que
instrui a LLM a produzir relatórios no formato esperado pelo restante do sistema.

Ambos os módulos são stateless, sem dependências externas além da Standard Library,
e se comunicam exclusivamente por parâmetros e valores de retorno.

## Arquitetura

```
CLI (cli.py)
    │
    ├─► prompt_builder.build_prompt(code, rules, file_path) ──► str (prompt)
    │
    └─► ai_service.call_llm(prompt) ──► str (Markdown da LLM)
                │
                ├─ [KIROSONAR_MOCK=1] ──► retorna MOCK_RESPONSE
                │
                └─ [modo real] ──► subprocess.run(["kiro-cli", "chat", "--message", prompt])
                                        │
                                        ├─ returncode == 0 ──► stdout.strip()
                                        └─ returncode != 0 ──► RuntimeError(stderr)
```

## Componentes

### `src/ai_service.py`

**Responsabilidade:** Enviar o prompt à LLM via subprocesso e retornar a resposta em texto.

#### Constante `MOCK_RESPONSE`

String Markdown estática que simula uma resposta completa da LLM. Contém as 5 seções
obrigatórias do Template_Fixo e um bloco de código refatorado delimitado por `[START]`/`[END]`.
Utilizada quando `KIROSONAR_MOCK=1` para permitir testes offline sem acesso ao `kiro-cli`.

```python
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
```

#### Função `call_llm`

```python
def call_llm(prompt: str) -> str
```

**Fluxo de execução:**

1. Verifica `os.environ.get("KIROSONAR_MOCK") == "1"`.
2. Se verdadeiro, retorna `MOCK_RESPONSE` imediatamente.
3. Caso contrário, executa `subprocess.run(["kiro-cli", "chat", "--message", prompt], capture_output=True, text=True)`.
4. Se `result.returncode != 0`, levanta `RuntimeError(f"Erro ao chamar kiro-cli: {result.stderr}")`.
5. Retorna `result.stdout.strip()`.

**Dependências:** `os` (Standard Library), `subprocess` (Standard Library).

---

### `src/prompt_builder.py`

**Responsabilidade:** Montar a string de prompt que será enviada à LLM, combinando
o código do arquivo, as regras da empresa e o Template_Fixo de resposta.

#### Função `build_prompt`

```python
def build_prompt(code: str, rules: str, file_path: str) -> str
```

**Estrutura do prompt gerado:**

```
Você é um auditor de código sênior. Analise o arquivo '{file_path}'
com base nas regras abaixo e retorne EXATAMENTE no template indicado.

## Regras da Empresa
{rules}

## Código para Análise
```
{code}
```

## Template de Resposta (siga exatamente)
## Bugs
(lista)

## Vulnerabilidades
(lista)

## Code Smells
(lista)

## Hotspots de Segurança
(lista)

## Código Refatorado
[START]
(código refatorado completo)
[END]
```

**Dependências:** nenhuma.

## Contratos de Interface

| Função | Parâmetros | Retorno | Exceções |
|---|---|---|---|
| `call_llm(prompt)` | `prompt: str` | `str` — Markdown da LLM | `RuntimeError` se `returncode != 0` |
| `build_prompt(code, rules, file_path)` | `code: str`, `rules: str`, `file_path: str` | `str` — prompt formatado | nenhuma |

## Decisões de Design

### Uso de subprocesso em vez de SDK

O PRD exige que apenas a Standard Library seja utilizada. O `kiro-cli` é a interface
disponível para acesso à LLM, portanto `subprocess.run` é a única abordagem viável
sem introduzir dependências externas.

### Mock via variável de ambiente

A flag `KIROSONAR_MOCK=1` permite que toda a equipe execute testes e desenvolva
módulos dependentes (como `cli.py` e `autofix.py`) sem precisar de acesso ao `kiro-cli`
real. O mock retorna um Markdown completo e válido, cobrindo todos os casos de uso
do sistema downstream.

### Template_Fixo embutido no prompt

O `build_prompt` injeta o template de resposta diretamente no prompt para forçar
a LLM a produzir saída no formato esperado pelo `autofix.py` (tags `[START]`/`[END]`)
e pelo `report.py` (seções Markdown). Isso elimina a necessidade de parsing defensivo
no downstream.

### Separação de responsabilidades

`prompt_builder.py` e `ai_service.py` são módulos distintos e sem acoplamento direto.
O orquestrador (`cli.py`) é responsável por chamar `build_prompt` e passar o resultado
para `call_llm`, mantendo cada módulo com uma única responsabilidade.

## Propriedades de Correção

### 1. Invariante de modo mock

Para qualquer valor de `prompt`, se `KIROSONAR_MOCK == "1"`, então
`call_llm(prompt) == MOCK_RESPONSE`. O retorno é determinístico e independente da entrada.

### 2. Invariante de conteúdo do prompt

Para quaisquer valores de `code`, `rules` e `file_path`, o resultado de
`build_prompt(code, rules, file_path)` sempre contém `code`, `rules`, `file_path`,
as 5 seções do Template_Fixo e as tags `[START]`/`[END]`.

### 3. Propagação de erro do subprocesso

Se `kiro-cli` retornar `returncode != 0`, `call_llm` sempre levanta `RuntimeError`.
Nunca retorna string vazia ou parcial em caso de falha.

### 4. Completude do MOCK_RESPONSE

`MOCK_RESPONSE` contém todas as 5 seções obrigatórias e as tags `[START]`/`[END]`,
garantindo que módulos downstream (`autofix.py`, `report.py`) funcionem corretamente
em modo mock sem tratamento especial de casos ausentes.
