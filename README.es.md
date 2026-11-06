<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-gongwen-flow-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-gongwen-flow-check-hero-en-light.webp" width="100%" alt="dsh-gongwen-flow-check, portada: la columna izquierda lleva el nombre del plugin, dos líneas de valor y la nota de límites; a la derecha hay un registro de recepción y tramitación (número de documento, título, fecha de recepción, tipo y organismo, más una fila de tramitación cuyo responsable está vacío, con fechas de recepción, plazo y cierre, y un estado) y, debajo, la lista de diferencias que produce: GF-001, un aviso warn, fila 1 sin responsable; GF-004, un skipped, values sin configurar; contadores skipped 1, warn 1, error 0, con un sello que dice solo diferencias, nunca un veredicto">
</picture>

# dsh-gongwen-flow-check

**Comprueba fila a fila un registro de recepción y tramitación de documentos oficiales —responsable consignado, fechas de recepción y cierre legibles y en orden, cierre dentro del plazo anotado, estados según tu vocabulario, números de documento únicos y cabecera que identifica el documento— y recibe una lista de qué es incoherente, dónde y cómo corregirlo.**

Un plugin de comprobación para DeepSeek Harness, pensado para secretaría y personal de oficina: el paquete de reglas cita literalmente el reglamento de tratamiento de documentos oficiales, solo señala diferencias literales frente a las cláusulas citadas, y nunca decide conformidad, nunca atribuye responsabilidad y nunca toca el original.

