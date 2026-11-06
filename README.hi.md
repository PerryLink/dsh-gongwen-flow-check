<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-gongwen-flow-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-gongwen-flow-check-hero-en-light.webp" width="100%" alt="dsh-gongwen-flow-check हीरो: बाईं ओर प्लगइन का नाम, दो मूल्य-पंक्तियाँ और सीमा-टिप्पणी हैं; दाईं ओर एक प्राप्ति-और-निपटान रजिस्टर है (दस्तावेज़ संख्या, शीर्षक, प्राप्ति तिथि, प्रकार और निकाय, तथा एक निपटान पंक्ति जिसका निपटान-कर्ता खाली है, प्राप्ति, समय-सीमा और समापन तिथियों तथा स्थिति के साथ), और नीचे उससे बनी अंतर-सूची: GF-001, एक warn, पंक्ति 1 में निपटान-कर्ता खाली; GF-004, एक skipped, values कॉन्फ़िगर नहीं; गणक skipped 1, warn 1, error 0, और एक मुहर जो कहती है केवल अंतर, कोई निर्णय नहीं">
</picture>

# dsh-gongwen-flow-check

**राजकीय पत्रों के प्राप्ति-और-निपटान रजिस्टर की पंक्ति-दर-पंक्ति जाँच करें — निपटान-कर्ता भरा है, प्राप्ति और समापन तिथियाँ पठनीय और क्रम में हैं, समापन रजिस्टर में लिखी समय-सीमा के भीतर है, स्थितियाँ आपकी सूची से हैं, दस्तावेज़ संख्याएँ अद्वितीय हैं, और हेडर दस्तावेज़ की पहचान करता है — और पाएँ कि क्या असंगत है, कहाँ, और कैसे ठीक करें।**

DeepSeek Harness के लिए जाँच प्लगइन, कार्यालय लिपिकों और पत्र-अधिकारियों के लिए बना: नियम-पैक राजकीय पत्र-प्रबंधन विनियम का शब्दशः उद्धरण देता है, उद्धृत धाराओं के सामने केवल शाब्दिक अंतर बताता है, और न अनुपालन तय करता है, न उत्तरदायित्व, न ही मूल दस्तावेज़ को छूता है।

