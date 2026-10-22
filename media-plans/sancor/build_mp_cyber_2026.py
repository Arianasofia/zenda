"""MP Cyber Monday 2026 de Sancor Seguros (Teaser, Cyber Monday y Cyber Week).

Uso: python3 build_mp_cyber_2026.py <salida.xlsx>

Día común: gasto real diario de cada campaña del 08/10 al 21/10/2026 (SeePM).
Hogar no pauta en 2026: base del Cyber 2025 (20/10 al 01/11/2025) ajustada por inflación.
SSM no tiene pauta: monto propuesto con benchmark de AP Search Not Brand.
"""
import sys, os, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment
from zenda_xlsx import (F, fill, put, cell, inp, band, header, total_row, brand, card, note, sheet,
                        MONEY, INT, PCT2, PCT0, DATE, L_VERDE, L_CYAN, L_ROSA, ZEBRA, VERDE, CYAN, MUTED, ROSA)
from openpyxl.utils import get_column_letter as L

OUT = sys.argv[1]
PCTS = "+0%;-0%;0%"

# producto, campaña, medio, día común (o fórmula), CPM, CPC, CR, % del extra, campaña de referencia, período
P26 = "08/10 al 21/10/2026"
P25 = "20/10 al 15/11/2025"
CAMP = [
    ("Auto", "SS_Auto_GL_Search_BrandSancor_Cotizaciones_2023_Performance", "Google Ads", 246885, 77209, 494, 0.0146, 0.30, None, P26),
    ("Auto", "SS_Auto_GL_Search_Category_Intent_2023_Performance", "Google Ads", 237221, 208546, 3148, 0.0753, 0, None, P26),
    ("Auto", "SS_Auto_GL_PMax_Conversiones_2023_Performance", "Google Ads", 317273, 6240, 501, 0.0297, 0.70, None, P26),
    ("Auto", "SS_Auto_FB_Conversiones_RMKT_2023", "Meta Ads", 70481, 9979, 241, 0.0024, 0, None, P26),
    ("Moto", "SS_Moto_GL_PMax_Conversiones_2023_Performance", "Google Ads", 5247, 6843, 98, 0.2273, 1, None, P26),
    ("Moto", "SS_Moto_GL_Search_Not Brand_Cotizaciones_2023_Performance", "Google Ads", 1793, 111555, 678, 0.1351, 0, None, P26),
    ("Moto", "SS_Moto_FB_Conversiones_2023", "Meta Ads", 3159, 5033, 307, 0.0625, 0, None, P26),
    ("Movilidad", "SS_Movilidad_GL_Search_NotBrand_Conversiones_2023", "Google Ads", 82392, 319703, 1882, 0.0667, 0, None, P26),
    ("Movilidad", "SS_Movilidad_GL_Search_Brand_Conversiones_2023", "Google Ads", 11126, 474873, 1331, 0.0679, 0, None, P26),
    ("Movilidad", "SS_Movilidad_GL_PMax_Conversiones_2026_Performance", "Google Ads", 18949, 10311, 209, 0.0224, 0.40, None, P26),
    ("Movilidad", "SS_Movilidad_Meta_Conversiones_2023", "Meta Ads", 33945, 4674, 500, 0.2295, 0.60, None, P26),
    ("AP", "SS_AP_GL_Search_Brand_Cotizaciones_2022_Performance", "Google Ads", 15376, 56828, 462, 0.0568, 0, None, P26),
    ("AP", "SS_AP_GL_Search_Not Brand_Cotizaciones_2022_Performance", "Google Ads", 30365, 291570, 2592, 0.2135, 0, None, P26),
    ("AP", "SS_AP_GL_PMax_Conversiones_2024", "Google Ads", 28545, 14516, 122, 0.0277, 0.60, None, P26),
    ("AP", "SS_AP_FB_Conversiones_2024", "Meta Ads", 23566, 3175, 168, 0.0367, 0.40, None, P26),
    ("Hogar", "SS_Hogar_GL_PMax_Conversiones_2023_Performance", "Google Ads", ("H", 52384), ("H", 11256), ("H", 241), 0.0043, 0, None, P25),
    ("Hogar", "SS_Hogar_GL_Search_Not Brand_Cotizaciones_2022_Performance", "Google Ads", ("H", 28419), ("H", 218874), ("H", 2126), 0.3086, 1, None, P25),
    ("Hogar", "SS_Hogar_GL_Search_Brand_Cotizaciones_2022_Performance", "Google Ads", ("H", 6759), ("H", 262817), ("H", 744), 0.0241, 0, None, P25),
    ("SSM", "SS_SSM_GL_Search_NotBrand_CyberMonday_2026", "Google Ads", 30000, 291570, 2592, 0.2135, 1,
     "SS_AP_GL_Search_Not Brand_Cotizaciones_2022_Performance", P26),
    ("Teaser de marca", "SS_CyberMonday_GL_DemandGen_Trafico_2026", "Google Ads", 40000, 293, 10.6, None, None,
     "SS_Agro_GL_DemandGen_Trafico_Clics_2026", P26),
    ("Teaser de marca", "SS_SancorSeguros_FB_Trafico_CyberMonday_Teaser_2026", "Meta Ads", 40000, 2808, 41.6, None, None,
     "SS_FAL_FB_Trafico_2026", P26),
]
N = len(CAMP)
PRODUCTOS = [("Auto", "Hasta 30% OFF"), ("Moto", "30% OFF"), ("Movilidad", "15% OFF"), ("AP", "AP 24 HS: 30% OFF"),
             ("Hogar", "30% OFF"), ("SSM", "30% OFF"), ("Teaser de marca", "–")]
