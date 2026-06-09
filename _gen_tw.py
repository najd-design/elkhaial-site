# -*- coding: utf-8 -*-
# Generates a self-contained tailwind.css with ONLY the utilities used by index.html,
# plus the custom theme (gold/ice/navy, cairo/tajawal) and Tailwind v3 Preflight.
# No Node, no CDN, no downloads. Deterministic.

THEME = {
    'gold':       '#D4A84B', 'gold-light': '#F5D78E', 'gold-dark': '#B8902F',
    'ice':        '#7EC8E3', 'ice-light':  '#C8E8F5', 'ice-deep':  '#5BA8C7',
    'navy':       '#1A2744', 'navy-dark':  '#0F1828',
    'ticket':     '#e63946',
}
RGB = {
    'white': (255, 255, 255),
    'gold':  (212, 168, 75),
    'ice':   (126, 200, 227),
}

# ---- Tailwind v3 Preflight (faithful, compact) ----
PREFLIGHT = r"""
/* Tailwind Preflight (v3) — base reset the page relies on */
*,::before,::after{box-sizing:border-box;border-width:0;border-style:solid;border-color:currentColor}
::before,::after{--tw-content:''}
html{line-height:1.5;-webkit-text-size-adjust:100%;-moz-tab-size:4;tab-size:4;font-family:inherit}
body{margin:0;line-height:inherit}
hr{height:0;color:inherit;border-top-width:1px}
h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit;margin:0}
a{color:inherit;text-decoration:inherit}
b,strong{font-weight:bolder}
button,input,optgroup,select,textarea{font-family:inherit;font-size:100%;font-weight:inherit;line-height:inherit;color:inherit;margin:0;padding:0}
button,select{text-transform:none}
button,[type=button],[type=reset],[type=submit]{-webkit-appearance:button;background-color:transparent;background-image:none;cursor:pointer}
:-moz-focusring{outline:auto}
p,blockquote,figure,h1,h2,h3,h4,h5,h6{margin:0}
ol,ul,menu{list-style:none;margin:0;padding:0}
img,svg,video,canvas,audio,iframe,embed,object{display:block;vertical-align:middle}
img,video{max-width:100%;height:auto}
[hidden]{display:none}
"""

# ---- scales ----
SPACE = {  # rem
    '0':'0','1':'0.25rem','2':'0.5rem','3':'0.75rem','4':'1rem','5':'1.25rem',
    '6':'1.5rem','7':'1.75rem','8':'2rem','10':'2.5rem','12':'3rem','14':'3.5rem',
    '20':'5rem','24':'6rem','32':'8rem','40':'10rem',
}
SIZE = dict(SPACE); SIZE['full']='100%'
TEXT = {  # (font-size, line-height)
    'xs':('0.75rem','1rem'),'sm':('0.875rem','1.25rem'),'base':('1rem','1.5rem'),
    'lg':('1.125rem','1.75rem'),'xl':('1.25rem','1.75rem'),'2xl':('1.5rem','2rem'),
    '3xl':('1.875rem','2.25rem'),'4xl':('2.25rem','2.5rem'),'5xl':('3rem','1'),
    '6xl':('3.75rem','1'),'7xl':('4.5rem','1'),'8xl':('6rem','1'),
}
ROUND = {'xl':'0.75rem','2xl':'1rem','3xl':'1.5rem','full':'9999px'}
MAXW = {'2xl':'42rem','3xl':'48rem','4xl':'56rem','5xl':'64rem','6xl':'72rem'}
WEIGHT = {'medium':'500','bold':'700','black':'900'}
LEAD = {'tight':'1.25','relaxed':'1.625','loose':'2'}

def color(name):
    return THEME[name]

def rgba(base, a):
    r,g,b = RGB[base]
    return f"rgba({r},{g},{b},{a})"

# escape '/' '[' ']' ':' '.' in class selectors
def sel(cls):
    out=''
    for ch in cls:
        if ch in '/[]:.%':
            out+='\\'+ch
        else:
            out+=ch
    return '.'+out

rules = []   # (selector, body)  -- base (non-responsive)
def add(cls, body):
    rules.append((sel(cls), body))

