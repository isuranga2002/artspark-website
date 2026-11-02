"""Generates every ArtSpark page into docs/ (the folder GitHub Pages serves).

All business details live in CONFIG below — change them there and re-run:
    python3 src/build.py
Pages share one header, footer and <head>, so a phone number or a nav link
only ever has to be right in one place.
"""
import json
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"

# ─────────────────────────────────────────────────────────────────────────────
# Business details. Everything customer-facing that is specific to ArtSpark.
# ─────────────────────────────────────────────────────────────────────────────
CONFIG = {
    "brand": "ArtSpark",
    "tagline": "Your Trusted Partner in Academic Excellence",
    "site_url": "https://artspark.edu.lk",         # the live domain, no trailing slash
    "whatsapp": "94719188867",                    # digits only, with country code
    "phone_display": "+94 71 918 8867",
    "email": "",                                  # leave empty to hide email everywhere
    "country": "Sri Lanka",
    "country_code": "LK",
    "founded": 2024,
    # Public profile URLs (Facebook, Instagram, TikTok, LinkedIn…). They go into
    # the footer and into the search-engine markup as "sameAs".
    "social": [
        # ("Facebook", "https://www.facebook.com/artspark"),
    ],
}

# Real student feedback only. Add entries as (quote, "Programme · City") and the
# reviews section appears on the home page automatically. Never invent these.
REVIEWS = [
    # ("Sent my brief at night and had a fixed quote by morning.", "MBA student · Colombo"),
]

TODAY = date.today().isoformat()
C = CONFIG
URL = C["site_url"]
B = C["brand"]


def wa(text=None):
    text = text or f"Hi {B}, I'd like a free quote for my academic work."
    return f"https://wa.me/{C['whatsapp']}?text={quote(text)}"


def unsplash(photo, w):
    return f"https://images.unsplash.com/photo-{photo}?auto=format&fit=crop&w={w}&q=75"


def img(photo, alt, ratio=(4, 3), w=1000, eager=False, sizes="(max-width: 760px) 100vw, 50vw"):
    """Responsive Unsplash image with intrinsic size set, so nothing jumps on load."""
    rw, rh = ratio
    h = round(w * rh / rw)
    half = w // 2
    srcset = f"{unsplash(photo, half)} {half}w, {unsplash(photo, w)} {w}w, {unsplash(photo, w * 3 // 2)} {w * 3 // 2}w"
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{unsplash(photo, w)}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{escape(alt)}" {load} decoding="async" />')


ICONS = {
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6Z"/><path d="m9 12 2 2 4-4"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5Z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/><path d="M22 9v6"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5v14Z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
    "file": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9Z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
    "slides": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M12 16v4M8 20h8"/>',
    "case": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.3-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8"/><path d="M18 14.8c1.9.6 3 2.4 3.5 5.2"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "edit": '<path d="M3 21h4L20 8l-4-4L3 17Z"/><path d="m14 6 4 4"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
}


def icon(name, size=22):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


WA_SVG = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Zm0 18.02c-1.5 0-2.97-.4-4.26-1.16l-.3-.18-3.12.82.83-3.04-.2-.31a8.07 8.07 0 0 1-1.24-4.24c0-4.47 3.64-8.11 8.11-8.11 4.47 0 8.1 3.64 8.1 8.11 0 4.47-3.63 8.11-8.1 8.11Zm4.44-6.07c-.24-.12-1.44-.71-1.66-.79-.22-.08-.38-.12-.55.12-.16.24-.63.79-.77.95-.14.16-.28.18-.52.06-.24-.12-1.03-.38-1.96-1.21-.72-.65-1.21-1.45-1.35-1.69-.14-.24-.02-.37.1-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.55-1.32-.75-1.8-.2-.48-.4-.42-.55-.42-.14 0-.3-.02-.46-.02-.16 0-.42.06-.64.3-.22.24-.84.82-.84 2 0 1.18.86 2.32.98 2.48.12.16 1.69 2.58 4.1 3.62.57.25 1.02.39 1.37.5.58.18 1.1.16 1.52.1.46-.07 1.42-.58 1.62-1.14.2-.56.2-1.04.14-1.14-.06-.1-.22-.16-.46-.28Z"/></svg>')

# ─────────────────────────────────────────────────────────────────────────────
# Content shared between pages
# ─────────────────────────────────────────────────────────────────────────────
PROGRAMMES = ["MBA", "MSc / MA", "BSc / BA / BBA", "HND / HNC", "SLIM / CIM", "PQHRM", "CIMA / AAT", "NVQ", "Diploma", "MPhil / PhD"]

DISTRICTS = ("Colombo, Gampaha, Kalutara, Kandy, Matale, Nuwara Eliya, Galle, Matara, Hambantota, Jaffna, "
             "Kilinochchi, Mannar, Vavuniya, Mullaitivu, Batticaloa, Ampara, Trincomalee, Kurunegala, Puttalam, "
             "Anuradhapura, Polonnaruwa, Badulla, Monaragala, Ratnapura and Kegalle")

SERVICE_ICONS = {"assignments": "pen", "thesis": "book", "research": "chart", "articles": "file",
                 "presentations": "slides", "case-studies": "case", "coaching": "users", "editing": "edit"}

