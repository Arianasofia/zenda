---
name: revision-post-reporte
description: Después de cerrar el reporte mensual de paid media de un cliente de Zenda, arma la lista de puntos a revisar con el equipo por medio (Google Ads, Meta Ads, LinkedIn Ads y los que haya) para el mes siguiente, como Doc para trabajar con el equipo y como página HTML con la estética Zenda. Usar SIEMPRE al terminar un reporte mensual (con la skill reportes-paid-media o a mano), aunque nadie lo pida, y cuando pidan "qué revisamos con el equipo", "lista de mejoras por medio", "próximos pasos por plataforma" o "puntos a revisar". Al empezar el reporte del mes siguiente, retomar la lista anterior y marcar qué se hizo y qué resultado dio.
---

# Revisión post reporte

Las ideas del reporte se pierden si no quedan en una lista con responsables y fecha. Esta skill convierte el reporte cerrado y el media plan del mes siguiente en una lista de revisión por medio, con estética Zenda.

## Cuándo correrla

- **Al cerrar cada reporte mensual.** Ofrecé la lista apenas el reporte está listo, sin esperar a que la pidan.
- **Al arrancar el reporte siguiente.** Buscá la lista del mes anterior: en los Docs del usuario o en el JSON de `revisiones/` dentro del repo. Sumá al reporte nuevo qué se hizo de cada punto y qué resultado dio.

## Insumos

1. **El reporte final del mes.** Usá la última versión que editó el usuario, no la que armaste vos.
2. **El media plan del mes siguiente, si está cerrado.** Suele estar en el Drive del cliente, en la pestaña "MP <Mes> <Año>".
   - Usá la pestaña prolija, no el borrador con `#REF!`.
   - Verificá que el resumen por medio coincida con la suma de las campañas. Si no coincide, anotalo como punto a revisar.
3. **Datos de plataforma que sostengan cada punto.** Por ejemplo keywords, creativos o eventos de conversión. Se sacan por SeePM o por el MCP de cada plataforma.

## Cómo armar cada punto

Cada punto lleva tres cosas: **qué revisar**, **el dato del mes** que lo justifica (con número) y **qué hacer**. Un punto sin dato no entra.

Buscá sobre todo:

- **Gasto sin resultado.** Keywords, campañas o creativos que se llevan inversión sin conversiones.
- **Lo que funciona y queda corto de presupuesto.** Por ejemplo términos de marca, el CPA más bajo, el mejor creativo.
- **Medición.** Pixel, API de conversiones, Insight Tag, carga del lead calificado y evento de optimización.
  - Va primero si hay un cambio de objetivo, como formulario nativo a landing.
- **Cambios grandes del plan contra el mes anterior.** Presupuesto que se multiplica, países que vuelven, campañas sin KPI definido.
- **Creativos.** Frecuencia alta, formatos que no rindieron (por ejemplo carruseles) y piezas a replicar.
- **Datos del negocio que faltan.** Registros, leads calificados, onboardings.

Ordená por medio y, dentro de cada medio, por urgencia. Cerrá con una sección "Para todos los medios" que lleve:

- la fecha de la revisión de mitad de mes;
- como último punto: "Llevar esta lista al próximo reporte y marcar qué se hizo".

## Redacción

- Castellano rioplatense, frases cortas, lenguaje de paid media.
- Nada de vocabulario de IA: "potenciar", "apalancar", "clave", "robusto", "en definitiva", "es importante destacar".
- Números en formato es-AR ($1.234.567; 0,52%).
- Cada sección abre con una frase que dice lo prioritario del medio.

## Entregables

1. **Doc para el equipo (Claude Docs).** Usá la skill `docs` y seguí sus pasos de creación.
   - Título: "<cliente> · Puntos a revisar en <mes> <año>".
   - Secciones: Contexto, una por medio y Para todos los medios.
   - Cada medio va en una tabla de 3 columnas: Qué revisar | Dato de <mes> | Qué hacer.
   - "Para todos los medios" va como lista de tareas (`- [ ]`).
2. **Página con estética Zenda (HTML).** Armá el JSON con la estructura de `scripts/ejemplo_revision.json` y corré:

   ```bash
   python3 -I scripts/build_revision.py <reporte_final.html> <revision.json> <salida.html>
   ```

   - El script toma del reporte el diseño (tokens, fuentes, CSS) y el editor, y reemplaza el contenido por la revisión. Así queda igual al reporte.
   - Revisalo con el chequeo del editor ("Revisar"): que cada lámina entre en A4 apaisado y que no haya texto ilegible.
   - Si un medio tiene más de 10 puntos, dividilo en dos láminas.
3. **Guardá el JSON** en `revisiones/<cliente>-<aaaa-mm>.json` dentro del repo y hacé commit, para retomarlo el mes siguiente.

Respondé en el chat con una línea por entregable. No repitas la lista.
