# dsh-gongwen-flow-check — Verificación del circuito de documentos oficiales y de los plazos de tramitación

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-gongwen-flow-check` lee un registro de entrada de documentos oficiales con su libro de fases de tramitación —la cabecera del documento más una fila por fase— y comprueba la completitud y la coherencia interna de ese registro: que cada fase indique su responsable en `handler`, que `receivedAt` y `doneAt` se analicen como fechas y sean sucesivas, que el cierre caiga dentro del plazo que el propio registro anota en `dueAt`, que cada `status` proceda de la lista que usted configuró, que `docNo` se registre una sola vez y que la cabecera declare el título del documento y la fecha de recepción. No decide si la tramitación llegó tarde, si debía reclamarse ni quién es responsable.

## Cómo se ve la salida

![Terminal demo of dsh-gongwen-flow-check: real output over its GF-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-gongwen-flow-check/main/docs/assets/dsh-gongwen-flow-check-demo.png)

Salida real de este plugin sobre su propio fixture de prueba `GF-002` — no es un montaje. El paquete de reglas no inventa citas, así que cada hallazgo nombra la cláusula aplicada y advierte que su texto no se obtuvo.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una fase de tramitación no tiene responsable. ¿Qué se le informa al registro? | `GF-001` exige la columna `handler` en cada fase y señala la fila en la que está vacía. Comprueba únicamente que la columna esté rellenada, no si la tramitación fue oportuna: no decide si esa fase debía reclamarse ni quién es responsable. |
| La fecha de cierre es anterior a la de recepción. ¿Se detecta? | Sí. `GF-002` analiza `receivedAt` frente a `doneAt` y señala la fila cuando las dos fechas no son sucesivas. Solo compara las dos fechas escritas en el libro —el mismo día cuenta como no posterior— y no juzga si la tramitación se mantuvo dentro de su plazo. Una fecha que no puede analizar se informa por separado en lugar de omitirse en silencio. |
| Una fila nunca registra un plazo de tramitación. ¿El chequeo supone alguno? | No. `GF-003` solo se ejecuta cuando el propio registro escribe un plazo en `dueAt`; con `dueAt` vacío la regla se informa a sí misma en `skipped`. El reglamento no fija ningún número de días y el plugin no codifica ninguno, así que nunca se deduce un plazo. Un aviso significa «esto no coincide con el plazo que usted anotó», no «esto está fuera de plazo». |
| El estado de tramitación trae un valor que no está en la lista configurada. | `GF-004` señala la fila cuando el valor de `status` no figura entre los que usted configuró en `values`. De fábrica esa lista está vacía, lo que significa sin configurar, así que la regla se informa a sí misma en `skipped` en lugar de pasar en silencio. Solo comprueba si el valor está en su lista, no en qué fase se encuentra realmente el documento. |
| El mismo número de documento aparece dos veces en el registro. | `GF-005` exige que `docNo` sea único en el registro; al comparar se ignoran los espacios en blanco. Un aviso suele significar un registro duplicado o un número mal copiado, y requiere confirmación humana: repetir el `docNo` impide saber si es un documento registrado dos veces o dos documentos distintos con un solo número. |
| El propio registro no declara el título del documento ni la fecha de recepción. | `GF-006` exige que la cabecera declare `title` y `receivedAt` en el nivel superior y señala la cabecera cuando falta alguno. Comprueba solo que ambos estén declarados, no si el título tiene la forma correcta ni si las anotaciones de tramitación corresponden de verdad a ese documento. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-gongwen-flow-check
dsh --profile <name> --dump-config | grep 'dsh-gongwen-flow-check'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/gongwen-flow-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-gongwen-flow-check
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-gongwen-flow-check contributors.
