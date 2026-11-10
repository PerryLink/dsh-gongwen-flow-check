<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-gongwen-flow-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-gongwen-flow-check-hero-en-light.webp" width="100%" alt="dsh-gongwen-flow-check hero: the left column carries the plugin name, two value lines and the boundary note; on the right is one receipt-and-handling register (document number, title, receipt date, kind and issuer, plus a single handling-stage row whose handler cell is empty, with receipt, due and completion dates and a status), and underneath the difference list it produces: GF-001, one warn, row 1 handler is empty; GF-004, one skipped, values not configured; counters skipped 1, warn 1, error 0, under a seal that reads differences only, never a verdict">
</picture>

# dsh-gongwen-flow-check

**Check a receipt-and-handling register row by row — handler filled, receipt and completion dates parse and follow each other, completion falls inside the recorded deadline, statuses come from your vocabulary, document numbers are unique, and the header names the document — and get back a list of what is inconsistent, where, and what to fix.**

A check plugin for DeepSeek Harness, built for office clerks and document officers: the rule pack quotes the official-document handling regulation verbatim, reports only literal differences against the cited clauses, and never decides compliance, never assigns liability, never touches your original.

[Install](#three-step-setup) · [Configuration](#configuration) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibility)
[![npm](https://img.shields.io/npm/v/dsh-gongwen-flow-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-gongwen-flow-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-gongwen-flow-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-gongwen-flow-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibility)

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

<sub>Community plugin, not affiliated with DeepSeek. Canonical repository: <https://github.com/PerryLink/dsh-gongwen-flow-check> (Gitee is a mirror).</sub>

## What it is

`dsh-gongwen-flow-check` reads one receipt-and-handling register — the document header (`docNo`, `title`, `receivedAt`, and so on) plus one row per handling step — and checks what a register can be held to mechanically: that every step fills the `handler` column, that `receivedAt` and `doneAt` parse as dates and follow each other, that a completion falls inside the deadline the register itself records in `dueAt`, that each `status` comes from the vocabulary you configure in `values`, that `docNo` is registered only once, and that the header declares both `title` and `receivedAt`. You hand it the source material (a table, register or document; Excel can be converted to JSON/YAML first, in chat if the platform supports it) and it returns a list of differences — which row, which column, what is missing. It does not decide whether handling was late, whether it should be chased, or who is accountable, and it never modifies the original.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-gongwen-flow-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-gongwen-flow-check-flow-v5-light.svg" width="100%" alt="dsh-gongwen-flow-check structure: one receipt-and-handling register (7 header fields plus 8 row columns, aliases normalized, at least one stage, status or handler column required) feeds six rules over a read-only bus. The rail above the gates records the severity ceiling: the pack has no direct basis, so error is never emitted; principle-based rules cap at warn (four rules) and institution-configured rules cap at info (two rules). In the real run of the bundled sample, GF-001 fires (row 1 handler empty, warn), GF-004 cannot run because values is unset and reports itself in skipped, and GF-002, GF-003, GF-005 and GF-006 ran clean and enter neither list; the three-state trays feed one report (error 0 / warn 1 / info 0, issueCount 1 / skippedCount 1, markdown + reportJson). The report lists differences only, the verdict stays with the reviewer, and the original is never modified">
</picture>

## Three-step setup

1. **Install**:

   ```sh
   dsh plugin --profile <name> add dsh-gongwen-flow-check
   ```

   Alternatively, search "Documents and Governance Suite" in WorkBuddy / Coze (the full set; this check is one part of it; availability as listed).

2. **Minimal config** (works out of the box):

   ```yaml
   - insert:
       - id: dsh-gongwen-flow-check
         name: dsh-gongwen-flow-check
   ```

   Every tunable lives in the Schemastery schema in `src/config.ts` and the defaults are production-ready; per-rule thresholds live in the rule pack under `rules/`.

3. **Verify it mounts**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-gongwen-flow-check'
   ```

   Then run the bundled sample (build first inside the repository; about a minute):

   ```sh
   pnpm run build
   node samples/quickstart/run.mjs
   ```

   Sample input lives in `samples/quickstart/input/`, the expected output in `samples/quickstart/expected/result.json`, and a captured run in `docs/assets/quickstart.png`.

**Uninstall**: `dsh plugin --profile <name> remove dsh-gongwen-flow-check` (or remove the row from the profile patch).

<details>
<summary>Install from the DSH Desktop market</summary>

Every PerryLink plugin is listed in the built-in DSH Desktop market: **Market → Sources → Add source → paste** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ select**. Installation still requires the market's npm identity check and your confirmation.

</details>

## Core capabilities

The plugin registers the `gongwen_flow_check` tool: it reads one register (document header plus handling-step rows), applies a versioned rule pack, and returns a structured report.

- **The rule pack is data, not code** — every rule lives in `rules/gongwen-flow-check.yaml`; swapping the file switches the rule set without touching TypeScript, and the pack is validated on load, not trusted.
- **Severity follows the evidence** — a rule resting on a general principle (`derived-from-principle`) is capped at `warn`; one resting on your institution's own configuration (`institutional-configuration`) is capped at `info`; neither can ever be declared `error` (a test asserts this).
- **An empty issue list is never "all clear"** — every check that could not run reports itself in `skipped` with its reason; when the `GF-004` vocabulary is unset, the rule reports itself in `skipped` rather than passing silently.
- **No adjudication** — the report lists differences and never pronounces on compliance, liability or correctness; a wording guard forces the report to always carry the disclaimer.
- **Verbatim citations only** — every rule carries a document, a document number, a clause in the source's own numbering, a verbatim excerpt and the URL it was read from; presenting a paraphrase as a quotation, or an unverifiable basis as `error`, fails at load.

```text
register (header · handling rows) ──gongwen_flow_check──▶ rule pack GF-001…GF-006 ──▶ report (findings + skipped)
            ▲                                                                              │
            └──────────────────────────── original never modified ─────────────────────────┘
```

### Rules at a glance

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `GF-001` | every handling step fills in its handler | warn | principle |
| `GF-002` | receipt and completion dates parse and follow each other | warn | principle |
| `GF-003` | completion falls inside the deadline the register records | info | local |
| `GF-004` | the status comes from your vocabulary (off by default) | info | local |
| `GF-005` | document numbers are unique in the register | warn | principle |
| `GF-006` | the register header declares title and receipt date | warn | principle |

### Examples

These are the plugin's real entry points; install once, then call one.

**Detailed output** — tool `gongwen_flow_check`, input (excerpt):

```json
{"rows":[{"办理环节":"承办","承办人":"张科","收文日期":"2026-03-02","办理期限":"2026-03-12","办结日期":"2026-02-28"}]}
```

Output:

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

*Observed from `tests/fixtures/GF-002/GF-002-unsafe.json (cases.json expects GF-002 count 1); run via lib/index.mjs rules/gongwen-flow-check.yaml`*

### What it answers

| You ask | What it answers |
|---|---|
| A handling step has not filled in its handler. What does the register get told? | `GF-001` requires the `handler` column on every step and reports the row where it is blank. It checks only that the column is filled in, not whether handling was timely — it does not decide whether the step should have been chased or who is accountable. |
| The completion date is earlier than the receipt date. Is that caught? | Yes. `GF-002` parses `receivedAt` against `doneAt` and reports the row when the two dates do not follow each other. It compares only the two dates written in the register — the same day counts as not later — and does not judge whether handling stayed inside its deadline. A date it cannot parse is reported separately rather than skipped in silence. |
| A row never records a handling deadline. Does the check assume one? | No. `GF-003` runs only when the register itself writes a deadline into `dueAt`; with `dueAt` empty the rule reports itself in `skipped`. The regulation fixes no number of days and the plugin hard-codes none, so no deadline is ever inferred. A hit means "this does not match the deadline you recorded", not "this is overdue". |
| The handling status is filled with a value that is not in the configured list. | `GF-004` reports the row when the `status` value is not among the values you configured in `values`. Shipped, that list is empty, which means unconfigured, so the rule reports itself in `skipped` instead of passing in silence. It checks only whether the value is on your list, not which stage the document is actually at. |
| The same document number appears twice in the register. | `GF-005` requires `docNo` to be unique in the register; whitespace is ignored when comparing. A hit usually means a duplicate registration or a mis-copied number, and needs a human to confirm: a repeated `docNo` leaves the reader unable to tell one document registered twice from two different documents carrying one number. |
| The register itself never declares the document title and receipt date. | `GF-006` requires the header to declare both `title` and `receivedAt` at the top level, and reports the header when either is missing. It checks only that the two are declared, not whether the title is in the correct form, and not whether the handling records really belong to that document. |

## Configuration

Every tunable lives in the Schemastery schema in `src/config.ts`, so it can be changed from `cordis.yml` without editing code; per-rule thresholds live in the rule pack under `rules/`. The five keys below are the complete list; rule-level parameters follow.

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/gongwen-flow-check.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `GF-001` `field` — the handler column, `handler` by default.
- `GF-003` `dueAt` — the register's handling-deadline column; without a recorded deadline the rule reports itself in `skipped`, and the plugin never computes a deadline from a day count.
- `GF-004` `values` — your step vocabulary, e.g. `[todo, in-progress, done, archived]`; empty means unconfigured and the rule does not run.
- `GF-005` — whitespace is ignored when comparing `docNo`.

Example override in your profile patch:

```yaml
- insert:
    - id: dsh-gongwen-flow-check
      name: dsh-gongwen-flow-check
      config:
        disabledRules: [GF-004]
        onlyRules: [GF-001, GF-002, GF-003]
        skipNotes: this institution's own handling rules are the basis for this check
```

## FAQ

<details>
<summary>Is my material modified or uploaded anywhere?</summary>

No. The tool only reads the JSON/YAML material text you hand it (`file` or `material`, one of the two) and **never modifies the original**; the plugin is plain ESM with no native code, **no network access and no model call** (see Compatibility), so the material never leaves your machine.

</details>

<details>
<summary>With no status vocabulary and no recorded deadline, does anything pass silently?</summary>

No. `GF-004`'s `values` and the `dueAt` that `GF-003` needs both ship unconfigured, and a check that cannot run reports itself in `skipped` with its reason — an empty difference list is never read as "nothing is wrong". `GF-004` checks only whether the value is on your list, not which stage the document is actually at.

</details>

<details>
<summary>Does the plugin decide that handling is "overdue"?</summary>

No. `GF-003` compares the completion date against the deadline **written in the register itself** (`dueAt`); with no deadline recorded it reports `skipped` rather than assuming a number of days. The regulation requires an urgent document's deadline to be stated and requires completion within a stated deadline, but **fixes no number of days** — the deadline always comes from the incoming document or your institution, and the plugin never invents one. A hit means "this does not match the recorded deadline", **not** "this is overdue": lateness also depends on reminders, extensions and the document's own urgency.

</details>

<details>
<summary>Which date formats are read? What about apparent time shifts?</summary>

The reader accepts `2026-03-02` and `2026-03-02 09:30`; a date written out in Chinese numerals is reported as unparseable on purpose, so you can decide whether to normalise the export. All arithmetic is wall-clock over the input strings, with no timezone conversion.

</details>

<details>
<summary>The plugin installs but the tool never appears, or installation is refused as version-incompatible — what now?</summary>

Check that `main` resolves to `lib/index.mjs` and that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently. The peer range covers the `0.1.x` and `0.2.x` lines; if your runtime sits outside it, grant an explicit exemption: `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`. Peer compatibility is enforced by the runtime at install time.

</details>

## Standards it follows

| Document | Number | Cited by rules |
|---|---|---|
| Regulations on the Handling of Official Documents by Party and Government Organs | CPC Central Committee and State Council General Offices [2012] No. 14 (in force since 2012-07-01) | GF-001, GF-002, GF-003, GF-004, GF-005, GF-006 |

Original titles of the cited documents:

```text
《党政机关公文处理工作条例》 中办发〔2012〕14号（自 2012 年 7 月 1 日起施行）
```

**Boundary:** this plugin checks one **receipt-and-handling register** for what a register can be held to mechanically — that every step names its handler, that the receipt and completion dates parse and follow each other, that a completion falls inside the deadline the register itself states, that statuses come from your vocabulary, that document numbers are unique, and that the header identifies the document. It does **not** decide whether handling was late, whether it should be chased, or who is accountable. The regulation requires an urgent document to have **its handling deadline stated** and requires work to finish within a stated deadline — **it fixes no number of days itself**, so the deadline always comes from the incoming document or your own rules, and this plugin never invents one.

> ### ⚠️ What the citations in this plugin's report actually rest on
>
> **The regulation's full text has been obtained and checked.** The Regulations on the Handling of Official Documents by Party and Government Organs (CPC Central Committee and State Council General Offices [2012] No. 14) were read verbatim from the central government portal, and the verification reports under `rules/evidence/` record the articles checked: article 5 (principles), article 23 (what document handling covers), article 24 (the seven receiving procedures, including "an urgent document shall have its handling deadline stated") and article 42 (in force from 2012-07-01, superseding two earlier documents). The rule pack's `excerpt` fields now carry verbatim quotations, and `pnpm run check:citations` checks each segment against the evidence record — currently 10 segments checked, 0 untraceable, baseline 0.
>
> **Yet every rule remains `warn` or `info`, and no `kind` was upgraded to `direct`** — deliberately. What this plugin checks is whether *a register* is complete and self-consistent; the regulation governs how a document is *handled*, which is a different proposition. Labelling "this column is blank" as a `direct` citation of "handling shall be recorded in detail" would dress a register gap up as a breach of the regulation, which is exactly the over-claim this family exists to avoid. The check also leaves the deadline's size to the incoming document and the institution, as article 24 does.
>
> The official document *format* standard (GB/T 9704-2012) **was not obtained**, and this plugin does not check layout in any case.
>
> The deadline rule deserves its own note. `GF-003` compares the completion date against the deadline **written in the register itself** (`dueAt`); with no deadline recorded it reports itself in `skipped` rather than assuming a number of days. Its finding says "this does not match the deadline you recorded", **not** "this is overdue" — lateness depends on reminders, extensions and the document's own urgency.

## Material format

The tool accepts JSON or YAML:

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

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the register's own column names are kept so a finding names the column it read. Dates may be `2026-03-02` or `2026-03-02 09:30`. Numbers are accepted as strings, so a spreadsheet export needs no cleaning.

## Rule sources

Rule data lives in `rules/gongwen-flow-check.yaml`, separate from the code. Every rule carries a document, a document number, a clause in the source's own numbering, a verbatim excerpt and the URL it was read from. The loader enforces that an excerpt is a real quotation of at least eight characters, and that a check resting on a general principle (`kind: derived-from-principle`, capped at `warn`) or on local policy (`kind: institutional-configuration`, capped at `info`) can **never** be declared `error`. A rule pack that over-claims fails at load instead of producing a report that looks more confident than its evidence.

The pack header states the citation discipline; each rule's `note` explains its basis and the conclusions it deliberately does not draw; `rules/evidence/` keeps the clause-verification record; and `pnpm run check:citations` compares every `excerpt` segment against that evidence (currently 10 segments checked, 0 untraceable, baseline 0). The `note` on `GF-003` records separately that the regulation leaves the length of the deadline to the incoming document and the institution, and that the plugin hard-codes no number of days.

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-rc.2`. `engines.dsh` is declared as `>=0.2.1-0 <0.3.0` and is enforced by the host since 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native` and `ptc`; for a full year of registers use `ptc` |

## Troubleshooting

- **`GF-003` reports itself as skipped.** The register records no deadline. That is deliberate: the plugin will not invent one, because the deadline comes from the incoming document or your own handling rules.
- **`GF-003` fires but I consider the handling timely.** The register's deadline and the completion date disagree. Either the deadline column is stale or the completion date is wrong — the finding names the two cells it compared.
- **`GF-004` never runs.** Its vocabulary is empty; fill it with your institution's step names.
- **`GF-002` fires on dates I can read.** The reader accepts `2026-03-02` and `2026-03-02 09:30`; a date written out in Chinese numerals is reported as unparseable on purpose.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if your runtime sits outside it, grant an explicit exemption: `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.
- **Times look shifted.** All arithmetic is wall-clock over the input strings, with no timezone conversion.

## Ecosystem and quality

- [Gitee mirror](https://gitee.com/perrylink/dsh-gongwen-flow-check) (synced mirror; GitHub is canonical)
- [dshfind plugin page](https://dshfind.com/plugins/PerryLink/dsh-gongwen-flow-check) (installs and ranking)
- [OpenSSF Scorecard report](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-gongwen-flow-check) (driven by [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listed)
- [Ecosystem knowledge base — choose a checker by material](https://perrylink.github.io/zh/checkers/choose/) (full family index: 62 checkers + general plugins)

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures per rule (tests/fixtures/<RULE>/)
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes     # five-language README consistency
pnpm run check:citations   # checks every rule quotation against rules/evidence/
node ../scripts/sync-shared.mjs dsh-gongwen-flow-check   # refresh src/shared from ../_shared
```

The plugin is **data-driven**: `src/model.ts` declares the table shape, the shared kit supplies the reader and the check engine, and the rule pack declares every check. Edit `rules/*.yaml` to switch the rule set without touching TypeScript; the pack is validated on load, not trusted. README images are generated programmatically by [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) and can be re-run safely: the hero banners with Pillow (zh / en × light / dark, four files) and the structure diagram as hand-written SVG (light and dark, labelled with command-surface tokens, real sample values and short annotations). The older single-skin flow diagram, hero and demo images stay in `docs/assets/` for external deep links, while the READMEs reference only the new hero set and the flow-v5 pair.

## Family and credits

This project is part of the DeepSeek Harness plugin family maintained by [PerryLink](https://github.com/PerryLink) (all Apache-2.0). If this plugin helps you, **a star** unlocks nothing but makes it easier for the next person to find.

- [@PerryLink](https://github.com/PerryLink) — creator and maintainer: the `gongwen_flow_check` tool, the verbatim-cited rule pack with its clause-verification record, and the five-language documentation.

<details>
<summary>Expand all plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 FROZEN — see the repo README |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 FROZEN — see the repo README |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRED (repo archived) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRED (repo archived) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRED (repo archived) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRED (repo archived) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 FROZEN — see the repo README |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 FROZEN — see the repo README |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 FROZEN — see the repo README |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 FROZEN — see the repo README |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 FROZEN — see the repo README |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRED (repo archived) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRED (repo archived) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRED (repo archived) |

</details>

## License

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-gongwen-flow-check contributors

<p align="center"><sub>Apache-2.0 · Community plugin, not affiliated with DeepSeek.</sub></p>
