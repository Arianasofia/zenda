---
name: media-plan
description: Arma o revisa el media plan mensual de paid media de cualquier cliente de la agencia (Google Ads, Meta Ads, LinkedIn Ads, TikTok) con el formato del equipo — inversión por campaña, benchmarks históricos del mes anterior y resultados estimados por fórmula, ordenado por país, unidad de negocio y campaña, con resúmenes por medio, unidad y país y la estética de la agencia. Usar SIEMPRE que pidan armar, actualizar, ajustar o revisar el MP / media plan / plan de medios del mes, redistribuir presupuesto entre campañas, estimar resultados para un presupuesto o bajar un plan anual a un mes, aunque no digan "media plan" — por ejemplo "armame el MP de noviembre", "cuánto le pongo a cada campaña", "con 9 M qué resultados esperamos". Aplica a cualquier cliente. Para una fecha especial o un flight corto (Cyber, Hot Sale, Black Friday) está la skill media-plan-evento.
---

# Media plan mensual

El media plan (MP) define cuánto se invierte en cada campaña del mes y qué resultados se esperan. Después es la base del control semanal, del budget control y de la comparación plan contra real del reporte.

Hay dos modelos de referencia de **estética, orden y lógica**: uno organizado por país y unidad de negocio y otro organizado por producto. Están descritos en `references/modelos.md`; leelo antes de armar. No copies números, campañas ni presupuestos de MP de otros clientes. Cada MP nuevo se arma con los datos del cliente y del mes. Si el cliente ya tiene un MP, su formato manda.

## Insumos

1. **Presupuesto del mes.** Lo da el cliente o sale del plan anual, si existe.
   - Si hay inversión que no entra en el presupuesto principal (por ejemplo campañas "por fuera del ejercicio"), va en un bloque aparte y se suma al total del mes.
2. **Campañas del mes.** Las que siguen, las nuevas, las pausadas y los tests. Si una campaña arranca o termina a mitad de mes, anotá las fechas reales.
3. **Métricas históricas del mes anterior por campaña.** Salen de la plataforma (SeePM o el MCP de cada medio) y son los benchmarks.
4. **Comentarios y decisiones del equipo.** Por ejemplo "inversión al 50 % desde octubre" o "estimar solo los primeros 15 días". Si hay un MP anterior en la planilla, leé sus comentarios con `includeComments`.

## Benchmarks

- **Campaña que ya corrió:** usá las métricas del mes anterior de esa misma campaña (CPC, CTR, CPM, Conv. Rate o CPA, según el modelo).
- **Campaña nueva** (producto o servicio que nunca se pautó): tomá benchmarks de otras campañas **con el mismo objetivo**, mejor si son del mismo medio y país. Ejemplos: una de conversiones en Search se compara con otra de conversiones en Search; una de leads en Meta, con otra de leads en Meta.
  - Dejá un comentario en la celda que diga de qué campaña salió el benchmark.
- **Cuentas en pesos:** si el benchmark es de un período anterior al mes del plan, se puede ajustar por inflación mensual. Usá el mismo supuesto que el plan anual del cliente y dejalo escrito en la planilla.
- **Objetivos sin conversión:** las campañas de tráfico, alcance, interacciones o views se miden con su KPI (Clicks/CPC/CTR, Alcance/Frecuencia/CPM, Views/CPV). La columna de conversiones queda en "-". No inventes una conversión.
- **Formularios y mensajes:** los leads de formulario y los mensajes van en columnas propias (Leads/CPL, Mensajes/CPMsj), separadas de las conversiones web.

## Modelo de cálculo

Por cada campaña se cargan a mano **solo la inversión y los benchmarks**. El resto es fórmula, nunca un valor pegado.

Las fórmulas tienen que ser las que haría un manager senior a mano, para que el cliente y el equipo las entiendan de un vistazo: una división o una multiplicación por celda (`=Inversión/CPC`, `=Clicks*CR`).
- Sin `BUSCARV` anidados, `SI.ERROR` encadenados ni topes con `MIN`.
- `SI.ERROR(…;"")` solo en una división que puede dar cero, nunca anidado.

**Por clic** (modelo B). Es el modelo por defecto.

| Insumo | Calculado |
| --- | --- |
| Inversión, CPC, CTR, Conv. Rate | Clicks = Inversión / CPC · Impresiones = Clicks / CTR · Conversiones = Clicks × Conv. Rate · CPA = Inversión / Conversiones · CPM = Inversión / Impresiones × 1000 |

**Por CPM y CPA** (modelo A). Usalo cuando el cliente ya trabaja así o cuando planifica en USD.

