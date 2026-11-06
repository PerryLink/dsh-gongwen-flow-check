<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-gongwen-flow-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-gongwen-flow-check-hero-en-light.webp" width="100%" alt="dsh-gongwen-flow-check, capa: a coluna esquerda leva o nome do plugin, duas linhas de valor e a nota de limites; à direita está um registo de receção e tramitação (número do documento, título, data de receção, tipo e organismo, mais uma linha de tramitação cujo responsável está vazio, com datas de receção, prazo e conclusão, e um estado) e, abaixo, a lista de diferenças que produz: GF-001, um warn, linha 1 sem responsável; GF-004, um skipped, values não configurado; contadores skipped 1, warn 1, error 0, com um selo que diz apenas diferenças, nunca um veredicto">
</picture>

# dsh-gongwen-flow-check

**Verifica linha a linha um registo de receção e tramitação de documentos oficiais — responsável preenchido, datas de receção e conclusão legíveis e em ordem, conclusão dentro do prazo anotado, estados conforme o seu vocabulário, números de documento únicos e cabeçalho que identifica o documento — e recebe uma lista do que está incoerente, onde e como corrigir.**

Um plugin de verificação para DeepSeek Harness, feito para secretariado e pessoal de escritório: o pacote de regras cita literalmente o regulamento de tratamento de documentos oficiais, assinala apenas diferenças literais face às cláusulas citadas, e nunca decide conformidade, nunca atribui responsabilidade e nunca toca no original.