SERVICES = [
    {
        "id": "assignments", "name": "Assignment writing", "photo": "1455390582262-044cdead277a",
        "alt": "Fountain pen writing on lined paper",
        "short": "Coursework, essays and reports from diploma to MBA, written to your rubric and referencing style.",
        "body": [
            "Send the question and the marking rubric, and the assignment is planned against the criteria your examiner will actually use. Each section is built from academic sources, referenced in the style your module handbook asks for, and read by an editor before it reaches you.",
            "Business reports, reflective essays, literature-based essays, lab-style reports and portfolio tasks are all covered, including assignments with practical components such as calculations, diagrams or short presentations.",
        ],
        "includes": [
            "Structure mapped to the learning outcomes and marking rubric",
            "Harvard, APA 7, IEEE, OSCOLA, MLA, Chicago or your institute's house style",
            "Tables, figures, appendices and word count formatted to the brief",
            "Turnitin similarity report and AI-detection report",
            "Seven days of free revisions against the original brief",
        ],
        "levels": "Diploma, HND, BSc / BA, MBA, MSc, SLIM, CIM, CIMA, AAT, PQHRM and NVQ",
    },
    {
        "id": "thesis", "name": "Thesis & dissertation", "photo": "1507842217343-583bb7270b66",
        "alt": "Tall shelves of books in a university library",
        "short": "Proposal to final chapter, shaped round your supervisor's feedback, with viva preparation at the end.",
        "body": [
            "A dissertation is a long project, so we run it like one: an agreed outline, chapter-by-chapter delivery on a timetable you can plan around, and a revision round after every supervisor meeting.",
            "You stay in control of the direction. We explain the choices behind the methodology and the analysis, so you can defend every chapter in your own words when the viva comes.",
        ],
        "includes": [
            "Topic refinement and research proposal",
            "Literature review built on a synthesis matrix of recent sources",
            "Methodology, sampling and questionnaire or interview design",
            "Findings, discussion, conclusion and recommendations",
            "Viva and defence question bank with model answers",
        ],
        "levels": "Final-year undergraduate, MBA, MSc, MA, MPhil and PhD",
    },
    {
        "id": "research", "name": "Research & data analysis", "photo": "1551288049-bebda4e38f71",
        "alt": "Charts and statistics on a laptop screen",
        "short": "Questionnaires, SPSS, Excel, R or NVivo analysis — with the output explained in plain words.",
        "body": [
            "Whether you are starting with a blank questionnaire or a spreadsheet of responses, we design, run and write up the analysis your study needs, in the format your chapter four is expected to follow.",
            "Every analysis is delivered with the raw output files and a short walk-through, so you understand what each test shows and why it was chosen.",
        ],
        "includes": [
            "Questionnaire, interview guide and sampling plan",
            "Reliability, descriptive, correlation, regression, t-test and ANOVA",
            "Thematic analysis for interviews and open-ended answers",
            "Tables and charts written up to APA presentation standards",
            "A walk-through call so you can explain every result",
        ],
        "levels": "Undergraduate research projects, MBA, MSc, MPhil and PhD",
    },
    {
        "id": "articles", "name": "Journal articles & papers", "photo": "1515378791036-0648a3ef77b2",
        "alt": "Researcher typing on a laptop",
        "short": "Research articles, review papers and conference abstracts prepared to the journal's author guidelines.",
        "body": [
            "Turning a dissertation into a paper, or writing a review article from scratch, takes a different discipline from coursework. We work to the target journal's scope, word limits and template from the first draft.",
            "Support continues after submission: we help you read reviewer comments, revise the manuscript and prepare a point-by-point response letter.",
        ],
        "includes": [
            "Journal or conference shortlisting by scope and indexing",
            "IMRaD structure, abstract and keywords",
            "Formatting to the publisher's template and reference style",
            "Cover letter for the editor",
            "Response-to-reviewers letter and revisions",
        ],
        "levels": "Postgraduate students, academics and early-career researchers",
    },
    {
        "id": "presentations", "name": "Presentations", "photo": "1524178232363-1fb2b075b655",
        "alt": "A presenter speaking to a seated audience",
        "short": "Clear, well-designed PowerPoint or Google Slides decks built from your report, with speaker notes.",
        "body": [
            "A good academic deck says less than the report and shows more. We turn your content into a clear sequence of slides — one idea per slide, real charts instead of bullet lists, and your university template where one is required.",
            "Speaker notes are written to your time slot, so you know exactly what to say on every slide and where the questions are likely to come.",
        ],
        "includes": [
            "Storyline and slide outline agreed before design",
            "Custom charts, diagrams and icons",
            "Speaker notes timed to your presentation slot",
            "Your university's template or a clean ArtSpark design",
            "Likely panel questions with suggested answers",
        ],
        "levels": "Coursework, proposal defences, viva presentations and conference talks",
    },
    {
        "id": "case-studies", "name": "Case study analysis", "photo": "1521737604893-d14cc237f11d",
        "alt": "A group discussing a project around a table",
        "short": "Applied analysis using the right framework — SWOT, PESTEL, Porter's Five Forces, VRIO and more.",
        "body": [
            "Case studies reward analysis, not description. We identify the core problem in the case, apply the frameworks your module teaches, and build recommendations that follow from the evidence.",
            "Where the case concerns a Sri Lankan company or sector, we bring in local data and context so the analysis reads as current and grounded.",
        ],
        "includes": [
            "Problem statement and key issues",
            "SWOT, PESTEL, Five Forces, VRIO, Ansoff, BCG or Balanced Scorecard",
            "Financial ratio and trend analysis where the case provides figures",
            "Evidence-based recommendations and an implementation plan",
            "Turnitin and AI-detection reports",
        ],
        "levels": "HND, BBA, MBA, SLIM, CIM and professional programmes",
    },
    {
        "id": "coaching", "name": "Academic coaching", "photo": "1513258496099-48168024aec0",
        "alt": "Student concentrating during an online session",
        "short": "One-to-one online sessions on methods, statistics, academic writing and viva practice.",
        "body": [
            "Some parts of a degree you have to own yourself — the viva, the presentation, the exam. Coaching sessions focus on exactly those, at your pace, online at a time that suits you.",
            "Sessions are practical: we work through your own draft, your own data or your own slides, and you leave each one with clear next steps.",
        ],
        "includes": [
            "Research methodology and statistics tutoring",
            "Academic writing, structure and critical analysis",
            "Mock viva and presentation rehearsal with feedback",
            "Study planning for long projects",
            "Sessions in English or Sinhala",
        ],
        "levels": "Any level, from diploma to doctoral",
    },
    {
        "id": "editing", "name": "Editing & proofreading", "photo": "1517842645767-c639042777db",
        "alt": "Open notebook with a pen and reading glasses",
        "short": "Grammar, flow, structure, referencing and similarity reduction on work you have already written.",
        "body": [
            "Already written your draft? We polish it: language and grammar, paragraph flow, argument structure, and a full check of in-text citations against the reference list.",
            "If your similarity score is too high, we rewrite the flagged passages properly — paraphrasing with correct citation — and show you every change in tracked mode.",
        ],
        "includes": [
            "Language, grammar and academic tone",
            "Structure and argument flow",
            "Citation and reference-list correction",
            "Similarity reduction with tracked changes",
            "Formatting to your institute's guidelines",
        ],
        "levels": "Assignments, dissertations, theses, articles and proposals",
    },
]

FAQS = [
    ("Is it acceptable to use ArtSpark?",
     ["ArtSpark is an academic consulting and tutoring service. We provide model answers, structured drafts, reference material, data analysis and one-to-one guidance to help you understand your subject and complete your own work.",
      "How the material is used is the student's responsibility, and we encourage every student to follow their institute's academic-integrity rules."]),
    ("How much does an order cost?",
     ["Price depends on the level, the word count, the deadline and how technical the work is. Send your brief and you will receive one fixed price within 30 minutes — no hidden fees and no obligation to accept."]),
    ("Can you deliver in 24 hours?",
     ["Often, yes — especially for shorter work. When you ask for a quote we tell you honestly what is possible in your time frame. We would rather decline a job than miss a deadline."]),
    ("Do I really get the Turnitin and AI-detection reports?",
     ["Yes. Every delivery includes a Turnitin similarity report and an AI-detection report at no extra charge. We keep plagiarism and AI-generated text below 10%, and the reports let you confirm it yourself."]),
    ("What if my lecturer asks for changes?",
     ["Revisions against the original brief are free for seven days after delivery, including changes requested by your lecturer or supervisor. New requirements outside the original brief are quoted separately before any work begins."]),
    ("Who works on my order?",
     ["Every writer on our panel is a graduate of a Sri Lankan government university and works only within their own faculty — management, finance, IT, engineering, nursing, education or law. An editor then checks structure, language and referencing before delivery."]),
    ("Will my details be kept confidential?",
     ["Always. Your name, university and documents are never shared or published. Writers see the brief, not your identity, and your files are deleted on request once the order is complete."]),
    ("Where is ArtSpark based?",
     ["ArtSpark is based in Sri Lanka and works online with students in every district, as well as Sri Lankan students studying in the UK, Australia, Canada and the Middle East. We work in English and Sinhala."]),
    ("How do I pay?",
     ["Payment details are sent on WhatsApp after you accept the quote — never before. Large projects such as dissertations can be paid in stages that match the chapter delivery schedule."]),
    ("Which programmes and subjects do you cover?",
     ["MBA, MSc, MA, MPhil, PhD, BSc, BA, BBA, HND, SLIM, CIM, PQHRM, CIMA, AAT, NVQ and diploma programmes. Subjects range from management, HRM, marketing and finance to IT, engineering, nursing, education, law and the social sciences."]),
]

