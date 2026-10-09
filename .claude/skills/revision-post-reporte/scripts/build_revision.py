"""Arma la página "Puntos a revisar" con el diseño Zenda del reporte mensual.

Uso: python3 -I build_revision.py <reporte.html> <revision.json> <salida.html>

Toma del reporte el <head> (tokens, fuentes, CSS) y el runtime del editor, y
reemplaza el contenido por la lista de revisión definida en el JSON.
"""
import html, json, re, sys

rep, data_path, out = sys.argv[1:4]
h = open(rep, encoding='utf-8').read()
d = json.load(open(data_path, encoding='utf-8'))
esc = html.escape

nav_i = h.index('<nav class="z-nav"')
foot_e = h.index('</footer>', nav_i) + len('</footer>')
ch_i = h.find('<!-- ZR:CHARTS:INICIO')
ch_e = h.find('<!-- ZR:CHARTS:FIN -->')

secs = [('contexto', 'Contexto')] + [(m['id'], m['nombre']) for m in d['medios']] + [('todos', 'Transversales')]
nav = ('<nav class="z-nav" data-print="hide"><a class="brand" href="#top">zenda<span class="dot">.</span></a><div class="pill">'
       + ''.join(f'<a href="#{i}">{esc(n)}</a>' for i, n in secs)
       + f'</div><span class="client-tag">{esc(d["cliente"])} · {esc(d["periodo"])}</span></nav>')

cover = f'''<section class="cover" id="top"><div class="cover-top"><div class="cover-brand"><span class="wordmark">zenda<span class="dot">.</span></span></div><span class="tag tag-g">Plan de acción</span></div><div class="cover-main"><div class="cover-kicker">{esc(d["kicker"])}</div><h1 class="cover-title">Plan de<br><span class="acc">acción</span></h1><p class="cover-sub">{esc(d["bajada"])}</p></div><div class="cover-stats">''' + ''.join(
    f'<div class="cover-stat"><div class="cs-label">{esc(s["label"])}</div><div class="cs-value">{esc(s["valor"])}</div><div class="cs-sub">{esc(s["sub"])}</div></div>'
    for s in d['stats']) + '</div></section>'

def header(label, titulo, acento, badge):
    return (f'<div class="section-header"><div><span class="mono sh-label">{esc(label)}</span>'
            f'<h2>{esc(titulo)} <span class="acc-g">{esc(acento)}</span></h2></div><span class="sh-badge">{esc(badge)}</span></div>')

body = [cover]
body.append(f'<section class="s-light" id="contexto"><div class="wrap">{header("plan de acción / contexto", "Contexto y", "prioridades", d["badge_plan"])}'
            + (('<div class="table-wrap"><table class="z-table rv-table"><thead><tr>' + ''.join(f'<th>{esc(c)}</th>' for c in d['tabla']['columnas']) + '</tr></thead><tbody>'
                + ''.join('<tr>' + ''.join(f'<td>{esc(str(v))}</td>' for v in r) + '</tr>' for r in d['tabla']['filas']) + '</tbody></table></div>') if d.get('tabla') else '')
            + f'<div class="analysis"><div class="analysis-insight"><strong>Contexto:</strong> <span>{esc(d["contexto"])}</span></div></div></div></section>')
for n, m in enumerate(d['medios']):
    cls = 's-light'
    rows = ''.join(f'<tr><td><strong>{esc(r[0])}</strong></td><td>{esc(r[1])}</td><td>{esc(r[2])}</td></tr>' for r in m['filas'])
    body.append(f'<section class="{cls}" id="{m["id"]}"><div class="wrap">{header("plan de acción / " + m["nombre"].lower(), m["nombre"] + ":", "plan de acción", m["badge"])}'
                f'<div class="analysis" style="margin-bottom:14px"><div class="analysis-insight"><strong>Prioridad:</strong> <span>{esc(m["lead"])}</span></div></div>'
                f'<div class="table-wrap"><table class="z-table rv-table"><thead><tr><th>Punto a revisar</th><th>Evidencia</th><th>Acción</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>')
steps = ''.join(f'<div class="next-step"><span class="ns-num">{i+1:02d}</span><h3>{esc(t["titulo"])}</h3><p>{esc(t["texto"])}</p></div>'
                for i, t in enumerate(d['transversales']))
body.append(f'<section class="s-dark" id="todos"><div class="wrap">{header("plan de acción / transversal", "Iniciativas", "transversales", d["badge_cierre"])}'
            f'<div class="conclusion-grid cols-2">{steps}</div></div></section>')
footer = (f'<footer class="z-footer"><div class="zf-inner"><div class="zf-brand">zenda<span class="dot">.</span></div>'
          f'<div class="zf-meta">Plan de acción · {esc(d["cliente"])} · {esc(d["periodo"])}</div></div></footer>')

css = '''<style id="rv-css">
.rv-table td,.rv-table th{font-size:12px;padding-top:6px!important;padding-bottom:6px!important;vertical-align:top;white-space:normal}
.rv-table td:first-child{width:24%}.rv-table td:nth-child(2){width:34%}
</style>'''
newh = h[:nav_i] + nav + '\n' + '\n'.join(body) + '\n\n' + footer + h[foot_e:]
if ch_i > 0:
    ch_i = newh.find('<!-- ZR:CHARTS:INICIO'); ch_e = newh.find('<!-- ZR:CHARTS:FIN -->')
    newh = newh[:ch_i] + '<!-- ZR:CHARTS:INICIO --><script></script>' + newh[ch_e:]
newh = re.sub(r'<title>.*?</title>', f'<title>Plan de acción · {esc(d["cliente"])}</title>', newh, count=1, flags=re.S)
newh = newh.replace('</head>', css + '</head>', 1)
open(out, 'w', encoding='utf-8').write(newh)
print('ok', out, len(newh))
