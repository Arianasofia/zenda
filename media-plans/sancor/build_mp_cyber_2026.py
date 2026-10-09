"""Genera el MP Cyber Monday 2026 de Sancor Seguros con estética Zenda.

Uso: python3 build_mp_cyber_2026.py <salida.xlsx>
Los datos de ejemplo (presupuesto, fechas) están en la hoja Supuestos, en rosa.
"""
import sys, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule, DataBarRule, ColorScaleRule
from openpyxl.utils import get_column_letter as L

OUT = sys.argv[1]

# ---- paleta Zenda
NEGRO, MUTED, VERDE, VERDE_INK, CYAN, ROSA = "0A0A0B", "6B6B6E", "59D7A2", "2FA37A", "95D6EA", "E71CA2"
L_VERDE, L_ROSA, L_CYAN, ZEBRA, GRID, INPUT = "EAF9F3", "FDEAF5", "EAF7FB", "F7F7F8", "E3E3E5", "1155CC"
F = lambda **k: Font(name="Calibri", **{"size": 10, "color": NEGRO, **k})
fill = lambda c: PatternFill("solid", fgColor=c)
side = Side(style="thin", color=GRID)
BOX = Border(left=side, right=side, top=side, bottom=side)
MONEY, INT, DEC1, PCT2, PCT0, DATE = '"$" #,##0', "#,##0", "#,##0.0", "0.00%", "0%", "dd/mm/yyyy"
NUMERIC = {MONEY, INT, DEC1, PCT2, PCT0, DATE, "ddd dd/mm"}

wb = Workbook()


def sheet(ws, widths):
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = VERDE
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def put(ws, ref, v, font=None, fmt=None, bg=None, al=None, box=False):
    c = ws[ref]
    c.value = v
    c.font = font or F()
    if fmt: c.number_format = fmt
    if bg: c.fill = fill(bg)
    if al is None:
        al = "right" if fmt in NUMERIC else "left"
    c.alignment = Alignment(horizontal=al, vertical="center", indent=1 if al == "left" else 0)
    if box: c.border = BOX
    return c


def cell(ws, ref, v, fmt=None, bg=None, bold=False, color=NEGRO, al=None):
    """Celda de tabla: con borde fino."""
    return put(ws, ref, v, F(bold=bold, color=color), fmt, bg, al, box=True)


def inp(ws, ref, v, fmt, note=None):
    """Dato cargado a mano: azul sobre celeste claro."""
    c = put(ws, ref, v, F(color=INPUT), fmt, L_CYAN, box=True)
    if note: c.comment = Comment(note, "Zenda")
    return c


def pend(c, note=None):
    c.fill = fill(L_ROSA)
    c.font = F(color=ROSA, bold=True)
    if note: c.comment = Comment(note, "Zenda")


def band(ws, row, c1, c2, text, size=12, bg=NEGRO, color="FFFFFF", h=24):
    for c in range(c1, c2 + 1):
        ws.cell(row, c).fill = fill(bg)
    put(ws, f"{L(c1)}{row}", text, F(size=size, bold=True, color=color), bg=bg)
    ws.row_dimensions[row].height = h


def header(ws, row, c1, names, bg=VERDE):
    for i, n in enumerate(names):
        c = put(ws, f"{L(c1+i)}{row}", n, F(bold=True), bg=bg, al="center", box=True)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 30


def groups(ws, row, spans):
    """Fila de grupos de columnas sobre el encabezado (Inversión / Benchmarks / Resultados)."""
    for c1, c2, text, bg, color in spans:
        for c in range(c1, c2 + 1):
            ws.cell(row, c).fill = fill(bg)
            ws.cell(row, c).border = BOX
        if c2 > c1:
            ws.merge_cells(start_row=row, start_column=c1, end_row=row, end_column=c2)
        put(ws, f"{L(c1)}{row}", text, F(size=9, bold=True, color=color), bg=bg, al="center", box=True)
    ws.row_dimensions[row].height = 18