| Insumo | Calculado |
| --- | --- |
| Inversión, CPM, CTR, CPC, CPA | Impresiones = Inversión / CPM × 1000 · Clics = Inversión / CPC · Conversiones = Inversión / CPA · CR = Conversiones / Clics · Inversión USD = Inversión / tipo de cambio |

Si el cliente ya tiene MP, seguí su modelo.

**Totales de cada tabla:** Inversión, Clicks, Impresiones y Conversiones se suman. Los ratios se recalculan con esas sumas: CPA = Inversión / Conversiones, CPC = Inversión / Clicks, CTR = Clicks / Impresiones, CR = Conversiones / Clicks. No se promedian.

**% de inversión:** inversión de la campaña sobre el total de su propio bloque.

**Reparto por porcentaje:** si un bloque reparte un monto fijo entre campañas (por ejemplo `=% × 900000`), el monto va en una sola celda y las filas la referencian.

## Orden de la pestaña

1. **Encabezado:** marca de la agencia y el título "<cliente> | Media Plan <Mes> <Año>". Al lado, el presupuesto mensual total y, si aplica, el tipo de cambio.
2. **Resúmenes,** cada uno con Inversión y % del total, y una fila TOTAL:
   - por medio (Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads);
   - por unidad de negocio o producto;
   - por país, si hay más de uno;
   - por cuenta publicitaria, si el cliente tiene una cuenta por producto.
3. **Detalle por campaña:** país → unidad de negocio o producto → tabla de campañas con fila de subtotal. Los bloques que van por fuera del presupuesto principal van al final, con título propio.
4. **Columnas de cada tabla:** Campaña, Medio, Estrategia (objetivo), %, Fecha inicio, Fecha fin, Inversión, y después las métricas del modelo en el orden de la tabla de arriba.

Nombres de campaña: el nombre exacto de la plataforma, así después se cruza con el real.

Estética: colores, tipografía y formatos de número en `references/modelos.md`.

## Controles antes de entregar

1. **Cada resumen suma solo lo suyo.** Por ejemplo, el total de Google suma solo filas con Medio = Google Ads. Recorré las referencias de cada `SUM`: si una fila queda afuera o se cuela una de otro medio, el total general puede cerrar igual y el error no se ve.
2. **Los totales no incluyen otros subtotales.** Si un `SUM` arranca en la fila del total del bloque anterior, duplica.
3. **El % de cada campaña divide por el total de su bloque,** y los % del bloque suman 100 %.
4. **Los resúmenes cierran entre sí:** total por medio = total por unidad = total por país = presupuesto mensual.
5. **No hay unidades mezcladas en un total.** Por ejemplo, no se suman conversiones con impresiones.
6. **No quedan `#REF!`, filas sin nombre ni bloques del mes anterior.**
7. **La inversión respeta las fechas.** Una campaña que corre medio mes lleva inversión de medio mes.

**Planilla en configuración es-AR:** en las fórmulas con más de un argumento el separador es `;`, también en el formato condicional. Una fórmula con `,` da `#ERROR!`. Después de cada cambio, leé los valores calculados y buscá `#ERROR!` y `#REF!`.

Para revisar una planilla de Drive: exportala a xlsx con el MCP de Drive y leé fórmulas y valores con `openpyxl` (`load_workbook` común y con `data_only=True`).

## Entrega

- **Formato:** pestaña nueva "MP <Mes> <Año>" en la planilla del cliente, sin pisar la del mes anterior. Si no hay permiso de edición, entregá un xlsx con la misma estética (skill de identidad visual de la agencia para la paleta) para que el equipo lo pegue.
- **Resumen para el equipo:**
  - presupuesto y reparto por medio, unidad y país;
  - cambios contra el mes anterior y su motivo;
  - resultados y CPA esperados contra el objetivo del cliente;
  - qué benchmarks son prestados de otra campaña.
- **Texto en la planilla:**
  - Solo leyendas para el cliente debajo de cada cuadro: de dónde salen los datos o qué aclara el cuadro.
  - Lo que haya que decirle al equipo va por el chat.
  - Los controles de arriba se hacen antes de entregar y no quedan como cuadro en la planilla.
- **Archivo del equipo:** si el equipo ya está trabajando la planilla, editá esa, sin crear otra versión. Leela primero, con comentarios, y respetá lo que agregaron.
- **Convenciones:** números en formato es-AR, castellano rioplatense sin vocabulario de IA, títulos de bloque descriptivos (ver `CLAUDE.md`).
- **Después:** el MP alimenta el control semanal, `revision-post-reporte` y la hoja plan contra real del reporte, si el cliente la tiene.
