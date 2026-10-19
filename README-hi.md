# dsh-gongwen-flow-check — राजकीय पत्र प्रवाह और निपटान समय-सीमा रजिस्टर की जाँच

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-gongwen-flow-check` एक प्राप्ति-रजिस्टर और उसके निपटान-चरण बही को पढ़ता है — पत्र का हेडर और प्रत्येक निपटान चरण की एक पंक्ति — और उसी रजिस्टर की पूर्णता तथा आंतरिक संगति जाँचता है: क्या प्रत्येक चरण में `handler` के अंतर्गत निपटान-कर्ता दर्ज है, क्या `receivedAt` और `doneAt` तिथियों के रूप में पढ़े जा सकते हैं और क्रम में हैं, क्या निपटान `dueAt` में रजिस्टर द्वारा ही लिखी समय-सीमा के भीतर है, क्या प्रत्येक `status` आपकी कॉन्फ़िगर की गई सूची से लिया गया है, क्या `docNo` केवल एक बार दर्ज है, और क्या हेडर पत्र का शीर्षक तथा प्राप्ति-तिथि घोषित करता है। यह नहीं तय करता कि निपटान विलंब से हुआ, उसे याद दिलाया जाना चाहिए था, या इसका उत्तरदायी कौन है।

## Install

```sh
dsh plugin --profile <name> add dsh-gongwen-flow-check
dsh --profile <name> --dump-config | grep 'dsh-gongwen-flow-check'
```

## आउटपुट कैसा दिखता है

![Terminal demo of dsh-gongwen-flow-check: real output over its GF-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-gongwen-flow-check/main/docs/assets/dsh-gongwen-flow-check-hero.png)

![Animated terminal demo of dsh-gongwen-flow-check](https://raw.githubusercontent.com/PerryLink/dsh-gongwen-flow-check/main/docs/assets/dsh-gongwen-flow-check-demo.gif)

इस प्लगइन का अपने ही `GF-002` टेस्ट फ़िक्स्चर पर वास्तविक आउटपुट — कोई नकली चित्र नहीं। नियम-पैक उद्धरण नहीं गढ़ता, इसलिए हर निष्कर्ष लागू किए गए खंड का नाम और यह भी बताता है कि उसका मूल पाठ इस बार प्राप्त नहीं हुआ।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| किसी निपटान चरण में निपटान-कर्ता नहीं भरा है। रजिस्टर को क्या बताया जाता है? | `GF-001` हर चरण में `handler` कॉलम की अपेक्षा करता है और जिस पंक्ति में वह खाली है उसे दर्ज करता है। यह केवल देखता है कि कॉलम भरा है या नहीं, यह नहीं कि निपटान समय पर हुआ — यह भी नहीं तय करता कि उस चरण को याद दिलाया जाना चाहिए था या उत्तरदायी कौन है। |
| निपटान की तिथि प्राप्ति की तिथि से पहले है। क्या यह पकड़ में आता है? | हाँ। `GF-002` `receivedAt` की `doneAt` से तुलना करता है और जहाँ दोनों तिथियाँ क्रम में नहीं हैं वह पंक्ति दर्ज करता है। यह केवल बही में लिखी दोनों तिथियों की तुलना करता है — एक ही दिन को बाद का नहीं माना जाता — और यह नहीं आँकता कि निपटान समय-सीमा के भीतर रहा। जो तिथि पढ़ी न जा सके वह चुपचाप छोड़े जाने के बजाय अलग से दर्ज होती है। |
| किसी पंक्ति में निपटान की समय-सीमा कभी दर्ज नहीं है। क्या जाँच कोई सीमा मान लेती है? | नहीं। `GF-003` केवल तब चलता है जब रजिस्टर स्वयं `dueAt` में समय-सीमा लिखता है; `dueAt` खाली होने पर यह नियम स्वयं को `skipped` में दर्ज करता है। नियमावली कोई दिन-संख्या तय नहीं करती और प्लगइन कोई संख्या कठोर-कोडित नहीं करता, इसलिए कोई समय-सीमा अनुमान से नहीं मानी जाती। चेतावनी का अर्थ है «यह आपकी लिखी समय-सीमा से मेल नहीं खाता», «यह विलंब से हुआ» नहीं। |
| निपटान की स्थिति में कॉन्फ़िगर की गई सूची से बाहर का मान भरा है। | `GF-004` उस पंक्ति को दर्ज करता है जिसमें `status` का मान आपके `values` में कॉन्फ़िगर किए गए मानों में नहीं है। फ़ैक्ट्री पर वह सूची खाली रहती है, अर्थात कॉन्फ़िगर नहीं है, इसलिए यह नियम चुपचाप पास होने के बजाय स्वयं को `skipped` में दर्ज करता है। यह केवल देखता है कि मान आपकी सूची में है या नहीं, यह नहीं कि पत्र वास्तव में किस चरण में है। |
| रजिस्टर में एक ही पत्र संख्यांक दो बार आया है। | `GF-005` रजिस्टर में `docNo` के अद्वितीय होने की अपेक्षा करता है; तुलना करते समय श्वेत-स्थान छोड़ दिए जाते हैं। चेतावनी का अर्थ सामान्यतः दोहरा पंजीकरण या ग़लत लिखा संख्यांक है, और इसकी पुष्टि मनुष्य को करनी होती है: `docNo` दोहराने से यह तय नहीं होता कि एक ही पत्र दो बार दर्ज हुआ है या दो भिन्न पत्रों को एक ही संख्यांक दे दिया गया है। |
| रजिस्टर स्वयं पत्र का शीर्षक और प्राप्ति-तिथि घोषित नहीं करता। | `GF-006` शीर्ष स्तर पर `title` और `receivedAt` दोनों घोषित होने की अपेक्षा करता है, और एक भी न हो तो हेडर दर्ज करता है। यह केवल देखता है कि दोनों घोषित हैं, यह नहीं कि शीर्षक का रूप सही है, और यह भी नहीं कि निपटान के अभिलेख वास्तव में उसी पत्र के हैं। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
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

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-rc.2` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` `>=0.2.1-0 <0.3.0` के रूप में घोषित है** और 0.2.1 से होस्ट इसे लागू करता है |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native` और `ptc` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/gongwen-flow-check.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-gongwen-flow-check
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## PerryLink DSH Plugin Family

यह प्रोजेक्ट [PerryLink](https://github.com/PerryLink) के DeepSeek Harness प्लगइन परिवार का हिस्सा है। पूरी सूची नीचे संक्षिप्त रखी गई है ताकि हर README की पहली स्क्रीन छोटी रहे; हर पंक्ति और उसकी स्थिति देखने के लिए इसे खोलें।

<details>
<summary>सभी प्लगइन खोलें</summary>

| प्लगइन | स्थिति |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** |  |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** |  |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** |  |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** |  |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** |  |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** |  |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** |  |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** |  |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** |  |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 फ़्रोज़न — रिपॉज़िटरी README देखें |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 फ़्रोज़न — रिपॉज़िटरी README देखें |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 फ़्रोज़न — रिपॉज़िटरी README देखें |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 फ़्रोज़न — रिपॉज़िटरी README देखें |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 फ़्रोज़न — रिपॉज़िटरी README देखें |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 सेवानिवृत्त — रिपॉज़िटरी README देखें |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 सेवानिवृत्त — रिपॉज़िटरी README देखें |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 सेवानिवृत्त — रिपॉज़िटरी README देखें |

</details>

## License

[Apache License 2.0](LICENSE) © 2026 dsh-gongwen-flow-check contributors.
