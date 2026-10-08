# dsh-gongwen-flow-check — 公文流转与办理时限台账核对

`dsh-gongwen-flow-check` 读取一份收文登记与办理环节台账——公文表头加每个办理环节一行——核对这份台账自身的齐备与自洽：每个环节是否在 `handler` 栏填写承办人、`receivedAt` 与 `doneAt` 是否可解析为日期且先后成立、办结是否落在台账自己写入 `dueAt` 的办理期限之内、每个 `status` 是否取自你配置的取值清单、`docNo` 是否只登记一次、表头是否声明公文标题与收文日期。它不判定办文是否超期、是否应当督办，也不判定由谁负责。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 某个办理环节的承办人漏填了，台账会收到什么提示？ | `GF-001` 要求每个环节都填写 `handler` 栏，并把空着的那一行报出。它只核对这一栏是否填写，不判断办理是否及时——既不判断这个环节是否应当督办，也不判断由谁负责。 |
| 办结日期早于收文日期，能查出来吗？ | 能。`GF-002` 解析 `receivedAt` 与 `doneAt` 两个日期，先后不成立时逐行报出。它只比较台账自己写的这两个日期——同一天视为不晚于——不判断办理是否在时限内。解析不了的日期会单独报出，而不是静默跳过。 |
| 有一行始终没有登记办理期限，插件会假定一个期限吗？ | 不会。`GF-003` 只在台账自己把期限写入 `dueAt` 时运行；`dueAt` 为空则本条报告 `skipped`。条例本身不规定天数，插件也不硬编码任何天数，因此不会替使用方推算期限。命中只表示「与你写在台账里的期限不一致」，不表示「已构成超期未办」。 |
| 办理状态填了一个不在配置清单里的值。 | `GF-004` 在 `status` 所填值不在 `values` 配置清单中时报出该行。出厂时这份清单为空，表示未配置，故本条报告 `skipped`，而不是静默通过。它只核对所填值是否在册，不判断该公文当前实际处于哪个环节。 |
| 同一份公文的文号在台账里出现了两次。 | `GF-005` 要求 `docNo` 在台账内唯一，比较时忽略空白字符。命中通常意味着重复登记或文号抄错，需人工确认：文号重复会让人无法判断，到底是一份公文被登记了两次，还是两份不同公文被错编成了同一号。 |
| 台账本身没有声明公文标题与收文日期。 | `GF-006` 要求顶层同时声明 `title` 与 `receivedAt`，缺一即报出表头。它只核对这两栏是否声明，既不判断标题的形式是否规范，也不判断办理记录是否真的与该公文对应。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
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

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-gongwen-flow-check
dsh --profile <name> --dump-config | grep 'dsh-gongwen-flow-check'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/gongwen-flow-check.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-gongwen-flow-check
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-gongwen-flow-check contributors.
