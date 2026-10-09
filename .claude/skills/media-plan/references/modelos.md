# Modelos de referencia

Dos MP de octubre 2026 sirven de modelo de estética, orden y lógica. **No copiar sus números, campañas ni presupuestos.**

- **Pickit:** "General 2026 | pickit", pestaña "MP Octubre 2026". Es el modelo principal de estética.
- **GSS:** "General Sancor Seguros | GSS", pestaña " Media Plan - OCT". Es el modelo de lógica por producto y de bloques por fuera del presupuesto. También tiene la pestaña "Ejercicio 2026-2027", que muestra cómo se baja un plan anual a meses.

## Estética (modelo Pickit)

| Elemento | Formato |
| --- | --- |
| Hoja | Sin líneas de cuadrícula. Columna A angosta (≈2,6) como margen. Columna B ancha (≈43) para nombres de campaña. |
| Tipografía | Calibri en toda la hoja. Datos en 10 pt. |
| Marca | "zenda." en B2, 11 pt negrita, verde `#2FA37A`. |
| Título | B3: "<cliente>  \|  Media Plan <Mes> <Año>", 16 pt negrita, `#0A0A0B`. |
| Título de sección ("RESUMEN POR MEDIO", "DETALLE POR CAMPAÑA - <MES> <AÑO>") | 12 pt negrita, texto blanco sobre `#0A0A0B`. |
| País | 11 pt negrita, blanco sobre `#0A0A0B`. |
| Unidad de negocio | 11 pt negrita, `#0A0A0B` sobre celeste claro `#EAF7FB`, con sangría de dos espacios. |
| Encabezado de tabla | 10 pt negrita, `#0A0A0B` sobre verde `#59D7A2`. |
| Filas de campaña | Fondo blanco, alternado con gris `#F7F7F8` (zebra). |
| Subtotal / TOTAL | Negrita sobre verde muy claro `#EAF9F3`. Montos en verde `#2FA37A`. |
| Insumos cargados a mano (inversión y benchmarks) | Texto azul `#0000FF`, para distinguirlos de las fórmulas, que van en negro. |
| Montos en el resumen | Verde `#2FA37A`. |

Formatos de número:
- Montos: `"$" #,##0`.
- Volúmenes (impresiones, clics, conversiones): `#,##0`.
- Tasas: `0.00%`.
- % de inversión: `0%`.

GSS usa la misma base con un acento rosa `#E71CA2` en el título de cada producto y celeste `#95D6EA` en los encabezados de tabla. En un cliente nuevo, usá la estética Pickit.

## Orden

**Pickit:** organiza por país y unidad de negocio.
1. Encabezado y tipo de cambio.
2. Resumen por medio a la izquierda y resumen por unidad de negocio a la derecha. Debajo, resumen por país y presupuesto mensual total.
3. "DETALLE POR CAMPAÑA": un bloque por país, adentro un bloque por unidad de negocio, y cada tabla con su subtotal.

**GSS:** organiza por producto.
1. Título.
2. Desglose por cuenta publicitaria (GL - <producto>, FB - <producto>, TIKTOK).
3. Presupuesto mensual del plan, presupuesto por fuera y total. Totales de inversión, conversiones e impresiones planificadas, y reparto por medio.
4. Un bloque por producto, cada uno con su tabla y su fila TOTAL.
5. Al final, "Campañas por fuera del ejercicio", con el mismo formato.

## Lógica

**Pickit: modelo por CPM y CPA.**
- Insumos: inversión, CPM, CTR, CPC y CPA.
- Calculados: impresiones, clics, conversiones, CR e inversión en USD (contra la celda de tipo de cambio).
- Algunos bloques reparten un monto fijo por % entre campañas.

**GSS: modelo por clic.**
- Insumos: inversión, CPC, CTR y Conv. Rate.
- Calculados: clicks, impresiones, conversiones, CPA y CPM.
- Los bloques de views llevan Views/CPV y Alcance/Frecuencia.
- Prevención Salud suma columnas Leads/CPL para los formularios.

**Plan anual (GSS, "Ejercicio").**
- Un bloque por producto y una columna por mes.
- Parte del objetivo de conversiones del mes: Clicks = Conversiones / Conv. Rate; Inversión = Clicks × CPC.
- El CPC de cada mes es el del mes anterior por (1 + inflación mensual), con la inflación en una celda de supuestos.
- Columnas "Objetivos <cliente>" y "Diferencia": objetivo del cliente contra lo planificado.
- El MP mensual toma la inversión de cada producto de este plan y la reparte entre campañas.
