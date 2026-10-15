"""Genera el MP Cyber Monday 2026 B2B Argentina de Pickit (dos escenarios) con estética Zenda.

Uso: python3 build_mp_cyber_b2b_2026.py <salida.xlsx>
Brief: briefs/pickit-cyber-monday-2026-b2b.md
"""
import os, sys, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule, DataBarRule, ColorScaleRule
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter as L
from zenda_xlsx import *  # noqa: F401,F403

OUT = sys.argv[1]
wb = Workbook()

# =====================================================================
# SUPUESTOS
# =====================================================================
S = wb.active
S.title = "Supuestos"
sheet(S, {"A": 2.6, "B": 36, "C": 18, "D": 18, "E": 14, "F": 14, "G": 14, "H": 14, "I": 14, "J": 14, "K": 14, "L": 14})
brand(S, "Supuestos del Media Plan", "Lo único que se edita a mano está acá. El MP y el BGT Diario se recalculan solos.")

put(S, "B6", "REFERENCIAS", F(size=9, bold=True, color=MUTED))
put(S, "B7", "Dato cargado a mano", F(color=INPUT), bg=L_CYAN, box=True)
c = put(S, "B8", "Pendiente de confirmar", box=True); pend(c)
put(S, "B9", "Fórmula (no tocar)", box=True)

band(S, 11, 2, 5, "FECHAS")
header(S, 12, 2, ["Etapa", "Inicio", "Fin", "Días"])
fechas = [("Previa: presencia de marca", dt.date(2026, 10, 26), dt.date(2026, 11, 1)),
          ("Pico de ventas (Cyber Monday)", dt.date(2026, 11, 2), dt.date(2026, 11, 4))]
for i, (n, a, b) in enumerate(fechas):
    r = 13 + i
    cell(S, f"B{r}", n, bold=True)
    for col, v in (("C", a), ("D", b)):
        x = inp(S, f"{col}{r}", v, DATE)
        if i == 0 and col == "C":
            pend(x, "Lanzamiento estimado: última semana de octubre o apenas estén listos los boost de LinkedIn.")
    cell(S, f"E{r}", f"=D{r}-C{r}+1", INT)
total_row(S, 15, 2, 5)
put(S, "B15", "Flight total", F(bold=True), bg=L_VERDE, box=True)
put(S, "C15", "=C13", F(bold=True), DATE, L_VERDE, box=True)
put(S, "D15", "=D14", F(bold=True), DATE, L_VERDE, box=True)
put(S, "E15", "=E13+E14", F(bold=True), INT, L_VERDE, box=True)
INI, FIN, DIAS = "Supuestos!$C$15", "Supuestos!$D$15", "Supuestos!$E$15"

band(S, 17, 2, 5, "PRESUPUESTO POR ESCENARIO")
header(S, 18, 2, ["Escenario", "Criterio", "Inversión total", "Inversión diaria"])
esc = [("Conservador", "Cercano a la inversión B2B actual de Argentina (oct.: $1.562.500/mes)", 1500000),
       ("Arriesgado", "≈ 2,3 veces el conservador, con más peso en Meta", 3500000)]
PRES = {}
for i, (n, crit, v) in enumerate(esc):
    r = 19 + i
    cell(S, f"B{r}", n, bold=True)
    cell(S, f"C{r}", crit, color=MUTED)
    pend(inp(S, f"D{r}", v, MONEY), "Monto de ejemplo: el cliente no definió presupuesto. Reemplazar cuando haya un número.")
    cell(S, f"E{r}", f"=IFERROR(D{r}/{DIAS},\"\")", MONEY)
    PRES[n] = f"Supuestos!$D${r}"
S.column_dimensions["C"].width = 58

