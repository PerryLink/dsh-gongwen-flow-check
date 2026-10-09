# dsh-gongwen-flow-check — Official document circulation and handling deadline register check

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-gongwen-flow-check` reads one incoming-document register with its handling-step ledger — the document header plus one row per handling step — and checks that register’s own completeness and internal consistency: that every step names a handler in `handler`, that `receivedAt` and `doneAt` parse as dates and follow each other, that a completion falls inside the deadline the register itself records in `dueAt`, that each `status` comes from the vocabulary you configured, that `docNo` is registered only once, and that the header declares the document title and receipt date. It does not decide whether handling was late, whether it should be chased, or who is accountable.

## What it looks like

![Terminal demo of dsh-gongwen-flow-check: real output over its GF-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-gongwen-flow-check/main/docs/assets/dsh-gongwen-flow-check-demo.png)

Real output from this plugin over its own `GF-002` test fixture — not a mock-up. The rule pack ships no invented quotations, so a finding names both the clause it applied and the fact that the clause text was not obtained.

## What it answers

| You ask | What it answers |
|---|---|
| A handling step has no handler filled in. What does the register get told? | `GF-001` requires the `handler` column on every step and reports the step where it is blank. It checks only that the column is filled in, not whether the handling was timely — it does not decide whether the step should have been chased or who is accountable. |
| The completion date is earlier than the receipt date. Is that caught? | Yes. `GF-002` parses `receivedAt` against `doneAt` and reports the step when the two dates do not follow each other. It compares the two dates written in the ledger only — the same day counts as not later — and does not judge whether the handling stayed inside its deadline. A date it cannot parse is reported separately rather than skipped in silence. |
| A row never records a handling deadline. Does the check assume one? | No. `GF-003` runs only when the register itself writes a deadline into `dueAt`; with `dueAt` empty the rule reports itself in `skipped`. The regulation fixes no number of days and the plugin hard-codes none, so no deadline is ever inferred. A hit means “this does not match the deadline you recorded”, not “this is overdue”. |
| The handling status is filled with a value that is not in the configured list. | `GF-004` reports the row when the `status` value is not among the values you configured in `values`. Shipped, that list is empty, which means unconfigured, so the rule reports itself in `skipped` instead of passing in silence. It checks only whether the value is on your list, not which stage the document is actually at. |
| The same document number appears twice in the register. | `GF-005` requires `docNo` to be unique in the register; whitespace is ignored when comparing. A hit usually means a duplicate registration or a mis-copied number, and needs a human to confirm: a repeated `docNo` leaves the reader unable to tell one document registered twice from two different documents carrying one number. |
| The register itself never declares the document title and receipt date. | `GF-006` requires the header to declare both `title` and `receivedAt` at the top level, and reports the header when either is missing. It checks only that the two are declared, not whether the title is in the correct form, and not whether the handling records really belong to that document. |

## Standards it follows

| Document | Number | Cited by rules |
|---|---|---|
| 《党政机关公文处理工作条例》 | 中办发〔2012〕14号（自 2012 年 7 月 1 日起施行） | GF-001, GF-002, GF-003, GF-004, GF-005, GF-006 |

**Boundary:** this plugin checks a **收文登记与办理环节台账** for what a register can be held to
mechanically — that every step names its handler, that the receipt and completion dates parse and follow
each other, that a completion falls inside the deadline the register itself states, that statuses come from
your vocabulary, that document numbers are unique, and that the header identifies the document. It does
**not** decide whether handling was late, whether it should be chased, or who is accountable. The regulation
requires an urgent document to have **its handling deadline stated** and requires work to finish within a
stated deadline — **it fixes no number of days itself**, so the deadline always comes from the incoming
document or your own rules, and this plugin never invents one.

> ### ⚠️ What the citations in this plugin's report actually rest on
>
> **The regulation's full text has been obtained and checked.** 《党政机关公文处理工作条例》(中办发〔2012〕14号)
> was read verbatim from the central government portal, and `rules/evidence/clause-verification.md` records
> exactly which articles were quoted — article 5 (principles), article 24 (the seven receiving procedures,
> including 「紧急公文应当明确办理时限」) and article 42 (in force from 2012-07-01, superseding two earlier
> documents). That check **corrected this pack's own wording**: it previously said national rules contain only a
> general principle, when article 24 in fact requires an urgent document's deadline to be *stated*.
>
> **The rule `excerpt` fields still say "本次未取得", and every rule remains `warn` or `info`** — deliberately.
> What this plugin checks is whether *a register* is complete and self-consistent; the regulation governs how a
> document is *handled*, which is a different proposition. Labelling "this column is blank" as a `direct`
> citation of "handling shall be recorded in detail" would dress a register gap up as a breach of the regulation,
> which is exactly the over-claim this family exists to avoid. The check also leaves the deadline's size to the
> incoming document and the institution, as article 24 does.
>
> 《党政机关公文格式》(GB/T 9704-2012) **was not obtained**, and this plugin does not check layout in any case.
>
> The deadline rule deserves its own note. `GF-003` compares the completion date against the deadline
> **written in the register itself** (`dueAt`); with no deadline recorded it reports itself in `skipped`
> rather than assuming a number of days. Its finding says "this does not match the deadline you recorded",
> **not** "this is overdue" — lateness depends on reminders, extensions and the document's own urgency.

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a year's register use `ptc` |

## What it does

Registers the `gongwen_flow_check` tool. It reads one handling register — the document's header plus one row
per handling step — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `GF-001` | every step names its handler | warn | principle |
| `GF-002` | receipt and completion dates parse and follow each other | warn | principle |
| `GF-003` | completion falls inside the recorded deadline | info | local |
| `GF-004` | the status comes from your vocabulary (off by default) | info | local |
| `GF-005` | document numbers are unique in the register | warn | principle |
| `GF-006` | the register declares the document title and receipt date | warn | principle |

## Install

```sh
dsh plugin --profile <name> add dsh-gongwen-flow-check
dsh --profile <name> --dump-config | grep 'dsh-gongwen-flow-check'
```

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/gongwen-flow-check.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `GF-003` needs the register's `办理期限` / `dueAt` column; without it the rule does not run and says so.
  The plugin never computes a deadline from a day count.
- `GF-004` `values` — your step vocabulary, e.g. `[待办, 承办中, 已办结, 已归档]`. Empty means no check.
- `GF-001` `field` — the handler column, `handler` by default.

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

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the register's own
column names are kept so a finding names the column it read. Dates may be `2026-03-02` or
`2026-03-02 09:30`.

## Rule sources

Rule data lives in `rules/gongwen-flow-check.yaml`. The pack's header states the citation gap in full, and
each rule's `note` repeats the part that matters for that rule. The load-time guard that normally enforces
"an excerpt must be a real quotation of at least eight characters" cannot tell a quotation from a
description — so this pack leans on the header, the per-rule notes and a test that asserts every `excerpt`
admits the gap.

## Troubleshooting

- **`GF-003` reports itself as skipped.** The register records no deadline. That is deliberate: the plugin
  will not invent one, because the deadline comes from the incoming document or your own handling rules.
- **`GF-003` fires but I consider the handling timely.** The register's `办理期限` disagrees with the
  completion date. Either the deadline column is stale or the completion date is wrong — the finding says
  which two cells it compared.
- **`GF-004` never runs.** Its vocabulary is empty; fill it with your institution's step names.
- **`GF-002` fires on dates I can read.** The reader accepts `2026-03-02` and `2026-03-02 09:30`;
  `2026年3月2日` is reported as unparseable on purpose.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-gongwen-flow-check   # refresh src/shared from ../_shared
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and
the check engine, and the rule pack declares every check.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-gongwen-flow-check contributors.