def total_row(ws, row, c1, c2):
    for c in range(c1, c2 + 1):
        x = ws.cell(row, c)
        x.fill = fill(L_VERDE)
        x.border = Border(left=side, right=side, top=Side(style="medium", color=VERDE), bottom=side)
    ws.row_dimensions[row].height = 20


def brand(ws, title, subtitle=None):
    put(ws, "B2", "zenda.", F(size=12, bold=True, color=VERDE_INK))
    put(ws, "B3", title, F(size=18, bold=True))
    ws.row_dimensions[3].height = 28
    if subtitle:
        put(ws, "B4", subtitle, F(size=9, italic=True, color=MUTED))


def card(ws, row, c1, c2, label, formula, fmt, bg, sub=None):
    """KPI card: label chico gris, número grande, aclaración abajo."""
    for r in range(row, row + 3):
        for c in range(c1, c2 + 1):
            ws.cell(r, c).fill = fill(bg)
        ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
    put(ws, f"{L(c1)}{row}", label.upper(), F(size=9, bold=True, color=MUTED), bg=bg, al="left")
    v = put(ws, f"{L(c1)}{row+1}", formula, F(size=20, bold=True, color=NEGRO), fmt, bg, al="left")
    if sub:
        put(ws, f"{L(c1)}{row+2}", sub, F(size=9, color=MUTED), bg=bg, al="left")
    ws.row_dimensions[row].height = 18
    ws.row_dimensions[row + 1].height = 32
    ws.row_dimensions[row + 2].height = 16
    return v


def note(ws, ref, text):
    put(ws, ref, text, F(size=9, italic=True, color=MUTED))


# =====================================================================
# SUPUESTOS
# =====================================================================
S = wb.active
S.title = "Supuestos"
sheet(S, {"A": 2.6, "B": 32, "C": 18, "D": 18, "E": 16, "F": 14, "G": 14, "H": 14, "I": 14, "J": 3, "K": 60})
brand(S, "Supuestos del Media Plan", "Lo único que se edita a mano está acá. El MP y el BGT Diario se recalculan solos.")

# leyenda
put(S, "B6", "REFERENCIAS", F(size=9, bold=True, color=MUTED))
put(S, "B7", "Dato cargado a mano", F(color=INPUT), bg=L_CYAN, box=True)
c = put(S, "B8", "Pendiente de confirmar con el cliente", box=True); pend(c)
put(S, "B9", "Fórmula (no tocar)", box=True)

band(S, 11, 2, 5, "FECHAS")
header(S, 12, 2, ["Etapa", "Inicio", "Fin", "Días"])
fechas = [("Teaser", dt.date(2026, 10, 28), dt.date(2026, 11, 1)),
          ("Cyber Monday + Cyber Week", dt.date(2026, 11, 2), dt.date(2026, 11, 8))]
for i, (n, a, b) in enumerate(fechas):
    r = 13 + i
    cell(S, f"B{r}", n, bold=True)
    for col, v in (("C", a), ("D", b)):
        pend(inp(S, f"{col}{r}", v, DATE),
             "Fecha estimada: Cyber Monday 2025 fue del 3 al 5/11 con extensión a toda la semana. Confirmar fechas oficiales 2026.")
    cell(S, f"E{r}", f"=D{r}-C{r}+1", INT)
TEASER_INI, TEASER_FIN, TEASER_DIAS = "Supuestos!$C$13", "Supuestos!$D$13", "Supuestos!$E$13"
EV_INI, EV_FIN, EV_DIAS = "Supuestos!$C$14", "Supuestos!$D$14", "Supuestos!$E$14"

band(S, 17, 2, 5, "PRESUPUESTO POR PRODUCTO")
header(S, 18, 2, ["Producto", "Etapa", "Inversión", "% del total"])
productos = [("Teaser", "Teaser", 325000), ("Auto", "Performance", 5700000), ("Moto", "Performance", 1500000),
             ("Movilidad", "Performance", 980000), ("Hogar", "Performance", 910000)]