band(S, 22, 2, 5, "AUDIENCIA DE LINKEDIN")
cell(S, "B23", "Tamaño de la audiencia (miembros)", bold=True)
pend(inp(S, "D23", 120000, INT), "Pendiente: tomar el tamaño estimado del print de la audiencia guardada en LinkedIn.")
cell(S, "B24", "Cobertura máxima en el flight", bold=True)
inp(S, "D24", 0.5, PCT0, "Tope de la audiencia que se puede alcanzar en 10 días. 40-60 % es razonable para un boost B2B.")
cell(S, "B25", "Alcance máximo", bold=True)
cell(S, "D25", "=D23*D24", INT, bold=True)
cell(S, "B26", "Frecuencia mínima por persona", bold=True)
inp(S, "D26", 2.5, DEC1, "LinkedIn reparte las impresiones con al menos 2-3 vistas por persona en un flight corto.")
AUD_ALC, FREC_MIN = "Supuestos!$D$25", "Supuestos!$D$26"
note(S, "B27", "Alcance = impresiones / frecuencia mínima, hasta el tope. Pasado el tope sube la frecuencia; si supera 8-10, conviene ampliar la audiencia.")

band(S, 28, 2, 5, "AJUSTE DE COSTOS POR TEMPORADA")
cell(S, "B29", "Suba de CPM y CPC por el pico de demanda", bold=True)
inp(S, "D29", 0.15, PCT0, "Las subastas se encarecen en la semana del Cyber, sobre todo en Meta y Google. Se aplica sobre los benchmarks de octubre.")
AJ = "Supuestos!$D$29"

band(S, 31, 2, 12, "DISTRIBUCIÓN DIARIA DE LA INVERSIÓN")
header(S, 32, 2, [""] + [f"Día {i+1}" for i in range(10)])
cell(S, "B33", "Fecha", bold=True)
cell(S, "B34", "% de la inversión", bold=True)
pesos = [0.07, 0.07, 0.08, 0.08, 0.08, 0.08, 0.09, 0.15, 0.15, 0.15]
for i, w in enumerate(pesos):
    col = L(3 + i)
    cell(S, f"{col}33", f"=Supuestos!$C$13+{i}", "ddd dd/mm")
    inp(S, f"{col}34", w, PCT0)
total_row(S, 35, 2, 12)
put(S, "B35", "Control (debe dar 100 %)", F(bold=True), bg=L_VERDE, box=True)
put(S, "C35", "=SUM(C34:L34)", F(bold=True), PCT0, L_VERDE, box=True)
note(S, "B36", "Arranca más suave en la previa y concentra el 45 % en los tres días del pico. Si cambia el largo del flight, ajustar los días.")
CURVA_FECHA, CURVA_PCT = 33, 34

# =====================================================================
# MP
# =====================================================================
M = wb.create_sheet("MP Cyber B2B", 0)
widths = {"A": 2.6, "B": 45, "C": 12, "D": 13, "E": 26, "F": 7, "G": 13, "H": 12, "I": 13, "J": 11, "K": 9,
          "L": 12, "M": 10, "N": 9, "O": 11, "P": 10, "Q": 11, "R": 12}
sheet(M, widths)
brand(M, "pickit  |  Media Plan Cyber Monday B2B · Argentina 2026",
      "Objetivo: presencia como aliado logístico durante el pico de ventas. Montos de ejemplo hasta que el cliente defina presupuesto.")

