"""Generate AI Recruiter Agent Swarm pitch deck .pptx"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Widescreen 16:9
W = Inches(13.333)
H = Inches(7.5)

prs = Presentation()
prs.slide_width = W
prs.slide_height = H

# Colors
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x1E, 0x29, 0x3B)
MUTED = RGBColor(0x64, 0x74, 0x8B)
LIGHT = RGBColor(0x94, 0xA3, 0xB8)
ACCENT = RGBColor(0x4F, 0x46, 0xE5)
GREEN = RGBColor(0x16, 0xA3, 0x4A)
BG = RGBColor(0xFA, 0xFA, 0xFA)
BORDER = RGBColor(0xE2, 0xE8, 0xF0)
AMBER = RGBColor(0xD9, 0x77, 0x06)
PINK = RGBColor(0xDB, 0x27, 0x77)
RED = RGBColor(0xDC, 0x26, 0x26)

M = Inches(0.7)  # margin

def new_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = WHITE
    return slide

def box(slide, l, t, w, h, fill=None, border=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.line.fill.background()
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if border:
        s.line.fill.solid()
        s.line.color.rgb = border
        s.line.width = Pt(1)
    return s

def add_text(slide, l, t, w, h, text, size=14, bold=False, color=DARK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tb.text_frame.word_wrap = True
    p = tb.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = 'Calibri'
    p.alignment = align
    return tb

def add_para(tf, text, size=14, bold=False, color=DARK, align=PP_ALIGN.LEFT, space=0):
    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = 'Calibri'
    p.alignment = align
    if space:
        p.space_before = Pt(space)
    return p

def tag_bar(slide, x, y, label, color=ACCENT):
    bg_c = RGBColor(0xEE, 0xF2, 0xFF) if color == ACCENT else RGBColor(0xF0, 0xFD, 0xF4)
    box(slide, x, y, Inches(1.6), Inches(0.32), fill=bg_c)
    add_text(slide, x + Inches(0.1), y + Inches(0.04), Inches(1.4), Inches(0.28), label, 10, True, color)

# ============================================================
# SLIDE 1: Title
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'AI SYSTEMS ARCHITECT', ACCENT)
tag_bar(s, M + Inches(1.8), Inches(0.5), 'INDIA RUNS 2026', GREEN)

add_text(s, M, Inches(1.5), Inches(8), Inches(1.2), 'AI Recruiter', 44, True, DARK)

tb = s.shapes.add_textbox(M, Inches(2.5), Inches(8), Inches(1.2))
tb.text_frame.word_wrap = True
p = tb.text_frame.paragraphs[0]
p.text = 'Agent Swarm'
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = ACCENT
p.font.name = 'Calibri'

add_text(s, M, Inches(3.8), Inches(8), Inches(0.5), 'Autonomous multi-agent hiring for the next India', 20, False, MUTED)

add_text(s, M, Inches(5.8), Inches(4), Inches(0.3), 'peter14l', 14, True, DARK)
add_text(s, M, Inches(6.1), Inches(4), Inches(0.3), 'India Runs by Redrob AI', 12, False, LIGHT)

add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '1/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 2: Problem
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'THE PROBLEM', ACCENT)

add_text(s, M, Inches(1.2), Inches(8), Inches(0.6), "India's hiring is broken at scale", 30, True, DARK)

cards = [
    ('500+', 'Applications per role', "95% irrelevant — recruiters drown in noise", ACCENT),
    ('60%', 'Time spent screening', "Not interviewing. Not hiring. Just filtering.", ACCENT),
    ('Hidden', 'Non-obvious talent', "Tier 2/3, non-IIT, non-English candidates get missed", GREEN),
]
for i, (num, label, desc, clr) in enumerate(cards):
    x = M + i * Inches(4.0)
    box(s, x, Inches(2.0), Inches(3.7), Inches(2.0), fill=BG, border=BORDER)
    add_text(s, x + Inches(0.2), Inches(2.1), Inches(3.3), Inches(0.5), num, 30, True, clr)
    add_text(s, x + Inches(0.2), Inches(2.55), Inches(3.3), Inches(0.3), label, 11, True, LIGHT)
    add_text(s, x + Inches(0.2), Inches(2.95), Inches(3.3), Inches(0.7), desc, 13, False, MUTED)

# Warning box
y = Inches(4.3)
box(s, M, y, Inches(11.5), Inches(1.0), fill=BG, border=RGBColor(0xFE, 0xCA, 0xCA))
add_text(s, M + Inches(0.25), y + Inches(0.1), Inches(11), Inches(0.3), 'Current AI tools are black boxes', 14, True, RED)
add_text(s, M + Inches(0.25), y + Inches(0.45), Inches(11), Inches(0.4), 'They reject without explanation. No transparency, no trust, no feedback loop. Keyword filters miss transferable skills entirely.', 12, False, MUTED)

add_text(s, M, Inches(5.6), Inches(8), Inches(0.3), "India's recruitment market: $2B+ and growing 15% YoY — core tech hasn't changed in a decade.", 11, False, LIGHT)
add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '2/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 3: Why Now
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'WHY NOW', GREEN)

add_text(s, M, Inches(1.2), Inches(8), Inches(0.6), 'Three forces make this possible today', 30, True, DARK)

forces = [
    ('AI Maturity', "LLMs reason, plan, and use tools. Multi-agent frameworks are production-ready (CrewAI, AutoGen). Voice AI in Indian languages works (Sarvam, Bhashini)."),
    ("India's Talent Boom", "1.5M+ engineers graduate annually. Tier 2/3 cities produce world-class talent. Remote work demands location-agnostic hiring."),
    ("Redrob's Mission", "Building India's AI OS for work. AI-native hiring is the foundational layer. Built for India, in India — not a Silicon Valley port."),
]
for i, (title, desc) in enumerate(forces):
    x = M + i * Inches(4.0)
    box(s, x, Inches(2.0), Inches(3.7), Inches(2.5), fill=BG, border=BORDER)
    add_text(s, x + Inches(0.2), Inches(2.15), Inches(3.3), Inches(0.3), title, 16, True, DARK)
    add_text(s, x + Inches(0.2), Inches(2.6), Inches(3.3), Inches(1.5), desc, 13, False, MUTED)

box(s, M, Inches(4.8), Inches(11.5), Inches(0.55), fill=BG, border=BORDER)
add_text(s, M + Inches(0.25), Inches(4.88), Inches(11), Inches(0.4), 'This combination of AI maturity, market need, and platform timing has never existed before.', 13, True, MUTED)

add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '3/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 4: Solution
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'THE SOLUTION', ACCENT)

add_text(s, M, Inches(1.2), Inches(8), Inches(0.5), 'Enter the Agent Swarm', 30, True, DARK)
add_text(s, M, Inches(1.7), Inches(8), Inches(0.3), '5 specialized AI agents + 1 Orchestrator. From JD to shortlist in under 10 minutes.', 14, False, MUTED)

agents = [
    ('Orchestrator', 'Brain', 'Routes tasks, manages state, escalates to humans', ACCENT),
    ('Sourcer', 'Scout', 'Searches LinkedIn, GitHub, Naukri, internal DBs', GREEN),
    ('Matcher', 'Judge', 'Semantic ranking, transferable skill detection', AMBER),
    ('Screener', 'Interviewer', 'Voice calls in Hinglish, dynamic questioning', PINK),
    ('Scheduler', 'Coordinator', 'Calendar sync, negotiation, reminders', RGBColor(0x08, 0x91, 0xB2)),
]

x0, y0 = M, Inches(2.2)
hdr_h = Inches(0.35)
row_h = Inches(0.42)
col_w = [Inches(1.8), Inches(0.9), Inches(7.2)]

# Table header
box(s, x0, y0, col_w[0]+col_w[1]+col_w[2], hdr_h, fill=BG, border=BORDER)
add_text(s, x0 + Inches(0.15), y0 + Inches(0.05), col_w[0], hdr_h, 'Agent', 10, True, LIGHT)
add_text(s, x0 + col_w[0] + Inches(0.15), y0 + Inches(0.05), col_w[1], hdr_h, 'Role', 10, True, LIGHT)
add_text(s, x0 + col_w[0] + col_w[1] + Inches(0.15), y0 + Inches(0.05), col_w[2], hdr_h, 'Responsibility', 10, True, LIGHT)

for i, (name, role, desc, clr) in enumerate(agents):
    y = y0 + hdr_h + i * row_h
    box(s, x0, y, col_w[0]+col_w[1]+col_w[2], row_h, border=BORDER)
    add_text(s, x0 + Inches(0.15), y + Inches(0.07), col_w[0], row_h, name, 13, True, clr)
    add_text(s, x0 + col_w[0] + Inches(0.15), y + Inches(0.07), col_w[1], row_h, role, 12, False, MUTED)
    add_text(s, x0 + col_w[0] + col_w[1] + Inches(0.15), y + Inches(0.07), col_w[2], row_h, desc, 12, False, LIGHT)

add_text(s, M, Inches(5.8), Inches(8), Inches(0.3), 'Every decision explained. Every candidate gets a fair shot. No black boxes.', 12, True, ACCENT)
add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '4/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 5: How It Works
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'HOW IT WORKS', ACCENT)
add_text(s, M, Inches(1.2), Inches(8), Inches(0.5), 'From JD to shortlist in under 10 minutes', 30, True, DARK)

steps = [
    ('1', 'JD Submitted', 'Recruiter pastes job description. Orchestrator parses and activates the swarm.'),
    ('2', 'Multi-Source Sourcing', 'Sourcer Agent searches 4+ sources simultaneously — LinkedIn, GitHub, Naukri, internal DB.'),
    ('3', 'Semantic Matching', 'Matcher Agent scores candidates across 5 dimensions with full transparency.'),
    ('4', 'Voice Screening', 'Screener Agent conducts natural voice calls in Hinglish — adaptive, contextual, fair.'),
    ('5', 'Auto-Scheduling', 'Scheduler Agent books interviews in one click. No email tennis required.'),
    ('6', 'Human Review', 'Recruiter reviews top candidates with full scoring breakdown and call transcripts.'),
]

col_w = Inches(5.8)
for idx, (num, title, desc) in enumerate(steps):
    col = idx // 3
    row = idx % 3
    x = M + col * (col_w + Inches(0.5))
    y = Inches(2.0) + row * Inches(1.2)

    circle = s.shapes.add_shape(MSO_SHAPE.OVAL, x, y + Inches(0.05), Inches(0.35), Inches(0.35))
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
    circle.line.fill.background()

    add_text(s, x + Inches(0.07), y + Inches(0.07), Inches(0.25), Inches(0.3), num, 14, True, ACCENT, PP_ALIGN.CENTER)
    add_text(s, x + Inches(0.55), y, Inches(5.0), Inches(0.3), title, 16, True, DARK)
    add_text(s, x + Inches(0.55), y + Inches(0.35), Inches(5.0), Inches(0.5), desc, 13, False, MUTED)

add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '5/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 6: Architecture
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'ARCHITECTURE', ACCENT)
add_text(s, M, Inches(1.2), Inches(8), Inches(0.5), 'Clean, scalable multi-agent design', 30, True, DARK)

# Simplified visual: boxes and connectors
# Layer 1: Dashboard
y_l1 = Inches(1.9)
bx_w = Inches(4.0)
bx_h = Inches(0.45)
box(s, Inches(4.5), y_l1, bx_w, bx_h, fill=BG, border=BORDER)
add_text(s, Inches(4.7), y_l1 + Inches(0.06), bx_w, bx_h, 'Recruiter Dashboard', 12, True, DARK, PP_ALIGN.CENTER)

# Arrow down
add_text(s, Inches(6.3), y_l1 + bx_h, Inches(0.5), Inches(0.3), '\u25bc', 12, False, LIGHT, PP_ALIGN.CENTER)

# Layer 2: Orchestrator
y_l2 = y_l1 + bx_h + Inches(0.3)
box(s, Inches(4.0), y_l2, Inches(5.0), Inches(0.55), fill=RGBColor(0xEE, 0xF2, 0xFF), border=BORDER)
add_text(s, Inches(4.2), y_l2 + Inches(0.06), Inches(4.6), Inches(0.45), 'Orchestrator Agent  (Task Router + State + Escalation)', 12, True, ACCENT, PP_ALIGN.CENTER)

# Layer 3: Four agents
y_l3 = y_l2 + bx_h + Inches(0.4)
agent_names = ['Sourcer', 'Matcher', 'Screener', 'Scheduler']
agent_colors = [GREEN, AMBER, PINK, RGBColor(0x08, 0x91, 0xB2)]
agent_w = Inches(2.6)
gap = Inches(0.4)
total_w = 4 * agent_w + 3 * gap
start_x = (W - total_w) / 2

for i in range(4):
    x = start_x + i * (agent_w + gap)
    box(s, x, y_l3, agent_w, bx_h, fill=BG, border=BORDER)
    add_text(s, x + Inches(0.1), y_l3 + Inches(0.06), agent_w, bx_h, agent_names[i], 12, True, agent_colors[i], PP_ALIGN.CENTER)

# Connector bar below agents
y_conn = y_l3 + bx_h + Inches(0.15)
add_text(s, Inches(5.0), y_conn + Inches(0.05), Inches(3), Inches(0.2), '|         |         |         |', 10, False, LIGHT, PP_ALIGN.CENTER)
add_text(s, Inches(6.3), y_conn + Inches(0.2), Inches(0.5), Inches(0.2), '\u2514\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2518', 10, False, LIGHT, PP_ALIGN.CENTER)
add_text(s, Inches(6.3), y_conn + Inches(0.35), Inches(0.5), Inches(0.2), '\u25bc', 10, False, LIGHT, PP_ALIGN.CENTER)

# Layer 4: Memory
y_l4 = y_conn + Inches(0.7)
box(s, Inches(4.0), y_l4, Inches(5.0), Inches(0.55), fill=BG, border=BORDER)
add_text(s, Inches(4.2), y_l4 + Inches(0.06), Inches(4.6), Inches(0.45), 'Memory Layer  (Qdrant + Redis + PostgreSQL)', 12, True, MUTED, PP_ALIGN.CENTER)

# Tech stack boxes on right side
stacks = [('Framework', 'CrewAI'), ('LLM', 'Gemini 1.5 Pro'), ('Voice', 'Sarvam AI'),
          ('Vector DB', 'Qdrant'), ('Embeddings', 'BGE-M3'), ('Backend', 'FastAPI')]
for i, (label, val) in enumerate(stacks):
    x = Inches(8.8) + (i % 2) * Inches(2.2)
    y = Inches(1.9) + (i // 2) * Inches(0.95)
    box(s, x, y, Inches(2.0), Inches(0.75), fill=BG, border=BORDER)
    add_text(s, x + Inches(0.1), y + Inches(0.05), Inches(1.8), Inches(0.25), label, 11, True, DARK)
    add_text(s, x + Inches(0.1), y + Inches(0.35), Inches(1.8), Inches(0.3), val, 12, False, MUTED)

add_text(s, Inches(8.8), Inches(5.2), Inches(4), Inches(0.5), 'Each agent independently deployable. Async messaging via Redis pub/sub. Horizontal scaling.', 11, False, LIGHT)
add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '6/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 7: Key Differentiator
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'KEY DIFFERENTIATOR', GREEN)
add_text(s, M, Inches(1.2), Inches(10), Inches(0.6), "Voice screening that speaks India's language", 30, True, DARK)

# Left card
box(s, M, Inches(2.0), Inches(5.7), Inches(2.8), fill=BG, border=BORDER)
add_text(s, M + Inches(0.2), Inches(2.15), Inches(5.3), Inches(0.3), 'Traditional screening', 16, True, MUTED)
for j, line in enumerate([
    '  Text-only, English-only, rigid Q&A',
    '  Filters out great candidates lacking English fluency',
    '  Misses communication nuance and personality',
    '  Feels robotic and impersonal',
]):
    add_text(s, M + Inches(0.2), Inches(2.55 + j * 0.4), Inches(5.3), Inches(0.35), line, 13, False, MUTED)

# Right card
box(s, Inches(6.8), Inches(2.0), Inches(5.7), Inches(2.8), fill=BG, border=RGBColor(0xBB, 0xF7, 0xD0))
add_text(s, Inches(7.0), Inches(2.15), Inches(5.3), Inches(0.3), 'Our Screener Agent', 16, True, GREEN)
for j, line in enumerate([
    '  Natural conversation in Hinglish, Hindi, English',
    '  Dynamic questioning that adapts to responses',
    '  Evaluates communication, confidence, cultural fit',
    '  Removes English fluency bias from early filtering',
]):
    add_text(s, Inches(7.0), Inches(2.55 + j * 0.4), Inches(5.3), Inches(0.35), line, 13, False, MUTED)

# Bottom metrics
for i, (num, label) in enumerate([('80%', 'of Indians prefer native language'), ('+34%', 'accuracy with voice vs text-only'), ('2x', 'candidate pool from language inclusion')]):
    x = M + i * Inches(4.0)
    y = Inches(5.3)
    add_text(s, x, y, Inches(3.5), Inches(0.5), num, 28, True, GREEN)
    add_text(s, x, y + Inches(0.5), Inches(3.5), Inches(0.3), label, 11, False, LIGHT)

add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '7/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 8: Impact
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'IMPACT', ACCENT)
add_text(s, M, Inches(1.2), Inches(8), Inches(0.5), 'What this means for a hiring team', 30, True, DARK)

impacts = [
    ('Time to shortlist', '5\u20137 days', '10 minutes'),
    ('Recruiter screening time', '60% of day', '10% of day'),
    ('Candidates evaluated per role', '50\u2013100', '500+'),
    ('Candidate experience', 'Generic, English-only', 'Personalized, multilingual'),
    ('Decision transparency', 'Black box', 'Full reasoning per candidate'),
]

y = Inches(2.0)
for label, before, after in impacts:
    add_text(s, M, y, Inches(5.0), Inches(0.4), label, 14, False, DARK)
    add_text(s, Inches(5.5), y, Inches(2.0), Inches(0.4), before, 13, False, LIGHT, PP_ALIGN.RIGHT)
    add_text(s, Inches(7.6), y, Inches(0.4), Inches(0.4), '\u2192', 16, False, BORDER, PP_ALIGN.CENTER)
    add_text(s, Inches(8.2), y, Inches(3.0), Inches(0.4), after, 14, True, GREEN)
    y += Inches(0.55)

# Bottom bar with CTA
y = Inches(5.2)
box(s, M, y, Inches(11.5), Inches(0.65), fill=BG, border=BORDER)
add_text(s, M, y + Inches(0.08), Inches(11.5), Inches(0.35), '~70% reduction in cost-per-hire', 20, True, DARK, PP_ALIGN.CENTER)
add_text(s, M, y + Inches(0.38), Inches(11.5), Inches(0.2), 'for mid-to-senior roles', 11, False, LIGHT, PP_ALIGN.CENTER)

add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '8/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 9: Market
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'MARKET OPPORTUNITY', GREEN)

tb = s.shapes.add_textbox(M, Inches(1.2), Inches(10), Inches(0.6))
tb.text_frame.word_wrap = True
p = tb.text_frame.paragraphs[0]
p.text = 'Built for Redrob, relevant for '
p.font.size = Pt(30)
p.font.bold = True
p.font.color.rgb = DARK
p.font.name = 'Calibri'
p = tb.text_frame.add_paragraph()
p.text = 'everyone'
p.font.size = Pt(30)
p.font.bold = True
p.font.color.rgb = GREEN
p.font.name = 'Calibri'

gtm = [
    ('Redrob Integration', "Native AI hiring layer for India's AI OS. Directly aligns with Redrob's mission as India's AI super app for work."),
    ('Enterprise SaaS', 'Standalone product for Indian companies (200\u20135000 employees). Plugs into existing ATS systems.'),
    ('API-First', 'Embeddable agent swarm for any ATS. White-label options for recruitment agencies and platforms.'),
]
for i, (title, desc) in enumerate(gtm):
    x = M + i * Inches(4.0)
    box(s, x, Inches(2.0), Inches(3.7), Inches(2.2), fill=BG, border=BORDER)
    add_text(s, x + Inches(0.2), Inches(2.15), Inches(3.3), Inches(0.3), title, 16, True, DARK)
    add_text(s, x + Inches(0.2), Inches(2.6), Inches(3.3), Inches(1.3), desc, 13, False, MUTED)

# Bottom metrics
for i, (num, label) in enumerate([('$2B+', 'India recruitment software\nTAM by 2027'), ('500', 'Mid-size Indian companies\n\u2014 initial target')]):
    x = Inches(2.5 + i * 5.0)
    y = Inches(4.6)
    add_text(s, x, y, Inches(4), Inches(0.5), num, 28, True, [ACCENT, GREEN][i], PP_ALIGN.CENTER)
    add_text(s, x, y + Inches(0.5), Inches(4), Inches(0.4), label, 11, False, LIGHT, PP_ALIGN.CENTER)

add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '9/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 10: Roadmap
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'ROADMAP', ACCENT)
add_text(s, M, Inches(1.2), Inches(8), Inches(0.5), 'Beyond the hackathon', 30, True, DARK)

roadmap = [
    ('Q3 2026', 'PoC', 'Core swarm with synthetic data.\nOrchestrator + Matcher + mock sources.', ACCENT),
    ('Q4 2026', 'MVP', 'Live with 5 beta customers.\nLinkedIn source, 3 agents.', GREEN),
    ('Q1 2027', 'Growth', '4+ sources, all 5 agents.\nHinglish voice screening, production.', AMBER),
    ('Q2 2027', 'Scale', 'Multi-lingual voice, learning loop.\nEnterprise features, API marketplace.', PINK),
]
for i, (quarter, title, desc, clr) in enumerate(roadmap):
    x = M + i * Inches(3.1)
    box(s, x, Inches(2.0), Inches(2.85), Inches(2.8), fill=BG, border=BORDER)
    box(s, x, Inches(2.0), Inches(2.85), Inches(0.06), fill=clr)
    add_text(s, x + Inches(0.15), Inches(2.2), Inches(2.5), Inches(0.25), quarter, 11, True, clr)
    add_text(s, x + Inches(0.15), Inches(2.55), Inches(2.5), Inches(0.3), title, 16, True, DARK)
    add_text(s, x + Inches(0.15), Inches(3.0), Inches(2.5), Inches(1.2), desc, 12, False, MUTED)

add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '10/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 11: About Me
# ============================================================
s = new_slide()
tag_bar(s, M, Inches(0.5), 'ABOUT ME', GREEN)

tb = s.shapes.add_textbox(M, Inches(1.2), Inches(10), Inches(0.6))
tb.text_frame.word_wrap = True
p = tb.text_frame.paragraphs[0]
p.text = 'Builder, not just a '
p.font.size = Pt(30)
p.font.bold = True
p.font.color.rgb = DARK
p.font.name = 'Calibri'
p = tb.text_frame.add_paragraph()
p.text = 'presenter'
p.font.size = Pt(30)
p.font.bold = True
p.font.color.rgb = GREEN
p.font.name = 'Calibri'

# Profile card
box(s, M, Inches(2.0), Inches(11.5), Inches(2.0), fill=BG, border=BORDER)

# Avatar circle
circle = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.0), Inches(2.3), Inches(1.0), Inches(1.0))
circle.fill.solid()
circle.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
circle.line.fill.background()
add_text(s, Inches(1.0), Inches(2.5), Inches(1.0), Inches(0.6), 'PB', 24, True, ACCENT, PP_ALIGN.CENTER)

add_text(s, Inches(2.3), Inches(2.2), Inches(9.5), Inches(0.35), 'Class 12 graduate \u00b7 Proficient with AI tools', 16, True, DARK)
add_text(s, Inches(2.3), Inches(2.7), Inches(9.5), Inches(0.8), "I just experienced the hiring process as a candidate. I know firsthand how broken it feels on the other side. This isn't theoretical \u2014 it's personal.", 14, False, MUTED)
add_text(s, Inches(2.3), Inches(3.4), Inches(9.5), Inches(0.3), 'Building for India \u2014 where I live, study, and will work.', 14, True, ACCENT)

# Quote
box(s, Inches(2.0), Inches(4.5), Inches(8.5), Inches(0.6), fill=BG, border=BORDER)
add_text(s, Inches(2.3), Inches(4.55), Inches(8.0), Inches(0.5), '\u201cI\u2019m not here to pitch. I\u2019m here to build what next India runs on.\u201d', 16, True, DARK, PP_ALIGN.CENTER)

add_text(s, Inches(11.5), Inches(6.8), Inches(1.2), Inches(0.35), '11/12', 11, False, LIGHT, PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 12: Thank You
# ============================================================
s = new_slide()
add_text(s, Inches(1.0), Inches(2.0), Inches(10), Inches(1.0), 'Thank', 48, True, DARK, PP_ALIGN.CENTER)
add_text(s, Inches(1.0), Inches(3.0), Inches(10), Inches(1.0), 'You', 48, True, ACCENT, PP_ALIGN.CENTER)
add_text(s, Inches(1.0), Inches(4.0), Inches(10), Inches(0.5), "Let's build India's AI-native hiring layer", 20, False, MUTED, PP_ALIGN.CENTER)

add_text(s, Inches(1.0), Inches(5.0), Inches(10), Inches(0.4), 'GitHub:  github.com/peter14l/india-runs-ai-recruiter', 14, False, DARK, PP_ALIGN.CENTER)
add_text(s, Inches(1.0), Inches(5.4), Inches(10), Inches(0.3), 'Event:  India Runs by Redrob AI', 14, False, MUTED, PP_ALIGN.CENTER)
add_text(s, Inches(1.0), Inches(5.7), Inches(10), Inches(0.3), 'Track:  Challenge 1 \u2014 AI Systems Architect', 14, False, MUTED, PP_ALIGN.CENTER)

# Tag boxes
for i, (tag, clr) in enumerate([('#IndiaRuns', ACCENT), ('#RedrobAI', GREEN), ('#AIAgentSwarm', ACCENT)]):
    x = Inches(4.0 + i * 2.0)
    bg_c = RGBColor(0xEE, 0xF2, 0xFF) if i != 1 else RGBColor(0xF0, 0xFD, 0xF4)
    box(s, x, Inches(6.3), Inches(1.6), Inches(0.35), fill=bg_c)
    add_text(s, x + Inches(0.05), Inches(6.33), Inches(1.5), Inches(0.3), tag, 11, True, clr, PP_ALIGN.CENTER)

add_text(s, M, Inches(6.8), Inches(1.2), Inches(0.35), '12/12', 11, False, LIGHT)

# Save
import shutil
out = r'E:\india-runs-ai-recruiter\assets\pitch-deck.pptx'
# Remove old if exists
try:
    os.remove(out)
except:
    pass
prs.save(out)
print(f'Saved: {out}')