PRES = {}
for i, (p, et, v) in enumerate(productos):
    r = 19 + i
    bg = ZEBRA if i % 2 else None
    cell(S, f"B{r}", p, bg=bg, bold=True); cell(S, f"C{r}", et, bg=bg)
    pend(inp(S, f"D{r}", v, MONEY),
         "Monto de ejemplo (inversión Cyber 2025 + ~30 %). Reemplazar con el presupuesto que mande el cliente.")
    cell(S, f"E{r}", f"=IFERROR(D{r}/$D$24,\"\")", PCT0, bg)
    PRES[p] = f"Supuestos!$D${r}"
total_row(S, 24, 2, 5)
put(S, "B24", "TOTAL", F(bold=True), bg=L_VERDE, box=True)
put(S, "D24", "=SUM(D19:D23)", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
put(S, "E24", "=SUM(E19:E23)", F(bold=True), PCT0, L_VERDE, box=True)
S.conditional_formatting.add("E19:E23", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=VERDE))

band(S, 26, 2, 6, "REFERENCIA CYBER 2025 Y AJUSTE DE CONVERSIONES")
header(S, 27, 2, ["Producto", "Conv. proyectadas 2025", "Conv. reales 2025", "Cumplimiento 2025", "Ajuste 2026"])
ref25 = [("Auto", 215, 169.24), ("Moto", 243, 234.71), ("Movilidad", 84, 55.61), ("Hogar", 16, 10)]
AJ = {}
for i, (p, pr, re) in enumerate(ref25):
    r = 28 + i
    bg = ZEBRA if i % 2 else None
    cell(S, f"B{r}", p, bg=bg, bold=True)
    inp(S, f"C{r}", pr, INT); inp(S, f"D{r}", re, INT)
    cell(S, f"E{r}", f"=IFERROR(D{r}/C{r},\"\")", PCT0, bg)
    cell(S, f"F{r}", f"=MIN(1,E{r})", PCT0, bg, bold=True)
    AJ[p] = f"Supuestos!$F${r}"
S.conditional_formatting.add("E28:E31", CellIsRule(operator="lessThan", formula=["0.8"], font=Font(color=ROSA, bold=True)))
S.conditional_formatting.add("E28:E31", CellIsRule(operator="greaterThanOrEqual", formula=["0.8"], font=Font(color=VERDE_INK, bold=True)))
note(S, "B32", "Fuente: hoja \"Conversiones - Plataforma\" del MP Cyber 2025. El ajuste (tope 100 %) multiplica la Conv. Rate del mes anterior; se puede pisar a mano.")

band(S, 34, 2, 9, "DISTRIBUCIÓN DIARIA DE LA SEMANA CYBER")
header(S, 35, 2, ["", "Día 1", "Día 2", "Día 3", "Día 4", "Día 5", "Día 6", "Día 7"])
cell(S, "B36", "Fecha", bold=True)
cell(S, "B37", "% de la inversión", bold=True)
pesos = [0.17, 0.17, 0.16, 0.15, 0.13, 0.11, 0.11]
for i, w in enumerate(pesos):
    col = L(3 + i)
    cell(S, f"{col}36", f"={EV_INI}+{i}", "ddd dd/mm")
    inp(S, f"{col}37", w, PCT0)
total_row(S, 38, 2, 9)
put(S, "B38", "Control (debe dar 100 %)", F(bold=True), bg=L_VERDE, box=True)
put(S, "C38", "=SUM(C37:I37)", F(bold=True), PCT0, L_VERDE, box=True)
note(S, "B39", "Curva tomada del BGT Diario 2025. Si la semana cambia de largo, ajustar los días y que el control dé 100 %.")
CURVA_FECHA, CURVA_PCT = 36, 37