TEASER = [i for i, c in enumerate(CAMP) if c[0] == "Teaser de marca"]

# ---- filas fijas
R_CMP, R_ETA = 11, 11
R_PROD = 21
R_DC = 34                       # detalle conservador: filas R_DC .. R_DC+N-1, total R_DC+N
R_DCT = R_DC + N
R_DA = R_DCT + 5                # detalle agresivo
R_DAT = R_DA + N
R_SUP = R_DAT + 5               # supuestos
R_ET = R_SUP + 2                # etapas: Teaser, Cyber Monday, Cyber Week
R_SUBA = R_ET + 4               # subas: filas R_SUBA .. +2
R_COST = R_SUBA + 3
R_INFL = R_COST + 1
R_BEN = R_INFL + 4              # benchmarks
DIAS = [f"$E${R_ET + k}" for k in range(3)]
SUBA_C = [f"$C${R_SUBA + k}" for k in range(3)]
SUBA_A = [f"$D${R_SUBA + k}" for k in range(3)]
COST, INFL = f"$C${R_COST}", f"$C${R_INFL}"

wb = Workbook()
M = wb.active
M.title = "MP"
sheet(M, {"A": 2.6, "B": 26, "C": 52, "D": 16, "E": 16, "F": 16, "G": 16, "H": 16, "I": 16, "J": 16,
          "K": 16, "L": 16, "M": 16, "N": 16, "O": 16})
brand(M, "Sancor Seguros  |  Media Plan Cyber Monday 2026  |  Argentina")

# ---- KPI
card(M, 5, 2, 2, "Período", f'=TEXT(C{R_ET},"dd/mm")&" al "&TEXT(D{R_ET+2},"dd/mm")', None, L_CYAN,
     "Teaser, Cyber Monday y Cyber Week")
card(M, 5, 4, 5, "Inversión conservador", f"=I{R_DCT}", MONEY, L_VERDE, "Escenario conservador")
card(M, 5, 7, 8, "Inversión agresivo", f"=I{R_DAT}", MONEY, L_VERDE, "Escenario agresivo")
card(M, 5, 10, 11, "Cotizaciones conservador", f"=M{R_DCT}", INT, L_ROSA, "Cotizaciones completas")
card(M, 5, 13, 14, "Cotizaciones agresivo", f"=M{R_DAT}", INT, L_ROSA, "Cotizaciones completas")

