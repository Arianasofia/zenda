import sys, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

OUT = sys.argv[1]

# ---- estética (modelo Pickit / Zenda)
NEGRO, VERDE, VERDE_H, VERDE_T, GRIS, CELESTE, AZUL = "0A0A0B", "2FA37A", "59D7A2", "EAF9F3", "F7F7F8", "EAF7FB", "0000FF"
ROSA_P = "FCE4F3"  # pendiente de confirmar con el cliente
F = lambda **k: Font(name="Calibri", **{"size": 10, "color": NEGRO, **k})
fill = lambda c: PatternFill("solid", fgColor=c)
MONEY, INT, PCT2, PCT0 = '"$" #,##0', "#,##0", "0.00%", "0%"
DATE = "dd/mm/yyyy"
thin = Side(style="thin", color="DDDDDD")

wb = Workbook()

def sheet(ws, widths):
    ws.sheet_view.showGridLines = False
    for col, w in widths.items():
        ws.column_dimensions[col].width = w

def put(ws, ref, v, font=None, fmt=None, bg=None, al="left"):
    c = ws[ref]
    c.value = v
    c.font = font or F()
    if fmt: c.number_format = fmt
    if bg: c.fill = fill(bg)
    c.alignment = Alignment(horizontal=al, vertical="center")
    return c

def band(ws, row, c1, c2, text, size=12, bg=NEGRO, color="FFFFFF"):
    for c in range(c1, c2 + 1):
        ws.cell(row, c).fill = fill(bg)
    put(ws, f"{L(c1)}{row}", text, F(size=size, bold=True, color=color), bg=bg)

def header(ws, row, c1, names):
    for i, n in enumerate(names):
        put(ws, f"{L(c1+i)}{row}", n, F(bold=True), bg=VERDE_H)

def brand(ws, title):
    put(ws, "B2", "zenda.", F(size=11, bold=True, color=VERDE))
    put(ws, "B3", title, F(size=16, bold=True))

def pend(c, note=None):
    c.fill = fill(ROSA_P)
    if note: c.comment = Comment(note, "Zenda")

# =====================================================================
# SUPUESTOS
# =====================================================================
S = wb.active
S.title = "Supuestos"
sheet(S, {"A": 2.6, "B": 34, "C": 16, "D": 16, "E": 16, "F": 14, "G": 14, "H": 14, "I": 14})
brand(S, "Sancor Seguros  |  Media Plan Cyber Monday 2026 · Supuestos")
put(S, "B4", "Celdas en rosa: datos de ejemplo, pendientes de confirmar con el cliente. Texto azul: dato cargado a mano. Negro: fórmula.", F(size=9, italic=True, color="666666"))

band(S, 6, 2, 5, "FECHAS")
header(S, 7, 2, ["Etapa", "Inicio", "Fin", "Días"])
fechas = [("Teaser", dt.date(2026, 10, 28), dt.date(2026, 11, 1)),
          ("Cyber Monday + Cyber Week", dt.date(2026, 11, 2), dt.date(2026, 11, 8))]
for i, (n, a, b) in enumerate(fechas):
    r = 8 + i
    put(S, f"B{r}", n)
    for col, v in (("C", a), ("D", b)):
        pend(put(S, f"{col}{r}", v, F(color=AZUL), DATE),
             "Fecha estimada: Cyber Monday 2025 fue del 3 al 5/11 con extensión a toda la semana. Confirmar fechas oficiales 2026.")
    put(S, f"E{r}", f"=D{r}-C{r}+1", fmt=INT)
TEASER_INI, TEASER_FIN, TEASER_DIAS = "Supuestos!$C$8", "Supuestos!$D$8", "Supuestos!$E$8"
EV_INI, EV_DIAS = "Supuestos!$C$9", "Supuestos!$E$9"

