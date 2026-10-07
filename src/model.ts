/**
 * dsh-gongwen-flow-check — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'gongwen_flow_check'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  seq: ['序号', '环节序号', '步骤', 'seq', 'step'],
  stage: ['办理环节', '环节', '流程环节', 'stage'],
  handler: ['承办人', '办理人', '责任人', 'handler', 'owner'],
  receivedAt: ['收文日期', '登记日期', 'receiptDate', 'receivedAt'],
  dueAt: ['办理期限', '期限', '应办结日期', 'dueAt', 'deadline'],
  doneAt: ['办结日期', '完成日期', 'doneAt', 'completedAt'],
  status: ['办理状态', '状态', 'status'],
  note: ['备注', '说明', 'note', 'remark'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'steps', 'items', '环节'],
  columns: COLUMNS,
  header: {
  docNo: ['docNo', '发文字号', '文件编号'],
  title: ['title', '文件标题', '公文标题'],
  docKind: ['docKind', '文种', '公文种类'],
  issuer: ['issuer', '发文机关', '制发机关'],
  receivedAt: ['receivedAt', '收文日期', '登记日期'],
  dueAt: ['dueAt', '办理期限', '应办结日期'],
  urgent: ['urgent', '紧急程度', '缓急'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '办理环节',
  'stage',
  '办理状态',
  'status',
  '承办人',
  'handler',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