# ---- comparativo
band(M, 9, 2, 5, "COMPARATIVO DE ESCENARIOS")
header(M, 10, 2, ["Indicador", "Conservador", "Agresivo", "Diferencia"])
dias_tot = "+".join(DIAS)
comp = [("Inversión", f"=I{R_DCT}", f"=I{R_DAT}", MONEY),
        ("Inversión adicional sobre el día común", f"=C11-SUM($D${R_PROD}:$D${R_PROD+5})*({dias_tot})",
         f"=D11-SUM($D${R_PROD}:$D${R_PROD+5})*({dias_tot})", MONEY),
        ("Impresiones", f"=J{R_DCT}", f"=J{R_DAT}", INT),
        ("Clics", f"=K{R_DCT}", f"=K{R_DAT}", INT),
        ("CTR", "=C14/C13", "=D14/D13", PCT2),
        ("Cotizaciones", f"=M{R_DCT}", f"=M{R_DAT}", INT),
        ("CPA por cotización", f"=N{R_DCT}", f"=N{R_DAT}", MONEY)]
for i, (lab, c, d, fmt) in enumerate(comp):
    r = R_CMP + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"B{r}", lab, bg=bg, bold=True)
    cell(M, f"C{r}", c, fmt, bg); cell(M, f"D{r}", d, fmt, bg)
    cell(M, f"E{r}", f"=IFERROR(D{r}/C{r}-1,\"\")", PCTS, bg)
note(M, f"B{R_CMP+7}", "Inversión adicional: lo que se invierte por encima del día común de cada producto en los 11 días.")

# ---- inversión por etapa
band(M, 9, 7, 10, "INVERSIÓN POR ETAPA")
header(M, 10, 7, ["Etapa", "Fechas", "Conservador", "Agresivo"])
for k, (et, col) in enumerate([("Teaser", "F"), ("Cyber Monday", "G"), ("Cyber Week", "H")]):
    r = R_ETA + k
    bg = ZEBRA if k % 2 else None
    cell(M, f"G{r}", et, bg=bg, bold=True)
    cell(M, f"H{r}", f'=TEXT(C{R_ET+k},"dd/mm")&" al "&TEXT(D{R_ET+k},"dd/mm")', bg=bg, al="center")
    cell(M, f"I{r}", f"={col}{R_DCT}", MONEY, bg)
    cell(M, f"J{r}", f"={col}{R_DAT}", MONEY, bg)
r = R_ETA + 3
total_row(M, r, 7, 10)
put(M, f"G{r}", "TOTAL", F(bold=True), bg=L_VERDE, box=True)
put(M, f"H{r}", f'=TEXT(C{R_ET},"dd/mm")&" al "&TEXT(D{R_ET+2},"dd/mm")', F(bold=True), bg=L_VERDE, al="center", box=True)
for c in "IJ":
    put(M, f"{c}{r}", f"=SUM({c}{R_ETA}:{c}{R_ETA+2})", F(bold=True), MONEY, L_VERDE, box=True)
note(M, f"G{R_ETA+4}", "Teaser: campañas de cada producto al día común y campañas de marca con piezas de expectativa.")

# ---- inversión por producto
band(M, 19, 2, 8, "INVERSIÓN POR PRODUCTO")
header(M, 20, 2, ["Producto", "Oferta Cyber", "Día común", "Conservador", "%", "Agresivo", "%"])
rng = lambda col, r0, r1: f"${col}${r0}:${col}${r1}"
for i, (p, of) in enumerate(PRODUCTOS):
    r = R_PROD + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"B{r}", p, bg=bg, bold=True); cell(M, f"C{r}", of, bg=bg)
    cell(M, f"D{r}", f"=SUMIF({rng('B', R_DC, R_DCT-1)},B{r},{rng('E', R_DC, R_DCT-1)})", MONEY, bg)
    cell(M, f"E{r}", f"=SUMIF({rng('B', R_DC, R_DCT-1)},B{r},{rng('I', R_DC, R_DCT-1)})", MONEY, bg)
    cell(M, f"F{r}", f"=E{r}/$E${R_PROD+7}", PCT0, bg)
    cell(M, f"G{r}", f"=SUMIF({rng('B', R_DA, R_DAT-1)},B{r},{rng('I', R_DA, R_DAT-1)})", MONEY, bg)
    cell(M, f"H{r}", f"=G{r}/$G${R_PROD+7}", PCT0, bg)