band(S, 11, 2, 5, "PRESUPUESTO POR PRODUCTO")
header(S, 12, 2, ["Producto", "Etapa", "Inversión", "% del total"])
productos = [("Teaser", "Teaser", 325000), ("Auto", "Performance", 5700000), ("Moto", "Performance", 1500000),
             ("Movilidad", "Performance", 980000), ("Hogar", "Performance", 910000)]
PRES = {}
for i, (p, et, v) in enumerate(productos):
    r = 13 + i
    put(S, f"B{r}", p); put(S, f"C{r}", et)
    pend(put(S, f"D{r}", v, F(color=AZUL), MONEY),
         "Monto de ejemplo (inversión Cyber 2025 + ~30 %). Reemplazar con el presupuesto que mande el cliente.")
    put(S, f"E{r}", f"=IFERROR(D{r}/$D$18,\"\")", fmt=PCT0)
    PRES[p] = f"Supuestos!$D${r}"
put(S, "B18", "TOTAL", F(bold=True), bg=VERDE_T); put(S, "C18", None, bg=VERDE_T)
put(S, "D18", "=SUM(D13:D17)", F(bold=True, color=VERDE), MONEY, VERDE_T)
put(S, "E18", "=SUM(E13:E17)", F(bold=True), PCT0, VERDE_T)

band(S, 20, 2, 7, "REFERENCIA CYBER 2025 Y AJUSTE DE CONVERSIONES")
header(S, 21, 2, ["Producto", "Conv. proyectadas 2025", "Conv. reales 2025", "Cumplimiento 2025", "Ajuste 2026", "Comentario"])
ref25 = [("Auto", 215, 169.24), ("Moto", 243, 234.71), ("Movilidad", 84, 55.61), ("Hogar", 16, 10)]
AJ = {}
for i, (p, pr, re) in enumerate(ref25):
    r = 22 + i
    put(S, f"B{r}", p)
    put(S, f"C{r}", pr, F(color=AZUL), INT); put(S, f"D{r}", re, F(color=AZUL), INT)
    put(S, f"E{r}", f"=IFERROR(D{r}/C{r},\"\")", fmt=PCT0)
    put(S, f"F{r}", f"=MIN(1,E{r})", fmt=PCT0)
    put(S, f"G{r}", "Por defecto, el cumplimiento 2025 (tope 100 %). Se puede pisar a mano.", F(size=9, color="666666"))
    AJ[p] = f"Supuestos!$F${r}"
put(S, "B26", "Fuente: hoja \"Conversiones - Plataforma\" del MP Cyber 2025. El ajuste multiplica la Conv. Rate del mes anterior.", F(size=9, italic=True, color="666666"))

band(S, 28, 2, 9, "DISTRIBUCIÓN DIARIA DE LA SEMANA CYBER")
header(S, 29, 2, ["", "Día 1", "Día 2", "Día 3", "Día 4", "Día 5", "Día 6", "Día 7"])
put(S, "B30", "Fecha")
put(S, "B31", "% de la inversión")
pesos = [0.17, 0.17, 0.16, 0.15, 0.13, 0.11, 0.11]
for i, w in enumerate(pesos):
    col = L(3 + i)
    put(S, f"{col}30", f"={EV_INI}+{i}", fmt="ddd dd/mm")
    put(S, f"{col}31", w, F(color=AZUL), PCT0)
put(S, "B32", "Control (debe dar 100 %)", F(bold=True), bg=VERDE_T)
put(S, "C32", "=SUM(C31:I31)", F(bold=True), PCT0, VERDE_T)
put(S, "B33", "Curva tomada del BGT Diario 2025. Si la semana cambia de largo, ajustar los días y que el control dé 100 %.", F(size=9, italic=True, color="666666"))

# =====================================================================
# MP
# =====================================================================
M = wb.create_sheet("MP Cyber 2026", 0)
sheet(M, {"A": 2.6, "B": 34, "C": 13, "D": 14, "E": 7, "F": 14, "G": 11, "H": 9, "I": 10, "J": 9,
          "K": 10, "L": 11, "M": 13, "N": 13, "O": 13, "P": 11, "Q": 14})
