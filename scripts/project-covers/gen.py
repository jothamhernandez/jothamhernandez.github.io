"""Generate the project cover images for the portfolio (navy/gold design system).

1. python3 -I scripts/project-covers/gen.py scripts/project-covers
   -> writes skills-bridge.html, digital-government.html, event-tabulation.html (1200x675)
2. Render each at 2x with headless Chrome, then downscale to WebP:
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
     --force-device-scale-factor=2 --window-size=1200,675 --virtual-time-budget=8000 \
     --screenshot=out@2x.png file://$PWD/scripts/project-covers/skills-bridge.html
   magick out@2x.png -resize 1600x900 -quality 86 public/projects/skills-bridge.webp
Diagram content is schematic/illustrative (generic occupations, candidates, scores).
"""
import math, random, sys, os

OUT = sys.argv[1]
GOLD = '#c9a96a'; PAPER = '#f7f5f0'; MUTED = '#8d97a6'; INK3 = '#1b3150'

def page(name, svg, label, title, sub, corner):
    html = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"></head>
<body><div class="grid"></div><div class="frame"></div>
<div class="corner mono" style="top:36px;left:40px">{corner[0]}</div>
<div class="corner mono" style="top:36px;right:40px">{corner[1]}</div>
{svg}
<div class="cap"><div class="label mono">{label}</div><h1>{title}</h1><p>{sub}</p></div>
</body></html>"""
    open(os.path.join(OUT, name + '.html'), 'w').write(html)

# ---------------------------------------------------------------- 1. Skills Bridge
def skills_bridge():
    rnd = random.Random(7)
    s = ['<svg width="1200" height="675" style="position:absolute;inset:0">']
    # vector space panel
    px, py, pw, ph = 64, 96, 330, 330
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="rgba(17,35,59,.7)" stroke="rgba(247,245,240,.12)"/>')
    s.append(f'<text x="{px+16}" y="{py+26}" fill="{GOLD}" font-size="11" letter-spacing="2">01 · VECTOR RETRIEVAL</text>')
    qx, qy = px + 190, py + 190
    pts = []
    for c, (cx, cy, n) in enumerate([(px+90, py+110, 26), (px+240, py+120, 22), (px+120, py+250, 22), (px+210, py+210, 18)]):
        for _ in range(n):
            pts.append((cx + rnd.gauss(0, 28), cy + rnd.gauss(0, 24)))
    pts = [(x, y) for x, y in pts if px + 12 < x < px + pw - 12 and py + 40 < y < py + ph - 12]
    near = sorted(pts, key=lambda p: (p[0]-qx)**2 + (p[1]-qy)**2)[:6]
    s.append(f'<circle cx="{qx}" cy="{qy}" r="62" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-dasharray="3 4"/>')
    for x, y in pts:
        on = (x, y) in near
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.2 if on else 2.4}" fill="{GOLD if on else MUTED}" fill-opacity="{1 if on else .45}"/>')
    for x, y in near:
        s.append(f'<line x1="{qx}" y1="{qy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1"/>')
    s.append(f'<circle cx="{qx}" cy="{qy}" r="7" fill="{PAPER}"/><circle cx="{qx}" cy="{qy}" r="12" fill="none" stroke="{PAPER}" stroke-opacity=".5"/>')
    s.append(f'<text x="{qx+16}" y="{qy-14}" fill="{PAPER}" font-size="10" letter-spacing="1">QUERY</text>')
    s.append(f'<text x="{px+16}" y="{py+ph-16}" fill="{MUTED}" font-size="10" letter-spacing="1.5">TOP-K CANDIDATES (k=6)</text>')

    # arrow from panel to graph
    s.append(f'<line x1="{px+pw+14}" y1="{py+ph/2}" x2="{px+pw+64}" y2="{py+ph/2}" stroke="{GOLD}" stroke-width="1.2"/>')
    s.append(f'<path d="M{px+pw+64},{py+ph/2-5} l8,5 l-8,5 z" fill="{GOLD}"/>')

    # bipartite knowledge graph
    gx0, gx1 = 560, 960
    s.append(f'<text x="{gx0-60}" y="{py+26}" fill="{GOLD}" font-size="11" letter-spacing="2">02 · GRAPH VALIDATION</text>')
    occ = ['Web Developer', 'Data Analyst', 'Network Technician', 'Cloud Engineer', 'ICT Trainer']
    skl = ['JavaScript', 'SQL', 'Python', 'Data Modeling', 'Network Security', 'Cloud Architecture', 'Instructional Design']
    oy = [py + 70 + i * 66 for i in range(len(occ))]
    sy = [py + 52 + i * 49 for i in range(len(skl))]
    valid = [(0,0),(0,1),(1,1),(1,2),(1,3),(2,4),(3,5),(3,2),(3,4),(4,6),(4,0)]
    rejected = [(0,5),(2,2),(4,3)]
    for a, b in rejected:
        s.append(f'<path d="M{gx0+150},{oy[a]} C{gx0+260},{oy[a]} {gx1-110},{sy[b]} {gx1-12},{sy[b]}" fill="none" stroke="{MUTED}" stroke-opacity=".45" stroke-dasharray="4 5"/>')
        mx, my = (gx0 + 150 + gx1 - 12) / 2, (oy[a] + sy[b]) / 2
        s.append(f'<g stroke="{MUTED}" stroke-opacity=".8"><line x1="{mx-4}" y1="{my-4}" x2="{mx+4}" y2="{my+4}"/><line x1="{mx-4}" y1="{my+4}" x2="{mx+4}" y2="{my-4}"/></g>')
    for a, b in valid:
        s.append(f'<path d="M{gx0+150},{oy[a]} C{gx0+260},{oy[a]} {gx1-110},{sy[b]} {gx1-12},{sy[b]}" fill="none" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.3"/>')
    for i, o in enumerate(occ):
        s.append(f'<rect x="{gx0-30}" y="{oy[i]-16}" width="180" height="32" rx="2" fill="{INK3}" stroke="rgba(247,245,240,.22)"/>')
        s.append(f'<circle cx="{gx0-14}" cy="{oy[i]}" r="4" fill="{PAPER}"/>')
        s.append(f'<text x="{gx0}" y="{oy[i]+4}" fill="{PAPER}" font-size="12" font-family="Inter" letter-spacing="0">{o}</text>')
    for i, k in enumerate(skl):
        s.append(f'<circle cx="{gx1-8}" cy="{sy[i]}" r="5" fill="{GOLD}"/>')
        s.append(f'<text x="{gx1+6}" y="{sy[i]+4}" fill="rgba(247,245,240,.85)" font-size="12" font-family="Inter" letter-spacing="0">{k}</text>')
    s.append(f'<text x="{gx0-30}" y="{py+ph+48}" fill="{MUTED}" font-size="10" letter-spacing="1.5">OCCUPATIONS</text>')
    s.append(f'<text x="{gx1-14}" y="{py+ph+48}" fill="{MUTED}" font-size="10" letter-spacing="1.5">SKILLS</text>')
    # legend
    lx, ly = 760, 560
    s.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+28}" y2="{ly}" stroke="{GOLD}" stroke-width="1.5"/><text x="{lx+38}" y="{ly+4}" fill="rgba(247,245,240,.7)" font-size="10" letter-spacing="1.2">GRAPH-VALIDATED LINK</text>')
    s.append(f'<line x1="{lx}" y1="{ly+24}" x2="{lx+28}" y2="{ly+24}" stroke="{MUTED}" stroke-dasharray="4 5"/><text x="{lx+38}" y="{ly+28}" fill="rgba(247,245,240,.7)" font-size="10" letter-spacing="1.2">REJECTED CANDIDATE</text>')
    s.append('</svg>')
    page('skills-bridge', '\n'.join(s), 'Hybrid RAG · Knowledge Graph', 'Skills Bridge',
         'Occupation–skill mapping with graph-validated retrieval', ('Research project · 2026', 'Neo4j · PostgreSQL · Vector DB'))

# ---------------------------------------------------------------- 2. Digital Government AI Readiness
def digital_gov():
    s = ['<svg width="1200" height="675" style="position:absolute;inset:0">']
    cx, cy, R = 870, 290, 186
    axes = ['Infrastructure', 'Data Governance', 'Digital Skills', 'Policy & Regulation', 'Leadership', 'Ethics & Trust']
    n = len(axes)
    ang = [-math.pi/2 + i * 2*math.pi/n for i in range(n)]
    pt = lambda i, r: (cx + math.cos(ang[i]) * r, cy + math.sin(ang[i]) * r)
    for lvl in range(1, 6):
        r = R * lvl / 5
        poly = ' '.join(f'{x:.1f},{y:.1f}' for x, y in (pt(i, r) for i in range(n)))
        s.append(f'<polygon points="{poly}" fill="none" stroke="rgba(247,245,240,{.08 if lvl < 5 else .2})"/>')
        x, y = pt(0, r)
        s.append(f'<text x="{x+6:.1f}" y="{y+12:.1f}" fill="{MUTED}" font-size="9">{lvl}</text>')
    for i in range(n):
        x, y = pt(i, R)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="rgba(247,245,240,.12)"/>')
        lx, ly = pt(i, R + 26)
        anchor = 'middle' if abs(lx - cx) < 10 else ('start' if lx > cx else 'end')
        s.append(f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="{anchor}" fill="rgba(247,245,240,.8)" font-size="11" letter-spacing="1.2">{axes[i].upper()}</text>')
    current = [3.2, 2.1, 2.6, 2.0, 2.9, 1.8]
    target = [4.4, 4.0, 4.1, 3.8, 4.3, 4.0]
    for vals, fill, stroke, dash, op in [(target, GOLD, GOLD, '', .14), (current, PAPER, PAPER, '4 4', .05)]:
        poly = ' '.join(f'{x:.1f},{y:.1f}' for x, y in (pt(i, R * v / 5) for i, v in enumerate(vals)))
        s.append(f'<polygon points="{poly}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="1.5" {"stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""}/>')
    for i, v in enumerate(target):
        x, y = pt(i, R * v / 5)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{GOLD}"/>')
    # maturity ladder (left)
    lx, ly = 64, 120
    s.append(f'<text x="{lx}" y="{ly-24}" fill="{GOLD}" font-size="11" letter-spacing="2">AI READINESS MATURITY</text>')
    levels = ['Initial', 'Developing', 'Defined', 'Managed', 'Optimized']
    for i, name in enumerate(levels):
        y = ly + (4 - i) * 52
        w = 70 + i * 52
        on = i == 2
        s.append(f'<rect x="{lx}" y="{y}" width="{w}" height="36" fill="{GOLD if on else INK3}" fill-opacity="{.95 if on else 1}" stroke="rgba(247,245,240,{0 if on else .15})"/>')
        s.append(f'<text x="{lx+12}" y="{y+23}" fill="{"#0b1a2e" if on else PAPER}" font-size="11" letter-spacing="1.2">{i+1}</text>')
        s.append(f'<text x="{lx+w+14}" y="{y+23}" fill="rgba(247,245,240,{.95 if on else .6})" font-size="13" font-family="Inter" letter-spacing="0">{name}</text>')
    # legend
    gx, gy = 700, 636
    s.append(f'<rect x="{gx}" y="{gy-8}" width="22" height="10" fill="{GOLD}" fill-opacity=".25" stroke="{GOLD}"/><text x="{gx+32}" y="{gy+2}" fill="rgba(247,245,240,.7)" font-size="10" letter-spacing="1.2">TARGET STATE</text>')
    s.append(f'<rect x="{gx+150}" y="{gy-8}" width="22" height="10" fill="none" stroke="{PAPER}" stroke-dasharray="3 3"/><text x="{gx+182}" y="{gy+2}" fill="rgba(247,245,240,.7)" font-size="10" letter-spacing="1.2">BASELINE ASSESSMENT</text>')
    s.append(f'<text x="{gx+340}" y="{gy+2}" fill="{MUTED}" font-size="9" letter-spacing="1.2">ILLUSTRATIVE</text>')
    s.append('</svg>')
    page('digital-government', '\n'.join(s), 'Policy · Governance Framework', 'Digital Government AI Readiness',
         'Indicators and pathways for AI adoption in public institutions', ('Research project · 2025', 'Concept'))

# ---------------------------------------------------------------- 3. Event Tabulation
def tabulation():
    s = ['<svg width="1200" height="675" style="position:absolute;inset:0">']
    bx, by, bw, bh = 64, 76, 700, 400
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="rgba(17,35,59,.85)" stroke="rgba(247,245,240,.14)"/>')
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="44" fill="{INK3}"/>')
    s.append(f'<circle cx="{bx+22}" cy="{by+22}" r="5" fill="{GOLD}"/><circle cx="{bx+22}" cy="{by+22}" r="10" fill="none" stroke="{GOLD}" stroke-opacity=".4"/>')
    s.append(f'<text x="{bx+40}" y="{by+26}" fill="{GOLD}" font-size="11" letter-spacing="2">LIVE</text>')
    s.append(f'<text x="{bx+90}" y="{by+26}" fill="{PAPER}" font-size="11" letter-spacing="2">FINAL ROUND · OVERALL STANDINGS</text>')
    s.append(f'<text x="{bx+bw-20}" y="{by+26}" text-anchor="end" fill="{MUTED}" font-size="10" letter-spacing="1.5">5 JUDGES · SYNCED</text>')
    cols = ['RANK', 'CANDIDATE', 'J1', 'J2', 'J3', 'J4', 'J5', 'TOTAL']
    cx = [bx+20, bx+80, bx+260, bx+320, bx+380, bx+440, bx+500, bx+590]
    hy = by + 76
    for c, x in zip(cols, cx):
        s.append(f'<text x="{x}" y="{hy}" fill="{MUTED}" font-size="10" letter-spacing="1.5">{c}</text>')
    rows = [('07', [9.6, 9.4, 9.7, 9.5, 9.6]), ('12', [9.5, 9.6, 9.3, 9.6, 9.4]), ('03', [9.2, 9.4, 9.5, 9.1, 9.3]),
            ('18', [9.1, 9.0, 9.3, 9.2, 9.0]), ('05', [8.9, 9.1, 8.8, 9.0, 8.9])]
    for r, (cand, sc) in enumerate(rows):
        y = hy + 26 + r * 58
        top = r == 0
        if top:
            s.append(f'<rect x="{bx+8}" y="{y-6}" width="{bw-16}" height="50" fill="{GOLD}" fill-opacity=".09"/>')
            s.append(f'<rect x="{bx+8}" y="{y-6}" width="3" height="50" fill="{GOLD}"/>')
        s.append(f'<line x1="{bx+8}" y1="{y+48}" x2="{bx+bw-8}" y2="{y+48}" stroke="rgba(247,245,240,.07)"/>')
        s.append(f'<text x="{cx[0]}" y="{y+24}" fill="{GOLD if top else PAPER}" font-size="20" font-family="Source Serif 4" font-weight="600" letter-spacing="0">{r+1}</text>')
        s.append(f'<text x="{cx[1]}" y="{y+16}" fill="{PAPER}" font-size="13" font-family="Inter" letter-spacing="0">Candidate {cand}</text>')
        total = sum(sc) / len(sc)
        s.append(f'<rect x="{cx[1]}" y="{y+26}" width="150" height="4" fill="rgba(247,245,240,.08)"/>')
        s.append(f'<rect x="{cx[1]}" y="{y+26}" width="{150 * (total - 8.5) / 1.3:.1f}" height="4" fill="{GOLD if top else MUTED}"/>')
        for v, x in zip(sc, cx[2:7]):
            s.append(f'<text x="{x}" y="{y+20}" fill="rgba(247,245,240,.75)" font-size="13" letter-spacing="0">{v:.1f}</text>')
        s.append(f'<text x="{cx[7]}" y="{y+21}" fill="{GOLD if top else PAPER}" font-size="15" font-weight="600" letter-spacing="0">{total:.2f}</text>')
    # websocket stream (right)
    sx, sy = 812, 96
    s.append(f'<text x="{sx}" y="{sy}" fill="{GOLD}" font-size="11" letter-spacing="2">WEBSOCKET STREAM</text>')
    events = [('20:41:07.112', 'score.submit', 'J3 → C07'), ('20:41:07.118', 'tally.update', 'C07 9.56'), ('20:41:07.121', 'rank.push', 'board ✓'),
              ('20:41:09.540', 'score.submit', 'J5 → C12'), ('20:41:09.546', 'tally.update', 'C12 9.48'), ('20:41:09.549', 'rank.push', 'board ✓'),
              ('20:41:12.003', 'score.lock', 'J1 · round 3')]
    for i, (t, e, d) in enumerate(events):
        y = sy + 40 + i * 50
        s.append(f'<line x1="{sx+4}" y1="{y-18}" x2="{sx+4}" y2="{y+32}" stroke="rgba(247,245,240,.1)"/>')
        s.append(f'<circle cx="{sx+4}" cy="{y}" r="3.5" fill="{GOLD if "rank" in e else MUTED}"/>')
        s.append(f'<text x="{sx+20}" y="{y-6}" fill="{MUTED}" font-size="9" letter-spacing="1">{t}</text>')
        s.append(f'<text x="{sx+20}" y="{y+10}" fill="{PAPER}" font-size="12" letter-spacing=".5">{e}</text>')
        s.append(f'<text x="{sx+150}" y="{y+10}" fill="rgba(247,245,240,.55)" font-size="11" letter-spacing=".5">{d}</text>')
    s.append('</svg>')
    page('event-tabulation', '\n'.join(s), 'Real-time · WebSocket', 'Event Tabulation Systems',
         'Instant, auditable results for live competitions', ('Commercial projects · 2017–2019', 'PHP · JavaScript · MySQL'))

skills_bridge(); digital_gov(); tabulation()
print('ok')