r = R_PROD + 7
total_row(M, r, 2, 8)
put(M, f"B{r}", "TOTAL", F(bold=True), bg=L_VERDE, box=True)
put(M, f"C{r}", "", bg=L_VERDE, box=True)
for c, fmt in (("D", MONEY), ("E", MONEY), ("F", PCT0), ("G", MONEY), ("H", PCT0)):
    f = f"=SUM({c}{R_PROD}:{c}{r-1})"
    put(M, f"{c}{r}", f, F(bold=True), fmt, L_VERDE, box=True)
note(M, f"B{R_PROD+8}", "Día común: inversión diaria real de cada campaña del 08/10 al 21/10/2026. Hogar no pauta en 2026: "
     "base del Cyber 2025 ajustada por inflación. SSM y el teaser de marca no tienen pauta vigente: monto propuesto.")

# ---- inversión diaria vs día común
band(M, 19, 10, 15, "INVERSIÓN DIARIA VS. DÍA COMÚN")
header(M, 20, 10, ["Etapa", "Día común", "Conservador", "Vs. día común", "Agresivo", "Vs. día común"])
for k, et in enumerate(["Teaser", "Cyber Monday", "Cyber Week"]):
    r = R_PROD + k
    bg = ZEBRA if k % 2 else None
    cell(M, f"J{r}", et, bg=bg, bold=True)
    cell(M, f"K{r}", f"=SUM($D${R_PROD}:$D${R_PROD+5})", MONEY, bg)
    cell(M, f"L{r}", f"=I{R_ETA+k}/{DIAS[k]}", MONEY, bg)
    cell(M, f"M{r}", f"=L{r}/K{r}-1", PCTS, bg)
    cell(M, f"N{r}", f"=J{R_ETA+k}/{DIAS[k]}", MONEY, bg)
    cell(M, f"O{r}", f"=N{r}/K{r}-1", PCTS, bg)
note(M, f"J{R_PROD+3}", "Día común: suma de los productos, sin el teaser de marca.")