brand(M, "Sancor Seguros  |  Media Plan Cyber Monday 2026")
put(M, "B4", "Versión de ejemplo: presupuesto, productos y fechas pendientes de confirmar (celdas en rosa en Supuestos).", F(size=9, italic=True, color="666666"))

# ---- bloques de detalle (se escriben primero para conocer las filas)
PERF_COLS = ["Campaña", "Medio", "Estrategia", "%", "Inversión", "CPC", "CTR", "CR base", "Ajuste", "CR Cyber",
             "Clicks", "Impresiones", "Conversiones", "CPA", "CPM", "Inv. diaria prom."]
NOTA_BENCH = "Benchmark: real de la misma campaña en octubre 2026 (MP GSS octubre)."
bloques = {
    "Auto": [("GOOGLE SEARCH - BRAND", "Google Ads", 0.32, 542.37, 0.3084, 0.0140, NOTA_BENCH),
             ("GOOGLE SEARCH - NOT BRAND", "Google Ads", 0.26, 3108.27, 0.0572, 0.0581, "Benchmark: Search Category de Auto, octubre 2026."),
             ("PERFORMANCE MAX", "Google Ads", 0.37, 547.06, 0.0143, 0.0278, NOTA_BENCH),
             ("META", "Meta Ads", 0.05, 246.54, 0.0055, 0.0067, NOTA_BENCH)],
    "Moto": [("SEM - BRAND", "Google Ads", 0.16, 270.30, 0.6377, 0.1538, NOTA_BENCH),
             ("SEM - CATEGORÍA", "Google Ads", 0.26, 187.97, 0.1514, 0.1568, "Benchmark: Search Not Brand de Moto, octubre 2026."),
             ("PERFORMANCE MAX", "Google Ads", 0.53, 244.10, 0.0419, 0.2040, NOTA_BENCH),
             ("META", "Meta Ads", 0.05, 292.91, 0.0136, 0.1086, NOTA_BENCH)],
    "Movilidad": [("SEM - BRAND", "Google Ads", 0.07, 1742.57, 0.3835, 0.1191, NOTA_BENCH),
                  ("SEM - CATEGORÍA", "Google Ads", 0.63, 1261.64, 0.1450, 0.0762, NOTA_BENCH),
                  ("PERFORMANCE MAX", "Google Ads", 0.15, 214.53, 0.0429, 0.0358, "Campaña nueva para el Cyber de Movilidad (en 2025 no corrió). " + NOTA_BENCH),
                  ("META", "Meta Ads", 0.15, 461.64, 0.0064, 0.0388, NOTA_BENCH)],
    "Hogar": [("GOOGLE SEARCH - BRAND", "Google Ads", 0.10, 872.46, 0.3918, 0.0526, "Hogar no pauta en octubre: benchmark del Cyber 2025 con CPC + 22 % de inflación anual."),
              ("GOOGLE SEARCH - NOT BRAND", "Google Ads", 0.33, 2186.44, 0.0843, 0.0234, "Hogar no pauta en octubre: benchmark del Cyber 2025 con CPC + 22 % de inflación anual."),
              ("PERFORMANCE MAX", "Google Ads", 0.57, 500.10, 0.0183, 0.0079, "Hogar no pauta en octubre: benchmark del Cyber 2025 con CPC + 22 % de inflación anual.")],
}

row = 26  # el detalle arranca debajo de los resúmenes
band(M, row, 2, 17, "DETALLE POR CAMPAÑA")
row += 2

# Teaser
TEASER_COLS = ["Campaña", "Medio", "Estrategia", "%", "Inversión", "CPM", "CPC", "", "", "",
               "Clicks", "Impresiones", "CTR", "", "", "Inv. diaria prom."]