[Instalar](#instalação-em-três-passos) · [Configuração](#configuração) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidade)
[![npm](https://img.shields.io/npm/v/dsh-gongwen-flow-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-gongwen-flow-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-gongwen-flow-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-gongwen-flow-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidade)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-gongwen-flow-check?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-gongwen-flow-check/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-gongwen-flow-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-gongwen-flow-check)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-gongwen-flow-check?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-gongwen-flow-check?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-gongwen-flow-check/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-gongwen-flow-check)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-gongwen-flow-check)

```sh
dsh plugin --profile <name> add dsh-gongwen-flow-check
```

</div>

<sub>Plugin da comunidade, sem afiliação com a DeepSeek. Repositório canónico: <https://github.com/PerryLink/dsh-gongwen-flow-check> (o Gitee é um espelho).</sub>

## O que é

`dsh-gongwen-flow-check` lê um registo de receção e tramitação — o cabeçalho do documento (`docNo`, `title`, `receivedAt`, etc.) mais uma linha por fase de tramitação — e verifica o que um registo pode sustentar mecanicamente: se cada fase preenche a coluna `handler`, se `receivedAt` e `doneAt` são analisáveis como datas e são sucessivas, se a conclusão cai dentro do prazo que o próprio registo anota em `dueAt`, se cada `status` vem do vocabulário que configurar em `values`, se `docNo` é registado uma só vez e se o cabeçalho declara `title` e `receivedAt`. Você entrega o material original (uma tabela, um registo ou um documento; o Excel pode ser convertido antes para JSON/YAML, até no chat se a plataforma permitir) e recebe uma lista de diferenças: que linha, que coluna, o que falta. Não decide se a tramitação chegou tarde, se devia ser cobrada, nem quem é responsável — e jamais modifica o original.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-gongwen-flow-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-gongwen-flow-check-flow-v5-light.svg" width="100%" alt="Estrutura do dsh-gongwen-flow-check: um registo de receção e tramitação (7 campos de cabeçalho e 8 colunas de linha, aliases normalizados, é exigida pelo menos uma coluna de fase, estado ou responsável) alimenta seis regras através de um barramento só de leitura. A barra acima das portas fixa o teto de gravidade: o pacote não tem base direct, pelo que error nunca é emitido; as regras baseadas em princípios ficam limitadas a warn (quatro) e as de configuração institucional a info (duas). Na execução real da amostra, GF-001 dispara (linha 1 sem responsável, warn), GF-004 não pode correr porque values não está configurado e declara-se em skipped, e GF-002, GF-003, GF-005 e GF-006 correram sem achados e não entram em nenhuma lista; as três bandejas convergem num relatório (error 0 / warn 1 / info 0, issueCount 1 / skippedCount 1, markdown + reportJson). O relatório apenas lista diferenças, o veredicto fica com o revisor e o original nunca é modificado">
</picture>

## Instalação em três passos

1. **Instale**:

   ```sh
   dsh plugin --profile <name> add dsh-gongwen-flow-check
   ```

   Em alternativa, procure «Documents and Governance Suite» no WorkBuddy / Coze (o conjunto completo; esta verificação é uma parte; disponibilidade conforme a loja).

2. **Configuração mínima** (funciona com os valores padrão):

   ```yaml
   - insert:
       - id: dsh-gongwen-flow-check
         name: dsh-gongwen-flow-check
   ```

   Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts` e os padrões estão prontos a usar; os limites por regra ficam no pacote de regras sob `rules/`.

3. **Verifique que monta**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-gongwen-flow-check'
   ```

   Depois execute o exemplo incluído (compile antes dentro do repositório; cerca de um minuto):

   ```sh
   pnpm run build
   node samples/quickstart/run.mjs
   ```

   A entrada de exemplo está em `samples/quickstart/input/`, a saída esperada em `samples/quickstart/expected/result.json` e uma captura da execução em `docs/assets/quickstart.png`.

**Desinstalar**: `dsh plugin --profile <name> remove dsh-gongwen-flow-check` (ou remova a linha do patch do perfil).

<details>
<summary>Instalar a partir do mercado do DSH Desktop</summary>

Todos os plugins da PerryLink podem ser explorados no mercado integrado do DSH Desktop: **Market → Sources → Add source → colar** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ selecionar**. A instalação continua a exigir a verificação de identidade npm do mercado e a sua confirmação.

</details>

## Capacidades principais

O plugin regista a ferramenta `gongwen_flow_check`: lê um registo (cabeçalho do documento e linhas de tramitação), aplica um pacote de regras versionado e devolve um relatório estruturado.

- **O pacote de regras é dado, não código** — todas as regras vivem em `rules/gongwen-flow-check.yaml`; trocar o ficheiro troca o conjunto de regras sem tocar em TypeScript, e o pacote é validado ao carregar, não é confiado.
- **A severidade segue a evidência** — uma regra baseada num princípio geral (`derived-from-principle`) tem teto `warn`; uma baseada na configuração da sua instituição (`institutional-configuration`) tem teto `info`; nenhuma pode ser declarada `error` (um teste garante-o).
- **Uma lista vazia nunca é «tudo em ordem»** — cada verificação que não pôde executar-se declara-se em `skipped` com o seu motivo; quando o vocabulário de `GF-004` não está configurado, a regra declara-se em `skipped` em vez de passar em silêncio.
- **Sem adjudicação** — o relatório apenas enumera diferenças e nunca se pronuncia sobre conformidade, responsabilidade ou correção; um guarda de redação obriga a que o relatório traga sempre o aviso.
- **Citações só literais** — cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e o URL de onde foi lido; apresentar uma paráfrase como citação, ou uma base não verificável como `error`, falha ao carregar.

```text
registo (cabeçalho · linhas de tramitação) ──gongwen_flow_check──▶ regras GF-001…GF-006 ──▶ relatório (findings + skipped)
                 ▲                                                                                    │
                 └────────────────────────────── o original nunca é modificado ────────────────────────┘
```

### Regras em resumo

| Regra | Verificação | Severidade | Tipo de base |
|---|---|---|---|
| `GF-001` | cada fase de tramitação indica o seu responsável | warn | princípio |
| `GF-002` | as datas de receção e conclusão são analisáveis e sucessivas | warn | princípio |
| `GF-003` | a conclusão cai dentro do prazo anotado no registo | info | local |
| `GF-004` | o estado vem do teu vocabulário (desligada por padrão) | info | local |
| `GF-005` | os números de documento são únicos no registo | warn | princípio |
| `GF-006` | o cabeçalho declara o título e a data de receção | warn | princípio |

### Exemplos

São os pontos de entrada reais do plugin; instala uma vez e chama um.

**Saída detalhada** — ferramenta `gongwen_flow_check`, entrada (extrato):

```json
{"rows":[{"办理环节":"承办","承办人":"张科","收文日期":"2026-03-02","办理期限":"2026-03-12","办结日期":"2026-02-28"}]}
```

Saída:

```json
{
  "id": "dsh-gongwen-flow-check.GF-002.de09b5a6",
  "ruleId": "GF-002",
  "severity": "warn",
  "locator": {
    "field": "receivedAt",
    "row": 1
  },
  "found": "第 1 行「receivedAt」为 2026-03-02，晚于 「doneAt」的 2026-02-28",
  "expected": "「receivedAt」不应晚于 2026-02-28",
  "fix": "办结日期不应早于收文日期；核对两个日期的填写"
}
```

*Observado em `tests/fixtures/GF-002/GF-002-unsafe.json (cases.json expects GF-002 count 1); run via lib/index.mjs rules/gongwen-flow-check.yaml`*

### O que responde

| Você pergunta | O que responde |
|---|---|
| Uma fase de tramitação não tem responsável preenchido. O que o registo recebe? | `GF-001` exige a coluna `handler` em cada fase e assinala a linha em que está vazia. Verifica apenas se a coluna está preenchida, não se a tramitação foi atempada: não decide se essa fase devia ser cobrada nem quem é responsável. |
| A data de conclusão é anterior à de receção. Isso é detetado? | Sim. `GF-002` analisa `receivedAt` face a `doneAt` e assinala a linha quando as duas datas não são sucessivas. Compara apenas as duas datas escritas no registo — o mesmo dia conta como não posterior — e não julga se a tramitação ficou dentro do prazo. Uma data que não consegue analisar é comunicada em separado, em vez de omitida em silêncio. |
| Uma linha nunca regista um prazo de tramitação. A verificação assume algum? | Não. `GF-003` só corre quando o próprio registo escreve um prazo em `dueAt`; com `dueAt` vazio a regra declara-se em `skipped`. O regulamento não fixa qualquer número de dias e o plugin não codifica nenhum, pelo que nunca se deduz um prazo. Um aviso significa «isto não coincide com o prazo que registou», não «isto está fora de prazo». |
| O estado de tramitação traz um valor que não está na lista configurada. | `GF-004` assinala a linha quando o valor de `status` não consta dos que configurou em `values`. De fábrica essa lista está vazia, o que significa sem configuração, pelo que a regra se declara em `skipped` em vez de passar em silêncio. Verifica apenas se o valor está na sua lista, não em que fase está realmente o documento. |
| O mesmo número de documento aparece duas vezes no registo. | `GF-005` exige que `docNo` seja único no registo; ao comparar ignoram-se os espaços em branco. Um aviso costuma significar registo duplicado ou número mal copiado, e exige confirmação humana: repetir o `docNo` impede saber se é um documento registado duas vezes ou dois documentos distintos com um só número. |
| O próprio registo não declara o título do documento nem a data de receção. | `GF-006` exige que o cabeçalho declare `title` e `receivedAt` ao nível superior e assinala o cabeçalho quando falta algum. Verifica apenas se ambos estão declarados, não se o título tem a forma correta nem se as anotações de tramitação correspondem de facto a esse documento. |

## Configuração

Todos os parâmetros ajustáveis vivem no esquema Schemastery de `src/config.ts`, pelo que se alteram a partir de `cordis.yml` sem tocar no código; os limites por regra estão no pacote de regras sob `rules/`. As cinco chaves da tabela são a lista completa; os parâmetros por regra vêm depois.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/gongwen-flow-check.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras que deixam de correr; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Correr apenas estas regras; vazio corre todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo de espera cooperativo da ferramenta |

Parâmetros por regra que vale a pena conhecer:

- `GF-001` `field` — a coluna do responsável, `handler` por padrão.
- `GF-003` `dueAt` — a coluna do prazo de tramitação; sem prazo registado a regra declara-se em `skipped`, e o plugin nunca calcula um prazo a partir de um número de dias.
- `GF-004` `values` — o seu vocabulário de fases, p. ex. `[待办, 承办中, 已办结, 已归档]`; vazio significa sem configuração e a regra não corre.
- `GF-005` — ao comparar `docNo` ignoram-se os espaços em branco.

Exemplo de sobreposição no patch do perfil:

```yaml
- insert:
    - id: dsh-gongwen-flow-check
      name: dsh-gongwen-flow-check
      config:
        disabledRules: [GF-004]
        onlyRules: [GF-001, GF-002, GF-003]
        skipNotes: as regras próprias desta instituição são a base desta verificação
```

## FAQ

<details>
<summary>O meu material é modificado ou enviado para algum lado?</summary>

Não. A ferramenta apenas lê o texto JSON/YAML que lhe entrega (`file` ou `material`, um dos dois) e **nunca modifica o original**; o plugin é ESM puro, sem código nativo, **sem rede e sem chamada ao modelo** (ver Compatibilidade), pelo que o material nunca sai da sua máquina.

</details>

<details>
<summary>Sem vocabulário de estados e sem prazo registado, algo passa em silêncio?</summary>

Não. Os `values` de `GF-004` e o `dueAt` de que `GF-003` precisa saem de fábrica sem configuração, e uma verificação que não pode correr declara-se em `skipped` com o motivo: uma lista de diferenças vazia nunca é lida como «não há nada de errado». `GF-004` verifica apenas se o valor está na sua lista, não em que fase está realmente o documento.

</details>

<details>
<summary>O plugin decide que a tramitação está «fora de prazo»?</summary>

Não. `GF-003` compara a data de conclusão com o prazo **escrito no próprio registo** (`dueAt`); sem prazo registado informa `skipped` em vez de supor um número de dias. O regulamento exige que um documento urgente **declare o seu prazo** e que se conclua dentro do prazo declarado, mas **não fixa qualquer número de dias**: o prazo vem sempre do documento recebido ou da sua instituição, e o plugin nunca o inventa. Um aviso significa «isto não coincide com o prazo registado», **não** «isto está fora de prazo»: o atraso também depende de cobranças, prorrogações e da urgência do próprio documento.

</details>

<details>
<summary>Que formatos de data são lidos? E os desvios de hora?</summary>

O leitor aceita `2026-03-02` e `2026-03-02 09:30`; uma data escrita com numerais chineses é comunicada como não analisável de propósito, para que decida se normaliza a exportação. Toda a aritmética é de hora local sobre as cadeias entregues, sem conversão de fusos horários.

</details>

<details>
<summary>O plugin instala-se mas a ferramenta nunca aparece, ou a instalação é recusada por versão — o que fazer?</summary>

Confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou; um `main` errado faz o carregador saltar a entrada em silêncio. O intervalo de peers cobre as linhas `0.1.x` e `0.2.x`; se o seu runtime ficar fora, conceda uma isenção explícita: `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`. A compatibilidade de peers é aplicada pelo runtime na instalação.

</details>

## Normas que segue

| Documento | Número | Regras que o citam |
|---|---|---|
| Regulamento de tratamento de documentos oficiais dos órgãos do Partido e do Estado | 中办发〔2012〕14号 (em vigor desde 2012-07-01) | GF-001, GF-002, GF-003, GF-004, GF-005, GF-006 |

Títulos originais dos documentos citados:

```text
《党政机关公文处理工作条例》 中办发〔2012〕14号（自 2012 年 7 月 1 日起施行）
```

**Limite:** este plugin verifica um **registo de receção e tramitação** no que um registo pode sustentar mecanicamente: que cada fase indique o seu responsável, que as datas de receção e conclusão sejam analisáveis e sucessivas, que a conclusão caia dentro do prazo que o próprio registo anota, que os estados venham do seu vocabulário, que os números de documento sejam únicos e que o cabeçalho identifique o documento. **Não** decide se a tramitação chegou tarde, se devia ser cobrada nem quem é responsável. O regulamento exige que um documento urgente **declare o seu prazo** e que se conclua dentro do prazo declarado, mas **não fixa qualquer número de dias**: o prazo vem sempre do documento recebido ou das suas próprias normas, e este plugin nunca o inventa.

> ### ⚠️ Em que se baseiam realmente as citações do relatório deste plugin
>
> **O texto integral do regulamento foi obtido e verificado.** O Regulamento de tratamento de documentos
> oficiais (中办发〔2012〕14号) foi lido literalmente no portal do Governo central, e os relatórios de
> verificação em `rules/evidence/` registam os artigos verificados: artigo 5 (princípios), artigo 23 (âmbito
> do tratamento), artigo 24 (os sete procedimentos de receção, incluindo «os documentos urgentes devem indicar
> o seu prazo de tramitação») e artigo 42 (em vigor desde 2012-07-01, substituindo dois documentos
> anteriores). Os campos `excerpt` do pacote passaram a conter citações literais, e
> `pnpm run check:citations` confronta cada segmento com o registo de evidência: atualmente 10 segmentos
> verificados, 0 não rastreáveis, base 0.
>
> **Mas cada regra continua `warn` ou `info`, e nenhum `kind` subiu a `direct`** — deliberadamente. Este
> plugin verifica se *um registo* está completo e coerente; o regulamento regula como um documento é
> *tramitado*, que é outra proposição. Rotular «esta coluna está vazia» como citação `direct` de «deve
> registar-se detalhadamente a tramitação» transformaria uma lacuna do registo numa violação do regulamento,
> exatamente a exageração que esta família evita. A verificação também deixa a dimensão do prazo ao documento
> recebido e à instituição, como faz o artigo 24.
>
> A norma de **formatação** de documentos oficiais (GB/T 9704-2012) **não foi obtida**, e este plugin não
> verifica maquetagem em caso algum.
>
> A regra do prazo merece nota própria. `GF-003` compara a data de conclusão com o prazo **escrito no próprio
> registo** (`dueAt`); sem prazo registado declara-se em `skipped` em vez de supor um número de dias. O seu
> achado diz «isto não coincide com o prazo que registou», **não** «isto está fora de prazo»: o atraso depende
> de cobranças, prorrogações e da urgência do documento.

## Formato do material

A ferramenta aceita JSON ou YAML:

```yaml
docNo: 某发〔2026〕15号
title: 关于某某工作的通知
docKind: 通知
issuer: 某某机关
receivedAt: 2026-03-02
rows:
  - { 序号: '1', 办理环节: 承办, 承办人: 张科, 收文日期: 2026-03-02,
      办理期限: 2026-03-12, 办结日期: 2026-03-10, 办理状态: 已办结 }
```

Os nomes de coluna são reconhecidos sem distinguir maiúsculas de minúsculas e ignorando espaços, underscores e hífenes; os nomes próprios do registo são mantidos, para que um achado nomeie a coluna que leu. As datas podem ser `2026-03-02` ou `2026-03-02 09:30`. Os números são aceites como cadeias, pelo que uma exportação de folha de cálculo não precisa de limpeza.

## Fontes das regras

Os dados das regras vivem em `rules/gongwen-flow-check.yaml`, separados do código. Cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e o URL de onde foi lido. O carregador impõe que o trecho seja uma citação real de pelo menos oito caracteres e que uma verificação baseada apenas num princípio geral (`kind: derived-from-principle`, teto `warn`) ou na política local (`kind: institutional-configuration`, teto `info`) **nunca** seja declarada `error`. Um pacote que exagera a sua base falha ao carregar em vez de produzir um relatório que parece mais seguro do que é.

O cabeçalho do pacote declara a disciplina de citações; o `note` de cada regra explica a sua base e as conclusões que deliberadamente não tira; `rules/evidence/` guarda o registo de verificação de cláusulas; e `pnpm run check:citations` compara cada segmento de `excerpt` com essa evidência (atualmente 10 segmentos verificados, 0 não rastreáveis, base 0). O `note` de `GF-003` registra à parte que o regulamento entrega a duração do prazo ao documento recebido e à instituição, e que o plugin não codifica qualquer número de dias.

## Compatibilidade

| Superfície | Estado |
|---|---|
| Harness | Intervalo de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceitar tanto `0.2.0-rc.2` como `0.2.1-rc.2`. `engines.dsh` é declarado como `>=0.2.1-0 <0.3.0` e o host aplica-o desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native` e `ptc`; para um ano inteiro de registos usa `ptc` |

## Solução de problemas

- **`GF-003` declara-se em `skipped`.** O registo não anota prazo. É deliberado: o plugin não o inventa, porque o prazo vem do documento recebido ou das suas próprias normas de tramitação.
- **`GF-003` dispara mas considero a tramitação atempada.** O prazo do registo e a data de conclusão não coincidem. Ou a coluna do prazo está desatualizada ou a data de conclusão está errada; o achado nomeia as duas células que comparou.
- **`GF-004` nunca corre.** O seu vocabulário está vazio; preencha-o com os nomes de fase da sua instituição.
- **`GF-002` dispara sobre datas que consigo ler.** O leitor aceita `2026-03-02` e `2026-03-02 09:30`; uma data com numerais chineses é comunicada como não analisável de propósito.
- **O plugin instala-se mas a ferramenta nunca aparece.** Confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou; um `main` errado faz o carregador saltar a entrada em silêncio.
- **`dsh plugin add` recusa o pacote como incompatível.** O intervalo de peers cobre `0.1.x` e `0.2.x`; se o seu runtime ficar fora, conceda uma isenção explícita: `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` informa `manifest-peers` como falha.** O verificador estático compara contra um intervalo de peers fixado no código anterior à linha 0.2. O runtime aplica a compatibilidade na instalação, pelo que o intervalo declarado é o correto; é um problema conhecido do `dsh-plugin-dev`.
- **Os horários parecem desviados.** Toda a aritmética é de hora local sobre as cadeias entregues, sem conversão de fusos horários.

## Ecossistema e qualidade

- [Espelho no Gitee](https://gitee.com/perrylink/dsh-gongwen-flow-check) (espelho sincronizado; o GitHub é o canónico)
- [Página do plugin no dshfind](https://dshfind.com/plugins/PerryLink/dsh-gongwen-flow-check) (instalações e ranking)
- [Relatório do OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-gongwen-flow-check) (impulsionado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listado)
- [Base de conhecimento do ecossistema — escolha um verificador por material](https://perrylink.github.io/zh/checkers/choose/) (índice completo da família: 62 verificadores + plugins gerais)

## Desenvolvimento

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, a suíte partilhada de plugins de tabela + fixtures emparelhados por regra (tests/fixtures/<RULE>/)
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes     # consistência dos README em cinco idiomas
pnpm run check:citations   # confronta cada citação de regra com rules/evidence/
node ../scripts/sync-shared.mjs dsh-gongwen-flow-check   # atualiza src/shared a partir de ../_shared
```

O plugin é **orientado por dados**: `src/model.ts` declara a forma da tabela, o kit partilhado fornece o leitor e o motor de verificação, e o pacote de regras declara cada verificação. Edite `rules/*.yaml` para trocar o conjunto de regras sem tocar em TypeScript; o pacote é validado ao carregar, não é confiado. As imagens do README são geradas programaticamente por [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) e podem ser reexecutadas sem risco: as capas com Pillow (zh / en × claro / escuro, quatro ficheiros) e o diagrama de estrutura como SVG escrito à mão (claro e escuro, com tokens da superfície de comandos, valores reais da amostra e anotações breves). O antigo diagrama de fluxo, a capa anterior e as imagens de demonstração permanecem em `docs/assets/` para ligações externas; o README referencia apenas o novo conjunto de capas e o par flow-v5.

## Família e agradecimentos

Este projeto faz parte da família de plugins de DeepSeek Harness da [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Se lhe for útil, **uma estrela** não desbloqueia nada, mas ajuda a que a próxima pessoa o encontre.

- [@PerryLink](https://github.com/PerryLink) — criador e mantenedor: a ferramenta `gongwen_flow_check`, o pacote de regras com citações literais e o seu registo de verificação de cláusulas, e a documentação em cinco idiomas.

<details>
<summary>Expandir todos os plugins</summary>

| Plugin | Estado |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** |  |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** |  |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** |  |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** |  |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** |  |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** |  |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** |  |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** |  |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** |  |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** |  |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** |  |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** |  |
| **[dsh-github](https://github.com/PerryLink/dsh-github)** |  |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** |  |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** |  |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** |  |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** |  |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** |  |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** |  |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** |  |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** |  |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** |  |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** |  |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** |  |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** |  |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** |  |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** |  |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** |  |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** |  |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** |  |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** |  |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** |  |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** |  |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** |  |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** |  |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** |  |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** |  |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** |  |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** |  |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** |  |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** |  |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** |  |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** |  |
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** |  |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** |  |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** |  |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** |  |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** |  |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** |  |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** |  |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** |  |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** |  |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** |  |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** |  |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** |  |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** |  |
| **[dsh-skill-pack-security](https://github.com/PerryLink/dsh-skill-pack-security)** |  |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** |  |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** |  |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** |  |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** |  |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** |  |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** |  |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** |  |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** |  |
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 APOSENTADO (repo arquivado) |

</details>

## Licença

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-gongwen-flow-check contributors

<p align="center"><sub>Apache-2.0 · Plugin da comunidade, sem afiliação com a DeepSeek.</sub></p>