# ---- detalle por campaña
def detalle(r0, titulo, agresivo):
    band(M, r0 - 2, 2, 14, titulo, bg=CYAN, color="0A0A0B")
    header(M, r0 - 1, 2, ["Producto", "Campaña", "Medio", "% del extra" if agresivo else "Día común",
                          "Teaser", "Cyber Monday", "Cyber Week", "Inversión total", "Impresiones", "Clics",
                          "CTR", "Cotizaciones", "CPA"])
    for i, c in enumerate(CAMP):
        r, rc, b = r0 + i, R_DC + i, R_BEN + i
        prod, camp, medio, dc = c[0], c[1], c[2], c[3]
        teaser = prod == "Teaser de marca"
        bg = ZEBRA if i % 2 else None
        cell(M, f"B{r}", prod, bg=bg, bold=True); cell(M, f"C{r}", camp, bg=bg); cell(M, f"D{r}", medio, bg=bg)
        if not agresivo:
            if isinstance(dc, tuple):
                cell(M, f"E{r}", f"=ROUND({dc[1]}*(1+{INFL}),0)", MONEY, bg)
            else:
                inp(M, f"E{r}", dc, MONEY)
            if teaser:
                vals = [f"=E{r}*{DIAS[0]}", 0, 0]
            else:
                vals = [f"=E{r}*(1+{SUBA_C[k]})*{DIAS[k]}" for k in range(3)]
        else:
            if teaser:
                cell(M, f"E{r}", "–", bg=bg, al="center")
                vals = [f"={col}{rc}" for col in "FGH"]
            else:
                inp(M, f"E{r}", c[7], PCT0)
                dcp = f"SUMIF({rng('B', R_DC, R_DCT-1)},B{r},{rng('E', R_DC, R_DCT-1)})"
                vals = [f"={col}{rc}+{dcp}*({SUBA_A[k]}-{SUBA_C[k]})*{DIAS[k]}*E{r}" for k, col in enumerate("FGH")]
        for col, v in zip("FGH", vals):
            cell(M, f"{col}{r}", v, MONEY, bg)
        cell(M, f"I{r}", f"=SUM(F{r}:H{r})", MONEY, bg)
        cell(M, f"J{r}", f"=I{r}/H{b}*1000", INT, bg)
        cell(M, f"K{r}", f"=I{r}/I{b}", INT, bg)
        cell(M, f"L{r}", f"=K{r}/J{r}", PCT2, bg)
        if teaser:
            cell(M, f"M{r}", "–", bg=bg, al="center"); cell(M, f"N{r}", "–", bg=bg, al="center")
        else:
            cell(M, f"M{r}", f"=K{r}*G{b}", INT, bg)
            cell(M, f"N{r}", f"=IFERROR(I{r}/M{r},\"\")", MONEY, bg)
    rt = r0 + N
    total_row(M, rt, 2, 14)
    put(M, f"B{rt}", "Total escenario " + ("agresivo" if agresivo else "conservador"), F(bold=True), bg=L_VERDE, box=True)
    for col in "CD":
        put(M, f"{col}{rt}", "", bg=L_VERDE, box=True)
    put(M, f"E{rt}", f"=SUM(E{r0}:E{rt-1})" if not agresivo else "", F(bold=True), MONEY, L_VERDE, box=True)
    for col, fmt in (("F", MONEY), ("G", MONEY), ("H", MONEY), ("I", MONEY), ("J", INT), ("K", INT), ("M", INT)):
        put(M, f"{col}{rt}", f"=SUM({col}{r0}:{col}{rt-1})", F(bold=True), fmt, L_VERDE, box=True)
    put(M, f"L{rt}", f"=K{rt}/J{rt}", F(bold=True), PCT2, L_VERDE, box=True)
    tz = "".join(f"-I{r0+i}" for i in TEASER)
    put(M, f"N{rt}", f"=(I{rt}{tz})/M{rt}", F(bold=True), MONEY, L_VERDE, box=True)
    return rt


detalle(R_DC, "DETALLE POR CAMPAÑA · ESCENARIO CONSERVADOR", False)
note(M, f"B{R_DCT+1}", "Teaser: productos al día común. Cyber Monday y Cyber Week: día común más la suba de Supuestos. "
     "Cotizaciones: cotizaciones completas según la plataforma.")
detalle(R_DA, "DETALLE POR CAMPAÑA · ESCENARIO AGRESIVO", True)
note(M, f"B{R_DAT+1}", "El agresivo suma la inversión extra de cada producto en sus campañas de mejor costo por cotización, "
     "según el % del extra.")

# ---- supuestos
band(M, R_SUP, 2, 5, "SUPUESTOS")
header(M, R_SUP + 1, 2, ["Etapa", "Inicio", "Fin", "Días"])
for k, (et, a, b) in enumerate([("Teaser", dt.date(2026, 10, 29), dt.date(2026, 11, 1)),
                                ("Cyber Monday", dt.date(2026, 11, 2), dt.date(2026, 11, 4)),
                                ("Cyber Week", dt.date(2026, 11, 5), dt.date(2026, 11, 8))]):
    r = R_ET + k
    cell(M, f"B{r}", et, bold=True)
    inp(M, f"C{r}", a, DATE); inp(M, f"D{r}", b, DATE)
    cell(M, f"E{r}", f"=D{r}-C{r}+1", INT)