HISTORY = [
    ("2024", "Q1", "The desk opens", "A small panel of writers and one WhatsApp line, taking MBA and HND assignments through word of mouth."),
    ("2024", "Q4", "Proof becomes standard", "Turnitin and AI-detection reports are attached to every delivery, free of charge."),
    ("2025", "", "The panel grows", "Engineering, IT, nursing and law join the panel, along with thesis, research and data-analysis support."),
    ("2026", "", "Online, island-wide", "The website goes live: one desk, a quote within 30 minutes, the same promise."),
]

PROMISES = [
    ("shield", "Plagiarism free", "Written from source material for your brief, checked digitally and read by a proofreader before it leaves us. Similarity stays low, and the report proves it."),
    ("clock", "Always on time", "The delivery date and time are fixed in your quote. We turn work down rather than miss a deadline — that is the whole point of choosing us."),
    ("file", "Free Turnitin & AI report", "Every delivery includes a similarity report and an AI-detection report. You never take our word for it, and you never pay extra for the proof."),
    ("lock", "100% confidential", "Your name, university and documents are never shown to anyone. Writers see the brief, not you, and files are deleted on request."),
]

# ─────────────────────────────────────────────────────────────────────────────
# Page frame
# ─────────────────────────────────────────────────────────────────────────────
NAV = [("index.html", "Home"), ("services.html", "Services"), ("about.html", "About"), ("order.html#faq", "FAQ")]


def org_schema():
    contact = {"@type": "ContactPoint", "contactType": "customer support", "telephone": f"+{C['whatsapp']}",
               "availableLanguage": ["English", "Sinhala"]}
    if C["email"]:
        contact["email"] = C["email"]
    org = {
        "@type": "ProfessionalService",
        "@id": f"{URL}/#organization",
        "name": B,
        "slogan": C["tagline"],
        "url": f"{URL}/",
        "logo": f"{URL}/assets/icon-512.png",
        "image": f"{URL}/assets/artspark-og.jpg",
        "description": f"{B} is a Sri Lankan academic consulting and writing-support service founded in {C['founded']}, offering assignment writing, thesis and dissertation support, research and data analysis, journal articles, case studies, presentations, academic coaching, and editing and proofreading.",
        "foundingDate": str(C["founded"]),
        "telephone": f"+{C['whatsapp']}",
        "priceRange": "Quoted per project",
        "address": {"@type": "PostalAddress", "addressCountry": C["country_code"]},
        "areaServed": [{"@type": "Country", "name": C["country"]}, {"@type": "Place", "name": "Worldwide (Sri Lankan students abroad)"}],
        "availableLanguage": ["English", "Sinhala"],
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59",
        },
        "contactPoint": contact,
        "knowsAbout": ["Academic writing", "Assignment writing", "Dissertation support", "Research methodology",
                       "SPSS data analysis", "Harvard referencing", "APA referencing", "Turnitin similarity reports",
                       "AI detection reports"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": f"{B} services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["short"],
                                                   "url": f"{URL}/services.html#{s['id']}"}}
                for s in SERVICES
            ],
        },
    }
    if C["email"]:
        org["email"] = C["email"]
    if C["social"]:
        org["sameAs"] = [u for _, u in C["social"]]
    return org


def breadcrumbs(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{URL}/{path}"}
            for i, (path, name) in enumerate(trail)
        ],
    }


def head(path, title, desc, extra_schema=(), page_type="WebPage", robots="index, follow, max-image-preview:large, max-snippet:-1"):
    canonical = f"{URL}/" if path == "index.html" else f"{URL}/{path}"
    graph = [
        org_schema(),
        {"@type": "WebSite", "@id": f"{URL}/#website", "url": f"{URL}/", "name": B,
         "inLanguage": "en", "publisher": {"@id": f"{URL}/#organization"}},
        {"@type": page_type, "@id": f"{canonical}#webpage", "url": canonical, "name": title, "description": desc,
         "isPartOf": {"@id": f"{URL}/#website"}, "about": {"@id": f"{URL}/#organization"},
         "inLanguage": "en", "dateModified": TODAY},
        *extra_schema,
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")
    t, d = escape(title), escape(desc)
    og_img = f"{URL}/assets/artspark-og.jpg"
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{t}</title>
<meta name="description" content="{d}" />
<link rel="canonical" href="{canonical}" />
<meta name="robots" content="{robots}" />
<meta name="author" content="{B}" />
<meta name="geo.region" content="{C['country_code']}" />
<meta name="geo.placename" content="{C['country']}" />
<meta name="theme-color" content="#0a0a0a" />
<meta name="color-scheme" content="dark" />
<meta name="format-detection" content="telephone=no" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{B}" />
<meta property="og:locale" content="en_GB" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_img}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{B} — {C['tagline']}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{t}" />
<meta name="twitter:description" content="{d}" />
<meta name="twitter:image" content="{og_img}" />
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png" />
<link rel="icon" type="image/png" sizes="192x192" href="assets/icon-192.png" />
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png" />
<link rel="manifest" href="site.webmanifest" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preconnect" href="https://images.unsplash.com" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Hind:wght@400;500;600;700&display=swap" />
<link rel="stylesheet" href="styles.css" />
<script>document.documentElement.className='js'</script>
<script src="site.js" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(active):
    cur = ' aria-current="page"'
    links = "\n        ".join(f'<a href="{h}"{cur if h == active else ""}>{label}</a>' for h, label in NAV)
    return f"""<header class="site-header">
  <div class="wrap header-in nav">
    <a href="index.html" class="brand" aria-label="{B} home"><img src="assets/artspark-wordmark.png" width="520" height="165" alt="{B}" /></a>
    <a class="header-phone" href="{wa()}" target="_blank" rel="noopener">{WA_SVG}{C['phone_display']}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu"><span class="nav-toggle-bars"></span></button>
    <nav class="nav-links" id="nav-links" aria-label="Main">
        {links}
        <a href="order.html" class="btn btn-gold"{cur if active == "order.html" else ""}>Get a free quote</a>
    </nav>
  </div>
</header>
"""


def cta(title="Send the brief. Get your quote in 30 minutes."):
    return f"""<section class="section" aria-label="Get a quote">
  <div class="wrap">
    <div class="cta-panel reveal">
      <div>
        <h2 class="title">{title}</h2>
        <p>Photograph the question, tell us the deadline, and we reply with a fixed price and a delivery time. No payment until you agree to both.</p>
      </div>
      <div class="btn-row">
        <a href="{wa()}" target="_blank" rel="noopener" class="btn btn-dark">{WA_SVG} Chat on WhatsApp</a>
        <a href="order.html" class="btn btn-on-gold">Fill the order form</a>
      </div>
    </div>
  </div>
</section>
"""