# =====================================================================
# MP
# =====================================================================
M = wb.create_sheet("MP Cyber 2026", 0)
sheet(M, {"A": 2.6, "B": 30, "C": 12, "D": 15, "E": 8, "F": 14, "G": 11, "H": 10, "I": 10, "J": 12,
          "K": 10, "L": 11, "M": 13, "N": 13, "O": 13, "P": 12, "Q": 14})
brand(M, "Sancor Seguros  |  Media Plan Cyber Monday 2026",
      "Versión de ejemplo: presupuesto, productos y fechas pendientes de confirmar (en rosa, hoja Supuestos).")

# El detalle se arma primero para conocer las filas; los resúmenes van arriba.
DET = 30
band(M, DET, 2, 17, "DETALLE POR CAMPAÑA", h=26)
row = DET + 2

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

GRUPOS_PERF = [(2, 4, "CAMPAÑA", NEGRO, "FFFFFF"), (5, 6, "INVERSIÓN", VERDE_INK, "FFFFFF"),
               (7, 10, "BENCHMARKS", CYAN, NEGRO), (11, 17, "RESULTADOS ESTIMADOS", ROSA, "FFFFFF")]
PERF_COLS = ["Campaña", "Medio", "Estrategia", "%", "Inversión", "CPC", "CTR", "CR base", "Ajuste Cyber",
             "CR Cyber", "Clicks", "Impresiones", "Conversiones", "CPA", "CPM", "Inv. diaria prom."]

# ---- Teaser
band(M, row, 2, 17, "Teaser  ·  tráfico previo al evento", 11, CYAN, NEGRO, h=22); row += 1
groups(M, row, [(2, 4, "CAMPAÑA", NEGRO, "FFFFFF"), (5, 6, "INVERSIÓN", VERDE_INK, "FFFFFF"),
                (7, 10, "BENCHMARKS", CYAN, NEGRO), (11, 17, "RESULTADOS ESTIMADOS", ROSA, "FFFFFF")]); row += 1
header(M, row, 2, ["Campaña", "Medio", "Estrategia", "%", "Inversión", "CPM", "CPC", "", "",
                   "", "Clicks", "Impresiones", "CTR", "", "", "Inv. diaria prom."]); row += 1
teaser = [("DEMAND GEN - TRÁFICO", "Google Ads", 0.5, 325.17, 10.62, "Benchmark: Demand Gen de tráfico (PS NOA), octubre 2026."),
          ("META - TRÁFICO", "Meta Ads", 0.5, 400.00, 37.10, "Benchmark: Meta clics (PS ION), octubre 2026.")]
t0 = row
for i, (n, med, pct, cpm, cpc, nt) in enumerate(teaser):
    r = row
    bg = ZEBRA if i % 2 else None
    cell(M, f"B{r}", n, bg=bg, bold=True); cell(M, f"C{r}", med, bg=bg); cell(M, f"D{r}", "Tráfico", bg=bg)
    inp(M, f"E{r}", pct, PCT0)
    cell(M, f"F{r}", f"=E{r}*{PRES['Teaser']}", MONEY, bg)
    inp(M, f"G{r}", cpm, MONEY, nt); inp(M, f"H{r}", cpc, MONEY, nt)
    for col in "IJKOP": cell(M, f"{col}{r}", None, bg=bg)
    cell(M, f"L{r}", f"=IFERROR(F{r}/H{r},\"\")", INT, bg)
    cell(M, f"M{r}", f"=IFERROR(F{r}/G{r}*1000,\"\")", INT, bg)
    cell(M, f"N{r}", f"=IFERROR(L{r}/M{r},\"\")", PCT2, bg)
    cell(M, f"Q{r}", f"=IFERROR(F{r}/{TEASER_DIAS},\"\")", MONEY, bg)
    row += 1
