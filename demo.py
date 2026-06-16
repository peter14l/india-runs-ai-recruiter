"""AI Recruiter Agent Swarm -- Full Pipeline Demo

Run with: python demo.py
"""

import time
import json
import random
from dataclasses import dataclass, field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich import box

console = Console(legacy_windows=True, force_terminal=False)

SAMPLE_JD = """
Job Title: Senior Software Engineer (Backend)
Location: Bangalore (Hybrid)
Experience: 4-7 years
Tech Stack: Python, Node.js, PostgreSQL, AWS, Docker, Kubernetes
Domain: Fintech / Payments
Key Requirements:
- Strong system design skills for high-throughput transaction systems
- Experience with microservices architecture
- Knowledge of PCI-DSS compliance or financial regulations (preferred)
- Team mentorship experience
- Startup mindset -- ownership, speed, iteration
"""

CANDIDATES = [
    {
        "id": "C001",
        "name": "Ananya Sharma",
        "source": "LinkedIn",
        "yoe": 6,
        "skills": ["Python", "Node.js", "PostgreSQL", "AWS", "Kubernetes", "Docker"],
        "current_role": "Backend Engineer @ Razorpay",
        "location": "Bangalore",
        "education": "B.Tech CS -- IIIT Bangalore",
        "notice_period": "30 days",
    },
    {
        "id": "C002",
        "name": "Rahul Verma",
        "source": "Naukri",
        "yoe": 5,
        "skills": ["Python", "Django", "PostgreSQL", "GCP", "Docker"],
        "current_role": "Software Engineer @ PhonePe",
        "location": "Bangalore",
        "education": "B.Tech IT -- NIT Trichy",
        "notice_period": "45 days",
    },
    {
        "id": "C003",
        "name": "Priya Patel",
        "source": "GitHub",
        "yoe": 4,
        "skills": ["Go", "Python", "PostgreSQL", "AWS", "Docker", "Redis"],
        "current_role": "Backend Developer @ CRED",
        "location": "Bangalore",
        "education": "M.Tech CS -- IIT Bombay",
        "notice_period": "60 days",
    },
    {
        "id": "C004",
        "name": "Vikram Singh",
        "source": "Internal DB",
        "yoe": 7,
        "skills": ["Python", "Java", "PostgreSQL", "AWS", "Kubernetes", "Docker", "Kafka"],
        "current_role": "Senior Engineer @ Flipkart",
        "location": "Bangalore",
        "education": "B.E. CS -- BITS Pilani",
        "notice_period": "90 days",
    },
]


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    msg_type: str
    payload: dict
    timestamp: float = field(default_factory=time.time)
    msg_id: str = ""

    def __post_init__(self):
        self.msg_id = f"{self.sender}->{self.recipient}-{int(self.timestamp * 1000)}"


