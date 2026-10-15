# Modelos de referencia

Hay dos modelos de MP mensual: el **A** está organizado por país y unidad de negocio, y el **B** por producto. Sirven de modelo de estética, orden y lógica. **No copiar números, campañas ni presupuestos de un cliente a otro.** Si el cliente ya tiene MP, se sigue el suyo.

## Estética (base de la agencia)

| Elemento | Formato |
| --- | --- |
| Hoja | Sin líneas de cuadrícula. Columna A angosta (≈2,6) como margen. Columna B ancha (≈43) para nombres de campaña. |
| Tipografía | Calibri en toda la hoja. Datos en 10 pt. |
| Marca | Marca de la agencia en B2, 11 pt negrita, verde `#2FA37A`. |
| Título | B3: "<cliente>  \|  Media Plan <Mes> <Año>", 16 pt negrita, `#0A0A0B`. |
| Título de sección ("RESUMEN POR MEDIO", "DETALLE POR CAMPAÑA - <MES> <AÑO>") | 12 pt negrita, texto blanco sobre `#0A0A0B`. |
| País | 11 pt negrita, blanco sobre `#0A0A0B`. |
| Unidad de negocio | 11 pt negrita, `#0A0A0B` sobre celeste claro `#EAF7FB`, con sangría de dos espacios. |
| Encabezado de tabla | 10 pt negrita, `#0A0A0B` sobre verde `#59D7A2`. |
| Filas de campaña | Fondo blanco, alternado con gris `#F7F7F8` (zebra). |
| Subtotal / TOTAL | Negrita sobre verde muy claro `#EAF9F3`. Montos en verde `#2FA37A`. |
| Insumos cargados a mano (inversión y benchmarks) | Texto azul `#0000FF`, para distinguirlos de las fórmulas, que van en negro. |
| Montos en el resumen | Verde `#2FA37A`. |
| Leyendas | Gris, itálica, 9 pt, debajo del cuadro que aclaran. |

Formatos de número:
- Montos: `"$" #,##0`.
- Volúmenes (impresiones, clics, conversiones): `#,##0`.
- Tasas: `0.00%`.
- % de inversión: `0%`.

Variante del modelo B: acento rosa `#E71CA2` en el título de cada producto y celeste `#95D6EA` en los encabezados de tabla. En un cliente nuevo, usá la base.

## Orden

**Modelo A, por país y unidad de negocio.**
1. Encabezado y tipo de cambio.
2. Resúmenes:
   - por medio a la izquierda y por unidad de negocio a la derecha;
   - debajo, por país y el presupuesto mensual total.
3. "DETALLE POR CAMPAÑA": un bloque por país, adentro un bloque por unidad de negocio, y cada tabla con su subtotal.

**Modelo B, por producto.**
1. Título.
2. Desglose por cuenta publicitaria (por ejemplo GL - <producto>, FB - <producto>, TIKTOK).
3. Presupuesto mensual del plan, presupuesto por fuera y total.
   - Totales de inversión, conversiones e impresiones planificadas.
   - Reparto por medio.
4. Un bloque por producto, cada uno con su tabla y su fila TOTAL.
5. Al final, "Campañas por fuera del ejercicio", con el mismo formato.

## Lógica

**Modelo A: por CPM y CPA.**
- Insumos: inversión, CPM, CTR, CPC y CPA.
- Calculados: impresiones, clics, conversiones, CR e inversión en USD (contra la celda de tipo de cambio).
- Algunos bloques reparten un monto fijo por % entre campañas.

**Modelo B: por clic.**
- Insumos: inversión, CPC, CTR y Conv. Rate.
- Calculados: clicks, impresiones, conversiones, CPA y CPM.
- Los bloques de views llevan Views/CPV y Alcance/Frecuencia.
- Los productos con formularios suman columnas Leads/CPL.

**Plan anual (variante del modelo B).**
- Un bloque por producto y una columna por mes.
- Parte del objetivo de conversiones del mes: Clicks = Conversiones / Conv. Rate; Inversión = Clicks × CPC.
- El CPC de cada mes es el del mes anterior por (1 + inflación mensual), con la inflación en una celda de supuestos.
- Columnas "Objetivos <cliente>" y "Diferencia": objetivo del cliente contra lo planificado.
- El MP mensual toma la inversión de cada producto de este plan y la reparte entre campañas.
