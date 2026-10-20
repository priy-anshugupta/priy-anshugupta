"""Original editorial SVG artwork: ink, paper, cobalt and burnt orange."""
from html import escape

PAPER = '#f1eee7'
INK = '#17212c'
ORANGE = '#dc613b'
BLUE = '#6575f0'


def start(w, h, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>'


def text(x, y, value, size=16, fill=INK, weight=400, mono=False, extra=''):
    font = 'Consolas,monospace' if mono else 'Segoe UI,Arial,Helvetica,sans-serif'
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}>{escape(value)}</text>'


def motion():
    return '<style>.cursor{animation:blink 1.2s steps(1,end) infinite}.traveller{animation:travel 6s ease-in-out infinite}@keyframes blink{50%{opacity:0}}@keyframes travel{0%,10%{transform:translateY(0)}40%,55%{transform:translateY(60px)}85%,100%{transform:translateY(120px)}}@media(prefers-reduced-motion:reduce){.cursor,.traveller{animation:none}}</style>'


def header(theme):
    p = [start(1000, 420, 'Priyanshu Gupta — Agent systems, backend engineering and machine learning. Mumbai. Open to internships.'), motion(),
         f'<rect width="1000" height="400" rx="22" fill="{PAPER}"/>',
         '<path d="M38 58H962M38 330H962" stroke="#d0cdc6"/>',
         text(38,37,'priy-anshugupta',13,INK,mono=True),
         text(962,37,'MUMBAI, INDIA',12,INK,mono=True,extra='letter-spacing="1" text-anchor="end"'),
         text(32,160,'Priyanshu',102,INK,700,extra='letter-spacing="-6"'),
         text(32,267,'Gupta',112,INK,700,extra='letter-spacing="-6"'),
         f'<circle cx="366" cy="254" r="10" fill="{ORANGE}"/>',
         text(38,367,'AI/ML & Software Engineering',21,INK,600),
         '<rect x="704" y="346" width="258" height="36" rx="18" fill="#e0ebe4" stroke="#bccfc2"/>',
         '<circle cx="724" cy="364" r="4" fill="#2b7a50"/>',
         text(742,369,'Open to internships',15,'#245c40',600),
         f'<rect x="642" y="78" width="320" height="228" rx="15" fill="{INK}"/>',
         text(666,107,'WHAT I WORK ON',11,'#aab5c0',mono=True,extra='letter-spacing="1.5"')]
    for i, (label, tools) in enumerate([
        ('Agentic AI', 'LangGraph · MCP · RAG · OpenAI'),
        ('Backend systems', 'Django · FastAPI · PostgreSQL'),
        ('Machine learning', 'PyTorch · XGBoost · Whisper')
    ]):
        y = 143 + i * 64
        p += [text(666,y,label,21,PAPER,600),
              text(666,y+21,tools,12,'#bcc6cf',mono=True)]
        if i < 2:
            p.append(f'<path d="M666 {y+34}H938" stroke="#394754"/>')
    return ''.join(p)+'</svg>'


def contact(name, detail, icon):
    tint, accent = {'web':('#402c29','#f2aa83'), 'in':('#24304d','#a4b4ff'), 'mail':('#203b39','#80d4bd')}[icon]
    p=[start(320,88,name+' — '+detail),
       f'<defs><linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{INK}"/><stop offset="1" stop-color="{tint}"/></linearGradient></defs>',
       '<rect x=".5" y=".5" width="319" height="87" rx="14" fill="url(#card)" stroke="#394450"/>',
       f'<rect x="17" y="21" width="43" height="43" rx="11" fill="{tint}"/>']
    if icon=='web':
        p.append(f'<g stroke="{accent}" stroke-width="1.4" fill="none"><circle cx="38" cy="42" r="11"/><ellipse cx="38" cy="42" rx="5" ry="11"/><path d="M27 42H49M29 37H47M29 47H47"/></g>')
    elif icon=='mail':
        p.append(f'<g stroke="{accent}" stroke-width="1.5" fill="none"><rect x="26" y="34" width="24" height="17" rx="2"/><path d="M27 35L38 44L49 35"/></g>')
    else:
        p.append(text(29,49,'in',23,accent,700))
    p += [text(75,39,name,18,PAPER,600),text(75,60,detail,10,'#c1cad3',mono=True),f'<path d="M282 29H296V43M296 29L279 46" stroke="{accent}" stroke-width="2" fill="none"/>']
    return ''.join(p)+'</svg>'