band(M, row, 2, 17, "  Teaser", 11, CELESTE, NEGRO); row += 1
header(M, row, 2, TEASER_COLS); row += 1
teaser = [("DEMAND GEN - TRÁFICO", "Google Ads", 0.5, 325.17, 10.62, "Benchmark: Demand Gen de tráfico (PS NOA), octubre 2026."),
          ("META - TRÁFICO", "Meta Ads", 0.5, 400.00, 37.10, "Benchmark: Meta clics (PS ION), octubre 2026.")]
t0 = row
for i, (n, med, pct, cpm, cpc, nota) in enumerate(teaser):
    r = row
    bg = GRIS if i % 2 else None
    put(M, f"B{r}", n, bg=bg); put(M, f"C{r}", med, bg=bg); put(M, f"D{r}", "TRÁFICO", bg=bg)
    put(M, f"E{r}", pct, F(color=AZUL), PCT0, bg)
    put(M, f"F{r}", f"=E{r}*{PRES['Teaser']}", fmt=MONEY, bg=bg)
    c = put(M, f"G{r}", cpm, F(color=AZUL), MONEY, bg); c.comment = Comment(nota, "Zenda")
    put(M, f"H{r}", cpc, F(color=AZUL), MONEY, bg)
    for col in "IJK": put(M, f"{col}{r}", None, bg=bg)
    put(M, f"L{r}", f"=IFERROR(F{r}/H{r},\"\")", fmt=INT, bg=bg)
    put(M, f"M{r}", f"=IFERROR(F{r}/G{r}*1000,\"\")", fmt=INT, bg=bg)
    put(M, f"N{r}", f"=IFERROR(L{r}/M{r},\"\")", fmt=PCT2, bg=bg)
    for col in "OP": put(M, f"{col}{r}", None, bg=bg)
    put(M, f"Q{r}", f"=IFERROR(F{r}/{TEASER_DIAS},\"\")", fmt=MONEY, bg=bg)
    row += 1
t1 = row - 1
TT = row
put(M, f"B{TT}", "Subtotal Teaser", F(bold=True), bg=VERDE_T)
for col in "CDGHIJKOP": put(M, f"{col}{TT}", None, bg=VERDE_T)
put(M, f"E{TT}", f"=SUM(E{t0}:E{t1})", F(bold=True), PCT0, VERDE_T)
put(M, f"F{TT}", f"=SUM(F{t0}:F{t1})", F(bold=True, color=VERDE), MONEY, VERDE_T)
put(M, f"L{TT}", f"=SUM(L{t0}:L{t1})", F(bold=True), INT, VERDE_T)
put(M, f"M{TT}", f"=SUM(M{t0}:M{t1})", F(bold=True), INT, VERDE_T)
put(M, f"N{TT}", f"=IFERROR(L{TT}/M{TT},\"\")", F(bold=True), PCT2, VERDE_T)
put(M, f"Q{TT}", f"=SUM(Q{t0}:Q{t1})", F(bold=True), MONEY, VERDE_T)
TEASER_ROWS = (t0, t1)
row += 2

