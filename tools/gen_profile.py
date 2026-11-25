"""Generate the AARROWdev profile assets (hero + cards, dark and light). Run: python tools/gen_profile.py
Look matches Aaron's portfolio (M:\\VIBING\\AARONSIMPSON-PORTFOLIO-V2): JetBrains Mono, #0a0a0a, blue accent #4da3ff."""
import base64, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'assets')
PORT = r'M:\VIBING\AARONSIMPSON-PORTFOLIO-V2'
FONT = base64.b64encode(open(os.path.join(PORT, 'fonts', 'jetbrains-mono-latin.woff2'), 'rb').read()).decode()
MONO = "'JBM', 'JetBrains Mono', ui-monospace, Consolas, monospace"


def img(name):
    return 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(ROOT, 'src_img', name), 'rb').read()).decode()   # icons kept here (the portfolio renamed its images)


THEMES = {
    'dark': dict(bg='#0a0a0a', fg='#e8e8e8', muted='#8a8a8a', pill='#141414', line='#222222', glow='0.28'),
    'light': dict(bg='#ffffff', fg='#16181b', muted='#5b6168', pill='#f2f4f6', line='#d9dde2', glow='0.14'),
}
BLUE = {'dark': '#4da3ff', 'light': '#1f6fd1'}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def head(w, h, title, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">\n'
            f'<title id="t">{esc(title)}</title>\n'
            f'<defs><style>@font-face{{font-family:"JBM";src:url(data:font/woff2;base64,{FONT}) format("woff2");font-weight:400 700}}'
            f'.gl{{animation:gl 12s ease-in-out infinite alternate}}@keyframes gl{{to{{transform:translate(-120px,40px) scale(1.2)}}}}'
            f'.cur{{animation:bl 1.1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}'
            f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>\n'
            f'<clipPath id="c"><rect width="{w}" height="{h}" rx="20"/></clipPath></defs>\n<g clip-path="url(#c)">\n'
            f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>\n')


def pills(items, t, x, y, size=17):
    out = []
    for p in items:
        w = 24 + len(p) * size * 0.6
        out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="34" rx="17" fill="{t["pill"]}" stroke="{t["line"]}"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + 23}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{t["fg"]}">{esc(p)}</text>')
        x += w + 10
    return ''.join(out)


def glow(t, a, cx, cy):
    return (f'<defs><radialGradient id="g"><stop offset="0" stop-color="{a}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle class="gl" cx="{cx}" cy="{cy}" r="240" fill="url(#g)"/>\n')


def hero(mode):
    t, a = THEMES[mode], BLUE[mode]
    w, h = 1200, 340
    s = head(w, h, 'Aaron Simpson. Full-stack engineer. Desktop, Android and web apps, built and shipped with AI coding agents.', t)
    s += glow(t, a, 1080, 40)
    s += f'<rect width="{w}" height="6" fill="{a}"/>\n'
    s += f'<text x="60" y="78" font-family="{MONO}" font-size="22" fill="{a}">$ whoami<tspan class="cur" fill="{a}"> _</tspan></text>\n'
    s += f'<text x="60" y="152" font-family="{MONO}" font-weight="700" font-size="64" letter-spacing="-1" fill="{t["fg"]}">Aaron Simpson</text>\n'
    s += f'<text x="60" y="204" font-family="{MONO}" font-size="26" fill="{t["fg"]}">Full-stack engineer.</text>\n'
    s += f'<text x="60" y="242" font-family="{MONO}" font-size="22" fill="{t["muted"]}">Desktop, Android and web apps, built and shipped with AI coding agents.</text>\n'
    s += pills(['Python', 'Qt 6', 'Kotlin', 'Android', 'Web', 'Generative AI'], t, 60, 274, 16)
    s += f'</g>\n<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="none" stroke="{t["line"]}"/>\n</svg>\n'
    return s


# Cards are full-width rows, drawn 1224 wide so a card at width="100%" on GitHub's 830px column keeps the two-up text
# size (scale 0.678). Left: name, tagline, subtitle. A thin divider. Right: the features (accent colour, split onto two
# lines when long) above the tech pills; the right block is vertically centred on the left block so the card reads as
# one row. The height fits the content. An icon (Sensitive P.I.) sits at the far right, centred.
DIV = 520                                    # the divider (the widest left line ends ~470); the right block starts 36 after it


def text_w(s, size):
    return len(s) * size * 0.6                 # JetBrains Mono: every glyph is 0.6 em wide


def feature_lines(stat, size, room):
    """The features on one line, or split at a ' · ' into two lines when one doesn't fit."""
    if text_w(stat, size) <= room:
        return [stat]
    parts = stat.split(' · ')
    best = None
    for k in range(1, len(parts)):
        a, b = ' · '.join(parts[:k]), ' · '.join(parts[k:])
        widest = max(text_w(a, size), text_w(b, size))
        if best is None or widest < best[0]:
            best = (widest, [a, b])
    return best[1]