def terminal(theme, profile=None, events=None, stamp=None, rows=None):
    bg = '#111820' if theme == 'dark' else '#f5f3ee'
    fg = PAPER if theme == 'dark' else INK
    muted = '#aab5c0' if theme == 'dark' else '#596575'
    border = '#34404b' if theme == 'dark' else '#d5d2cc'
    accent = '#ffb185' if theme == 'dark' else '#a34725'
    prompt = '#9ca8ff' if theme == 'dark' else '#4b55be'
    p = [start(1000,530,'Priyanshu Gupta — education, interests and recognition'), motion(),
         f'<rect x=".5" y=".5" width="999" height="529" rx="17" fill="{bg}" stroke="{border}"/>',
         f'<path d="M1 45H999" stroke="{border}"/>',
         f'<circle cx="26" cy="24" r="5" fill="{accent}"/><circle cx="44" cy="24" r="5" fill="{muted}"/><circle cx="62" cy="24" r="5" fill="{border}"/>',
         text(500,28,'priyanshu@mumbai: ~',13,muted,mono=True,extra='text-anchor="middle"')]
    lines = [
        (80, '$ whoami', 18, prompt),
        (108, 'Priyanshu Gupta — AI/ML & Software Engineering', 19, fg),
        (146, '$ cat about.txt', 18, prompt),
        (172, 'I build agent workflows, backend services and ML pipelines.', 18, fg),
        (198, 'I’m interested in how models reason, how agents act, and where both break.', 18, fg),
        (240, '$ cat education.txt', 18, prompt),
        (266, 'Information Technology · Class of 2028', 19, fg),
        (292, 'Vidyalankar Institute of Technology, Mumbai', 19, fg),
        (318, 'CGPA 9.83 / 10', 19, accent),
        (360, '$ cat recognition.txt', 18, prompt),
        (386, 'HackerRank Orchestrate · September 2026', 18, fg),
        (412, '#65 / 3,062 globally · Top 2.2% · 20+ hackathons', 19, accent),
        (450, '$ echo $BASE', 18, prompt),
        (476, 'Mumbai, India', 19, fg),
    ]
    timings=[]
    elapsed=.4
    for _,value,_,_ in lines:
        duration=max(.5,min(2.6,len(value)*(.065 if value.startswith('$') else .04)))
        timings.append((elapsed,elapsed+duration))
        elapsed+=duration+.3
    cycle=round(elapsed+12,2)
    rules=[]
    clips=[]
    for i,(y,value,size,colour) in enumerate(lines):
        begin=timings[i][0]/cycle*100
        end=timings[i][1]/cycle*100
        width=min(924,len(value)*size*.63+8)
        rules.append(f'.line-{i}{{animation:line-{i} {cycle}s steps({len(value)},end) infinite}}'
                     f'@keyframes line-{i}{{0%,{begin:.3f}%{{width:0px}}{end:.3f}%,100%{{width:{width:.1f}px}}}}')
        clips.append(f'<clipPath id="line-{i}"><rect class="line-{i}" x="38" y="{y-size-4}" width="924" height="{size+10}"/></clipPath>')
        p.append(f'<g clip-path="url(#line-{i})">'+text(38,y,value,size,colour,mono=True)+'</g>')
    p.append('<defs>'+''.join(clips)+'</defs>')
    p.append('<style>'+''.join(rules)+'@media(prefers-reduced-motion:reduce){'+','.join('.line-'+str(i) for i in range(len(lines)))+'{animation:none!important;width:924px}}</style>')
    p += [text(38,508,'$',18,prompt,mono=True),
          f'<rect class="cursor" x="57" y="493" width="9" height="18" fill="{prompt}"/>']
    return ''.join(p)+'</svg>'


def project(index,title,description,stack,nodes,status):
    p=[start(1000,82,title+' — '+description+' '+stack),
       f'<rect x=".5" y=".5" width="999" height="81" rx="12" fill="{INK}" stroke="#36424e"/>',
       f'<path d="M63 18V64" stroke="#36424e"/>',
       text(20,48,index,15,ORANGE,mono=True),text(84,49,title,25,PAPER,700),
       text(295,33,description,15,'#d1d7dc'),text(295,58,stack,12,'#aab5c0',mono=True),
       f'<path d="M950 29H968V47M968 29L949 48" stroke="{PAPER}" stroke-width="1.7" fill="none"/>']
    return ''.join(p)+'</svg>'


def extra_assets():
    return {
        'contact-portfolio.svg':contact('Portfolio','Selected work & demos','web'),
        'contact-linkedin.svg':contact('LinkedIn','Let’s connect','in'),
        'contact-email.svg':contact('Email','Get in touch','mail'),
        'project-plexus.svg':project('01','Plexus','Graph-based context for developer security.','Python · LangGraph · Neo4j · FastAPI',[],''),
        'project-sanket.svg':project('02','Sanket AI','Industrial safety signals and incident-risk analysis.','Next.js · FastAPI · PostgreSQL · Whisper',[],''),
        'project-finbuddy.svg':project('03','FinBuddy','Personal finance with 13 specialised agents.','Python · LangChain · Groq · MCP',[],''),
        'project-codemri.svg':project('04','Code MRI','Repository exploration and RAG-based onboarding.','FastAPI · Next.js · TypeScript · FAISS',[],''),
    }
