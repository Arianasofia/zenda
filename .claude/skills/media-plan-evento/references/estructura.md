# Estructura de las hojas

Estética de la agencia (paleta, tipografía, KPI cards): skill de identidad visual de la agencia.
- Bandas de título en negro con texto blanco.
- Encabezados de tabla en verde.
- Subtítulos de escenario en cyan.
- Totales con fondo verde claro.
- Datos cargados a mano en azul.
- Leyendas en gris, itálica, tamaño 9, debajo de cada cuadro.

## Hoja MP

### 1. Encabezado y KPI
- Marca de la agencia y título "<cliente> | Media Plan <Evento> | <País>".
- Cuatro o cinco tarjetas:
  - Período ("26/10 al 08/11"), con fórmula `TEXT(inicio;"dd/mm")&" al "&TEXT(fin;"dd/mm")`.
  - Inversión de cada escenario.
  - Impresiones de cada escenario o el KPI principal del objetivo.

### 2. Comparativo de escenarios
Columnas: Indicador, Conservador, Ampliado, Diferencia (`=Ampliado/Conservador-1`).

Filas, todas referencias a los totales del detalle:
- Inversión
- Impresiones
- Clics
- CTR
- CPM promedio (`=Inversión/Impresiones*1000`)
- Alcance (si hay awareness)
- Inversión diaria
- Conversiones estimadas

### 3. Inversión por medio
Columnas: Medio, Conservador, %, Ampliado, % y fila TOTAL.

Monto del medio = inversión diaria del escenario × días.

### 4. Inversión diaria vs. día común
Columnas: Medio, Día común (dato cargado), Conservador, Vs. día común, Ampliado, Vs. día común.
- Conservador = `Día común*(1+suba conservador)`.
- Vs. día común = `Conservador/Día común-1`, con formato `+0%`.
- Fila TOTAL.
- Leyenda: "Día común: inversión diaria de cada medio en las campañas <unidad> de <país>, según <fuente y mes>."

### 5. Detalle por campaña (un bloque por escenario)
- Fila de grupos: CAMPAÑA | INVERSIÓN | RESULTADOS ESTIMADOS.
- Columnas: Campaña, Medio, Objetivo, Audiencia / grupo de anuncios, % del medio, Inversión, Inv. diaria, Impresiones, Clics, CTR, Alcance, Conversiones, CPA.
- Una campaña con varios grupos: celda de campaña combinada en vertical, una fila por grupo.
- Objetivos sin conversión (reconocimiento, alcance): Conversiones y CPA en "–".
- Fila Total por escenario.
- CPA del total = inversión de las campañas con conversión / conversiones.
- Leyenda debajo si hace falta, por ejemplo cómo se reparte una campaña en grupos.

### 6. Supuestos (una sola tabla al pie)
Columnas: Concepto | Valor | Aclaración.
- Inicio
- Fin
- Días (`=Fin-Inicio+1`)
- Suba de inversión diaria · conservador
- Suba de inversión diaria · ampliado
- Suba de CPM y CPC por temporada
- Frecuencia (si hay awareness)

Abajo, la distribución diaria:
- Fila de fechas (`=Inicio+0`, `=Inicio+1`, …), con formato `ddd dd/mm`.
- Fila de % con Total = 100 %.

Curva sugerida para 14 días (previa de 7 más evento extendido de 7):
5, 5, 5, 5, 6, 6, 6, 10, 10, 10, 9, 8, 8, 7 %.

Los días pico del evento concentran el 30 %; la previa crece hacia el fin de semana.

### 7. Benchmarks de referencia
Columnas: Medio, Campaña de referencia, Período, CPM, CPC, CTR, CR, CPM con suba (`=CPM*(1+suba)`), CPC con suba.

Leyendas:
- La fuente: datos reales de las plataformas, con el período de cada medio.
- Cómo se estimó lo que no tiene historia.

## Hoja BGT Diario

### Plan por escenario
- Columnas: Campaña, Inversión, un día por columna (fechas del MP) y Control (`=SUM(días)-Inversión`, debe dar 0).
- Una fila por campaña o grupo de anuncios con presupuesto propio.
- Cada día = `$Inversión * % del día del MP`.
- Fila Total.
- Gradiente de color sobre los montos diarios.

### Control de consumo por escenario
- Columnas: Campaña, Inversión, y por cada día un par "real | %".
- Real = carga manual. Formato `"$" #,##0`.
- % = `=SI(real="";"";SI.ERROR(real/plan del día;""))`, en blanco hasta que se cargue el gasto.
- Fila Total:
  - real = `=SI(CONTAR(rango)=0;"";SUMA(rango))`;
  - % contra el total del plan del día.
- Al costado, "Consumo TOTAL" = suma de los reales.
- Semáforo con formato condicional: verde entre 90 % y 110 %, rosa fuera de ese rango. Solo en las columnas "%".
- Leyenda: "Cargar el consumo real de cada día. El % compara contra el plan del día: en verde entre 90 % y 110 %, en rosa fuera de ese rango."

## Hoja Audiencias

Un bloque por medio:
- nombre de la audiencia guardada;
- ubicación e idioma;
- segmentación (cargos, intereses, listas);
- exclusiones;
- expansión de audiencia;
- tamaño;
- presupuesto cargado;
- previsión de la plataforma como referencia.

Leyenda con la fuente.

## Hoja Copys
Ver `specs-copys.md`.
- Mensaje central arriba, con la bajada.
- Reglas generales: marca del evento, rol de la marca, datos a validar, tono y destino.
- Por medio: un bloque de requisitos y una tabla con columnas Grupo | Recurso | Texto | Caracteres (`=LARGO(texto)`) | Máximo | Estado.
- Formato condicional en rosa si Caracteres supera el Máximo.
- Estado "Validar" en todo lo que afirme plazos, cobertura, servicios o nombre otras marcas.