SUB = {}
CAMP_ROWS = {}
for prod, camps in bloques.items():
    band(M, row, 2, 17, f"  Performance {prod}", 11, CELESTE, NEGRO); row += 1
    header(M, row, 2, PERF_COLS); row += 1
    r0 = row
    for i, (n, med, pct, cpc, ctr, cr, nota) in enumerate(camps):
        r = row
        bg = GRIS if i % 2 else None
        put(M, f"B{r}", n, bg=bg); put(M, f"C{r}", med, bg=bg); put(M, f"D{r}", "CONVERSIONES", bg=bg)
        put(M, f"E{r}", pct, F(color=AZUL), PCT0, bg)
        put(M, f"F{r}", f"=E{r}*{PRES[prod]}", fmt=MONEY, bg=bg)
        c = put(M, f"G{r}", cpc, F(color=AZUL), MONEY, bg); c.comment = Comment(nota, "Zenda")
        put(M, f"H{r}", ctr, F(color=AZUL), PCT2, bg)
        put(M, f"I{r}", cr, F(color=AZUL), PCT2, bg)
        put(M, f"J{r}", f"={AJ[prod]}", fmt=PCT0, bg=bg)
        put(M, f"K{r}", f"=I{r}*J{r}", fmt=PCT2, bg=bg)
        put(M, f"L{r}", f"=IFERROR(F{r}/G{r},\"\")", fmt=INT, bg=bg)
        put(M, f"M{r}", f"=IFERROR(L{r}/H{r},\"\")", fmt=INT, bg=bg)
        put(M, f"N{r}", f"=IFERROR(L{r}*K{r},\"\")", fmt="#,##0.0", bg=bg)
        put(M, f"O{r}", f"=IFERROR(F{r}/N{r},\"\")", fmt=MONEY, bg=bg)
        put(M, f"P{r}", f"=IFERROR(F{r}/M{r}*1000,\"\")", fmt=MONEY, bg=bg)
        put(M, f"Q{r}", f"=IFERROR(F{r}/{EV_DIAS},\"\")", fmt=MONEY, bg=bg)
        row += 1
    r1 = row - 1
    T = row
    put(M, f"B{T}", f"Subtotal {prod}", F(bold=True), bg=VERDE_T)
    for col in "CDGHIJ": put(M, f"{col}{T}", None, bg=VERDE_T)
    put(M, f"E{T}", f"=SUM(E{r0}:E{r1})", F(bold=True), PCT0, VERDE_T)
    put(M, f"F{T}", f"=SUM(F{r0}:F{r1})", F(bold=True, color=VERDE), MONEY, VERDE_T)
    put(M, f"K{T}", f"=IFERROR(N{T}/L{T},\"\")", F(bold=True), PCT2, VERDE_T)
    for col, fm in (("L", INT), ("M", INT), ("N", "#,##0.0"), ("Q", MONEY)):
        put(M, f"{col}{T}", f"=SUM({col}{r0}:{col}{r1})", F(bold=True), fm, VERDE_T)
    put(M, f"O{T}", f"=IFERROR(F{T}/N{T},\"\")", F(bold=True), MONEY, VERDE_T)
    put(M, f"P{T}", f"=IFERROR(F{T}/M{T}*1000,\"\")", F(bold=True), MONEY, VERDE_T)
    # CPC y CTR del subtotal, recalculados
    put(M, f"G{T}", f"=IFERROR(F{T}/L{T},\"\")", F(bold=True), MONEY, VERDE_T)
    put(M, f"H{T}", f"=IFERROR(L{T}/M{T},\"\")", F(bold=True), PCT2, VERDE_T)
    SUB[prod] = T
    CAMP_ROWS[prod] = (r0, r1)
    row += 2
LAST = row

# rango completo del detalle para SUMIF por medio
D0, D1 = 28, LAST

# ---- resúmenes arriba
band(M, 6, 2, 8, "RESUMEN POR ETAPA Y PRODUCTO")
header(M, 7, 2, ["Producto", "Etapa", "Inversión", "% del total", "Conversiones", "CPA", "Clicks"])
filas = [("Teaser", "Teaser", TT)] + [(p, "Performance", SUB[p]) for p in bloques]
for i, (p, et, T) in enumerate(filas):
    r = 8 + i
    bg = GRIS if i % 2 else None
    put(M, f"B{r}", p, bg=bg); put(M, f"C{r}", et, bg=bg)
    put(M, f"D{r}", f"=F{T}", F(color=VERDE), MONEY, bg)
    put(M, f"E{r}", f"=IFERROR(D{r}/$D$13,\"\")", fmt=PCT0, bg=bg)
    if p == "Teaser":
        put(M, f"F{r}", "-", bg=bg, al="right"); put(M, f"G{r}", "-", bg=bg, al="right")
    else:
        put(M, f"F{r}", f"=N{T}", fmt="#,##0", bg=bg)
        put(M, f"G{r}", f"=IFERROR(D{r}/F{r},\"\")", fmt=MONEY, bg=bg)
    put(M, f"H{r}", f"=L{T}", fmt=INT, bg=bg)