[Instalar](#instalación-en-tres-pasos) · [Configuración](#configuración) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidad)
[![npm](https://img.shields.io/npm/v/dsh-gongwen-flow-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-gongwen-flow-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-gongwen-flow-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-gongwen-flow-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidad)

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

<sub>Plugin de la comunidad, no afiliado a DeepSeek. Repositorio canónico: <https://github.com/PerryLink/dsh-gongwen-flow-check> (Gitee es un espejo).</sub>

## Qué es

`dsh-gongwen-flow-check` lee un registro de recepción y tramitación —la cabecera del documento (`docNo`, `title`, `receivedAt`, etc.) más una fila por fase de tramitación— y comprueba lo que un registro puede sostener mecánicamente: que cada fase rellene la columna `handler`, que `receivedAt` y `doneAt` se analicen como fechas y sean sucesivas, que el cierre caiga dentro del plazo que el propio registro anota en `dueAt`, que cada `status` proceda del vocabulario que configures en `values`, que `docNo` se registre una sola vez y que la cabecera declare `title` y `receivedAt`. Usted entrega el material original (una tabla, un registro o un documento; Excel puede convertirse antes a JSON/YAML, incluso en el chat si la plataforma lo permite) y recibe una lista de diferencias: qué fila, qué columna, qué falta. No decide si la tramitación llegó tarde, si debía reclamarse ni quién es responsable, y jamás modifica el original.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-gongwen-flow-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-gongwen-flow-check-flow-v5-light.svg" width="100%" alt="Estructura de dsh-gongwen-flow-check: un registro de recepción y tramitación (7 campos de cabecera y 8 columnas de fila, alias normalizados, se exige al menos una columna de fase, estado o responsable) alimenta seis reglas por un bus de solo lectura. La barra sobre las compuertas fija el techo de gravedad: el paquete no tiene base direct, así que error nunca se emite; las reglas basadas en principios se limitan a warn (cuatro) y las de configuración institucional a info (dos). En la ejecución real de la muestra, GF-001 salta (fila 1 sin responsable, warn), GF-004 no puede ejecutarse porque values no está configurado y se declara en skipped, y GF-002, GF-003, GF-005 y GF-006 se ejecutaron sin hallazgos y no entran en ninguna lista; las tres bandejas confluyen en un informe (error 0 / warn 1 / info 0, issueCount 1 / skippedCount 1, markdown + reportJson). El informe solo enumera diferencias, el veredicto queda en el revisor y el original nunca se modifica">
</picture>

## Instalación en tres pasos

1. **Instala**:

   ```sh
   dsh plugin --profile <name> add dsh-gongwen-flow-check
   ```

   También puedes buscar «Documents and Governance Suite» en WorkBuddy / Coze (el conjunto completo; esta comprobación es una parte; disponibilidad según la tienda).

2. **Configuración mínima** (funciona con los valores por defecto):

   ```yaml
   - insert:
       - id: dsh-gongwen-flow-check
         name: dsh-gongwen-flow-check
   ```

   Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts` y los valores por defecto están listos para usar; los umbrales por regla están en el paquete de reglas bajo `rules/`.

3. **Verifica que se monta**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-gongwen-flow-check'
   ```

   Después ejecuta el ejemplo incluido (compila antes dentro del repositorio; aproximadamente un minuto):

   ```sh
   pnpm run build
   node samples/quickstart/run.mjs
   ```

   La entrada de ejemplo está en `samples/quickstart/input/`, la salida esperada en `samples/quickstart/expected/result.json` y una captura de la ejecución en `docs/assets/quickstart.png`.

**Desinstalar**: `dsh plugin --profile <name> remove dsh-gongwen-flow-check` (o elimina la fila del patch del perfil).

<details>
<summary>Instalar desde el mercado de DSH Desktop</summary>

Todos los plugins de PerryLink pueden explorarse en el mercado integrado de DSH Desktop: **Market → Sources → Add source → pegar** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ seleccionarlo**. La instalación sigue pasando por la verificación de identidad npm del mercado y tu confirmación.

</details>

## Capacidades clave

El plugin registra la herramienta `gongwen_flow_check`: lee un registro (cabecera del documento y filas de tramitación), aplica un paquete de reglas versionado y devuelve un informe estructurado.

- **El paquete de reglas es dato, no código** — todas las reglas viven en `rules/gongwen-flow-check.yaml`; cambiar el archivo cambia el conjunto de reglas sin tocar TypeScript, y el paquete se valida al cargar, no se confía en él.
- **La severidad sigue a la evidencia** — una regla basada en un principio general (`derived-from-principle`) tiene tope `warn`; una basada en la configuración de tu institución (`institutional-configuration`) tiene tope `info`; ninguna puede declararse `error` (un test lo garantiza).
- **Una lista vacía nunca es «todo en orden»** — cada comprobación que no pudo ejecutarse se declara en `skipped` con su motivo; cuando el vocabulario de `GF-004` no está configurado, la regla se declara en `skipped` en lugar de pasar en silencio.
- **Sin adjudicación** — el informe solo enumera diferencias y nunca se pronuncia sobre conformidad, responsabilidad o corrección; un guardián de redacción obliga a que el informe lleve siempre el descargo.
- **Citas solo literales** — cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y la URL de donde se leyó; presentar una paráfrasis como cita, o una base no verificable como `error`, falla al cargar.

```text
registro (cabecera · filas de tramitación) ──gongwen_flow_check──▶ reglas GF-001…GF-006 ──▶ informe (findings + skipped)
                ▲                                                                                   │
                └────────────────────────────── el original nunca se modifica ───────────────────────┘
```

### Reglas en resumen

| Regla | Comprobación | Severidad | Tipo de base |
|---|---|---|---|
| `GF-001` | cada fase de tramitación indica su responsable | warn | principio |
| `GF-002` | las fechas de recepción y cierre se analizan y son sucesivas | warn | principio |
| `GF-003` | el cierre cae dentro del plazo que el registro anota | info | local |
| `GF-004` | el estado procede de tu vocabulario (apagada por defecto) | info | local |
| `GF-005` | los números de documento son únicos en el registro | warn | principio |
| `GF-006` | la cabecera declara el título y la fecha de recepción | warn | principio |

### Ejemplos

Son los puntos de entrada reales del plugin; instala una vez y llama a uno.

**Salida detallada** — herramienta `gongwen_flow_check`, entrada (extracto):

```json
{"rows":[{"办理环节":"承办","承办人":"张科","收文日期":"2026-03-02","办理期限":"2026-03-12","办结日期":"2026-02-28"}]}
```

Salida:

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

*Observado en `tests/fixtures/GF-002/GF-002-unsafe.json (cases.json expects GF-002 count 1); run via lib/index.mjs rules/gongwen-flow-check.yaml`*

### Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una fase de tramitación no tiene responsable. ¿Qué se le informa al registro? | `GF-001` exige la columna `handler` en cada fase y señala la fila en la que está vacía. Comprueba únicamente que la columna esté rellenada, no si la tramitación fue oportuna: no decide si esa fase debía reclamarse ni quién es responsable. |
| La fecha de cierre es anterior a la de recepción. ¿Se detecta? | Sí. `GF-002` analiza `receivedAt` frente a `doneAt` y señala la fila cuando las dos fechas no son sucesivas. Solo compara las dos fechas escritas en el registro —el mismo día cuenta como no posterior— y no juzga si la tramitación se mantuvo dentro de su plazo. Una fecha que no puede analizar se informa por separado en lugar de omitirse en silencio. |
| Una fila nunca registra un plazo de tramitación. ¿El chequeo supone alguno? | No. `GF-003` solo se ejecuta cuando el propio registro escribe un plazo en `dueAt`; con `dueAt` vacío la regla se informa a sí misma en `skipped`. El reglamento no fija ningún número de días y el plugin no codifica ninguno, así que nunca se deduce un plazo. Un aviso significa «esto no coincide con el plazo que usted anotó», no «esto está fuera de plazo». |
| El estado de tramitación trae un valor que no está en la lista configurada. | `GF-004` señala la fila cuando el valor de `status` no figura entre los que usted configuró en `values`. De fábrica esa lista está vacía, lo que significa sin configurar, así que la regla se informa a sí misma en `skipped` en lugar de pasar en silencio. Solo comprueba si el valor está en su lista, no en qué fase se encuentra realmente el documento. |
| El mismo número de documento aparece dos veces en el registro. | `GF-005` exige que `docNo` sea único en el registro; al comparar se ignoran los espacios en blanco. Un aviso suele significar un registro duplicado o un número mal copiado, y requiere confirmación humana: repetir el `docNo` impide saber si es un documento registrado dos veces o dos documentos distintos con un solo número. |
| El propio registro no declara el título del documento ni la fecha de recepción. | `GF-006` exige que la cabecera declare `title` y `receivedAt` en el nivel superior y señala la cabecera cuando falta alguno. Comprueba solo que ambos estén declarados, no si el título tiene la forma correcta ni si las anotaciones de tramitación corresponden de verdad a ese documento. |

## Configuración

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`. Las cinco claves de la tabla son la lista completa; los parámetros por regla vienen después.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/gongwen-flow-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

Parámetros por regla que conviene conocer:

- `GF-001` `field` — la columna del responsable, `handler` por defecto.
- `GF-003` `dueAt` — la columna del plazo de tramitación; sin plazo registrado la regla se declara en `skipped`, y el plugin nunca calcula un plazo a partir de un número de días.
- `GF-004` `values` — tu vocabulario de fases, p. ej. `[待办, 承办中, 已办结, 已归档]`; vacío significa sin configurar y la regla no se ejecuta.
- `GF-005` — al comparar `docNo` se ignoran los espacios en blanco.

Ejemplo de sobrescritura en el patch del perfil:

```yaml
- insert:
    - id: dsh-gongwen-flow-check
      name: dsh-gongwen-flow-check
      config:
        disabledRules: [GF-004]
        onlyRules: [GF-001, GF-002, GF-003]
        skipNotes: las reglas propias de esta institución son la base de esta comprobación
```

## FAQ

<details>
<summary>¿Mi material se modifica o se sube a algún sitio?</summary>

No. La herramienta solo lee el texto JSON/YAML que le entregas (`file` o `material`, uno de los dos) y **nunca modifica el original**; el plugin es ESM puro, sin código nativo, **sin red y sin llamada al modelo** (véase Compatibilidad), así que el material nunca sale de tu máquina.

</details>

<details>
<summary>Sin vocabulario de estados ni plazo registrado, ¿algo pasa en silencio?</summary>

No. Los `values` de `GF-004` y el `dueAt` que necesita `GF-003` salen de fábrica sin configurar, y una comprobación que no puede ejecutarse se declara en `skipped` con su motivo: una lista de diferencias vacía nunca se lee como «no hay nada mal». `GF-004` solo comprueba si el valor está en tu lista, no en qué fase se encuentra realmente el documento.

</details>

<details>
<summary>¿El plugin decide que la tramitación está «fuera de plazo»?</summary>

No. `GF-003` compara la fecha de cierre con el plazo **escrito en el propio registro** (`dueAt`); sin plazo registrado informa `skipped` en lugar de suponer un número de días. El reglamento exige que un documento urgente **declare su plazo** y que se termine dentro del plazo declarado, pero **no fija ningún número de días**: el plazo siempre viene del documento recibido o de tu institución, y el plugin nunca lo inventa. Un aviso significa «esto no coincide con el plazo registrado», **no** «esto está fuera de plazo»: el retraso también depende de los recordatorios, las prórrogas y la urgencia del propio documento.

</details>

<details>
<summary>¿Qué formatos de fecha se leen? ¿Y los desfases horarios?</summary>

El lector acepta `2026-03-02` y `2026-03-02 09:30`; una fecha escrita con numerales chinos se informa como no analizable a propósito, para que decidas si normalizar la exportación. Toda la aritmética es de hora local sobre las cadenas entregadas, sin conversión de zonas horarias.

</details>

<details>
<summary>El plugin se instala pero la herramienta nunca aparece, o la instalación se rechaza por versión — ¿qué hago?</summary>

Comprueba que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó; un `main` erróneo hace que el cargador se salte la entrada en silencio. El rango de peers cubre las líneas `0.1.x` y `0.2.x`; si tu runtime queda fuera, concede una exención explícita: `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`. La compatibilidad de peers la aplica el runtime al instalar.

</details>

## Normas que sigue

| Documento | Número | Reglas que lo citan |
|---|---|---|
| Reglamento de tratamiento de documentos oficiales de los órganos del Partido y del Estado | 中办发〔2012〕14号 (en vigor desde el 2012-07-01) | GF-001, GF-002, GF-003, GF-004, GF-005, GF-006 |

Títulos originales de los documentos citados:

```text
《党政机关公文处理工作条例》 中办发〔2012〕14号（自 2012 年 7 月 1 日起施行）
```

**Límite:** este plugin comprueba un **registro de recepción y tramitación** en lo que un registro puede sostener mecánicamente: que cada fase indique su responsable, que las fechas de recepción y cierre se analicen y sean sucesivas, que el cierre caiga dentro del plazo que el propio registro anota, que los estados vengan de tu vocabulario, que los números de documento sean únicos y que la cabecera identifique el documento. **No** decide si la tramitación llegó tarde, si debía reclamarse ni quién es responsable. El reglamento exige que un documento urgente **declare su plazo** y que se termine dentro del plazo declarado, pero **no fija ningún número de días**: el plazo siempre viene del documento recibido o de tus propias normas, y este plugin nunca lo inventa.

> ### ⚠️ En qué se basan realmente las citas del informe de este plugin
>
> **El texto completo del reglamento se ha obtenido y verificado.** El Reglamento de tratamiento de documentos
> oficiales (中办发〔2012〕14号) se leyó literalmente en el portal del Gobierno central, y los informes de
> verificación bajo `rules/evidence/` registran los artículos comprobados: artículo 5 (principios), artículo 23
> (alcance del tratamiento), artículo 24 (los siete procedimientos de recepción, incluido «los documentos
> urgentes deben indicar su plazo de tramitación») y artículo 42 (en vigor desde el 2012-07-01, que sustituye a
> dos documentos anteriores). Los campos `excerpt` del paquete ya llevan citas literales, y
> `pnpm run check:citations` contrasta cada segmento con el registro de evidencia: actualmente 10 segmentos
> comprobados, 0 no rastreables, base 0.
>
> **Pero cada regla sigue siendo `warn` o `info`, y ningún `kind` se ascendió a `direct`** —deliberadamente.
> Este plugin comprueba si *un registro* está completo y es coherente; el reglamento regula cómo se *tramita*
> un documento, que es otra proposición. Etiquetar «esta columna está vacía» como cita `direct` de «debe
> dejarse constancia detallada de la tramitación» convertiría una laguna del registro en un incumplimiento del
> reglamento, justo la exageración que esta familia evita. La comprobación también deja el tamaño del plazo al
> documento recibido y a la institución, como hace el artículo 24.
>
> La norma de **formato** de documentos oficiales (GB/T 9704-2012) **no se obtuvo**, y este plugin no comprueba
> maquetación en ningún caso.
>
> La regla del plazo merece una nota propia. `GF-003` compara la fecha de cierre con el plazo **escrito en el
> propio registro** (`dueAt`); sin plazo registrado se declara en `skipped` en lugar de suponer un número de
> días. Su hallazgo dice «esto no coincide con el plazo que usted registró», **no** «esto está fuera de
> plazo»: el retraso depende de los recordatorios, las prórrogas y la urgencia del documento.

## Formato del material

La herramienta acepta JSON o YAML:

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

Los nombres de columna se reconocen sin distinguir mayúsculas y minúsculas y ignorando espacios, guiones bajos y guiones; se conservan los nombres propios del registro, de modo que un hallazgo nombra la columna que leyó. Las fechas pueden ser `2026-03-02` o `2026-03-02 09:30`. Los números se aceptan como cadenas, así que una exportación de hoja de cálculo no necesita limpieza.

## Fuentes de las reglas

Los datos de las reglas viven en `rules/gongwen-flow-check.yaml`, separados del código. Cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y la URL de donde se leyó. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada solo en un principio general (`kind: derived-from-principle`, tope `warn`) o en la política local (`kind: institutional-configuration`, tope `info`) **nunca** se declare `error`. Un paquete que exagera su base falla al cargar en lugar de producir un informe que parece más seguro de lo que es.

La cabecera del paquete declara la disciplina de citas; el `note` de cada regla explica su base y las conclusiones que deliberadamente no extrae; `rules/evidence/` guarda el registro de verificación de cláusulas; y `pnpm run check:citations` compara cada segmento de `excerpt` con esa evidencia (actualmente 10 segmentos comprobados, 0 no rastreables, base 0). El `note` de `GF-003` deja constancia aparte de que el reglamento entrega la duración del plazo al documento recibido y a la institución, y de que el plugin no codifica ningún número de días.

## Compatibilidad

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-rc.2`. `engines.dsh` se declara como `>=0.2.1-0 <0.3.0` y el host lo aplica desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native` y `ptc`; para un año entero de registros usa `ptc` |

## Solución de problemas

- **`GF-003` se declara en `skipped`.** El registro no anota plazo. Es deliberado: el plugin no lo inventa, porque el plazo viene del documento recibido o de tus propias normas de tramitación.
- **`GF-003` salta pero considero que la tramitación fue oportuna.** El plazo del registro y la fecha de cierre no coinciden. O la columna del plazo está obsoleta o la fecha de cierre es errónea; el hallazgo nombra las dos celdas que comparó.
- **`GF-004` nunca se ejecuta.** Su vocabulario está vacío; rellénalo con los nombres de fase de tu institución.
- **`GF-002` salta sobre fechas que sí puedo leer.** El lector acepta `2026-03-02` y `2026-03-02 09:30`; una fecha con numerales chinos se informa como no analizable a propósito.
- **El plugin se instala pero la herramienta nunca aparece.** Comprueba que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó; un `main` erróneo hace que el cargador se salte la entrada en silencio.
- **`dsh plugin add` rechaza el paquete como incompatible.** El rango de peers cubre `0.1.x` y `0.2.x`; si tu runtime queda fuera, concede una exención explícita: `dsh plugin --profile <name> allow-version dsh-gongwen-flow-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` informa `manifest-peers` como fallo.** El comprobador estático compara contra un rango de peers fijado en código anterior a la línea 0.2. El runtime aplica la compatibilidad al instalar, así que el rango declarado es el correcto; es un problema conocido de `dsh-plugin-dev`.
- **Los horarios parecen desplazados.** Toda la aritmética es de hora local sobre las cadenas entregadas, sin conversión de zonas horarias.

## Ecosistema y calidad

- [Espejo de Gitee](https://gitee.com/perrylink/dsh-gongwen-flow-check) (espejo sincronizado; GitHub es el canónico)
- [Página del plugin en dshfind](https://dshfind.com/plugins/PerryLink/dsh-gongwen-flow-check) (instalaciones y ranking)
- [Informe de OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-gongwen-flow-check) (impulsado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listado)
- [Base de conocimiento del ecosistema — elige un verificador por material](https://perrylink.github.io/zh/checkers/choose/) (índice completo de la familia: 62 verificadores + plugins generales)

## Desarrollo

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, la suite compartida de plugins de tabla + fixtures emparejados por regla (tests/fixtures/<RULE>/)
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes     # consistencia de los README en cinco idiomas
pnpm run check:citations   # contrasta cada cita de regla con rules/evidence/
node ../scripts/sync-shared.mjs dsh-gongwen-flow-check   # refresca src/shared desde ../_shared
```

El plugin es **dirigido por datos**: `src/model.ts` declara la forma de la tabla, el kit compartido aporta el lector y el motor de comprobación, y el paquete de reglas declara cada comprobación. Edita `rules/*.yaml` para cambiar el conjunto de reglas sin tocar TypeScript; el paquete se valida al cargar, no se confía en él. Las imágenes del README se generan programáticamente con [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) y pueden reejecutarse sin riesgo: las portadas con Pillow (zh / en × claro / oscuro, cuatro archivos) y el diagrama de estructura como SVG escrito a mano (claro y oscuro, con tokens de la superficie de comandos, valores reales del ejemplo y anotaciones breves). El antiguo diagrama de flujo, la portada anterior y las imágenes de demostración permanecen en `docs/assets/` para enlaces externos; el README solo referencia el nuevo conjunto de portadas y el par flow-v5.

## Familia y agradecimientos

Este proyecto forma parte de la familia de plugins de DeepSeek Harness de [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Si te resulta útil, **una estrella** no desbloquea nada, pero ayuda a que la siguiente persona lo encuentre.

- [@PerryLink](https://github.com/PerryLink) — creador y mantenedor: la herramienta `gongwen_flow_check`, el paquete de reglas con citas literales y su registro de verificación de cláusulas, y la documentación en cinco idiomas.

<details>
<summary>Expandir todos los plugins</summary>

| Plugin | Estado |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 CONGELADO — ver el README del repo |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 CONGELADO — ver el README del repo |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRADO (repo archivado) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 CONGELADO — ver el README del repo |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRADO (repo archivado) |

</details>

## Licencia

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-gongwen-flow-check contributors

<p align="center"><sub>Apache-2.0 · Plugin de la comunidad, no afiliado a DeepSeek.</sub></p>