campanias = [
    # nombre, medio, objetivo, audiencia, %cons, %arr, cpm, cpc, cr, es_linkedin, nota
    ("AR_B2B_LinkedIn_Boost_Awareness_Cyber2026", "LinkedIn Ads", "Reconocimiento",
     "Audiencia guardada B2B", 0.30, 0.20, 10239, 2343, None, True,
     "Benchmark: AR_MX_H2_B2B_LinkedIn_Branding_2026, octubre 2026 (mismo objetivo)."),
    ("AR_B2B_FB_BBDD_Trafico_Cyber2026", "Meta Ads", "Tráfico web",
     "Base de datos de clientes y leads", 0.10, 0.10, 4500, 1030, 0.0163, False,
     "Benchmark: AR_Hunting&SameDay_H2_FB_Conversiones_2026, octubre 2026. Con objetivo tráfico el CPC suele bajar."),
    ("AR_B2B_FB_Lookalike_Trafico_Cyber2026", "Meta Ads", "Tráfico web",
     "Similar 1-3 % de la base de datos", 0.20, 0.30, 4500, 1030, 0.0163, False,
     "Benchmark: AR_Hunting&SameDay_H2_FB_Conversiones_2026, octubre 2026."),
    ("AR_B2B_GL_PMax_AliadoLogistico_Cyber2026", "Google Ads", "Conversiones",
     "Señales: términos de búsqueda + remarketing BBDD", 0.40, 0.40, 15960, 1596, 0.0046, False,
     "Campaña nueva. Benchmark prestado de AR_Flex_SameDay_H2_GL_Search_2026 (mismo objetivo, conversiones B2B AR), octubre 2026. CPM calculado con CTR de 1 %."),
]

GRUPOS = [(2, 5, "CAMPAÑA", NEGRO, "FFFFFF"), (6, 8, "INVERSIÓN", VERDE_INK, "FFFFFF"),
          (9, 11, "BENCHMARKS (OCT.)", CYAN, NEGRO), (12, 18, "RESULTADOS ESTIMADOS", ROSA, "FFFFFF")]
COLS = ["Campaña", "Medio", "Objetivo", "Audiencia / señales", "%", "Inversión", "Inv. diaria", "CPM", "CPC", "CR",
        "Impresiones", "Clics", "CTR", "Alcance", "Frecuencia", "Conversiones", "CPA"]