put(M, "B13", "TOTAL", F(bold=True), bg=VERDE_T); put(M, "C13", None, bg=VERDE_T)
put(M, "D13", "=SUM(D8:D12)", F(bold=True, color=VERDE), MONEY, VERDE_T)
put(M, "E13", "=SUM(E8:E12)", F(bold=True), PCT0, VERDE_T)
put(M, "F13", "=SUM(F9:F12)", F(bold=True), "#,##0", VERDE_T)
put(M, "G13", "=IFERROR(SUM(D9:D12)/F13,\"\")", F(bold=True), MONEY, VERDE_T)
put(M, "H13", "=SUM(H8:H12)", F(bold=True), INT, VERDE_T)
put(M, "B14", "CPA total calculado solo sobre Performance (el teaser no lleva conversiones).", F(size=9, italic=True, color="666666"))

band(M, 6, 10, 14, "RESUMEN POR MEDIO")
header(M, 7, 10, ["Medio", "Inversión", "% del total", "Conversiones", "CPA"])
for i, med in enumerate(["Google Ads", "Meta Ads"]):
    r = 8 + i
    bg = GRIS if i % 2 else None
    put(M, f"J{r}", med, bg=bg)
    put(M, f"K{r}", f"=SUMIF($C${D0}:$C${D1},J{r},$F${D0}:$F${D1})", F(color=VERDE), MONEY, bg)
    put(M, f"L{r}", f"=IFERROR(K{r}/$K$10,\"\")", fmt=PCT0, bg=bg)
    # conversiones solo de bloques de performance (columna N)
    put(M, f"M{r}", f"=SUMIF($C${CAMP_ROWS['Auto'][0]}:$C${D1},J{r},$N${CAMP_ROWS['Auto'][0]}:$N${D1})", fmt="#,##0", bg=bg)
    put(M, f"N{r}", f"=IFERROR(SUMIF($C${CAMP_ROWS['Auto'][0]}:$C${D1},J{r},$F${CAMP_ROWS['Auto'][0]}:$F${D1})/M{r},\"\")", fmt=MONEY, bg=bg)
put(M, "J10", "TOTAL", F(bold=True), bg=VERDE_T)
put(M, "K10", "=SUM(K8:K9)", F(bold=True, color=VERDE), MONEY, VERDE_T)
put(M, "L10", "=SUM(L8:L9)", F(bold=True), PCT0, VERDE_T)
put(M, "M10", "=SUM(M8:M9)", F(bold=True), "#,##0", VERDE_T)
put(M, "N10", "=IFERROR(SUM(D9:D12)/M10,"")", F(bold=True), MONEY, VERDE_T)

band(M, 16, 10, 14, "CONTROLES")
controles = [
    ("Detalle = presupuesto", "=IF(ROUND(D13-Supuestos!D18,0)=0,\"OK\",\"REVISAR\")"),
    ("Medios = total", "=IF(ROUND(K10-D13,0)=0,\"OK\",\"REVISAR\")"),
    ("% de cada bloque = 100 %", "=IF(AND(" + ",".join([f"ROUND(E{TT},4)=1"] + [f"ROUND(E{SUB[p]},4)=1" for p in bloques]) + "),\"OK\",\"REVISAR\")"),
    ("Curva diaria = 100 %", "=IF(ROUND(Supuestos!C32,4)=1,\"OK\",\"REVISAR\")"),
]
for i, (n, f) in enumerate(controles):
    r = 17 + i
    put(M, f"J{r}", n)
    put(M, f"M{r}", f, F(bold=True))