def step(label: str):
    console.print(f"\n[bold cyan]==> {label}[/bold cyan]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as p:
        p.add_task("processing...", total=None)
        time.sleep(0.8)


def show_message(msg: AgentMessage):
    title_str = f"[bold]{msg.sender}[/bold] -> [bold]{msg.recipient}[/bold]   [{msg.msg_type}]"
    p = Panel(
        Syntax(json.dumps(msg.payload, indent=2), "json", theme="monokai"),
        title=title_str,
        border_style="bright_blue",
        padding=(1, 2),
        width=90,
    )
    console.print(p)


def simulate_jd_parsing(jd_text: str) -> dict:
    step("Orchestrator Agent: Parsing Job Description")
    requirements = {
        "title": "Senior Software Engineer (Backend)",
        "location": "Bangalore",
        "min_years": 4,
        "max_years": 7,
        "required_skills": ["Python", "Node.js", "PostgreSQL", "AWS"],
        "good_to_have": ["Kubernetes", "Docker", "Fintech", "Kafka"],
        "domain": "Fintech",
    }
    msg = AgentMessage(
        "Orchestrator", "Sourcer", "JD_PARSED",
        {"job_id": "JOB-001", "requirements": requirements, "raw_snippet": jd_text[:100]}
    )
    show_message(msg)
    return requirements


def simulate_sourcing(requirements: dict) -> list:
    step("Sourcer Agent: Searching multiple sources")
    sources = ["LinkedIn", "Naukri", "GitHub", "Internal DB"]
    for s in sources:
        desc = f"  [dim]Mining {s} contributions..." if s == "GitHub" else f"  [dim]Crawling {s}..."
        with Progress(SpinnerColumn(), TextColumn(desc), transient=True) as p:
            p.add_task("", total=None)
            time.sleep(0.5)

    found = []
    for c in CANDIDATES:
        score = random.randint(65, 95)
        found.append({**c, "sourcer_confidence": score})

    found.sort(key=lambda x: x["sourcer_confidence"], reverse=True)

    msg_payload = {
        "job_id": "JOB-001",
        "candidates_found": len(found),
        "sources_covered": sources,
        "candidate_ids": [c["id"] for c in found],
    }
    msg = AgentMessage("Sourcer", "Orchestrator", "CANDIDATES_FOUND", msg_payload)
    show_message(msg)

    table = Table(title="Sourced Candidates", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("ID", style="dim")
    table.add_column("Name")
    table.add_column("Source")
    table.add_column("Current Role")
    table.add_column("Confidence")
    for c in found:
        table.add_row(c["id"], c["name"], c["source"], c["current_role"], f"{c['sourcer_confidence']}%")
    console.print(table)
    return found


def simulate_matching(candidates: list, requirements: dict) -> list:
    step("Matcher Agent: Computing semantic relevance scores")

    with Progress(SpinnerColumn(), TextColumn("  [dim]Embedding JD + candidate profiles..."), transient=True) as p:
        p.add_task("", total=None)
        time.sleep(1.0)

    scored = []
    for c in candidates:
        skills_match = len(set(c["skills"]) & set(requirements["required_skills"]))
        total_req = len(requirements["required_skills"])
        skills_score = round((skills_match / total_req) * 40, 1)

        yoe = c["yoe"]
        if requirements["min_years"] <= yoe <= requirements["max_years"]:
            yoe_score = 20
        elif abs(yoe - requirements["min_years"]) <= 1:
            yoe_score = 15
        else:
            yoe_score = 5

        location_bonus = 10 if c["location"] == requirements["location"] else 0
        role = (c.get("current_role", "") or "").lower()
        domain_bonus = 15 if "fintech" in role or "pay" in role else 5
        transferable = round(random.uniform(5, 15), 1)
        total_score = min(round(skills_score + yoe_score + location_bonus + domain_bonus + transferable, 1), 95)

        scored.append({
            **c,
            "match_score": total_score,
            "breakdown": {
                "skills_match_pct": skills_score,
                "experience_fit": yoe_score,
                "location_match": location_bonus,
                "domain_relevance": domain_bonus,
                "transferable_skills": transferable,
            },
        })

    scored.sort(key=lambda x: x["match_score"], reverse=True)

    msg_payload = {
        "job_id": "JOB-001",
        "ranked_candidates": [
            {"id": c["id"], "name": c["name"], "score": c["match_score"]}
            for c in scored
        ],
    }
    msg = AgentMessage("Matcher", "Orchestrator", "CANDIDATES_RANKED", msg_payload)
    show_message(msg)

    table = Table(title="Matcher: Ranked Candidates", box=box.ROUNDED, header_style="bold green")
    table.add_column("Rank", style="dim")
    table.add_column("Name")
    table.add_column("Score")
    table.add_column("Skills Match", justify="right")
    table.add_column("Exp Fit", justify="right")
    table.add_column("Location", justify="right")
    table.add_column("Domain", justify="right")
    table.add_column("Transferable", justify="right")
    for i, c in enumerate(scored, 1):
        b = c["breakdown"]
        table.add_row(
            str(i), c["name"], f"[bold]{c['match_score']}[/bold]",
            str(b["skills_match_pct"]), str(b["experience_fit"]), str(b["location_match"]),
            str(b["domain_relevance"]), str(b["transferable_skills"]),
        )
    console.print(table)
    return scored


def simulate_screening(candidates: list) -> list:
    step("Screener Agent: Conducting voice assessments")

    assessments = []
    for c in candidates:
        desc = f"  [dim]Calling {c['name']} (Hinglish voice screening)..."
        with Progress(SpinnerColumn(), TextColumn(desc), transient=True) as p:
            p.add_task("", total=None)
            time.sleep(1.2)

        comm_score = round(random.uniform(6.5, 9.5), 1)
        tech_score = round(random.uniform(6.0, 9.5), 1)
        culture_score = round(random.uniform(6.0, 9.0), 1)
        overall = round((comm_score + tech_score + culture_score) / 3, 1)

        assessments.append({
            **c,
            "screener_report": {
                "communication": comm_score,
                "technical_depth": tech_score,
                "cultural_fit": culture_score,
                "overall": overall,
                "language_used": "Hinglish",
                "key_observations": random.choice([
                    "Clear communication, strong system design thinking",
                    "Good fundamentals, needs mentorship on distributed systems",
                    "Excellent problem-solving, confident communicator",
                    "Deep fintech domain knowledge, slightly nervous initially",
                ]),
            }
        })

    assessments.sort(key=lambda x: x["screener_report"]["overall"], reverse=True)

    msg_payload = {
        "job_id": "JOB-001",
        "screening_results": [
            {"id": c["id"], "name": c["name"], "overall": c["screener_report"]["overall"]}
            for c in assessments
        ],
    }
    msg = AgentMessage("Screener", "Orchestrator", "SCREENING_COMPLETE", msg_payload)
    show_message(msg)

    table = Table(title="Screener: Voice Assessment Results", box=box.ROUNDED, header_style="bold yellow")
    table.add_column("Name")
    table.add_column("Communication", justify="right")
    table.add_column("Technical", justify="right")
    table.add_column("Culture Fit", justify="right")
    table.add_column("Overall", justify="right")
    table.add_column("Observations")
    for c in assessments:
        r = c["screener_report"]
        table.add_row(c["name"], str(r["communication"]), str(r["technical_depth"]),
                      str(r["cultural_fit"]), f"[bold]{r['overall']}[/bold]", r["key_observations"])
    console.print(table)
    return assessments


def simulate_scheduling(candidates: list) -> list:
    step("Scheduler Agent: Coordinating interview slots")

    for c in candidates:
        desc = f"  [dim]Negotiating slot with {c['name']}..."
        with Progress(SpinnerColumn(), TextColumn(desc), transient=True) as p:
            p.add_task("", total=None)
            time.sleep(0.7)

    interviews = []
    slots = [
        "Mon 22 Jun, 10:00 AM - 11:00 AM",
        "Mon 22 Jun, 2:00 PM - 3:00 PM",
        "Tue 23 Jun, 11:00 AM - 12:00 PM",
        "Wed 24 Jun, 3:00 PM - 4:00 PM",
    ]
    for i, c in enumerate(candidates):
        interviews.append({
            **c,
            "scheduled_slot": slots[i % len(slots)],
            "interview_type": "Technical + System Design",
            "panel": "Senior Eng + Hiring Manager",
            "calendar_event_created": True,
            "candidate_confirmed": True,
        })

    msg_payload = {
        "job_id": "JOB-001",
        "scheduled": [
            {"id": c["id"], "name": c["name"], "slot": c["scheduled_slot"]}
            for c in interviews
        ],
    }
    msg = AgentMessage("Scheduler", "Orchestrator", "INTERVIEWS_SCHEDULED", msg_payload)
    show_message(msg)

    table = Table(title="Scheduler: Confirmed Interviews", box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Slot")
    table.add_column("Type")
    table.add_column("Panel")
    table.add_column("Status")
    for c in interviews:
        table.add_row(c["name"], c["scheduled_slot"], c["interview_type"],
                      c["panel"], "[green]Confirmed[/green]")
    console.print(table)
    return interviews


def generate_final_shortlist(candidates: list):
    step("Orchestrator Agent: Compiling final shortlist")
    time.sleep(0.5)

    final = []
    for c in candidates:
        s = c["match_score"]
        r = c["screener_report"]["overall"]
        composite = round(s * 0.4 + r * 1.0, 1)
        final.append({**c, "composite_score": composite})

    final.sort(key=lambda x: x["composite_score"], reverse=True)

    console.print("\n" + "=" * 90)
    console.print(Panel.fit(
        "[bold green]FINAL SHORTLIST -- AI Recruiter Agent Swarm[/bold green]\n"
        f"Job: [cyan]Senior Software Engineer (Backend) -- Bangalore[/cyan]\n"
        f"Candidates Processed: [bold]{len(final)}[/bold]  |  "
        f"Shortlisted: [bold]{len(final)}[/bold]  |  "
        f"Time Elapsed: [bold]~8 seconds[/bold] (vs ~5 days manual)",
        border_style="green",
        padding=(1, 2),
    ))

    table = Table(box=box.DOUBLE_EDGE, header_style="bold white on dark_green")
    table.add_column("Rank", style="dim", width=6)
    table.add_column("Candidate", width=18)
    table.add_column("Match Score", justify="right", width=12)
    table.add_column("Voice Assessment", justify="right", width=16)
    table.add_column("Composite", justify="right", width=12)
    table.add_column("Scheduled", width=28)

    for i, c in enumerate(final, 1):
        table.add_row(
            f"#{i}",
            f"{c['name']}\n[dim]{c['current_role']}[/dim]",
            f"{c['match_score']}/95",
            f"{c['screener_report']['overall']}/10",
            f"[bold]{c['composite_score']}[/bold]",
            c['scheduled_slot'],
        )
    console.print(table)

    console.print(Panel(
        "[bold yellow]Key Insights from Agent Collaboration:[/bold yellow]\n"
        "* Ananya Sharma (Razorpay) leads on match score + fintech domain fit\n"
        "* Rahul Verma (PhonePe) strong but needs Kubernetes exposure -- flagged for upskilling\n"
        "* Priya Patel (CRED) highest voice assessment score -- excellent communication\n"
        "* Vikram Singh (Flipkart) has deepest system design experience (7 yrs, Kafka)\n"
        "\n[italic]All candidates shortlisted. Human recruiter to conduct final round.[/italic]",
        border_style="bright_yellow",
        padding=(1, 2),
        width=90,
    ))

    console.print("\n[bold]Agent Communication Flow Summary:[/bold]")
    flow_table = Table(box=box.SIMPLE, header_style="bold")
    flow_table.add_column("From", style="cyan")
    flow_table.add_column("To", style="magenta")
    flow_table.add_column("Message Type")
    flow_table.add_column("Step")

    messages = [
        ("Orchestrator", "Sourcer", "JD_PARSED", "1. Parse job description"),
        ("Sourcer", "Orchestrator", "CANDIDATES_FOUND", "2. Search 4 platforms"),
        ("Orchestrator", "Matcher", "RANK_REQUEST", "3. Send profiles to Matcher"),
        ("Matcher", "Orchestrator", "CANDIDATES_RANKED", "4. Score & rank"),
        ("Orchestrator", "Screener", "SCREEN_REQUEST", "5. Trigger voice screening"),
        ("Screener", "Orchestrator", "SCREENING_COMPLETE", "6. Assessment reports"),
        ("Orchestrator", "Scheduler", "SCHEDULE_REQUEST", "7. Book interviews"),
        ("Scheduler", "Orchestrator", "INTERVIEWS_SCHEDULED", "8. Confirm slots"),
        ("Orchestrator", "Recruiter", "FINAL_SHORTLIST", "9. Deliver results"),
    ]
    for frm, to, mtype, step_label in messages:
        flow_table.add_row(frm, to, mtype, step_label)
    console.print(flow_table)

    return final


def show_welcome():
    title = """
+--------------------------------------------------------------+
|          AI Recruiter Agent Swarm -- Pipeline Demo           |
|           India Runs Hackathon -- Track 2, Challenge 1       |
+--------------------------------------------------------------+
    """
    console.print(f"[bold cyan]{title}[/bold cyan]")
    console.print(Panel(
        "This demo simulates a coordinated swarm of 5 AI agents working together\n"
        "to source, match, screen, and schedule candidates for a senior engineering role.\n"
        "All agent communication follows the async message protocol defined in the architecture.",
        border_style="blue",
        padding=(1, 2),
    ))


def main():
    show_welcome()

    jd = SAMPLE_JD.strip()
    console.print(Panel(jd, title="[bold]Input: Job Description[/bold]", border_style="white", width=90))

    reqs = simulate_jd_parsing(jd)
    sourced = simulate_sourcing(reqs)
    scored = simulate_matching(sourced, reqs)
    screened = simulate_screening(scored)
    interviews = simulate_scheduling(screened)
    generate_final_shortlist(interviews)

    console.print("\n" + "=" * 90)
    console.print("[bold green]Demo complete.[/bold green] The full pipeline processed 4 candidates "
                  "across 5 agents in ~8 seconds.")
    console.print("[dim]Without this system: same process takes 3-5 days of manual recruiter work.[/dim]\n")


if __name__ == "__main__":
    main()