DET = 30
band(M, DET, 2, 18, "DETALLE POR CAMPAÑA", h=26)
row = DET + 2
TOT, ROWS = {}, {}
for k, (escn, idx) in enumerate((("Conservador", 4), ("Arriesgado", 5))):
    band(M, row, 2, 18, f"Escenario {escn.lower()}", 11, CYAN, NEGRO, h=22); row += 1
    groups(M, row, GRUPOS); row += 1
    header(M, row, 2, COLS); row += 1
    r0 = row
    for i, cp in enumerate(campanias):
        n, med, obj, aud, pc, pa, cpm, cpc, cr, li, nt = cp
        r = row
        bg = ZEBRA if i % 2 else None
        cell(M, f"B{r}", n, bg=bg, bold=True); cell(M, f"C{r}", med, bg=bg)
        cell(M, f"D{r}", obj, bg=bg); cell(M, f"E{r}", aud, bg=bg, color=MUTED)
        inp(M, f"F{r}", cp[idx], PCT0)
        cell(M, f"G{r}", f"=F{r}*{PRES[escn]}", MONEY, bg)
        cell(M, f"H{r}", f"=IFERROR(G{r}/{DIAS},\"\")", MONEY, bg)
        inp(M, f"I{r}", cpm, MONEY, nt); inp(M, f"J{r}", cpc, MONEY, nt)
        if cr is None:
            cell(M, f"K{r}", "–", bg=bg, al="right", color=MUTED)
        else:
            inp(M, f"K{r}", cr, PCT2)
        # costos ajustados por temporada
        cell(M, f"L{r}", f"=IFERROR(G{r}/(I{r}*(1+{AJ}))*1000,\"\")", INT, bg)
        cell(M, f"M{r}", f"=IFERROR(G{r}/(J{r}*(1+{AJ})),\"\")", INT, bg, bold=True)
        cell(M, f"N{r}", f"=IFERROR(M{r}/L{r},\"\")", PCT2, bg)
        if li:
            cell(M, f"O{r}", f"=MIN({AUD_ALC},L{r}/{FREC_MIN})", INT, bg, bold=True)
            cell(M, f"P{r}", f"=IFERROR(L{r}/O{r},\"\")", DEC1, bg, bold=True)
            cell(M, f"Q{r}", "–", bg=bg, al="right", color=MUTED)
            cell(M, f"R{r}", "–", bg=bg, al="right", color=MUTED)
        else:
            cell(M, f"O{r}", "–", bg=bg, al="right", color=MUTED)
            cell(M, f"P{r}", "–", bg=bg, al="right", color=MUTED)
            cell(M, f"Q{r}", f"=IFERROR(M{r}*K{r},\"\")", DEC1, bg)
            cell(M, f"R{r}", f"=IFERROR(G{r}/Q{r},\"\")", MONEY, bg)
        row += 1
    r1 = row - 1
    T = row
    total_row(M, T, 2, 18)
    put(M, f"B{T}", f"Total escenario {escn.lower()}", F(bold=True), bg=L_VERDE, box=True)
    put(M, f"F{T}", f"=SUM(F{r0}:F{r1})", F(bold=True), PCT0, L_VERDE, box=True)
    put(M, f"G{T}", f"=SUM(G{r0}:G{r1})", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
    put(M, f"H{T}", f"=SUM(H{r0}:H{r1})", F(bold=True), MONEY, L_VERDE, box=True)
    put(M, f"I{T}", f"=IFERROR(G{T}/L{T}*1000,\"\")", F(bold=True), MONEY, L_VERDE, box=True)
    put(M, f"J{T}", f"=IFERROR(G{T}/M{T},\"\")", F(bold=True), MONEY, L_VERDE, box=True)
    put(M, f"L{T}", f"=SUM(L{r0}:L{r1})", F(bold=True), INT, L_VERDE, box=True)
    put(M, f"M{T}", f"=SUM(M{r0}:M{r1})", F(bold=True), INT, L_VERDE, box=True)
    put(M, f"N{T}", f"=IFERROR(M{T}/L{T},\"\")", F(bold=True), PCT2, L_VERDE, box=True)
    put(M, f"Q{T}", f"=SUM(Q{r0}:Q{r1})", F(bold=True), DEC1, L_VERDE, box=True)
    put(M, f"R{T}", f"=IFERROR(SUMIF(D{r0}:D{r1},\"<>Reconocimiento\",G{r0}:G{r1})/Q{T},\"\")", F(bold=True), MONEY, L_VERDE, box=True)
    TOT[escn], ROWS[escn] = T, (r0, r1)
    row += 2
LI = {e: ROWS[e][0] for e in ROWS}  # fila de LinkedIn en cada escenario
ROW_END = row

# ---- KPI cards
card(M, 6, 2, 2, "Flight", f"=TEXT({INI},\"dd/mm\")&\" al \"&TEXT({FIN},\"dd/mm\")", None, L_CYAN, None)
put(M, "B8", f"={DIAS}&\" días · pico del 02 al 04/11\"", F(size=9, color=MUTED), bg=L_CYAN)
card(M, 6, 4, 6, "Inversión conservador", f"=G{TOT['Conservador']}", MONEY, L_VERDE, "Escenario conservador")
card(M, 6, 8, 10, "Inversión arriesgado", f"=G{TOT['Arriesgado']}", MONEY, L_ROSA, "Escenario arriesgado")
card(M, 6, 12, 14, "Impresiones (conservador)", f"=L{TOT['Conservador']}", INT, L_VERDE, "Todas las plataformas")
card(M, 6, 16, 18, "Alcance LinkedIn", f"=O{LI['Conservador']}", INT, L_CYAN, "Audiencia B2B guardada")

# ---- Comparativo de escenarios
band(M, 11, 2, 7, "COMPARATIVO DE ESCENARIOS")
header(M, 12, 2, ["Indicador", "Conservador", "Arriesgado", "Diferencia", "", ""])
M.merge_cells("F12:G12")
tc, ta = TOT["Conservador"], TOT["Arriesgado"]
lc, la = LI["Conservador"], LI["Arriesgado"]
ind = [("Inversión", "G{}", MONEY, "{t}"), ("Impresiones", "L{}", INT, "{t}"), ("Clics", "M{}", INT, "{t}"),
       ("CTR", "N{}", PCT2, "{t}"), ("CPM promedio", "I{}", MONEY, "{t}"),
       ("Alcance LinkedIn", "O{}", INT, "{l}"), ("Frecuencia LinkedIn", "P{}", DEC1, "{l}"),
       ("Conversiones estimadas (secundario)", "Q{}", DEC1, "{t}")]
for i, (n, ref, fm, which) in enumerate(ind):
    r = 13 + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"B{r}", n, bg=bg, bold=True)
    rc = ref.format(tc if which == "{t}" else lc)
    ra = ref.format(ta if which == "{t}" else la)
    cell(M, f"C{r}", f"={rc}", fm, bg)
    cell(M, f"D{r}", f"={ra}", fm, bg, bold=True)
    cell(M, f"E{r}", f"=IFERROR(D{r}/C{r}-1,\"\")", PCT0, bg, color=VERDE_INK)
    for col in "FG": cell(M, f"{col}{r}", None, bg=bg)
    M.merge_cells(f"F{r}:G{r}")