[इंस्टॉल](#तीन-चरणों-में-शुरुआत) · [कॉन्फ़िगरेशन](#कॉन्फ़िगरेशन) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#संगतता)
[![npm](https://img.shields.io/npm/v/dsh-gongwen-flow-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-gongwen-flow-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-gongwen-flow-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-gongwen-flow-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#संगतता)

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

<sub>सामुदायिक प्लगइन, DeepSeek से असंबद्ध। canonical रिपोज़िटरी: <https://github.com/PerryLink/dsh-gongwen-flow-check> (Gitee एक मिरर है)।</sub>

## यह क्या है

`dsh-gongwen-flow-check` एक प्राप्ति-और-निपटान रजिस्टर पढ़ता है — दस्तावेज़ का हेडर (`docNo`, `title`, `receivedAt` आदि) और प्रत्येक निपटान चरण की एक पंक्ति — और वह जाँचता है जो एक रजिस्टर से यंत्रवत् अपेक्षित किया जा सकता है: क्या प्रत्येक चरण `handler` कॉलम भरता है, क्या `receivedAt` और `doneAt` तिथियों के रूप में पढ़े जा सकते हैं और क्रम में हैं, क्या समापन उस समय-सीमा के भीतर है जो रजिस्टर स्वयं `dueAt` में लिखता है, क्या प्रत्येक `status` उस सूची से है जो आप `values` में कॉन्फ़िगर करते हैं, क्या `docNo` केवल एक बार दर्ज है, और क्या हेडर `title` तथा `receivedAt` दोनों घोषित करता है। आप मूल सामग्री सौंपते हैं (तालिका, रजिस्टर या दस्तावेज़; Excel को पहले JSON/YAML में बदला जा सकता है, प्लेटफ़ॉर्म समर्थन करे तो चैट में भी) और आपको अंतरों की सूची मिलती है: कौन-सी पंक्ति, कौन-सा कॉलम, क्या कम है। यह नहीं तय करता कि निपटान विलंब से हुआ, उसे याद दिलाया जाना चाहिए था, या उत्तरदायी कौन है — और मूल को कभी संशोधित नहीं करता।

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-gongwen-flow-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-gongwen-flow-check-flow-v5-light.svg" width="100%" alt="dsh-gongwen-flow-check संरचना: एक प्राप्ति-और-निपटान रजिस्टर (7 हेडर फ़ील्ड और 8 पंक्ति-कॉलम, उपनाम सामान्यीकृत, कम से कम एक चरण, स्थिति या निपटान-कर्ता कॉलम आवश्यक) एक केवल-पढ़ने वाले बस से छह नियमों को भेजता है। गेटों के ऊपर की पट्टी गंभीरता की सीमा दर्ज करती है: पैक में direct आधार नहीं है, इसलिए error कभी नहीं निकलता; सिद्धांत-आधारित नियम warn तक सीमित हैं (चार) और संस्थागत कॉन्फ़िगरेशन वाले info तक (दो)। साथ दिए नमूने के वास्तविक रन में GF-001 लगता है (पंक्ति 1 में निपटान-कर्ता खाली, warn), GF-004 values सेट न होने के कारण नहीं चलता और skipped में खुद को दर्ज करता है, और GF-002, GF-003, GF-005, GF-006 बिना किसी अंतर के चले और किसी सूची में नहीं आते; तीनों ट्रे एक रिपोर्ट में मिलते हैं (error 0 / warn 1 / info 0, issueCount 1 / skippedCount 1, markdown + reportJson)। रिपोर्ट केवल अंतर बताती है, निर्णय समीक्षक के पास रहता है, और मूल कभी संशोधित नहीं होता">
</picture>

## तीन चरणों में शुरुआत

1. **इंस्टॉल करें**:

   ```sh
   dsh plugin --profile <name> add dsh-gongwen-flow-check
   ```

   वैकल्पिक रूप से, WorkBuddy / Coze में «Documents and Governance Suite» खोजें (पूरा सेट; यह जाँच उसका एक हिस्सा है; उपलब्धता स्टोर के अनुसार)।

2. **न्यूनतम कॉन्फ़िगरेशन** (डिफ़ॉल्ट पर ही काम करता है):

   ```yaml
   - insert:
       - id: dsh-gongwen-flow-check
         name: dsh-gongwen-flow-check
   ```

   सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं और डिफ़ॉल्ट तैयार हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

3. **जाँचें कि माउंट हुआ**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-gongwen-flow-check'
   ```

   फिर bundled सैंपल चलाएँ (रिपॉज़िटरी के भीतर पहले बिल्ड करें; लगभग एक मिनट):

   ```sh
   pnpm run build
   node samples/quickstart/run.mjs
   ```

   सैंपल इनपुट `samples/quickstart/input/` में है, अपेक्षित आउटपुट `samples/quickstart/expected/result.json` में, और रन की स्क्रीनशॉट `docs/assets/quickstart.png` में।

**अनइंस्टॉल**: `dsh plugin --profile <name> remove dsh-gongwen-flow-check` (या profile patch से वह पंक्ति हटाएँ)।

<details>
<summary>DSH Desktop मार्केट से इंस्टॉल करें</summary>

सभी PerryLink प्लगइन DSH Desktop के अंतर्निहित मार्केट में ब्राउज़ किए जा सकते हैं: **Market → Sources → Add source → पेस्ट करें** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ चुनें**। इंस्टॉलेशन के लिए मार्केट की npm पहचान-जाँच और आपकी पुष्टि आवश्यक रहती है।

</details>

## मुख्य क्षमताएँ

यह प्लगइन `gongwen_flow_check` टूल रजिस्टर करता है: एक रजिस्टर (दस्तावेज़ हेडर और निपटान-चरण पंक्तियाँ) पढ़ता है, एक संस्करणित नियम-पैक लागू करता है, और एक संरचित रिपोर्ट लौटाता है।

- **नियम-पैक डेटा है, कोड नहीं** — सभी नियम `rules/gongwen-flow-check.yaml` में हैं; फ़ाइल बदलते ही नियम-सेट बदल जाता है, TypeScript छूने की ज़रूरत नहीं; पैक लोड के समय सत्यापित होता है, भरोसा नहीं किया जाता।
- **गंभीरता साक्ष्य के अनुसार** — सामान्य सिद्धांत पर आधारित नियम (`derived-from-principle`) की अधिकतम सीमा `warn`; आपकी संस्था के कॉन्फ़िगरेशन पर आधारित (`institutional-configuration`) की सीमा `info`; किसी को भी `error` घोषित नहीं किया जा सकता (एक टेस्ट इसका दावा करता है)।
- **खाली सूची कभी «सब ठीक» नहीं** — जो जाँच न चल सकी वह `skipped` में कारण सहित स्वयं दर्ज करती है; जब `GF-004` की शब्दावली सेट नहीं है, नियम चुपचाप पास होने के बजाय `skipped` में रिपोर्ट करता है।
- **कोई निर्णय नहीं** — रिपोर्ट केवल अंतर सूचीबद्ध करती है; अनुपालन, उत्तरदायित्व या शुद्धता पर कभी टिप्पणी नहीं; शब्दावली-गार्ड रिपोर्ट में हमेशा अस्वीकरण रखने को बाध्य करता है।
- **उद्धरण केवल शब्दशः** — प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन में धारा, शब्दशः उद्धरण और वह URL होता है जहाँ से पढ़ा गया; पुनर्कथन को उद्धरण बताना, या असत्यापनीय आधार को `error` बताना, लोड पर विफल होता है।

```text
रजिस्टर (हेडर · निपटान पंक्तियाँ) ──gongwen_flow_check──▶ नियम GF-001…GF-006 ──▶ रिपोर्ट (findings + skipped)
              ▲                                                                                │
              └──────────────────────────── मूल कभी संशोधित नहीं होता ──────────────────────────┘
```

### नियम एक नज़र में

| नियम | जाँच | गंभीरता | आधार का प्रकार |
|---|---|---|---|
| `GF-001` | प्रत्येक निपटान चरण अपना निपटान-कर्ता भरता है | warn | सिद्धांत |
| `GF-002` | प्राप्ति और समापन तिथियाँ पठनीय और क्रम में हैं | warn | सिद्धांत |
| `GF-003` | समापन रजिस्टर में लिखी समय-सीमा के भीतर है | info | स्थानीय |
| `GF-004` | स्थिति आपकी शब्दावली से है (डिफ़ॉल्ट बंद) | info | स्थानीय |
| `GF-005` | दस्तावेज़ संख्याएँ रजिस्टर में अद्वितीय हैं | warn | सिद्धांत |
| `GF-006` | रजिस्टर हेडर शीर्षक और प्राप्ति-तिथि घोषित करता है | warn | सिद्धांत |

### उदाहरण

ये प्लगइन के वास्तविक प्रवेश-बिंदु हैं; एक बार इंस्टॉल करें, फिर एक को कॉल करें।

**विस्तृत आउटपुट** — टूल `gongwen_flow_check`, इनपुट (अंश):

```json
{"rows":[{"办理环节":"承办","承办人":"张科","收文日期":"2026-03-02","办理期限":"2026-03-12","办结日期":"2026-02-28"}]}
```

आउटपुट:

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

*स्रोत `tests/fixtures/GF-002/GF-002-unsafe.json (cases.json expects GF-002 count 1); run via lib/index.mjs rules/gongwen-flow-check.yaml`*

### यह किन सवालों का जवाब देता है

| आप पूछते हैं | यह क्या उत्तर देता है |
|---|---|
| किसी निपटान चरण में निपटान-कर्ता नहीं भरा गया। रजिस्टर को क्या बताया जाता है? | `GF-001` प्रत्येक चरण में `handler` कॉलम अनिवार्य करता है और वह पंक्ति बताता है जहाँ यह खाली है। यह केवल यह जाँचता है कि कॉलम भरा है या नहीं, यह नहीं कि निपटान समय पर हुआ — यह नहीं तय करता कि उस चरण को याद दिलाया जाना चाहिए था या उत्तरदायी कौन है। |
| समापन तिथि प्राप्ति तिथि से पहले है। क्या यह पकड़ा जाता है? | हाँ। `GF-002` `receivedAt` की `doneAt` से तुलना करता है और पंक्ति बताता है जब दोनों तिथियाँ क्रम में नहीं हैं। यह केवल रजिस्टर में लिखी दो तिथियों की तुलना करता है — एक ही दिन को बाद नहीं माना जाता — और यह नहीं आँकता कि निपटान समय-सीमा के भीतर रहा। जो तिथि पढ़ी नहीं जा सकती, वह चुपचाप छोड़े जाने के बजाय अलग से बताई जाती है। |
| किसी पंक्ति में कभी निपटान समय-सीमा दर्ज नहीं है। क्या जाँच कोई सीमा मान लेती है? | नहीं। `GF-003` केवल तब चलता है जब रजिस्टर स्वयं `dueAt` में समय-सीमा लिखता है; `dueAt` खाली होने पर नियम स्वयं को `skipped` में बताता है। विनियम कोई दिन-संख्या तय नहीं करता और प्लगइन कोई संख्या हार्ड-कोड नहीं करता, इसलिए कोई समय-सीमा कभी अनुमानित नहीं होती। चेतावनी का अर्थ है «यह आपके दर्ज किए समय-सीमा से मेल नहीं खाता», «यह विलंबित है» नहीं। |
| निपटान स्थिति में ऐसा मान भरा गया है जो कॉन्फ़िगर की गई सूची में नहीं है। | `GF-004` तब पंक्ति बताता है जब `status` का मान आपके `values` में कॉन्फ़िगर किए मानों में न हो। फ़ैक्ट्री पर यह सूची खाली है, यानी बिना कॉन्फ़िगरेशन, इसलिए नियम चुपचाप पास होने के बजाय स्वयं को `skipped` में बताता है। यह केवल यह जाँचता है कि मान आपकी सूची में है या नहीं, यह नहीं कि दस्तावेज़ वास्तव में किस चरण में है। |
| वही दस्तावेज़ संख्या रजिस्टर में दो बार आती है। | `GF-005` रजिस्टर में `docNo` अद्वितीय होने की अपेक्षा करता है; तुलना में श्वेत-स्थान अनदेखा होता है। चेतावनी का अर्थ आम तौर पर दोहरा पंजीकरण या गलत लिखी संख्या है, और मानवीय पुष्टि आवश्यक है: दोहराया गया `docNo` यह बताना असंभव बनाता है कि एक ही दस्तावेज़ दो बार दर्ज हुआ या दो भिन्न दस्तावेज़ों को एक ही संख्या दी गई। |
| रजिस्टर स्वयं दस्तावेज़ का शीर्षक और प्राप्ति-तिथि घोषित नहीं करता। | `GF-006` शीर्ष स्तर पर `title` और `receivedAt` दोनों घोषित होने की अपेक्षा करता है और किसी के भी अनुपस्थित होने पर हेडर बताता है। यह केवल यह जाँचता है कि दोनों घोषित हैं, यह नहीं कि शीर्षक का रूप सही है, और यह नहीं कि निपटान अभिलेख वास्तव में उसी दस्तावेज़ के हैं। |

## कॉन्फ़िगरेशन

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए `cordis.yml` से बदले जा सकते हैं, कोड छूने की ज़रूरत नहीं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं। नीचे की पाँच कुंजियाँ पूरी सूची हैं; नियम-स्तरीय पैरामीटर इसके बाद हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/gongwen-flow-check.yaml` | नियम-पैक पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली का अर्थ सभी नियम |
| `skipNotes` | string | `""` | हर `skipped` कारण के साथ जोड़ा जाने वाला नोट |
| `timeoutMs` | number | `120000` | टूल का सहयोगी टाइमआउट बजट |

जानने योग्य नियम-स्तरीय पैरामीटर:

- `GF-001` `field` — निपटान-कर्ता कॉलम, डिफ़ॉल्ट `handler`।
- `GF-003` `dueAt` — रजिस्टर का निपटान-समय-सीमा कॉलम; समय-सीमा दर्ज न होने पर नियम `skipped` में जाता है, और प्लगइन कभी दिन-गणना से समय-सीमा नहीं निकालता।
- `GF-004` `values` — आपकी चरण-शब्दावली, जैसे `[待办, 承办中, 已办结, 已归档]`; खाली का अर्थ बिना कॉन्फ़िगरेशन, नियम नहीं चलता।
- `GF-005` — `docNo` की तुलना में श्वेत-स्थान अनदेखा होता है।

profile patch में ओवरराइड का उदाहरण:

```yaml
- insert:
    - id: dsh-gongwen-flow-check
      name: dsh-gongwen-flow-check
      config:
        disabledRules: [GF-004]
        onlyRules: [GF-001, GF-002, GF-003]
        skipNotes: इस संस्था के अपने नियम इस जाँच का आधार हैं
```

## FAQ

<details>
<summary>क्या मेरी सामग्री बदली या कहीं अपलोड होती है?</summary>

नहीं। टूल केवल आपके दिए JSON/YAML सामग्री टेक्स्ट (`file` या `material`, दोनों में से एक) पढ़ता है और **मूल को कभी संशोधित नहीं करता**; प्लगइन शुद्ध ESM है, कोई नेटिव कोड नहीं, **कोई नेटवर्क नहीं और कोई मॉडल कॉल नहीं** (संगतता देखें), इसलिए सामग्री आपकी मशीन से बाहर नहीं जाती।

</details>

<details>
<summary>स्थिति-सूची और समय-सीमा दोनों सेट न हों तो क्या कुछ चुपचाप पास हो जाता है?</summary>

नहीं। `GF-004` के `values` और `GF-003` को आवश्यक `dueAt` दोनों फ़ैक्ट्री पर सेट नहीं होते, और जो जाँच नहीं चल सकती वह कारण सहित स्वयं को `skipped` में बताती है — खाली अंतर-सूची को «कुछ गलत नहीं» नहीं पढ़ा जाता। `GF-004` केवल यह जाँचता है कि मान आपकी सूची में है, यह नहीं कि दस्तावेज़ वास्तव में किस चरण में है।

</details>

<details>
<summary>क्या प्लगइन तय करता है कि निपटान «विलंबित» है?</summary>

नहीं। `GF-003` समापन तिथि की तुलना **रजिस्टर में ही लिखी** समय-सीमा (`dueAt`) से करता है; समय-सीमा दर्ज न होने पर वह दिन-संख्या मान लेने के बजाय `skipped` बताता है। विनियम आवश्यक करता है कि अत्यावश्यक दस्तावेज़ **अपनी समय-सीमा स्पष्ट रूप से लिखे** और निर्धारित समय-सीमा में पूरा हो, पर **स्वयं कोई दिन-संख्या तय नहीं करता** — समय-सीमा सदैव आने वाले दस्तावेज़ या आपकी संस्था से आती है, और प्लगइन कभी उसे गढ़ता नहीं। चेतावनी का अर्थ है «यह दर्ज समय-सीमा से मेल नहीं खाता», **«यह विलंबित है» नहीं**: विलंबता याद-दिलाने, विस्तार और दस्तावेज़ की अपनी तात्कालिकता पर भी निर्भर है।

</details>

<details>
<summary>कौन-से दिनांक प्रारूप पढ़े जाते हैं? समय में बदलाव क्यों दिखता है?</summary>

रीडर `2026-03-02` और `2026-03-02 09:30` स्वीकार करता है; चीनी अंकों में लिखी तिथि जानबूझकर अपठनीय बताई जाती है, ताकि आप तय कर सकें कि निर्यात को सामान्य करना है या नहीं। सारा गणित इनपुट स्ट्रिंग्स पर वॉल-क्लॉक है, कोई समय-क्षेत्र रूपांतरण नहीं।

</details>

<details>
<summary>प्लगइन इंस्टॉल हो गया पर टूल नहीं दिखता, या इंस्टॉल संस्करण-असंगत कहकर अस्वीकार हो जाता है — क्या करें?</summary>

जाँचें कि `main` `lib/index.mjs` पर resolves होता है और `pnpm run build` ने उसे बनाया है; गलत `main` लोडर को प्रविष्टि चुपचाप छोड़ने पर मजबूर करता है। peer रेंज `0.1.x` और `0.2.x` पंक्तियों को कवर करती है; यदि आपका runtime उससे बाहर है, तो स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`. peer संगतता runtime इंस्टॉल के समय लागू करता है।

</details>

## जिन मानकों का पालन होता है

| दस्तावेज़ | संख्या | इसे उद्धृत करने वाले नियम |
|---|---|---|
| पार्टी और राज्य के अंगों के राजकीय पत्र-प्रबंधन विनियम | 中办发〔2012〕14号 (2012-07-01 से प्रभावी) | GF-001, GF-002, GF-003, GF-004, GF-005, GF-006 |

उद्धृत दस्तावेज़ों के मूल शीर्षक:

```text
《党政机关公文处理工作条例》 中办发〔2012〕14号（自 2012 年 7 月 1 日起施行）
```

**सीमा:** यह प्लगइन एक **प्राप्ति-और-निपटान रजिस्टर** की वह जाँच करता है जो एक रजिस्टर से यंत्रवत् अपेक्षित है — कि प्रत्येक चरण अपना निपटान-कर्ता बताए, प्राप्ति और समापन तिथियाँ पठनीय और क्रम में हों, समापन रजिस्टर में लिखी समय-सीमा के भीतर हो, स्थितियाँ आपकी शब्दावली से हों, दस्तावेज़ संख्याएँ अद्वितीय हों और हेडर दस्तावेज़ की पहचान करे। यह **नहीं** तय करता कि निपटान विलंबित हुआ, उसे याद दिलाया जाना चाहिए था, या उत्तरदायी कौन है। विनियम आवश्यक करता है कि अत्यावश्यक दस्तावेज़ **अपनी समय-सीमा स्पष्ट रूप से लिखे** और निर्धारित समय-सीमा में पूरा हो — **वह स्वयं कोई दिन-संख्या तय नहीं करता**, इसलिए समय-सीमा सदैव आने वाले दस्तावेज़ या आपके अपने नियमों से आती है, और यह प्लगइन कभी उसे नहीं गढ़ता।

> ### ⚠️ इस प्लगइन की रिपोर्ट के उद्धरण वास्तव में किस पर आधारित हैं
>
> **विनियम का पूरा पाठ प्राप्त और जाँचा जा चुका है।** राजकीय पत्र-प्रबंधन विनियम (中办发〔2012〕14号)
> केंद्रीय सरकार पोर्टल से शब्दशः पढ़ा गया, और `rules/evidence/` के सत्यापन रिकॉर्ड उन धाराओं को
> दर्ज करते हैं: धारा 5 (सिद्धांत), धारा 23 (पत्र-प्रबंधन का दायरा), धारा 24 (सात प्राप्ति प्रक्रियाएँ,
> जिनमें «अत्यावश्यक पत्रों की निपटान समय-सीमा स्पष्ट होनी चाहिए» शामिल है) और धारा 42 (2012-07-01 से
> प्रभावी, दो पूर्व दस्तावेज़ों का स्थान लेती है)। नियम-पैक के `excerpt` अब शब्दशः उद्धरण रखते हैं, और
> `pnpm run check:citations` प्रत्येक खंड की तुलना साक्ष्य-रिकॉर्ड से करता है: वर्तमान में 10 खंड जाँचे,
> 0 अ-अनुरेखणीय, आधार 0।
>
> **फिर भी प्रत्येक नियम `warn` या `info` ही है, और किसी `kind` को `direct` नहीं बनाया गया** — यह जानबूझकर
> है। यह प्लगइन देखता है कि *एक रजिस्टर* पूरा और सुसंगत है या नहीं; विनियम यह नियंत्रित करता है कि
> दस्तावेज़ *निपटाया* कैसे जाए, जो दूसरा प्रस्ताव है। «यह कॉलम खाली है» को «निपटान का विस्तृत अभिलेख
> रखा जाए» का `direct` उद्धरण कहना रजिस्टर की कमी को विनियम का उल्लंघन बना देगा — ठीक वही अति-दावा
> जिससे यह परिवार बचता है। जाँच समय-सीमा की अवधि आने वाले दस्तावेज़ और संस्था पर छोड़ती है, जैसे धारा 24
> करती है।
>
> राजकीय पत्रों का **प्रारूप** मानक (GB/T 9704-2012) **प्राप्त नहीं हुआ**, और यह प्लगइन किसी भी स्थिति में
> लेआउट की जाँच नहीं करता।
>
> समय-सीमा नियम पर अलग टिप्पणी आवश्यक है। `GF-003` समापन तिथि की तुलना **रजिस्टर में ही लिखी** समय-सीमा
> (`dueAt`) से करता है; समय-सीमा दर्ज न होने पर वह दिन-संख्या मानने के बजाय स्वयं को `skipped` में बताता
> है। उसका निष्कर्ष कहता है «यह आपके दर्ज समय-सीमा से मेल नहीं खाता», **«यह विलंबित है» नहीं** — विलंबता
> याद-दिलाने, विस्तार और दस्तावेज़ की तात्कालिकता पर निर्भर है।

## सामग्री का प्रारूप

टूल JSON या YAML स्वीकार करता है:

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

कॉलम नाम केस-असंवेदी हैं और रिक्त स्थान, अंडरस्कोर तथा हाइफ़न अनदेखे होते हैं; रजिस्टर के अपने कॉलम नाम सुरक्षित रहते हैं, इसलिए निष्कर्ष बताता है कि उसने कौन-सा कॉलम पढ़ा। तिथियाँ `2026-03-02` या `2026-03-02 09:30` हो सकती हैं। संख्याएँ स्ट्रिंग के रूप में स्वीकार्य हैं, इसलिए स्प्रेडशीट निर्यात को साफ़ करने की ज़रूरत नहीं।

## नियमों के स्रोत

नियमों का डेटा `rules/gongwen-flow-check.yaml` में, कोड से अलग रहता है। प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन में धारा, शब्दशः उद्धरण और वह URL होता है जहाँ से उद्धरण पढ़ा गया। लोडर अनिवार्य करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और सामान्य सिद्धांत (`kind: derived-from-principle`, सीमा `warn`) या स्थानीय नीति (`kind: institutional-configuration`, सीमा `info`) पर आधारित जाँच **कभी** `error` घोषित न हो। अपने आधार को बढ़ा-चढ़ाकर बताने वाला पैक लोड पर विफल होता है, ऐसी रिपोर्ट नहीं बनाता जो अपने साक्ष्य से अधिक विश्वासपूर्ण लगे।

पैक का हेडर उद्धरण-अनुशासन बताता है; प्रत्येक नियम का `note` उसका आधार और वे निष्कर्ष समझाता है जो वह जानबूझकर नहीं निकालता; `rules/evidence/` धारा-सत्यापन रिकॉर्ड रखता है; और `pnpm run check:citations` प्रत्येक `excerpt` खंड की तुलना उस साक्ष्य से करता है (वर्तमान में 10 खंड जाँचे, 0 अ-अनुरेखणीय, आधार 0)। `GF-003` का `note` अलग से दर्ज करता है कि विनियम समय-सीमा की अवधि आने वाले दस्तावेज़ और संस्था पर छोड़ता है, और प्लगइन कोई दिन-संख्या हार्ड-कोड नहीं करता।

## संगतता

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-rc.2` दोनों स्वीकार करने के लिए सत्यापित। `engines.dsh` `>=0.2.1-0 <0.3.0` के रूप में घोषित है और 0.2.1 से होस्ट इसे लागू करता है |
| Node | `^22.19.0 \|\| >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native` और `ptc` दोनों में काम करता है; पूरे वर्ष के रजिस्टर के लिए `ptc` |

## समस्या-निवारण

- **`GF-003` स्वयं को skipped बताता है।** रजिस्टर में कोई समय-सीमा दर्ज नहीं है। यह जानबूझकर है: प्लगइन उसे नहीं गढ़ता, क्योंकि समय-सीमा आने वाले दस्तावेज़ या आपके निपटान नियमों से आती है।
- **`GF-003` चलता है पर मुझे निपटान समय पर लगता है।** रजिस्टर की समय-सीमा और समापन तिथि में अंतर है। या समय-सीमा कॉलम पुराना है या समापन तिथि गलत — निष्कर्ष उन दो सेलों को बताता है जिनकी तुलना की गई।
- **`GF-004` कभी नहीं चलता।** उसकी शब्दावली खाली है; अपनी संस्था के चरण-नाम भरें।
- **`GF-002` उन तिथियों पर चलता है जो मैं पढ़ सकता हूँ।** रीडर `2026-03-02` और `2026-03-02 09:30` स्वीकार करता है; चीनी अंकों में लिखी तिथि जानबूझकर अपठनीय बताई जाती है।
- **प्लगइन इंस्टॉल हो गया पर टूल नहीं दिखता।** जाँचें कि `main` `lib/index.mjs` पर resolves होता है और `pnpm run build` ने उसे बनाया है; गलत `main` लोडर को प्रविष्टि चुपचाप छोड़ने पर मजबूर करता है।
- **`dsh plugin add` पैकेज को असंगत कहकर अस्वीकार करता है।** peer रेंज `0.1.x` और `0.2.x` को कवर करती है; यदि आपका runtime उससे बाहर है, तो स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` में `manifest-peers` विफल बताया जाता है।** स्थिर जाँचकर्ता 0.2 पंक्ति से पहले के हार्ड-कोडेड peer रेंज से तुलना करता है। runtime इंस्टॉल के समय peer संगतता लागू करता है, इसलिए घोषित रेंज सही है; यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है।
- **समय खिसका हुआ लगता है।** सारा गणित इनपुट स्ट्रिंग्स पर वॉल-क्लॉक है, कोई समय-क्षेत्र रूपांतरण नहीं।

## पारिस्थितिकी और गुणवत्ता

- [Gitee मिरर](https://gitee.com/perrylink/dsh-gongwen-flow-check) (समन्वित मिरर; GitHub canonical है)
- [dshfind प्लगइन पृष्ठ](https://dshfind.com/plugins/PerryLink/dsh-gongwen-flow-check) (इंस्टॉल और रैंकिंग)
- [OpenSSF Scorecard रिपोर्ट](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-gongwen-flow-check) ([.github/workflows/scorecard.yml](.github/workflows/scorecard.yml) द्वारा संचालित)
- [DSH Market](https://dsh.market/) (सूचीबद्ध)
- [पारिस्थितिकी ज्ञान-आधार — सामग्री के अनुसार जाँचकर्ता चुनें](https://perrylink.github.io/zh/checkers/choose/) (पूरा परिवार सूचकांक: 62 जाँचकर्ता + सामान्य प्लगइन)

## विकास

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, साझा टेबल-प्लगइन सूट + प्रति-नियम युग्मित फ़िक्स्चर (tests/fixtures/<RULE>/)
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes     # पाँच भाषाओं के README की संगति
pnpm run check:citations   # प्रत्येक नियम-उद्धरण की rules/evidence/ से तुलना
node ../scripts/sync-shared.mjs dsh-gongwen-flow-check   # ../_shared से src/shared ताज़ा करें
```

प्लगइन **डेटा-संचालित** है: `src/model.ts` तालिका का आकार घोषित करता है, साझा किट रीडर और जाँच-इंजन देता है, और नियम-पैक प्रत्येक जाँच घोषित करता है। TypeScript छुए बिना नियम-सेट बदलने के लिए `rules/*.yaml` संपादित करें; पैक लोड के समय सत्यापित होता है, भरोसा नहीं किया जाता। README की छवियाँ [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) से प्रोग्रामीक रूप से बनती हैं और सुरक्षित रूप से दोबारा चलाई जा सकती हैं: hero बैनर Pillow से (zh / en × हल्का / गहरा, चार फ़ाइलें) और संरचना-आरेख हाथ से लिखा SVG (हल्का और गहरा, कमांड-सतह टोकन, नमूने के वास्तविक मान और संक्षिप्त टिप्पणियों के साथ)। पुराना एकल-रूप प्रवाह-आरेख, पुराना hero और डेमो छवियाँ बाहरी लिंक के लिए `docs/assets/` में रहती हैं; README केवल नया hero सेट और flow-v5 युग्म संदर्भित करता है।

## परिवार और आभार

यह परियोजना [PerryLink](https://github.com/PerryLink) द्वारा अनुरक्षित DeepSeek Harness प्लगइन परिवार का हिस्सा है (सभी Apache-2.0)। यदि यह प्लगइन उपयोगी है, तो **एक स्टार** कुछ अनलॉक नहीं करता, पर अगले व्यक्ति को इसे खोजना आसान बनाता है।

- [@PerryLink](https://github.com/PerryLink) — निर्माता और अनुरक्षक: `gongwen_flow_check` टूल, शब्दशः उद्धृत नियम-पैक और उसका धारा-सत्यापन रिकॉर्ड, तथा पाँच-भाषा दस्तावेज़।

<details>
<summary>सभी प्लगइन विस्तारित करें</summary>

| प्लगइन | स्थिति |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 फ़्रोज़न — रेपो README देखें |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 फ़्रोज़न — रेपो README देखें |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 फ़्रोज़न — रेपो README देखें |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |

</details>

## लाइसेंस

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-gongwen-flow-check contributors

<p align="center"><sub>Apache-2.0 · सामुदायिक प्लगइन, DeepSeek से असंबद्ध।</sub></p>
