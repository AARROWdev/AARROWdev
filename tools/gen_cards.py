"""Generate the profile's project cards (dark + light SVG). Run: python tools/gen_cards.py"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    'dark': dict(bg='#0f1318', fg='#f3f5f8', muted='#9aa4b2', pill='#171c23', line='#252c36'),
    'light': dict(bg='#ffffff', fg='#1b1f24', muted='#57606a', pill='#f3f5f8', line='#d8dee4'),
}


def icon_treemap(a):
    return (f'<rect x="-34" y="-26" width="38" height="30" rx="3" fill="{a}"/>'
            f'<rect x="7" y="-26" width="27" height="17" rx="3" fill="{a}" opacity=".7"/>'
            f'<rect x="7" y="-6" width="27" height="10" rx="3" fill="{a}" opacity=".5"/>'
            f'<rect x="-34" y="7" width="20" height="19" rx="3" fill="{a}" opacity=".55"/>'
            f'<rect x="-11" y="7" width="45" height="19" rx="3" fill="{a}" opacity=".8"/>')


def icon_wave(a):
    hs = [10, 22, 34, 46, 30, 52, 26, 40, 18, 30, 12]
    return ''.join(f'<rect class="bar" style="animation-delay:{i * .12:.2f}s" x="{-38 + i * 7}" y="{-h / 2}" width="4" height="{h}" rx="2" fill="{a}"/>'
                   for i, h in enumerate(hs))


CARDS = [
    dict(slug='bigfoot', name='Bigfoot', accent='#f2b134', ink='#9a6700', icon=icon_treemap,
         lines=["Find what's eating your disk.", 'A disk space analyzer for Windows'],
         stat='space at a glance · treemap · 0 silent deletes', pills=['Python', 'Qt 6', 'Inno Setup']),
    dict(slug='cratedig', name='Cratedig', accent='#3aa8ff', ink='#0969da', icon=icon_wave,
         lines=['Dig through your crates.', 'Explorer + media player in one'],
         stat='plays in sort order · waveforms · playlists', pills=['Python', 'Qt 6', 'mpv', 'ffmpeg']),
]


def pills(items, t):
    x, out = 40, []
    for p in items:
        w = 26 + len(p) * 11.5
        out.append(f'<rect x="{x}" y="262" width="{w:.0f}" height="38" rx="19" fill="{t["pill"]}" stroke="{t["line"]}"/>'
                   f'<text x="{x + w / 2:.0f}" y="287" text-anchor="middle" font-family="{MONO}" font-size="18" fill="{t["fg"]}">{p}</text>')
        x += w + 10
    return ''.join(out)


def card(c, mode):
    t, a = THEMES[mode], c['accent']
    glow = '0.30' if mode == 'dark' else '0.16'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 330" width="600" height="330" role="img" aria-labelledby="t">
<title id="t">{c['name']}: {c['lines'][0]} {c['lines'][1]}. {c['stat']}.</title>
<defs><clipPath id="c"><rect width="600" height="330" rx="20"/></clipPath>
<radialGradient id="gl"><stop offset="0" stop-color="{a}" stop-opacity="{glow}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient></defs>
<style>
.gl{{animation:gl 12s ease-in-out infinite alternate}}
@keyframes gl{{to{{transform:translate(-120px,40px) scale(1.2)}}}}
.bar{{transform-box:fill-box;transform-origin:center;animation:eq 1.6s ease-in-out infinite alternate}}
@keyframes eq{{to{{transform:scaleY(.45)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<g clip-path="url(#c)">
<rect width="600" height="330" fill="{t['bg']}"/>
<circle class="gl" cx="560" cy="40" r="220" fill="url(#gl)"/>
<rect width="600" height="6" fill="{a}"/>
<g transform="translate(520 82)">{c['icon'](a)}</g>
<text x="40" y="96" font-family="{SANS}" font-weight="800" font-size="50" letter-spacing="-1" fill="{t['fg']}">{c['name']}</text>
<text font-family="{SANS}" font-size="27" fill="{t['fg']}"><tspan x="40" y="150">{c['lines'][0]}</tspan><tspan x="40" y="186" fill="{t['muted']}">{c['lines'][1]}</tspan></text>
<text x="40" y="232" font-family="{MONO}" font-size="19" fill="{a if mode == 'dark' else c['ink']}">{c['stat']}</text>
{pills(c['pills'], t)}
</g>
<rect x=".5" y=".5" width="599" height="329" rx="20" fill="none" stroke="{t['line']}"/>
</svg>
'''


os.makedirs(OUT, exist_ok=True)
for c in CARDS:
    for m in THEMES:
        open(os.path.join(OUT, f"card-{c['slug']}-{m}.svg"), 'w', encoding='utf-8', newline='\n').write(card(c, m))
print('cards written')
