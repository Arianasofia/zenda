---
name: media-plan-evento
description: Arma el media plan de una campaña de fecha especial o evento de paid media (Cyber Monday, Cyber Week, Hot Sale, Black Friday, Día del Padre, un lanzamiento) para cualquier cliente y cualquier medio (Google Ads, Meta Ads, LinkedIn Ads, TikTok). El plan lleva dos escenarios de inversión calculados sobre el gasto diario real del cliente, proyección con fórmulas simples, supuestos y benchmarks al pie, un BGT diario con control de consumo y una hoja de copys con los requisitos de cada plataforma. Usar SIEMPRE que pidan un MP, plan o presupuesto para una fecha puntual o un flight corto, "cuánto invertimos en el Cyber", "armame los escenarios para Hot Sale", "un plan conservador y otro más agresivo para la fecha", aunque no digan "media plan". Para el MP mensual de siempre está la skill media-plan.
---

# Media plan de evento

Un evento es un flight corto (de una a tres semanas) en el que todos los anunciantes suben la inversión al mismo tiempo. El plan tiene que contestar tres preguntas que el cliente va a hacer sí o sí:

1. ¿Cuánto más que un día normal vamos a invertir?
2. ¿Qué resultados esperamos con cada escenario?
3. ¿Cómo controlamos día a día que se gaste lo planeado?

El detalle de cada hoja (filas, columnas, fórmulas y formatos) está en `references/estructura.md`. Los requisitos de textos y piezas de cada plataforma están en `references/specs-copys.md`. Leé los dos antes de armar.

## Antes de armar: qué pedir

- **Fechas del evento y del flight.** Prevé que el evento se estire: un Cyber Monday casi siempre termina siendo una Cyber Week, y un Hot Sale arrastra el fin de semana. El flight arranca con una previa de presencia de marca (en general la semana anterior) y cierra el último día de la extensión.
- **Unidad de negocio y país.** El plan se arma para una sola unidad (por ejemplo B2B, B2C, un producto) y un solo país, salvo que pidan otra cosa.
- **Medios, campañas y objetivo de cada una.** Si en un medio hay una sola campaña con varios grupos de anuncios, se plantea así: una campaña y su presupuesto repartido por grupo, no varias campañas.
- **Mensaje central y restricciones de marca.** Por ejemplo, si se puede nombrar el evento o no. "Cyber Monday", "Hot Sale" y "Black Friday" son marcas de sus organizadores: si el cliente no está adherido, los textos hablan del pico de ventas o de la semana de ofertas.
- **Audiencias armadas.** Tamaño y configuración (capturas de LinkedIn, bases de datos de Meta, señales de PMax).
- **Budget control o MP del mes en curso,** para el día común.

## Día común: la base de todo

El día común es la inversión diaria real del cliente **en cada medio**, filtrada por la unidad de negocio y el país del plan.

- **Solo las campañas de esa unidad y ese país.** Nunca el total de la cuenta: las cuentas mezclan unidades y países, y el día común sale inflado. Buscá la nomenclatura de la unidad en los nombres de campaña (por ejemplo B2B, H2, Hunting).
- **Fuente:** el budget control del mes o el MP vigente. Si se calcula desde la plataforma, dividí por los días que la campaña corrió de verdad, no por 30. Revisá la fecha de inicio de cada campaña.
- **Por medio, no un total.** El cliente compara LinkedIn contra LinkedIn y Google contra Google.
- Si el equipo ya tiene una tabla de día común, usá esa y no la recalcules.

## Escenarios

- Son dos: **conservador** y **agresivo**. No uses "arriesgado", que tiene connotación negativa frente al cliente. Si el equipo prefiere otro nombre, usá el suyo.
- Cada escenario es una suba porcentual sobre el día común de cada medio. Referencia: conservador +20 a 30 %, agresivo +40 a 60 %.
  - Una suba de 2 o 3 veces el día común no la aprueba nadie. Si el cliente pide más, que sea una decisión explícita suya.
- **Presupuesto de cada medio** = día común × (1 + suba) × días del flight. El total es la suma de los medios.
- **El agresivo no reparte la plata extra en partes iguales.** Toma el conservador tal cual y suma el incremental (total agresivo − total conservador) a las campañas con mejor CPA o que generan conversiones. El reparto del incremental va como dos o tres % en Supuestos. Si se reparte igual, los resultados crecen exactamente lo mismo que la inversión y el cliente no ve para qué pagar más.
- Avisá en el chat si la diferencia de resultados entre escenarios es chica y ofrecé dejar un solo escenario más una línea de inversión adicional opcional.
- Dentro de cada medio, el reparto entre campañas o grupos se carga como **% del medio**. Más peso a lo que más rinde o más alcance tiene; menos a las audiencias chicas (por ejemplo un remarketing con pocas personas).