band(M, 16, 2, 8, "FECHAS")
put(M, "B17", "Teaser"); put(M, "C17", f"={TEASER_INI}", fmt=DATE); put(M, "D17", f"={TEASER_FIN}", fmt=DATE)
put(M, "B18", "Cyber Monday + Cyber Week"); put(M, "C18", f"={EV_INI}", fmt=DATE); put(M, "D18", "=Supuestos!D9", fmt=DATE)
put(M, "B19", "Presupuesto total"); put(M, "C19", "=Supuestos!D18", F(bold=True, color=VERDE), MONEY)

M.freeze_panes = "C1"

# =====================================================================
# BGT DIARIO
# =====================================================================
B = wb.create_sheet("BGT Diario", 1)
sheet(B, {"A": 2.6, "B": 34, "C": 14, **{L(4 + i): 12 for i in range(7)}, "K": 13})
brand(B, "Sancor Seguros  |  Cyber Monday 2026 · Inversión diaria")
put(B, "B4", "Semana Cyber: inversión de cada campaña × curva diaria de Supuestos. Teaser: inversión pareja por día.", F(size=9, italic=True, color="666666"))
r = 6
band(B, r, 2, 11, "SEMANA CYBER"); r += 1
for prod in bloques:
    band(B, r, 2, 11, f"  Performance {prod}", 11, CELESTE, NEGRO); r += 1
    header(B, r, 2, ["Campaña", "Inversión"] + [None] * 7 + ["Control"])
    for i in range(7):
        put(B, f"{L(4+i)}{r}", f"=Supuestos!{L(3+i)}30", F(bold=True), "ddd dd/mm", VERDE_H)
    r += 1
    a, b = CAMP_ROWS[prod]
    b0 = r
    for k, mr in enumerate(range(a, b + 1)):
        bg = GRIS if k % 2 else None
        put(B, f"B{r}", f"='MP Cyber 2026'!B{mr}", bg=bg)
        put(B, f"C{r}", f"='MP Cyber 2026'!F{mr}", fmt=MONEY, bg=bg)
        for i in range(7):
            put(B, f"{L(4+i)}{r}", f"=$C{r}*Supuestos!{L(3+i)}$31", fmt=MONEY, bg=bg)
        put(B, f"K{r}", f"=SUM(D{r}:J{r})-C{r}", fmt=MONEY, bg=bg)
        r += 1
    put(B, f"B{r}", f"Subtotal {prod}", F(bold=True), bg=VERDE_T)
    for col in ["C"] + [L(4 + i) for i in range(7)] + ["K"]:
        put(B, f"{col}{r}", f"=SUM({col}{b0}:{col}{r-1})", F(bold=True), MONEY, VERDE_T)
    r += 2

band(B, r, 2, 11, "TEASER"); r += 1
header(B, r, 2, ["Campaña", "Inversión", "Inicio", "Fin", "Días", "Por día", "", "", "", ""]); r += 1
for k, mr in enumerate(range(TEASER_ROWS[0], TEASER_ROWS[1] + 1)):
    bg = GRIS if k % 2 else None
    put(B, f"B{r}", f"='MP Cyber 2026'!B{mr}", bg=bg)
    put(B, f"C{r}", f"='MP Cyber 2026'!F{mr}", fmt=MONEY, bg=bg)
    put(B, f"D{r}", f"={TEASER_INI}", fmt=DATE, bg=bg)
    put(B, f"E{r}", f"={TEASER_FIN}", fmt=DATE, bg=bg)
    put(B, f"F{r}", f"={TEASER_DIAS}", fmt=INT, bg=bg)
    put(B, f"G{r}", f"=IFERROR(C{r}/F{r},\"\")", fmt=MONEY, bg=bg)
    r += 1

wb.save(OUT)
print("ok", OUT)