header(M, R_SUBA - 1, 2, ["Suba sobre el día común", "Conservador", "Agresivo"])
for k, (et, c, a) in enumerate([("Teaser", 0, 0), ("Cyber Monday", 0.30, 0.60), ("Cyber Week", 0.15, 0.30)]):
    r = R_SUBA + k
    cell(M, f"B{r}", et, bold=True); inp(M, f"C{r}", c, PCT0); inp(M, f"D{r}", a, PCT0)
cell(M, f"B{R_COST}", "Suba de CPM y CPC por evento", bold=True); inp(M, f"C{R_COST}", 0.15, PCT0)
cell(M, f"B{R_INFL}", "Inflación sobre la base 2025 (Hogar)", bold=True); inp(M, f"C{R_INFL}", 0.22, PCT0)

# ---- benchmarks
band(M, R_BEN - 2, 2, 9, "BENCHMARKS DE REFERENCIA")
header(M, R_BEN - 1, 2, ["Producto", "Campaña de referencia", "Período", "CPM", "CPC", "CR", "CPM con suba", "CPC con suba"])
for i, c in enumerate(CAMP):
    r = R_BEN + i
    bg = ZEBRA if i % 2 else None
    cell(M, f"B{r}", c[0], bg=bg, bold=True); cell(M, f"C{r}", c[8] or c[1], bg=bg); cell(M, f"D{r}", c[9], bg=bg, al="center")
    for col, v in (("E", c[4]), ("F", c[5])):
        if isinstance(v, tuple):
            cell(M, f"{col}{r}", f"={v[1]}*(1+{INFL})", MONEY, bg)
        else:
            cell(M, f"{col}{r}", v, MONEY, bg)
    if c[6] is None:
        cell(M, f"G{r}", "–", bg=bg, al="center")
    else:
        cell(M, f"G{r}", c[6], PCT2, bg)
    cell(M, f"H{r}", f"=E{r}*(1+{COST})", MONEY, bg)
    cell(M, f"I{r}", f"=F{r}*(1+{COST})", MONEY, bg)
note(M, f"B{R_BEN+N}", "Fuente: datos reales de Google Ads y Meta Ads. CR: cotizaciones completas sobre clics.")
note(M, f"B{R_BEN+N+1}", "Hogar: Cyber 2025 con CPM y CPC ajustados por inflación. SSM: benchmark de AP Search Not Brand. "
     "Teaser: Demand Gen y tráfico de Meta de octubre 2026.")

# =====================================================================
# BGT DIARIO
# =====================================================================
B = wb.create_sheet("BGT Diario")
FECHAS = [dt.date(2026, 10, 29) + dt.timedelta(days=k) for k in range(11)]
ETAPA = [0] * 4 + [1] * 3 + [2] * 4
sheet(B, {"A": 2.6, "B": 52, "C": 15, **{L(4 + k): 12 for k in range(26)}})
brand(B, "Inversión diaria  |  Cyber Monday 2026 Sancor Seguros",
      "Inversión de cada etapa repartida en partes iguales entre sus días.")


def plan(r0, titulo, rmp):
    band(B, r0 - 2, 2, 15, titulo)
    header(B, r0 - 1, 2, ["Campaña", "Inversión"] + [None] * 11 + ["Control"])
    for k in range(11):
        c = put(B, f"{L(4+k)}{r0-1}", f"=MP!$C${R_ET}+{k}", F(bold=True), "ddd dd/mm", VERDE, al="center", box=True)
    for i in range(N):
        r, m = r0 + i, rmp + i
        bg = ZEBRA if i % 2 else None
        cell(B, f"B{r}", f"=MP!C{m}", bg=bg, bold=True)
        cell(B, f"C{r}", f"=MP!I{m}", MONEY, bg)
        for k in range(11):
            col = "FGH"[ETAPA[k]]
            cell(B, f"{L(4+k)}{r}", f"=MP!{col}{m}/MP!{DIAS[ETAPA[k]]}", MONEY, bg)
        cell(B, f"O{r}", f"=SUM(D{r}:N{r})-C{r}", MONEY, bg)
    rt = r0 + N
    total_row(B, rt, 2, 15)
    put(B, f"B{rt}", "Total", F(bold=True), bg=L_VERDE, box=True)
    for k in range(13):
        col = L(3 + k)
        put(B, f"{col}{rt}", f"=SUM({col}{r0}:{col}{rt-1})", F(bold=True), MONEY, L_VERDE, box=True)
    return rt