## Proyección: fórmulas que entiende cualquiera

Escribí las fórmulas como las haría un manager senior a mano, para que el cliente y el equipo las sigan de un vistazo:

- Inversión = % del medio × presupuesto del medio
- Inversión diaria = Inversión / días
- Impresiones = Inversión / CPM × 1000
- Clics = Inversión / CPC
- CTR = Clics / Impresiones
- Conversiones = Clics × CR
- CPA = Inversión / Conversiones
- Alcance (solo awareness, por ejemplo LinkedIn) = Impresiones / frecuencia supuesta

Los totales suman inversión, impresiones, clics y conversiones, y recalculan los ratios con esas sumas.

**Qué no hacer:** nada de `BUSCARV` anidados, `SI.ERROR` encadenados, `MIN` con topes ni fórmulas de dos renglones. La suba de costos por temporada se aplica en la tabla de benchmarks, en columnas "CPM con suba" y "CPC con suba", y la proyección apunta a esa celda.

## Benchmarks

- Salen de datos reales de la plataforma (SeePM o el MCP de cada medio), de las mismas campañas de la unidad y el país, en el último mes. Anotá el período real: si una campaña arrancó a mitad de mes, el período empieza ese día.
- **Campaña nueva** (por ejemplo una PMax donde antes solo había Search): tomá CPC y CR de la campaña más parecida del mismo objetivo. Si falta un dato, estimalo y aclaralo en la leyenda (por ejemplo "CTR estimado de 1 %").
- **Suba por temporada:** +15 % de CPM y CPC por defecto, porque en el evento todos pujan más. Va en Supuestos.
- **Previsión de la plataforma** (por ejemplo el alcance que estima LinkedIn para una audiencia): no la uses para proyectar. Va como referencia en la hoja de audiencias, y en el chat avisá si difiere mucho del modelo.

## Hojas del archivo

1. **MP:** KPI arriba; comparativo de escenarios; inversión por medio; inversión diaria contra día común; detalle por campaña de cada escenario; Supuestos y Benchmarks al pie.
2. **BGT Diario:** plan por día de cada campaña o grupo según la distribución diaria, y abajo el control de consumo para cargar el gasto real.
3. **Audiencias:** configuración y tamaño por medio.
4. **Copys:** mensaje central, reglas generales y textos por medio y por grupo de anuncios, con requisitos y conteo de caracteres.

El detalle completo está en `references/estructura.md`.

## Texto en la planilla

- **Lo único que va escrito son leyendas para el cliente,** debajo de cada cuadro: de dónde salen los datos o qué aclara el cuadro.
- Lo que haya que decirle al equipo (dudas, supuestos a validar, decisiones pendientes) va por el chat, no en la planilla.
- Supuestos resumidos en una sola tabla al pie del MP, no en una hoja aparte con muchos cuadros.
- Sin hojas o celdas de "controles" internos a la vista del cliente. Los controles se hacen antes de entregar (ver abajo).
- Títulos descriptivos, castellano rioplatense, números en formato es-AR, sin vocabulario de IA.

## Trabajar sobre el archivo del equipo

- Si el equipo ya está editando la planilla, trabajá sobre esa, sin crear otra versión. Leela primero, con comentarios.
- Respetá lo que agregaron (hojas nuevas, controles, textos). Si algo de ellos tiene un error, arreglalo y contalo en el chat.
- Planilla en configuración regional es-AR: en las fórmulas con más de un argumento el separador es `;`, también en el formato condicional. Una fórmula con `,` da `#ERROR!`.
- Después de cada cambio grande, leé los valores calculados y buscá `#ERROR!`, `#REF!` y celdas vacías donde debería haber número.

## Controles antes de entregar (no van en la planilla)

1. Cada escenario suma lo mismo en el MP, en inversión por medio y en el BGT.
2. Los % de cada medio suman 100 % y la distribución diaria suma 100 %.
3. Inversión diaria contra día común: la suba de cada medio es la que dice Supuestos.
4. El BGT diario por campaña suma la inversión de la campaña (control en 0).
5. El control de consumo: cargá un gasto de prueba, verificá que el % contra el plan y el consumo total den bien, y borralo.
6. Sin `#ERROR!`, `#REF!` ni referencias a hojas borradas.
7. Si el presupuesto ya está cargado en una plataforma y no coincide con el plan, avisalo.

## Entrega

- Link al archivo y resumen corto en el chat:
  - inversión por escenario y por medio;
  - suba contra el día común;
  - qué cambió desde la versión anterior;
  - qué falta (bases de datos, términos de búsqueda, validaciones de copy).
- Si el equipo pide cambios de criterio (nombres, fórmulas, formato), sumalos a esta skill para la próxima.