# ---------- layout / display ----------
for c,b in [
    ('block','display:block'),('inline-block','display:inline-block'),
    ('flex','display:flex'),('grid','display:grid'),('hidden','display:none'),
    ('flex-col','flex-direction:column'),('flex-row','flex-direction:row'),
    ('flex-wrap','flex-wrap:wrap'),('flex-grow','flex-grow:1'),
    ('flex-shrink-0','flex-shrink:0'),
    ('items-center','align-items:center'),('items-start','align-items:flex-start'),
    ('justify-center','justify-content:center'),('justify-between','justify-content:space-between'),
    ('justify-start','justify-content:flex-start'),
    ('text-center','text-align:center'),('text-right','text-align:right'),
    ('relative','position:relative'),('absolute','position:absolute'),('fixed','position:fixed'),
    ('overflow-hidden','overflow:hidden'),('object-cover','object-fit:cover'),
    ('pointer-events-none','pointer-events:none'),('italic','font-style:italic'),
    ('underline','text-decoration-line:underline'),('mx-auto','margin-left:auto;margin-right:auto'),
    ('min-h-screen','min-height:100vh'),
    ('z-10','z-index:10'),('z-50','z-index:50'),
    ('opacity-0','opacity:0'),
]:
    add(c,b)

# grid cols
for n in (1,2,3,4):
    add(f'grid-cols-{n}', f'grid-template-columns:repeat({n},minmax(0,1fr))')

# ---------- spacing ----------
for k,v in SPACE.items():
    add(f'p-{k}', f'padding:{v}')
    add(f'px-{k}', f'padding-left:{v};padding-right:{v}')
    add(f'py-{k}', f'padding-top:{v};padding-bottom:{v}')
    add(f'pt-{k}', f'padding-top:{v}')
    add(f'pb-{k}', f'padding-bottom:{v}')
    add(f'mb-{k}', f'margin-bottom:{v}')
    add(f'mt-{k}', f'margin-top:{v}')
    add(f'gap-{k}', f'gap:{v}')
# space-y
for k in ('2','4','6'):
    add(f'space-y-{k}', f'')  # placeholder replaced below
# space-y needs child combinator
SPACEY=[]
for k in ('2','4','6'):
    SPACEY.append((sel(f'space-y-{k}')+'>:not([hidden])~:not([hidden])', f'margin-top:{SPACE[k]}'))

# ---------- sizing ----------
for k,v in SIZE.items():
    if k in ('3','6','8','10','12','24','32','40','full'):
        add(f'w-{k}', f'width:{v}')
        add(f'h-{k}', f'height:{v}')
for k,v in MAXW.items():
    add(f'max-w-{k}', f'max-width:{v}')
add('min-w-[180px]','min-width:180px')

# ---------- typography ----------
for k,(fs,lh) in TEXT.items():
    add(f'text-{k}', f'font-size:{fs};line-height:{lh}')
for k,v in WEIGHT.items():
    add(f'font-{k}', f'font-weight:{v}')
for k,v in LEAD.items():
    add(f'leading-{k}', f'line-height:{v}')
add('font-cairo','font-family:Cairo,sans-serif')
add('font-tajawal','font-family:Tajawal,sans-serif')

# ---------- radius ----------
for k,v in ROUND.items():
    add(f'rounded-{k}', f'border-radius:{v}')

# ---------- borders ----------
add('border','border-width:1px')
add('border-2','border-width:2px')
add('border-4','border-width:4px')
add('border-t','border-top-width:1px')
add('border-b','border-bottom-width:1px')
add('border-white','border-color:#fff')
add('border-white/10','border-color:'+rgba('white','0.1'))
for a in ('20','30','40'):
    add(f'border-gold/{a}','border-color:'+rgba('gold','0.'+a[:-1] if False else '0.'+a))
for a in ('20','30'):
    add(f'border-ice/{a}','border-color:'+rgba('ice','0.'+a))

# ---------- colors (text/bg) ----------
add('text-gold-light','color:'+color('gold-light'))
add('text-ice-light','color:'+color('ice-light'))
add('text-navy','color:'+color('navy'))
add('text-ticket','color:'+color('ticket'))
add('text-white','color:#fff')
for a in ('40','50','80','85','90'):
    add(f'text-white/{a}','color:'+rgba('white','0.'+a))
add('bg-navy-dark','background-color:'+color('navy-dark'))

# ---------- shadows ----------
add('shadow-xl','box-shadow:0 20px 25px -5px rgba(0,0,0,0.1),0 8px 10px -6px rgba(0,0,0,0.1)')
add('shadow-2xl','box-shadow:0 25px 50px -12px rgba(0,0,0,0.25)')