P1 = 8
T1 = plan(P1, "ESCENARIO CONSERVADOR", R_DC)
P2 = T1 + 4
T2 = plan(P2, "ESCENARIO AGRESIVO", R_DA)

# control de consumo (conservador)
C0 = T2 + 4
band(B, C0 - 2, 2, 27, "CONTROL DE CONSUMO · ESCENARIO CONSERVADOR")
header(B, C0 - 1, 2, ["Campaña", "Inversión"])
for k in range(11):
    put(B, f"{L(4+2*k)}{C0-1}", f"=MP!$C${R_ET}+{k}", F(bold=True), "ddd dd/mm", VERDE, al="center", box=True)
    put(B, f"{L(5+2*k)}{C0-1}", "%", F(bold=True), bg=VERDE, al="center", box=True)
put(B, f"AA{C0-1}", "Consumo TOTAL", F(bold=True), bg=VERDE, al="center", box=True)
B.column_dimensions["Z"].width = 3
B.column_dimensions["AA"].width = 16
for i in range(N + 1):
    r = C0 + i
    total = i == N
    bg = L_VERDE if total else (ZEBRA if i % 2 else None)
    pr = P1 + i
    if total:
        total_row(B, r, 2, 27)
        put(B, f"B{r}", "Total", F(bold=True), bg=L_VERDE, box=True)
        put(B, f"C{r}", f"=C{T1}", F(bold=True), MONEY, L_VERDE, box=True)
    else:
        cell(B, f"B{r}", f"=B{pr}", bg=bg, bold=True)
        cell(B, f"C{r}", f"=C{pr}", MONEY, bg)
    reales = []
    for k in range(11):
        rc, pc, plc = L(4 + 2 * k), L(5 + 2 * k), L(4 + k)
        reales.append(f"{rc}{r}")
        if total:
            put(B, f"{rc}{r}", f"=IF(COUNT({rc}{C0}:{rc}{r-1})=0,\"\",SUM({rc}{C0}:{rc}{r-1}))", F(bold=True), MONEY, L_VERDE, box=True)
        else:
            c = cell(B, f"{rc}{r}", None, MONEY, bg)
            c.font = F(color="1155CC")
        put(B, f"{pc}{r}", f"=IF({rc}{r}=\"\",\"\",IFERROR({rc}{r}/{plc}{pr},\"\"))", F(bold=total), "0.0%",
            L_VERDE if total else bg, al="center", box=True)
    put(B, f"AA{r}", f"=SUM({','.join(reales)})", F(bold=True), MONEY, L_VERDE if total else bg, box=True)
CT = C0 + N
rango = f"E{C0}:Y{CT}"
B.conditional_formatting.add(rango, FormulaRule(
    formula=[f'AND(E${C0-1}="%",ISNUMBER(E{C0}),E{C0}>=0.9,E{C0}<=1.1)'], fill=fill("D5F5E6")))
B.conditional_formatting.add(rango, FormulaRule(
    formula=[f'AND(E${C0-1}="%",ISNUMBER(E{C0}),OR(E{C0}<0.9,E{C0}>1.1))'], fill=fill("FBD3EC")))
note(B, f"B{CT+1}", "Cargar el consumo real de cada día. El % compara contra el plan del día: en verde entre 90 % y 110 %, "
     "en rosa fuera de ese rango.")

wb.save(OUT)
print("ok", OUT, "filas MP:", R_BEN + N + 1)