def footer():
    year = date.today().year
    years = f"{C['founded']}–{year}" if year > C["founded"] else str(year)
    svc = "\n          ".join(f'<a href="services.html#{s["id"]}">{escape(s["name"])}</a>' for s in SERVICES[:5])
    social = "".join(f'\n          <a href="{u}" target="_blank" rel="noopener me">{escape(n)}</a>' for n, u in C["social"])
    email = f'\n          <a href="mailto:{C["email"]}">{C["email"]}</a>' if C["email"] else ""
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/artspark-logo-white.png" width="900" height="319" alt="{B} — {C['tagline']}" loading="lazy" />
        <p class="footer-about">Academic consulting and writing support for students across {C['country']} and Sri Lankan students abroad. Since {C['founded']}.</p>
      </div>
      <div>
        <h2>Services</h2>
        <div class="footer-links">
          {svc}
          <a href="services.html" style="color:var(--gold-hi)">All eight services →</a>
        </div>
      </div>
      <div>
        <h2>Company</h2>
        <div class="footer-links">
          <a href="about.html">About {B}</a>
          <a href="about.html#team">Our writers</a>
          <a href="order.html">How to order</a>
          <a href="order.html#faq">FAQ</a>
          <a href="privacy.html">Privacy &amp; terms</a>
        </div>
      </div>
      <div>
        <h2>Contact</h2>
        <div class="footer-links">
          <a href="{wa()}" target="_blank" rel="noopener">WhatsApp {C['phone_display']}</a>{email}{social}
          <span>Open 24 hours, every day</span>
          <span>English &amp; Sinhala</span>
        </div>
      </div>
    </div>
    <div class="footer-base">
      <span>© {years} {B}. All rights reserved.</span>
      <span>{B} supplies consulting and reference material to support your own academic work. <a href="privacy.html#integrity">Academic integrity</a></span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa()}" target="_blank" rel="noopener" aria-label="Chat with {B} on WhatsApp">{WA_SVG}<span class="wa-text">WhatsApp us</span></a>
</body>
</html>
"""


def page(path, active, title, desc, main, **head_kw):
    html = head(path, title, desc, **head_kw) + header(active) + f'<main id="main">\n{main}</main>\n' + footer()
    (OUT / path).write_text(html, encoding="utf-8")
    return path


def kicker(text):
    return f'<div class="kicker-row"><span class="kicker">{text}</span></div>'


def faq_items(items, open_first=False):
    out = []
    for i, (q, a) in enumerate(items):
        paras = "".join(f"<p>{escape(p)}</p>" for p in a)
        out.append(f'<details{" open" if open_first and i == 0 else ""}><summary>{escape(q)}</summary><div class="answer">{paras}</div></details>')
    return "\n      ".join(out)


def page_hero(crumb, kick, h1, lede, extra=""):
    return f"""<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
    {kicker(kick)}
    <h1 class="title">{h1}</h1>
    <p class="lede">{lede}</p>{extra}
  </div>
</section>
"""


def promise_cards():
    return "\n      ".join(
        f'<div class="card reveal"><div class="ic">{icon(i)}</div><h3>{t}</h3><p>{b}</p></div>' for i, t, b in PROMISES
    )


def history_html():
    return "\n      ".join(
        f'<div class="history-item reveal"><p class="when gold-text">{y}{" · " + q if q else ""}</p><div><h3>{t}</h3><p>{b}</p></div></div>'
        for y, q, t, b in HISTORY
    )


HERO_SLIDES = [
    ("1571260899304-425eee4c7efc", "University students studying together in a classroom"),
    ("1627556704302-624286467c65", "Graduate holding up a black mortarboard cap"),
    ("1507842217343-583bb7270b66", "Tall shelves of books in a university library"),
    ("1488190211105-8b0e65b80b4e", "Student writing notes at a desk beside a laptop"),
    ("1606761568499-6d2451b23c66", "A university lecture theatre"),
]


def hero_slides():
    """Slow cross-fading, zooming photos behind the home hero (decorative, so hidden from screen readers).
    Only the first photo loads with priority; the rest arrive in the background."""
    slides = []
    for i, (photo, _) in enumerate(HERO_SLIDES):
        srcset = ", ".join(f"{unsplash(photo, w)} {w}w" for w in (800, 1400, 2000))
        prio = 'fetchpriority="high"' if i == 0 else 'fetchpriority="low"'
        slides.append(f'<img class="hero-slide" src="{unsplash(photo, 1400)}" srcset="{srcset}" sizes="100vw" '
                      f'width="1400" height="933" alt="" {prio} decoding="async" style="animation-delay:{i * 6}s" />')
    return '<div class="hero-bg" aria-hidden="true">' + "".join(slides) + "</div>"


# ─────────────────────────────────────────────────────────────────────────────
# Pages
# ─────────────────────────────────────────────────────────────────────────────
def build_home():
    check = icon("check", 18)
    ticker = "".join(f"<span>{escape(p)}</span>" for p in PROGRAMMES * 2)
    pills = "".join(f'<span class="pill">{escape(p)}</span>' for p in PROGRAMMES)

    def small_card(s):
        return (f'<a class="bento-card reveal" href="services.html#{s["id"]}"><span class="ic">{icon(SERVICE_ICONS[s["id"]])}</span>'
                f'<h3>{escape(s["name"])}</h3><p>{escape(s["short"])}</p><span class="link-arrow">Learn more</span></a>')

    feat = SERVICES[0]
    bento = (
        f'<a class="bento-card feature reveal" href="services.html#{feat["id"]}"><div class="feature-img">'
        f'{img(feat["photo"], feat["alt"], (4, 3), 900, sizes="(max-width: 600px) 100vw, 50vw")}</div>'
        f'<div class="feature-body"><span class="ic">{icon("pen")}</span>'
        f'<h3>{escape(feat["name"])}</h3><p>{escape(feat["short"])}</p><span class="link-arrow">Learn more</span></div></a>'
        + "".join(small_card(s) for s in SERVICES[1:])
        + f'<a class="bento-card bento-ask reveal" href="{wa("Hi " + B + ", I am not sure which service I need. Can you help?")}" target="_blank" rel="noopener">'
          f'<span class="ic">{icon("chat")}</span>'
          f'<h3>Not sure what you need?</h3><p>Send the question paper and we will tell you which service fits — free.</p>'
          f'<span class="link-arrow">Ask on WhatsApp</span></a>'
    )

    steps = [
        ("Send the brief", "Share the question, rubric, word count, deadline and referencing style. A photo of the handout is fine."),
        ("Free quote in 30 min", "One fixed price and a delivery date and time — never a range. If we cannot make it, we say so."),
        ("Confirm the order", "Approve the price and delivery time on WhatsApp and your file is booked into the schedule."),
        ("A matched writer starts", "Your work goes to a graduate of that faculty, not whoever is free. Long projects get progress notes."),
        ("Delivery with proof", "The document, the similarity report and the AI-detection report arrive together, on the agreed date."),
        ("Revise until it fits", "Free revisions for seven days against the original brief — including changes your lecturer asks for."),
    ]
    flow = "\n      ".join(f"<li><h3>{t}</h3><p>{b}</p></li>" for t, b in steps)

    facts = [
        ("Service", "Study consulting &amp; academic writing support"),
        ("Founded", str(C["founded"])),
        ("Based in", f"{C['country']} — online, island-wide"),
        ("Writers", "Sri Lankan government university graduates only"),
        ("Included free", "Turnitin report, AI-detection report, 7 days of revisions"),
        ("Quote time", "30 minutes, free, no obligation"),
        ("Languages", "English and Sinhala"),
        ("Contact", f'<a href="{wa()}" target="_blank" rel="noopener">WhatsApp {C["phone_display"]}</a>'
                    + (f' · <a href="mailto:{C["email"]}">{C["email"]}</a>' if C["email"] else "")),
    ]
    facts_html = "\n      ".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)
    contact_sentence = f"WhatsApp at {C['phone_display']}" + (f" and by email at {C['email']}" if C["email"] else "")

    reviews_html = ""
    if REVIEWS:
        cards = "".join(
            f'<figure class="review"{" aria-hidden=" + chr(34) + "true" + chr(34) if dup else ""}><span class="stars" aria-label="5 out of 5">★★★★★</span>'
            f'<blockquote>{escape(q)}</blockquote><figcaption>{escape(w)}</figcaption></figure>'
            for dup in (False, True) for q, w in REVIEWS
        )
        reviews_html = f"""