note(M, "B21", "Las conversiones son un indicador secundario: el objetivo de la campaña es presencia (alcance, frecuencia, clics).")

# ---- Resumen por medio (conservador | arriesgado)
band(M, 11, 9, 14, "INVERSIÓN POR MEDIO")
header(M, 12, 9, ["Medio", "Conservador", "%", "Arriesgado", "%", ""])
(c0, c1), (a0, a1) = ROWS["Conservador"], ROWS["Arriesgado"]
for i, med in enumerate(["LinkedIn Ads", "Meta Ads", "Google Ads"]):
    r = 13 + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"I{r}", med, bg=bg, bold=True)
    cell(M, f"J{r}", f"=SUMIF($C${c0}:$C${c1},I{r},$G${c0}:$G${c1})", MONEY, bg)
    cell(M, f"K{r}", f"=IFERROR(J{r}/$J$16,\"\")", PCT0, bg)
    cell(M, f"L{r}", f"=SUMIF($C${a0}:$C${a1},I{r},$G${a0}:$G${a1})", MONEY, bg)
    cell(M, f"M{r}", f"=IFERROR(L{r}/$L$16,\"\")", PCT0, bg)
    cell(M, f"N{r}", None, bg=bg)
total_row(M, 16, 9, 14)
put(M, "I16", "TOTAL", F(bold=True), bg=L_VERDE, box=True)
put(M, "J16", "=SUM(J13:J15)", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
put(M, "K16", "=SUM(K13:K15)", F(bold=True), PCT0, L_VERDE, box=True)
put(M, "L16", "=SUM(L13:L15)", F(bold=True, color=VERDE_INK), MONEY, L_VERDE, box=True)
put(M, "M16", "=SUM(M13:M15)", F(bold=True), PCT0, L_VERDE, box=True)
M.conditional_formatting.add("K13:K15", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=VERDE))
M.conditional_formatting.add("M13:M15", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=ROSA))

# ---- Controles
band(M, 18, 9, 14, "CONTROLES")
controles = [
    ("Conservador = presupuesto", f"=IF(ROUND(G{tc}-{PRES['Conservador']},0)=0,\"OK\",\"REVISAR\")"),
    ("Arriesgado = presupuesto", f"=IF(ROUND(G{ta}-{PRES['Arriesgado']},0)=0,\"OK\",\"REVISAR\")"),
    ("% de cada escenario = 100 %", f"=IF(AND(ROUND(F{tc},4)=1,ROUND(F{ta},4)=1),\"OK\",\"REVISAR\")"),
    ("Curva diaria = 100 %", "=IF(ROUND(Supuestos!C35,4)=1,\"OK\",\"REVISAR\")"),
    ("Frecuencia LinkedIn ≤ 10", f"=IF(MAX(P{lc},P{la})<=10,\"OK\",\"REVISAR\")"),
]
for i, (n, f) in enumerate(controles):
    r = 19 + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"I{r}", n, bg=bg)
    for col in "JK": cell(M, f"{col}{r}", None, bg=bg)
    M.merge_cells(f"I{r}:K{r}")
    for col in "LM": cell(M, f"{col}{r}", None, bg=bg)
    M.merge_cells(f"L{r}:M{r}")
    cell(M, f"L{r}", f, bold=True, al="center")
