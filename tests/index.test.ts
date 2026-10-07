import { describeTablePlugin } from './table-plugin-suite.ts'
import { Config } from '../src/config.ts'
import { parseMaterial, runCheck, SPEC } from '../src/model.ts'
import { buildView } from '../src/view.ts'
import { inject, name, resolvePackageFile, TOOL_NAME } from '../src/index.ts'

describeTablePlugin({
  name,
  inject,
  TOOL_NAME,
  resolvePackageFile,
  Config,
  rulesFile: 'rules/gongwen-flow-check.yaml',
  parseMaterial,
  runCheck,
  buildView,
  columnNames: SPEC.columns,
  samples: {
    good: {
      docNo: '某发〔2026〕15号',
      title: '关于某某工作的通知',
      docKind: '通知',
      issuer: '某某机关',
      receivedAt: '2026-03-02',
      rows: [
        {
          序号: '1',
          办理环节: '承办',
          承办人: '张科',
          收文日期: '2026-03-02',
          办理期限: '2026-03-12',
          办结日期: '2026-03-10',
          办理状态: '已办结',
        },
      ],
    },
    unknownColumn: { rows: [{ 备注: '甲' }] },
  },
})