t1 = row - 1
TT = row
total_row(M, TT, 2, 17)
put(M, f"B{TT}", "Subtotal Teaser", F(bold=True), bg=L_VERDE, box=True)
put(M, f"E{TT}", f"=SUM(E{t0}:E{t1})", F(bold=True), PCT0, L_VERDE, box=True)
put(M, f"F{TT}", f"=SUM(F{t0}:F{t1})", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
put(M, f"L{TT}", f"=SUM(L{t0}:L{t1})", F(bold=True), INT, L_VERDE, box=True)
put(M, f"M{TT}", f"=SUM(M{t0}:M{t1})", F(bold=True), INT, L_VERDE, box=True)
put(M, f"N{TT}", f"=IFERROR(L{TT}/M{TT},\"\")", F(bold=True), PCT2, L_VERDE, box=True)
put(M, f"Q{TT}", f"=SUM(Q{t0}:Q{t1})", F(bold=True), MONEY, L_VERDE, box=True)
TEASER_ROWS = (t0, t1)
row += 2

SUB, CAMP_ROWS = {}, {}
for prod, camps in bloques.items():
    band(M, row, 2, 17, f"Performance {prod}", 11, CYAN, NEGRO, h=22); row += 1
    groups(M, row, GRUPOS_PERF); row += 1
    header(M, row, 2, PERF_COLS); row += 1
    r0 = row
    for i, (n, med, pct, cpc, ctr, cr, nt) in enumerate(camps):
        r = row
        bg = ZEBRA if i % 2 else None
        cell(M, f"B{r}", n, bg=bg, bold=True); cell(M, f"C{r}", med, bg=bg); cell(M, f"D{r}", "Conversiones", bg=bg)
        inp(M, f"E{r}", pct, PCT0)
        cell(M, f"F{r}", f"=E{r}*{PRES[prod]}", MONEY, bg)
        inp(M, f"G{r}", cpc, MONEY, nt); inp(M, f"H{r}", ctr, PCT2); inp(M, f"I{r}", cr, PCT2)
        cell(M, f"J{r}", f"={AJ[prod]}", PCT0, bg, color=MUTED)
        cell(M, f"K{r}", f"=I{r}*J{r}", PCT2, bg)
        cell(M, f"L{r}", f"=IFERROR(F{r}/G{r},\"\")", INT, bg)
        cell(M, f"M{r}", f"=IFERROR(L{r}/H{r},\"\")", INT, bg)
        cell(M, f"N{r}", f"=IFERROR(L{r}*K{r},\"\")", DEC1, bg, bold=True)
        cell(M, f"O{r}", f"=IFERROR(F{r}/N{r},\"\")", MONEY, bg, bold=True)
        cell(M, f"P{r}", f"=IFERROR(F{r}/M{r}*1000,\"\")", MONEY, bg)
        cell(M, f"Q{r}", f"=IFERROR(F{r}/{EV_DIAS},\"\")", MONEY, bg)
        row += 1
    r1 = row - 1
    T = row
    total_row(M, T, 2, 17)
    put(M, f"B{T}", f"Subtotal {prod}", F(bold=True), bg=L_VERDE, box=True)
    put(M, f"E{T}", f"=SUM(E{r0}:E{r1})", F(bold=True), PCT0, L_VERDE, box=True)
    put(M, f"F{T}", f"=SUM(F{r0}:F{r1})", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
    put(M, f"G{T}", f"=IFERROR(F{T}/L{T},\"\")", F(bold=True), MONEY, L_VERDE, box=True)
    put(M, f"H{T}", f"=IFERROR(L{T}/M{T},\"\")", F(bold=True), PCT2, L_VERDE, box=True)
    put(M, f"K{T}", f"=IFERROR(N{T}/L{T},\"\")", F(bold=True), PCT2, L_VERDE, box=True)
    for col, fm in (("L", INT), ("M", INT), ("N", DEC1), ("Q", MONEY)):
        put(M, f"{col}{T}", f"=SUM({col}{r0}:{col}{r1})", F(bold=True), fm, L_VERDE, box=True)
    put(M, f"O{T}", f"=IFERROR(F{T}/N{T},\"\")", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
    put(M, f"P{T}", f"=IFERROR(F{T}/M{T}*1000,\"\")", F(bold=True), MONEY, L_VERDE, box=True)
    SUB[prod] = T
    CAMP_ROWS[prod] = (r0, r1)
    row += 2
D0, D1 = DET, row
P0 = CAMP_ROWS["Auto"][0]

# ---- KPI cards
card(M, 6, 2, 2, "Inversión total", "=D19", MONEY, L_VERDE, "Teaser + Performance")
card(M, 6, 4, 6, "Conversiones estimadas", "=F19", INT, L_VERDE, "Solo Performance")
card(M, 6, 8, 10, "CPA estimado", "=G19", MONEY, L_ROSA, "Solo Performance")
card(M, 6, 12, 14, "Clicks estimados", "=H19", INT, L_CYAN, "Teaser + Performance")
card(M, 6, 16, 17, "Semana Cyber", f"=TEXT({EV_INI},\"dd/mm\")&\" al \"&TEXT({EV_FIN},\"dd/mm\")", None, L_CYAN,
     None)
put(M, "P8", f"=\"Teaser desde el \"&TEXT({TEASER_INI},\"dd/mm\")", F(size=9, color=MUTED), bg=L_CYAN)

# ---- Resumen por etapa y producto
band(M, 11, 2, 8, "RESUMEN POR ETAPA Y PRODUCTO")
header(M, 12, 2, ["Producto", "Etapa", "Inversión", "% del total", "Conversiones", "CPA", "Clicks"])
filas = [("Teaser", "Teaser", TT)] + [(p, "Performance", SUB[p]) for p in bloques]
for i, (p, et, T) in enumerate(filas):
    r = 13 + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"B{r}", p, bg=bg, bold=True); cell(M, f"C{r}", et, bg=bg)
    cell(M, f"D{r}", f"=F{T}", MONEY, bg)
    cell(M, f"E{r}", f"=IFERROR(D{r}/$D$19,\"\")", PCT0, bg)
    if p == "Teaser":
        cell(M, f"F{r}", "–", bg=bg, al="right", color=MUTED); cell(M, f"G{r}", "–", bg=bg, al="right", color=MUTED)
    else:
        cell(M, f"F{r}", f"=N{T}", INT, bg, bold=True)
        cell(M, f"G{r}", f"=IFERROR(D{r}/F{r},\"\")", MONEY, bg)
    cell(M, f"H{r}", f"=L{T}", INT, bg)
# subtotal de Performance (la fila que mira el CPA)
for col in "BCDEFGH":
    M[f"{col}18"].fill = fill(L_CYAN); M[f"{col}18"].border = BOX
put(M, "B18", "Subtotal Performance", F(bold=True), bg=L_CYAN, box=True)
put(M, "D18", "=SUM(D14:D17)", F(bold=True), MONEY, L_CYAN, box=True)
put(M, "E18", "=IFERROR(D18/$D$19,\"\")", F(bold=True), PCT0, L_CYAN, box=True)
put(M, "F18", "=SUM(F14:F17)", F(bold=True), INT, L_CYAN, box=True)
put(M, "G18", "=IFERROR(D18/F18,\"\")", F(bold=True), MONEY, L_CYAN, box=True)
put(M, "H18", "=SUM(H14:H17)", F(bold=True), INT, L_CYAN, box=True)
total_row(M, 19, 2, 8)
put(M, "B19", "TOTAL", F(bold=True), bg=L_VERDE, box=True)
put(M, "D19", "=SUM(D13:D17)", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
put(M, "E19", "=SUM(E13:E17)", F(bold=True), PCT0, L_VERDE, box=True)
put(M, "F19", "=SUM(F14:F17)", F(bold=True), INT, L_VERDE, box=True)
put(M, "G19", "=IFERROR(SUM(D14:D17)/F19,\"\")", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
put(M, "H19", "=SUM(H13:H17)", F(bold=True), INT, L_VERDE, box=True)
note(M, "B20", "El CPA total se calcula solo sobre Performance: el teaser no lleva conversiones.")
M.conditional_formatting.add("E13:E17", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=VERDE))
# CPA por producto: el más caro en rosa, el más barato en verde
M.conditional_formatting.add("G14:G17", ColorScaleRule(start_type="min", start_color=L_VERDE, end_type="max", end_color=L_ROSA))

# ---- Resumen por medio
band(M, 11, 10, 14, "RESUMEN POR MEDIO")
header(M, 12, 10, ["Medio", "Inversión", "% del total", "Conversiones", "CPA"])
for i, med in enumerate(["Google Ads", "Meta Ads"]):
    r = 13 + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"J{r}", med, bg=bg, bold=True)
    cell(M, f"K{r}", f"=SUMIF($C${D0}:$C${D1},J{r},$F${D0}:$F${D1})", MONEY, bg)
    cell(M, f"L{r}", f"=IFERROR(K{r}/$K$15,\"\")", PCT0, bg)
    cell(M, f"M{r}", f"=SUMIF($C${P0}:$C${D1},J{r},$N${P0}:$N${D1})", INT, bg, bold=True)
    cell(M, f"N{r}", f"=IFERROR(SUMIF($C${P0}:$C${D1},J{r},$F${P0}:$F${D1})/M{r},\"\")", MONEY, bg)
total_row(M, 15, 10, 14)
put(M, "J15", "TOTAL", F(bold=True), bg=L_VERDE, box=True)
put(M, "K15", "=SUM(K13:K14)", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
put(M, "L15", "=SUM(L13:L14)", F(bold=True), PCT0, L_VERDE, box=True)
put(M, "M15", "=SUM(M13:M14)", F(bold=True), INT, L_VERDE, box=True)
put(M, "N15", "=IFERROR(SUM(D14:D17)/M15,\"\")", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
M.conditional_formatting.add("L13:L14", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=CYAN))

# ---- Controles
band(M, 21, 10, 14, "CONTROLES")
controles = [
    ("Detalle = presupuesto", "=IF(ROUND(D19-Supuestos!D24,0)=0,\"OK\",\"REVISAR\")"),
    ("Medios = total", "=IF(ROUND(K15-D19,0)=0,\"OK\",\"REVISAR\")"),
    ("% de cada bloque = 100 %", "=IF(AND(" + ",".join([f"ROUND(E{TT},4)=1"] + [f"ROUND(E{SUB[p]},4)=1" for p in bloques]) + "),\"OK\",\"REVISAR\")"),
    ("Curva diaria = 100 %", "=IF(ROUND(Supuestos!C38,4)=1,\"OK\",\"REVISAR\")"),
]
for i, (n, f) in enumerate(controles):
    r = 22 + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"J{r}", n, bg=bg)
    for col in "KL": cell(M, f"{col}{r}", None, bg=bg)
    M.merge_cells(f"J{r}:L{r}")
    for col in "MN": cell(M, f"{col}{r}", None, bg=bg)
    M.merge_cells(f"M{r}:N{r}")
    cell(M, f"M{r}", f, bold=True, al="center")
M.conditional_formatting.add("M22:N25", CellIsRule(operator="equal", formula=['"OK"'], fill=fill(L_VERDE), font=Font(color=VERDE_INK, bold=True)))
M.conditional_formatting.add("M22:N25", CellIsRule(operator="equal", formula=['"REVISAR"'], fill=fill(ROSA), font=Font(color="FFFFFF", bold=True)))

# ---- Referencias de color
band(M, 21, 2, 8, "CÓMO LEER EL DETALLE")
put(M, "B22", "Dato cargado a mano", F(color=INPUT), bg=L_CYAN, box=True)
note(M, "C22", "% de inversión y benchmarks. Cada benchmark tiene un comentario con su fuente.")
put(M, "B23", "Fórmula", box=True)
note(M, "C23", "Todo lo demás. Conversiones y CPA en negrita.")
put(M, "B24", "Subtotal", F(bold=True), bg=L_VERDE, box=True)
note(M, "C24", "Ratios recalculados sobre los totales, no promediados.")
note(M, "B26", "Ajuste Cyber = cumplimiento del Cyber 2025 por producto (hoja Supuestos).")

M.freeze_panes = "C1"

# =====================================================================
# BGT DIARIO
# =====================================================================
B = wb.create_sheet("BGT Diario", 1)
sheet(B, {"A": 2.6, "B": 30, "C": 14, **{L(4 + i): 12 for i in range(7)}, "K": 12})
brand(B, "Inversión diaria  |  Cyber Monday 2026",
      "Semana Cyber: inversión de cada campaña × curva diaria de Supuestos. Teaser: inversión pareja por día.")
r = 6
band(B, r, 2, 11, "SEMANA CYBER"); r += 1
daily_ranges = []
for prod in bloques:
    band(B, r, 2, 11, f"Performance {prod}", 11, CYAN, NEGRO, h=22); r += 1
    header(B, r, 2, ["Campaña", "Inversión"] + [None] * 7 + ["Control"])
    for i in range(7):
        c = put(B, f"{L(4+i)}{r}", f"=Supuestos!{L(3+i)}{CURVA_FECHA}", F(bold=True), "ddd dd/mm", VERDE, al="center", box=True)
    r += 1
    a, b = CAMP_ROWS[prod]
    b0 = r
    for k, mr in enumerate(range(a, b + 1)):
        bg = ZEBRA if k % 2 else None
        cell(B, f"B{r}", f"='MP Cyber 2026'!B{mr}", bg=bg, bold=True)
        cell(B, f"C{r}", f"='MP Cyber 2026'!F{mr}", MONEY, bg)
        for i in range(7):
            cell(B, f"{L(4+i)}{r}", f"=$C{r}*Supuestos!{L(3+i)}${CURVA_PCT}", MONEY, bg)
        cell(B, f"K{r}", f"=SUM(D{r}:J{r})-C{r}", MONEY, bg, color=MUTED)
        r += 1
    daily_ranges.append(f"D{b0}:J{r-1}")
    total_row(B, r, 2, 11)
    put(B, f"B{r}", f"Subtotal {prod}", F(bold=True), bg=L_VERDE, box=True)
    for col in ["C"] + [L(4 + i) for i in range(7)] + ["K"]:
        put(B, f"{col}{r}", f"=SUM({col}{b0}:{col}{r-1})", F(bold=True, color=VERDE_INK if col == "C" else NEGRO), MONEY, L_VERDE, box=True)
    r += 2
for rng in daily_ranges:  # mapa de calor: dónde se concentra la inversión
    B.conditional_formatting.add(rng, ColorScaleRule(start_type="min", start_color="FFFFFF", end_type="max", end_color=VERDE))

band(B, r, 2, 11, "TEASER"); r += 1
header(B, r, 2, ["Campaña", "Inversión", "Inicio", "Fin", "Días", "Por día"]); r += 1
for k, mr in enumerate(range(TEASER_ROWS[0], TEASER_ROWS[1] + 1)):
    bg = ZEBRA if k % 2 else None
    cell(B, f"B{r}", f"='MP Cyber 2026'!B{mr}", bg=bg, bold=True)
    cell(B, f"C{r}", f"='MP Cyber 2026'!F{mr}", MONEY, bg)
    cell(B, f"D{r}", f"={TEASER_INI}", DATE, bg)
    cell(B, f"E{r}", f"={TEASER_FIN}", DATE, bg)
    cell(B, f"F{r}", f"={TEASER_DIAS}", INT, bg)
    cell(B, f"G{r}", f"=IFERROR(C{r}/F{r},\"\")", MONEY, bg, bold=True)
    r += 1
B.freeze_panes = "C1"

# impresión: horizontal, ajustado al ancho
for ws in wb.worksheets:
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

wb.save(OUT)
print("ok", OUT)