<section id="reviews" class="section section-alt" style="overflow:hidden">
  <div class="wrap center head">
    {kicker("Student feedback")}
    <h2 class="title">What students say after they submit.</h2>
    <p class="lede">Shared with names and universities removed, as our confidentiality rule requires.</p>
  </div>
  <div class="reviews-strip"><div class="reviews-track">{cards}</div></div>
</section>
"""

    main = f"""
<section class="hero hero-home">
  {hero_slides()}
  <div class="wrap center">
    {kicker(f"Study consulting · {C['country']} · Since {C['founded']}")}
    <h1 class="display">Your trusted partner in <span class="gold-text">academic excellence</span></h1>
    <p class="lede">Assignments, theses, research, articles and presentations — prepared by graduates of Sri Lankan government universities, delivered on the date we agree, with a free Turnitin and AI report in the same folder.</p>
    <div class="btn-row">
      <a href="{wa()}" target="_blank" rel="noopener" class="btn btn-gold">{WA_SVG} Get a free quote on WhatsApp</a>
      <a href="order.html" class="btn btn-ghost">Send your brief</a>
    </div>
    <div class="trust"><span>{check}Quote in 30 minutes</span><span>{check}Free similarity &amp; AI report</span><span>{check}24/7 WhatsApp desk</span><span>{check}Below 10% plagiarism &amp; AI</span></div>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}</div></div>

<section class="section" aria-label="What we guarantee">
  <div class="wrap">
    <div class="stats">
      <div class="stat reveal"><p class="stat-num gold-text">100%</p><p class="stat-label">On-time delivery, fixed in your quote</p></div>
      <div class="stat reveal"><p class="stat-num gold-text">&lt;10%</p><p class="stat-label">Plagiarism and AI-generated text</p></div>
      <div class="stat reveal"><p class="stat-num gold-text">Free</p><p class="stat-label">Turnitin and AI-detection report</p></div>
      <div class="stat reveal"><p class="stat-num gold-text">24/7</p><p class="stat-label">WhatsApp desk, every day of the year</p></div>
    </div>
  </div>
</section>

<section id="about" class="section" style="padding-top:0">
  <div class="wrap two-col">
    <div class="photo-wrap reveal">
      <div class="badge-since"><div><small>Since</small><b>{C['founded']}</b></div></div>
      <div class="photo">{img("1531482615713-2afd69097998", "Two students reviewing coursework together on laptops", (5, 4), 1000)}</div>
    </div>
    <div>
      {kicker("Who we are")}
      <h2 class="title">A focused desk, run by graduates who sat the same exams.</h2>
      <p class="lede" style="font-size:18px">{B} started because students were stuck between two bad options: cheap work that fails the similarity check, and careful work that arrives late. We refuse both.</p>
      <ul class="ticks">
        <li>Every brief is read by a coordinator before it is quoted</li>
        <li>Matched to a writer from the right faculty — never whoever is free</li>
        <li>Returned with the similarity and AI-detection reports attached</li>
        <li>Model answers, structure and methodology guidance you can learn from</li>
      </ul>
      <div class="pills">{pills}</div>
      <div style="margin-top:30px"><a class="link-arrow" href="about.html">More about {B}</a></div>
    </div>
  </div>
</section>

<section id="services" class="section section-alt">
  <div class="wrap">
    <div class="head-row">
      <div>
        {kicker("Services")}
        <h2 class="title">Eight kinds of academic work.<br /><span class="gold-text">One standard.</span></h2>
      </div>
      <a href="services.html" class="btn btn-ghost">See what each one includes</a>
    </div>
    <div class="bento">
      {bento}
    </div>
  </div>
</section>

<section id="process" class="section">
  <div class="wrap">
    <div class="center head">
      {kicker("How it works")}
      <h2 class="title">Six steps. Only two of them are yours.</h2>
    </div>
    <ol class="flow reveal">
      {flow}
    </ol>
  </div>
</section>

<section id="why" class="section section-alt">
  <div class="wrap">
    <div class="center head">
      {kicker(f"Why {B}")}
      <h2 class="title">Four promises, with proof for each one.</h2>
    </div>
    <div class="cards">
      {promise_cards()}
    </div>
  </div>
</section>

<section id="team" class="section">
  <div class="wrap two-col">
    <div>
      {kicker("Our writers")}
      <h2 class="title">Every writer is a government-university graduate.</h2>
      <p class="text" style="margin-top:22px">No anonymous freelancers. Each member of our panel graduated from a state university in {C['country']} and writes only inside their own faculty — management, finance, IT, engineering, nursing, education and law.</p>
      <p class="text">We publish the faculties rather than the names. The confidentiality we give you, we give them too.</p>
      <div style="margin-top:28px"><a href="about.html#team" class="btn btn-ghost">Meet the panel</a></div>
    </div>
    <div class="photo reveal">{img("1606761568499-6d2451b23c66", "A university lecture theatre", (5, 4), 1000)}</div>
  </div>
</section>

<section id="history" class="section section-alt">
  <div class="wrap two-col top">
    <div>
      {kicker("Our story so far")}
      <h2 class="title">Small beginnings, one promise kept.</h2>
      <p class="text" style="margin-top:22px">From a single WhatsApp line to an island-wide desk — the way we work has grown, but the promise has not changed: the right writer, the agreed date, and the proof attached.</p>
    </div>
    <div class="history">
      {history_html()}
    </div>
  </div>
</section>

<section id="what-is-artspark" class="section">
  <div class="wrap two-col top">
    <div>
      {kicker(f"What is {B}?")}
      <h2 class="title-sm">{B} is a Sri Lankan study-consulting service for university and professional students.</h2>
      <p class="text" style="margin-top:22px">Founded in {C['founded']}, {B} works with students across {C['country']} and with Sri Lankan students studying abroad. It provides assignment writing, thesis and dissertation support, research and data analysis, journal articles, case studies, presentations, academic coaching, and editing and proofreading — for MBA, MSc, BSc, BA, HND, SLIM, CIM, PQHRM, NVQ, diploma and PhD level work.</p>
      <p class="text">Every writer is a graduate of a Sri Lankan government university. Every delivery includes a Turnitin similarity report and an AI-detection report at no extra charge, work is quoted with a fixed price and delivery time, and revisions are free for seven days. Orders and quotes are handled on {contact_sentence}.</p>
    </div>
    <dl class="facts reveal">
      {facts_html}
    </dl>
  </div>