# ---------- transitions / transform ----------
add('transition','transition-property:color,background-color,border-color,text-decoration-color,fill,stroke,opacity,box-shadow,transform,filter,backdrop-filter;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s')
add('transition-all','transition-property:all;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s')
add('transition-transform','transition-property:transform;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s')
add('duration-300','transition-duration:.3s')
add('duration-700','transition-duration:.7s')
add('translate-x-1/2','transform:translateX(50%)')

# ---------- position insets ----------
add('inset-0','top:0;right:0;bottom:0;left:0')
add('top-0','top:0')
add('top-20','top:5rem')
add('bottom-20','bottom:5rem')
add('left-0','left:0')
add('left-10','left:2.5rem')
add('right-0','right:0')
add('right-10','right:2.5rem')
add('right-1/2','right:50%')
add('-top-6','top:-1.5rem')

# ---------- container ----------
container_rules = [(sel('container'),'width:100%')]
CONTAINER_BP = [('640px','640px'),('768px','768px'),('1024px','1024px'),('1280px','1280px'),('1536px','1536px')]

# ---------- hover / group-hover ----------
HOVER = [
    (sel('hover:text-gold-light')+':hover','color:'+color('gold-light')),
    (sel('group')+':hover '+sel('group-hover:scale-110'),'transform:scale(1.1)'),
]

# ---------- responsive ----------
# map prefix -> min-width
BP = {'sm':'640px','md':'768px'}
RESP = {
    'sm': {
        'block':'display:block','flex-row':'flex-direction:row',
        'gap-3':'gap:0.75rem','gap-4':'gap:1rem','gap-6':'gap:1.5rem',
        'grid-cols-3':'grid-template-columns:repeat(3,minmax(0,1fr))',
        'h-14':'height:3.5rem','w-14':'width:3.5rem',
        'items-center':'align-items:center','p-10':'padding:2.5rem','p-12':'padding:3rem',
        'px-6':'padding-left:1.5rem;padding-right:1.5rem',
        'text-2xl':'font-size:1.5rem;line-height:2rem','text-3xl':'font-size:1.875rem;line-height:2.25rem',
        'text-4xl':'font-size:2.25rem;line-height:2.5rem','text-5xl':'font-size:3rem;line-height:1',
        'text-6xl':'font-size:3.75rem;line-height:1','text-7xl':'font-size:4.5rem;line-height:1',
        'text-base':'font-size:1rem;line-height:1.5rem','text-sm':'font-size:0.875rem;line-height:1.25rem',
        'text-xl':'font-size:1.25rem;line-height:1.75rem',
    },
    'md': {
        'grid-cols-2':'grid-template-columns:repeat(2,minmax(0,1fr))',
        'grid-cols-3':'grid-template-columns:repeat(3,minmax(0,1fr))',
        'grid-cols-4':'grid-template-columns:repeat(4,minmax(0,1fr))',
        'justify-start':'justify-content:flex-start',
        'text-8xl':'font-size:6rem;line-height:1',
    },
}

def emit():
    out=[]
    out.append('/* Generated: self-contained Tailwind subset for index.html — no CDN, no build step. */')
    out.append(PREFLIGHT.strip())
    out.append('\n/* Utilities */')
    for s,b in rules:
        if b:
            out.append(f'{s}{{{b}}}')
    for s,b in SPACEY:
        out.append(f'{s}{{{b}}}')
    out.append('\n/* container */')
    for s,b in container_rules:
        out.append(f'{s}{{{b}}}')
    for mn,mx in CONTAINER_BP:
        out.append(f'@media (min-width:{mn}){{{sel("container")}{{max-width:{mx}}}}}')
    out.append('\n/* hover / group-hover */')
    for s,b in HOVER:
        out.append(f'{s}{{{b}}}')
    for pre,mw in BP.items():
        out.append(f'\n@media (min-width:{mw}){{')
        for cls,body in RESP[pre].items():
            out.append(f'  {sel(pre+":"+cls)}{{{body}}}')
        out.append('}')
    return '\n'.join(out)+'\n'

open('tailwind.css','w',encoding='utf-8').write(emit())
print('tailwind.css written, bytes=', len(open('tailwind.css',encoding='utf-8').read()))