def card(c, mode, w=1224, h=196):
    t = THEMES[mode]
    a = c['accent'][mode]
    s = head(w, h, f"{c['name']}: {c['l1']} {c['l2']} {c['stat']}", t)
    s += glow(t, a, w - 60, 30)
    s += f'<rect width="{w}" height="6" fill="{a}"/>\n'
    # left block: name / tagline / subtitle (top of the name cap ~ y 46, bottom of the subtitle ~ y 156)
    s += f'<text x="44" y="84" font-family="{MONO}" font-weight="700" font-size="44" letter-spacing="-1" fill="{t["fg"]}">{esc(c["name"])}</text>\n'
    s += f'<text font-family="{MONO}" font-size="22" fill="{t["fg"]}"><tspan x="44" y="128">{esc(c["l1"])}</tspan><tspan x="44" y="158" fill="{t["muted"]}">{esc(c["l2"])}</tspan></text>\n'
    div = c.get('div', DIV)                    # a card whose tagline is wider than the left block moves its divider right
    s += f'<rect x="{div}" y="44" width="1" height="{h - 88}" fill="{t["line"]}"/>\n'
    # right block
    x = div + 36
    right = w - (140 if c.get('icon') else 44)
    fs, ps = 18, 17
    lines = feature_lines(c['stat'], fs, right - x)
    line_h = 28
    block = len(lines) * line_h + 14 + 34          # features, gap, pills
    top = (46 + 158) / 2 - block / 2               # centred on the left block
    y = top + 20
    for ln in lines:
        s += f'<text x="{x}" y="{y:.0f}" font-family="{MONO}" font-size="{fs}" fill="{a}">{esc(ln)}</text>\n'
        y += line_h
    s += pills(c['pills'], t, x, round(y - line_h + 22), ps)
    if c.get('icon'):
        s += f'<image x="{w - 112}" y="{(h - 72) // 2}" width="72" height="72" href="{c["icon"]}" clip-path="inset(0 round 16px)"/>\n'
    s += f'</g>\n<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="none" stroke="{t["line"]}"/>\n</svg>\n'
    return s


CARDS = [
    dict(slug='bigfoot', name='Bigfoot', accent={'dark': '#f2b134', 'light': '#9a6700'}, l1="Find what's eating your disk.", l2='Disk space analyzer for Windows',
         stat='space at a glance · treemap · 0 silent deletes', pills=['Python', 'Qt 6', 'Inno Setup']),
    dict(slug='cratedig', name='Cratedig', accent={'dark': '#4da3ff', 'light': '#1f6fd1'}, l1='Dig through your crates.', l2='Explorer + media player in one',
         stat='plays in sort order · waveforms · playlists', pills=['Python', 'Qt 6', 'mpv', 'ffmpeg', 'Inno Setup']),
    dict(slug='twinsweep', name='Twinsweep', accent={'dark': '#2ec4d6', 'light': '#0f7685'}, l1='Find and delete duplicates with ease.', l2='Duplicate file finder for Windows', div=556,
         stat='exact byte-for-byte matches · Recycle Bin only · one copy always stays', pills=['Python', 'Qt 6']),
    dict(slug='sensitive-pi', name='Sensitive P.I.', accent={'dark': '#ff6b6b', 'light': '#c23b3b'}, icon=img('sensitive-pi-icon-168.webp'),
         l1='Finds exposed IDs, cards and', l2='passwords in your photos.', stat='on Google Play · runs fully on-device', pills=['Kotlin', 'Android']),
    dict(slug='ulti-list', name='Ulti-List', accent={'dark': '#c8f23b', 'light': '#3a31a0'}, icon=img('ulti-list-icon-168.webp'),
         l1='Save movies, shows, books', l2='& games for later.', stat="pick what's next in seconds · no accounts · your list stays on your device", pills=['Kotlin', 'Jetpack Compose', 'Room']),
    dict(slug='websites', name='Manifest', accent={'dark': '#b58ef0', 'light': '#6b3fb5'}, l1='manifestdnb.com', l2='Label site + download store',
         stat='design · front end · back end · deploy', pills=['HTML/CSS/JS', 'PHP', 'PayPal']),
    dict(slug='grymlife', name='GrymLife', accent={'dark': '#4fd1a5', 'light': '#1f7a5c'}, l1='grymlife.com', l2='Artist portfolio site',
         stat='static pages · custom PHP admin', pills=['PHP', 'HTML/CSS/JS', 'Python']),
    dict(slug='play', name='PLAY', accent={'dark': '#ff8a3d', 'light': '#b85a12'}, l1='Your movies, on your Roku.', l2='Windows app + Roku TV app',
         stat='no accounts · no cloud · no transcoding', pills=['Python', 'Qt 6', 'BrightScript']),
    dict(slug='workout-calendar', name='Workout Calendar', accent={'dark': '#4da3ff', 'light': '#1a6fd4'}, l1='Tap a day. Mark the workout.', l2='Android app',
         stat='no internet permission · no accounts · stays on the phone', pills=['Kotlin', 'Jetpack Compose', 'Room']),
]

os.makedirs(OUT, exist_ok=True)
for m in THEMES:
    open(os.path.join(OUT, f'hero-{m}.svg'), 'w', encoding='utf-8', newline='\n').write(hero(m))
    for c in CARDS:
        open(os.path.join(OUT, f"card-{c['slug']}-{m}.svg"), 'w', encoding='utf-8', newline='\n').write(card(c, m))
print('assets written')