</section>

<section id="coverage" class="section section-alt">
  <div class="wrap">
    <div class="center head">
      {kicker("Who we work with")}
      <h2 class="title">Every programme. Every district. One desk.</h2>
    </div>
    <div class="cover">
      <div class="card reveal"><h3>Programmes</h3><p>MBA, MSc, MA, MPhil, PhD, BSc, BA, BBA, BCom, BEd, HND, HNC, SLIM, CIM, PQHRM, CMA, CIMA, AAT, NVQ, ICT diplomas and professional certificates.</p></div>
      <div class="card reveal"><h3>Subjects</h3><p>Management, HRM, marketing, finance, accounting, economics, banking, IT, software engineering, civil and mechanical engineering, nursing, public health, education, psychology, sociology, law, agriculture, tourism, statistics and project management.</p></div>
      <div class="card reveal"><h3>Districts</h3><p>{DISTRICTS} — plus Sri Lankan students in the UK, Australia, Canada and the Gulf.</p></div>
      <div class="card reveal"><h3>Referencing</h3><p>Harvard, APA 7, IEEE, OSCOLA, MLA, Chicago, Vancouver and any house style your university publishes.</p></div>
    </div>
  </div>
</section>

<section id="faq" class="section">
  <div class="wrap two-col top">
    <div>
      {kicker("Questions")}
      <h2 class="title">What students ask before they order.</h2>
      <p class="text" style="margin-top:22px">Straight answers on price, timing and privacy. Anything else — ask us on WhatsApp and a real person replies.</p>
      <div style="margin-top:28px"><a href="order.html#faq" class="link-arrow">Read all questions</a></div>
    </div>
    <div class="faq">
      {faq_items([FAQS[1], FAQS[2], FAQS[3], FAQS[6]], open_first=True)}
    </div>
  </div>
</section>
{reviews_html}
{cta()}"""
    return page(
        "index.html", "index.html",
        f"Assignment Writers in Sri Lanka | {B} — Your Trusted Academic Partner",
        f"{B} is a Sri Lankan study-consulting desk: assignments, theses, research, articles, case studies and presentations by government-university graduates. Fixed price, on-time delivery, free Turnitin and AI report. Free quote in 30 minutes on WhatsApp.",
        main,
    )


def build_services():
    chips = "".join(f'<a href="#{s["id"]}">{escape(s["name"])}</a>' for s in SERVICES)
    blocks = []
    for i, s in enumerate(SERVICES):
        inc = "".join(f"<li>{escape(x)}</li>" for x in s["includes"])
        paras = "".join(f'<p class="text"{" style=" + chr(34) + "margin-top:20px" + chr(34) if j == 0 else ""}>{escape(p)}</p>' for j, p in enumerate(s["body"]))
        blocks.append(f"""
  <section id="{s['id']}" class="svc">
    <div class="two-col">
      <div class="photo reveal">{img(s['photo'], s['alt'], (5, 4), 1000, eager=(i == 0))}</div>
      <div>
        <p class="svc-no">{i + 1:02d} / {len(SERVICES):02d}</p>
        <h2 class="title-sm">{escape(s['name'])}</h2>
        {paras}
        <ul class="ticks">{inc}</ul>
        <p class="meta"><strong>Suitable for:</strong> {escape(s['levels'])}</p>
        <div class="btn-row" style="margin-top:26px">
          <a href="{wa(f"Hi {B}, I'd like a quote for {s['name'].lower()}.")}" target="_blank" rel="noopener" class="btn btn-gold">Get a quote for this</a>
          <a href="order.html?service={quote(s['name'])}#form" class="btn btn-ghost">Use the order form</a>
        </div>
      </div>
    </div>
  </section>""")
    service_schema = {
        "@type": "ItemList", "name": f"{B} academic services",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "item": {"@type": "Service", "@id": f"{URL}/services.html#{s['id']}", "name": s["name"],
                      "description": s["short"], "serviceType": s["name"],
                      "provider": {"@id": f"{URL}/#organization"},
                      "areaServed": {"@type": "Country", "name": C["country"]}}}
            for i, s in enumerate(SERVICES)
        ],
    }
    main = page_hero(
        "Services", "Services",
        'Eight kinds of academic work, <span class="gold-text">one standard.</span>',
        "Every service comes with a fixed quote, a fixed delivery date, a Turnitin similarity report, an AI-detection report and seven days of free revisions.",
        f'\n    <div class="chips">{chips}</div>',
    ) + f"""
<div class="wrap">{''.join(blocks)}
</div>

<section class="section section-alt">
  <div class="wrap">
    <div class="center head">
      {kicker("Every order includes")}
      <h2 class="title">The same four promises, whatever you order.</h2>
    </div>
    <div class="cards">
      {promise_cards()}
    </div>
  </div>
</section>
{cta("Not sure which service fits? Send the brief and we'll advise.")}"""
    return page(
        "services.html", "services.html",
        f"Services — Assignment, Thesis, Research & PPT Help in Sri Lanka | {B}",
        f"Eight academic services from {B} Sri Lanka: assignment writing, thesis and dissertation support, research and SPSS analysis, journal articles, presentations, case studies, academic coaching, and editing and proofreading. Free Turnitin and AI report with every delivery.",
        main,
        extra_schema=[service_schema, breadcrumbs([("", "Home"), ("services.html", "Services")])],
    )


def build_about():
    values = [
        ("spark", "Art", "The craft of academic work: a clear argument, sound evidence, correct referencing and writing that reads well."),
        ("chat", "Spark", "The moment a topic finally clicks. We explain our choices and coach you for the viva, so the understanding is yours."),
        ("cap", "The cap", "The graduation cap in our logo is the goal behind every order — not just a submitted assignment, a finished degree."),
    ]
    values_html = "\n      ".join(
        f'<div class="card reveal"><div class="ic">{icon(i)}</div><h3>{t}</h3><p>{b}</p></div>' for i, t, b in values
    )
    faculties = ["Management", "Finance &amp; accounting", "Marketing &amp; HRM", "IT &amp; software", "Engineering",
                 "Nursing &amp; health", "Education", "Law"]
    fac_html = "".join(f'<span class="pill">{f}</span>' for f in faculties)
    main = page_hero(
        "About", f"About {B}",
        f'Founded in {C["founded"]} by graduates, for students who <span class="gold-text">cannot afford to be late.</span>',
        f"{B} is a study-consulting desk staffed only by graduates of Sri Lankan government universities. Fixed delivery times, free similarity and AI reports, and complete confidentiality — on every order.",
    ) + f"""