M.conditional_formatting.add("L19:M23", CellIsRule(operator="equal", formula=['"OK"'], fill=fill(L_VERDE), font=Font(color=VERDE_INK, bold=True)))
M.conditional_formatting.add("L19:M23", CellIsRule(operator="equal", formula=['"REVISAR"'], fill=fill(ROSA), font=Font(color="FFFFFF", bold=True)))

# ---- Mensaje y referencias
band(M, 23, 2, 7, "MENSAJE CENTRAL")
put(M, "B24", "¿Tu logística aguanta el pico de ventas?", F(size=14, bold=True, color=VERDE_INK))
M.row_dimensions[24].height = 24
note(M, "B25", "Sin mencionar \"Cyber Monday\": Pickit como aliado logístico de las empresas que venden mucho en la fecha.")
put(M, "B27", "Dato cargado a mano", F(color=INPUT), bg=L_CYAN, box=True)
note(M, "C27", "% de inversión y benchmarks de octubre. Cada benchmark tiene un comentario con su fuente.")
note(M, "B28", f"Impresiones y clics usan los benchmarks con la suba por temporada de la hoja Supuestos.")

M.freeze_panes = "C1"

# =====================================================================
# BGT DIARIO
# =====================================================================
B = wb.create_sheet("BGT Diario", 1)
sheet(B, {"A": 2.6, "B": 40, "C": 13, **{L(4 + i): 11 for i in range(10)}, "N": 11})
brand(B, "Inversión diaria  |  Cyber B2B Argentina",
      "Inversión de cada campaña × curva diaria de Supuestos. Los tres días del pico concentran el 45 %.")
r = 6
daily = []
for escn in ("Conservador", "Arriesgado"):
    band(B, r, 2, 14, f"ESCENARIO {escn.upper()}"); r += 1
    header(B, r, 2, ["Campaña", "Inversión"] + [None] * 10 + ["Control"])
    for i in range(10):
        put(B, f"{L(4+i)}{r}", f"=Supuestos!{L(3+i)}{CURVA_FECHA}", F(bold=True), "ddd dd/mm", VERDE, al="center", box=True)
    r += 1
    a, b = ROWS[escn]
    b0 = r
    for k, mr in enumerate(range(a, b + 1)):
        bg = ZEBRA if k % 2 else None
        cell(B, f"B{r}", f"='MP Cyber B2B'!B{mr}", bg=bg, bold=True)
        cell(B, f"C{r}", f"='MP Cyber B2B'!G{mr}", MONEY, bg)
        for i in range(10):
            cell(B, f"{L(4+i)}{r}", f"=$C{r}*Supuestos!{L(3+i)}${CURVA_PCT}", MONEY, bg)
        cell(B, f"N{r}", f"=SUM(D{r}:M{r})-C{r}", MONEY, bg, color=MUTED)
        r += 1
    daily.append(f"D{b0}:M{r-1}")
    total_row(B, r, 2, 14)
    put(B, f"B{r}", f"Total {escn.lower()}", F(bold=True), bg=L_VERDE, box=True)
    for col in ["C"] + [L(4 + i) for i in range(10)] + ["N"]:
        put(B, f"{col}{r}", f"=SUM({col}{b0}:{col}{r-1})", F(bold=True, color=VERDE_INK if col == "C" else NEGRO), MONEY, L_VERDE, box=True)
    r += 2
for rng in daily:
    B.conditional_formatting.add(rng, ColorScaleRule(start_type="min", start_color="FFFFFF", end_type="max", end_color=VERDE))
B.freeze_panes = "C1"

for ws in wb.worksheets:
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

wb.save(OUT)
print("ok", OUT)