<section class="section">
  <div class="wrap two-col">
    <div class="photo-wrap reveal">
      <div class="badge-since"><div><small>Since</small><b>{C['founded']}</b></div></div>
      <div class="photo">{img("1456513080510-7bf3a84b82f8", "Open academic books on a library desk", (5, 4), 1000, eager=True)}</div>
    </div>
    <div>
      {kicker("Why we started")}
      <h2 class="title">The market had two failures. We had lived through both as students.</h2>
      <p class="text" style="margin-top:22px">Cheap work that failed the similarity check, or careful work that arrived the day after the deadline. Either way the student lost a grade — sometimes a whole module.</p>
      <p class="text">{B} was built to fix both at once. Every delivery date is fixed in writing, every file is read by a second person, and every order comes with the similarity and AI-detection reports, so quality can be checked rather than promised.</p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="center head">
      {kicker("Behind the name")}
      <h2 class="title">Art, spark — and a graduation cap.</h2>
    </div>
    <div class="cards">
      {values_html}
    </div>
  </div>
</section>

<section id="team" class="section">
  <div class="wrap two-col">
    <div>
      {kicker("The panel")}
      <h2 class="title">Every writer is a graduate of a Sri Lankan government university.</h2>
      <p class="text" style="margin-top:22px">Writers join the panel for the faculty they studied in, and they write only inside it. Each order is matched on subject and level, a coordinator stays with it from quote to delivery, and an editor reads everything before it leaves us.</p>
      <p class="text">We publish the faculties rather than the names — the same confidentiality we give you, we give them.</p>
      <div class="pills">{fac_html}</div>
    </div>
    <div class="photo reveal">{img("1531482615713-2afd69097998", "Two writers reviewing work together on laptops", (5, 4), 1000)}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap two-col top">
    <div>
      {kicker("Our story so far")}
      <h2 class="title">From one WhatsApp line to an island-wide desk.</h2>
    </div>
    <div class="history">
      {history_html()}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center head">
      {kicker("How we work")}
      <h2 class="title">Four rules we do not bend.</h2>
    </div>
    <div class="cards">
      {promise_cards()}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap two-col top">
    <div>
      {kicker("Consulting, not shortcuts")}
      <h2 class="title-sm">We want you to understand the work — not just receive it.</h2>
    </div>
    <div>
      <p class="text">Our material is built to learn from: a clear structure, sources you can follow up, explained analysis, and coaching for the parts you must present or defend yourself. Ask why a framework was chosen or what a regression result means, and you will get a real answer.</p>
      <p class="text">We encourage every student to use our work in line with their university's academic-integrity policy. Read our full position in our <a href="privacy.html#integrity">privacy &amp; terms</a>.</p>
    </div>
  </div>
</section>
{cta()}"""
    return page(
        "about.html", "about.html",
        f"About {B} — Sri Lankan Academic Writers, Founded {C['founded']}",
        f"{B} was founded in {C['founded']} as a study-consulting desk staffed only by graduates of Sri Lankan government universities. Fixed delivery times, free similarity and AI reports, complete confidentiality.",
        main, page_type="AboutPage",
        extra_schema=[breadcrumbs([("", "Home"), ("about.html", "About")])],
    )


def build_order():
    def options(xs):
        return "".join(f"<option>{escape(x)}</option>" for x in xs)
    services = [s["name"] for s in SERVICES]
    levels = ["MBA", "MSc / MA", "BSc / BA / BBA", "HND / HNC", "SLIM / CIM", "PQHRM", "CIMA / AAT", "NVQ / Diploma", "MPhil / PhD", "Other"]
    refs = ["Harvard", "APA 7", "IEEE", "OSCOLA", "MLA", "Chicago", "Vancouver", "Not sure"]
    order_steps = [
        ("Send the brief", "Use the form below, or just photograph the question and send it on WhatsApp."),
        ("Free quote, 30 minutes", "A fixed price and a delivery date and time. Ask anything before you decide."),
        ("Confirm the order", "Approve the price and delivery time and the file is booked into the schedule."),
        ("Delivery + reports", "Document, Turnitin report and AI report together — then 7 days of free revisions."),
    ]
    flow = "\n      ".join(f"<li><h3>{t}</h3><p>{b}</p></li>" for t, b in order_steps)
    faq_schema = {
        "@type": "FAQPage", "@id": f"{URL}/order.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}}
            for q, a in FAQS
        ],
    }
    email_btn = (f'\n          <a class="btn btn-ghost" id="email-brief" href="mailto:{C["email"]}">Email it instead</a>'
                 if C["email"] else "")
    main = page_hero(
        "Make an order", "Make an order",
        'Fill it once. It arrives on our WhatsApp <span class="gold-text">already written.</span>',
        "Nothing is stored on this page and no account is needed. The form turns your brief into a WhatsApp message and opens the chat — you press send, we reply with a fixed price and a delivery time.",
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="center head">
      {kicker("How ordering works")}
      <h2 class="title">Four steps from question to delivery.</h2>
    </div>
    <ol class="flow four reveal">
      {flow}
    </ol>
  </div>
</section>

<section id="form" class="section section-alt" style="scroll-margin-top:80px">
  <div class="wrap two-col top">
    <div class="form-card">
      <h2 class="title-sm">Your brief</h2>
      <p class="text" style="margin:10px 0 28px">Only your name and the service are essential — send what you know and we will ask about the rest.</p>
      <form id="order-form" class="form" data-wa="{C['whatsapp']}" data-brand="{B}" novalidate>
        <div class="form-row">
          <div class="field"><label for="f-name">Your name <span class="req" aria-hidden="true">*</span></label><input class="input" id="f-name" name="name" type="text" autocomplete="given-name" placeholder="e.g. Nimali" required /></div>
          <div class="field"><label for="f-service">Service <span class="req" aria-hidden="true">*</span></label><select class="input" id="f-service" name="service" required>{options(services)}</select></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="f-level">Academic level</label><select class="input" id="f-level" name="level">{options(levels)}</select></div>
          <div class="field"><label for="f-subject">Subject or module</label><input class="input" id="f-subject" name="subject" type="text" placeholder="e.g. Strategic Management" /></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="f-words">Word count or pages</label><input class="input" id="f-words" name="words" type="text" placeholder="e.g. 3,000 words" /></div>
          <div class="field"><label for="f-deadline">Deadline</label><input class="input" id="f-deadline" name="deadline" type="date" /></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="f-ref">Referencing style</label><select class="input" id="f-ref" name="referencing">{options(refs)}</select></div>
          <div class="field"><label for="f-uni">University or institute</label><input class="input" id="f-uni" name="university" type="text" placeholder="Optional" /></div>
        </div>
        <div class="field"><label for="f-notes">Anything else we should know</label><textarea class="input" id="f-notes" name="notes" placeholder="Topic, rubric details, files you will send, preferred language…"></textarea></div>
        <p class="form-error" id="form-error" role="alert" hidden>Please add your name so we know who to reply to.</p>
        <div class="btn-row">
          <button class="btn btn-gold" type="submit">{WA_SVG} Send this brief on WhatsApp</button>{email_btn}
        </div>
        <p class="form-note">Attach the question paper, rubric or files in the chat once it opens. Nothing you type here is stored on this website.</p>
      </form>
    </div>
    <aside class="preview" aria-label="Message preview">
      <p class="preview-head">{WA_SVG} Message preview</p>
      <div class="bubble" id="order-preview" aria-live="polite"></div>
      <p class="form-note" style="margin-top:14px">Sent to {C['phone_display']}</p>
    </aside>
  </div>
</section>

<section id="faq" class="section" style="scroll-margin-top:80px">
  <div class="wrap two-col top">
    <div>
      {kicker("Frequently asked questions")}
      <h2 class="title">The price in the quote is the price.</h2>
      <p class="text" style="margin-top:22px">Everything students usually ask before ordering. Still unsure? <a href="{wa()}" target="_blank" rel="noopener">Ask us on WhatsApp</a>.</p>
    </div>
    <div class="faq">
      {faq_items(FAQS, open_first=True)}
    </div>
  </div>
</section>
{cta()}"""
    return page(
        "order.html", "order.html",
        f"Make an Order — Free Assignment Quote in 30 Minutes | {B} Sri Lanka",
        f"Send your brief to {B} and get a free fixed-price quote within 30 minutes on WhatsApp {C['phone_display']}. Assignment, thesis, research, PPT and proofreading orders for Sri Lankan students. FAQ on pricing, deadlines and revisions.",
        main,
        extra_schema=[faq_schema, breadcrumbs([("", "Home"), ("order.html", "Make an order")])],
    )


def build_privacy():
    email = f' or email <a href="mailto:{C["email"]}">{C["email"]}</a>' if C["email"] else ""
    main = page_hero(
        "Privacy &amp; terms", "Policies",
        "Privacy, terms and academic integrity.",
        f"How {B} handles your information, the terms every order follows, and how we expect our material to be used. Last updated {date.today().strftime('%d %B %Y')}.",
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2 id="privacy">1. Your privacy</h2>
      <p>We collect only what we need to quote and complete your order: your name, your contact number and the documents and details you send about the work. This website does not store anything you type into the order form — the form simply opens WhatsApp with a pre-written message.</p>
      <p>Your information is used only to communicate with you and complete your order. We never sell it, never share your identity with writers, and never publish your name, university or work. You can ask us to delete your files and conversation history at any time after delivery.</p>
      <p>This website loads fonts from Google Fonts and images from Unsplash, which receive standard technical data such as your IP address when the page loads. We do not use advertising trackers.</p>

      <h2 id="terms">2. Terms of service</h2>
      <ul>
        <li>Every order begins with a quote stating the price and the delivery date and time. Work begins only after you accept it.</li>
        <li>Revisions against the original brief are free for seven days after delivery. Changes outside the original brief are quoted separately.</li>
        <li>Each delivery includes a Turnitin similarity report and an AI-detection report.</li>
        <li>If we cannot meet a requested deadline we tell you before you pay.</li>
        <li>Large projects may be split into staged payments tied to delivery milestones, agreed in advance.</li>
      </ul>

      <h2 id="integrity">3. Academic integrity</h2>
      <p>{B} is a study-consulting service. We provide model answers, structured drafts, reference material, data analysis, editing and one-to-one coaching to help students understand their subject and complete their own work.</p>
      <p>Students are responsible for how they use our material and for following the rules of their university or institute. We encourage you to use our work as a guide and learning resource, to cite sources properly, and to make sure your final submission reflects your own understanding.</p>

      <h2 id="contact">4. Contact</h2>
      <p>Questions about this policy or your data: WhatsApp <a href="{wa()}" target="_blank" rel="noopener">{C['phone_display']}</a>{email}.</p>
    </div>
  </div>
</section>
"""
    return page(
        "privacy.html", "",
        f"Privacy, Terms & Academic Integrity | {B}",
        f"How {B} protects your privacy, the terms that apply to every order, and our academic-integrity policy.",
        main, extra_schema=[breadcrumbs([("", "Home"), ("privacy.html", "Privacy & terms")])],
    )


def build_404():
    main = f"""
<section class="hero">
  <div class="wrap center">
    {kicker("Error 404")}
    <h1 class="display" style="font-size:clamp(40px,6vw,76px)">This page was <span class="gold-text">handed in elsewhere.</span></h1>
    <p class="lede">The link may be old or mistyped. Try one of these instead — or message us and we will point you the right way.</p>
    <div class="btn-row" style="margin-top:34px">
      <a href="/" class="btn btn-gold">Back to home</a>
      <a href="services.html" class="btn btn-ghost">Our services</a>
      <a href="order.html" class="btn btn-ghost">Make an order</a>
    </div>
  </div>
</section>
"""
    # The 404 page is served from any path, so every link must resolve from the root.
    html = head("404.html", f"Page not found | {B}", "The page you were looking for could not be found.", robots="noindex, follow") \
        + header("") + f'<main id="main">\n{main}</main>\n' + footer()
    for a, b in [('href="index.html"', 'href="/"'), ('href="assets/', 'href="/assets/'), ('src="assets/', 'src="/assets/'),
                 ('href="styles.css"', 'href="/styles.css"'), ('src="site.js"', 'src="/site.js"'),
                 ('href="site.webmanifest"', 'href="/site.webmanifest"')] + \
                [(f'href="{p}', f'href="/{p}') for p in ("services.html", "about.html", "order.html", "privacy.html")]:
        html = html.replace(a, b)
    (OUT / "404.html").write_text(html, encoding="utf-8")
    return "404.html"


def build_meta(pages):
    priority = {"index.html": "1.0", "services.html": "0.9", "order.html": "0.9", "about.html": "0.8", "privacy.html": "0.3"}
    urls = "".join(
        f"""  <url>
    <loc>{URL}/{'' if p == 'index.html' else p}</loc>
    <lastmod>{TODAY}</lastmod>
    <priority>{priority[p]}</priority>
  </url>
""" for p in pages if p in priority)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"""User-agent: *
Allow: /
Disallow: /404.html

# Search and answer engines are welcome
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {URL}/sitemap.xml
""", encoding="utf-8")
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": B, "short_name": B, "description": C["tagline"],
        "start_url": "/", "display": "standalone", "background_color": "#0a0a0a", "theme_color": "#0a0a0a",
        "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
    }, indent=2), encoding="utf-8")
    svc_lines = "\n".join(f"- [{s['name']}]({URL}/services.html#{s['id']}): {s['short']}" for s in SERVICES)
    email = f" or by email ({C['email']})" if C["email"] else ""
    (OUT / "llms.txt").write_text(f"""# {B}

> {B} — "{C['tagline']}" — is a Sri Lankan study-consulting and academic writing-support service founded in {C['founded']}, for university and professional students in {C['country']} and Sri Lankan students abroad.

Every writer is a graduate of a Sri Lankan government university and works only within their own faculty. Every order receives a fixed price and delivery time before payment, a free Turnitin similarity report and AI-detection report (plagiarism and AI text kept below 10%), and seven days of free revisions. Free quotes are given within 30 minutes on WhatsApp ({C['phone_display']}){email}, 24 hours a day, in English and Sinhala.

## Services
{svc_lines}

## Pages
- [Home]({URL}/): Overview, guarantees, process, writer panel and coverage
- [Services]({URL}/services.html): What each service includes
- [About]({URL}/about.html): History, writer panel and working rules
- [Make an order / FAQ]({URL}/order.html): Order form and frequently asked questions
- [Privacy & terms]({URL}/privacy.html): Privacy, terms and academic-integrity policy
""", encoding="utf-8")


if __name__ == "__main__":
    built = [build_home(), build_services(), build_about(), build_order(), build_privacy(), build_404()]
    build_meta(built)
    print("built:", ", ".join(built))
    if not C["email"]:
        print("note: no email set in CONFIG — email is hidden on every page.")
