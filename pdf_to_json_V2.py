import pdfplumber
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Contact:
    phone: str = ""
    email: str = ""
    linkedin: str = ""
    github: str = ""
    address: str = ""
    website: str = ""


@dataclass
class Experience:
    company: str = ""
    role: str = ""
    location: str = ""
    duration: str = ""
    details: List[str] = field(default_factory=list)


@dataclass
class Education:
    degree: str = ""
    school: str = ""
    location: str = ""
    year: str = ""
    gpa: str = ""
    achievements: List[str] = field(default_factory=list)
    project_github_url: str = ""  # Added for education project link


@dataclass
class Project:
    name: str = ""
    link: str = ""
    github_url: str = ""
    duration: str = ""
    description: str = ""
    technologies: List[str] = field(default_factory=list)


@dataclass
class Certification:
    name: str = ""
    issuer: str = ""
    date: str = ""
    credential_url: str = ""
    details: str = ""


@dataclass
class Skill:
    category: str = ""
    items: List[str] = field(default_factory=list)


@dataclass
class ResumeData:
    name: str = ""
    title: str = ""
    contact: Contact = field(default_factory=Contact)
    summary: str = ""
    experience: List[Experience] = field(default_factory=list)
    skills: List[Skill] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)



class ResumeParser:

    SECTION_KEYWORDS = {
        "summary": ["about me", "summary", "profile"],
        "experience": ["experience", "work experience"],
        "skills": ["skills", "technical skills"],
        "projects": ["projects"],
        "education": ["education"],
        "certifications": ["certifications"],
        "languages": ["languages", "laguages"],
    }

    def __init__(self, debug=False):
        self.debug = debug
        self.data = ResumeData()
        self.raw_text = ""
        self.links = []  # List of {'page': int, 'text': str, 'url': str}

    def log(self, msg):
        if self.debug:
            print(f"[DEBUG] {msg}")


    def extract_text(self, pdf_path: str) -> List[str]:
        lines = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(use_text_flow=True)
                buffer = ""
                last_top = None

                for w in words:
                    if last_top is None or abs(w["top"] - last_top) < 3:
                        buffer += " " + w["text"]
                    else:
                        lines.append(buffer.strip())
                        buffer = w["text"]
                    last_top = w["top"]

                if buffer:
                    lines.append(buffer.strip())

        self.raw_text = "\n".join(lines)
        return lines

    def extract_links(self, pdf_path: str):
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                if page.annots:
                    for annot in page.annots:
                        if 'uri' in annot:
                            uri = annot['uri']
                            bbox = (annot['x0'], annot['top'], annot['x1'], annot['bottom'])
                            cropped = page.crop(bbox)
                            text = cropped.extract_text()
                            if text:
                                text = re.sub(r"\s+", " ", text).strip()
                                self.links.append({
                                    'page': page_num,
                                    'text': text,
                                    'url': uri
                                })
                                self.log(f"Extracted link: text='{text}', url='{uri}'")


    def clean(self, text: str) -> str:
        text = re.sub(r"[•●▪▫■□]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def identify_section(self, line: str) -> Optional[str]:
        key = self.clean(line.lower().replace(":", ""))
        for section, keys in self.SECTION_KEYWORDS.items():
            if key in keys:
                return section
        return None


    def parse_header(self, lines: List[str]):
        for line in lines[:5]:
            l = self.clean(line)
            if not self.data.name:
                self.data.name = l
            elif not self.data.title:
                self.data.title = l
                break

        header = "\n".join(lines[:10])

        email = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", header)
        phone = re.search(r"\+?\d[\d\s\-]{9,}", header)
        linkedin = re.search(r"linkedin\.com/in/[\w\-]+", header)
        github = re.search(r"github\.com/[\w\-]+", header)

        self.data.contact.email = email.group(0) if email else ""
        self.data.contact.phone = re.sub(r"[^\d+]", "", phone.group(0)) if phone else ""
        self.data.contact.linkedin = f"https://{linkedin.group(0)}" if linkedin else ""
        self.data.contact.github = f"https://{github.group(0)}" if github else ""

        if "bangladesh" in header.lower():
            self.data.contact.address = "Dhaka, Bangladesh"

    def parse_summary(self, lines):
        self.data.summary = " ".join(self.clean(l) for l in lines)

    def parse_skills(self, lines):
        skills = []
        current = None

        for line in lines:
            line = self.clean(line)
            if ":" in line:
                category, rest = line.split(":", 1)
                items = re.split(r",|;|\band\b", rest)
                items = [self.clean(i) for i in items if len(i.strip()) > 2]
                current = Skill(category=category, items=items)
                skills.append(current)
            elif current:
                extra = re.split(r",|;|\band\b", line)
                current.items.extend(self.clean(i) for i in extra if len(i.strip()) > 2)

        self.data.skills = skills

    def parse_experience(self, lines):
        exps = []
        current = None

        for line in lines:
            line = self.clean(line)
            if "|" in line and re.search(r"20\d{2}", line):
                if current:
                    exps.append(current)
                parts = [p.strip() for p in line.split("|")]
                current = Experience(company=parts[0], duration=parts[-1])
            elif current and not current.role:
                if "|" in line:
                    r, loc = line.split("|", 1)
                    current.role = r.strip()
                    current.location = loc.strip()
            elif current:
                current.details.append(line)

        if current:
            exps.append(current)

        self.data.experience = exps

    def parse_projects(self, lines, github_links):
        projects = []
        current = None
        github_index = 0

        for line in lines:
            line = self.clean(line)
            if "|" in line and "github" in line.lower():
                if current:
                    projects.append(current)
                parts = [p.strip() for p in line.split("|")]
                name = parts[0]
                link_text = parts[1] if len(parts) > 1 else ""
                duration = parts[2] if len(parts) > 2 else ""
                current = Project(name=name, link=link_text, duration=duration)
                if github_index < len(github_links):
                    current.github_url = github_links[github_index]
                    github_index += 1
            elif current:
                current.description += " " + line

        if current:
            projects.append(current)

        self.data.projects = projects

    def parse_education(self, lines, github_links):
        edus = []
        current = None
        # Assuming the education GitHub link is after the projects' links
        github_index = len(self.data.projects)  # Start from the next index after projects

        for line in lines:
            line = self.clean(line)
            if "|" in line and re.search(r"20\d{2}", line):
                if current:
                    edus.append(current)
                parts = [p.strip() for p in line.split("|")]
                school = parts[0]
                year = parts[1] if len(parts) > 1 else ""
                current = Education(school=school, year=year)
            elif current:
                # GPA detection
                gpa_match = re.search(r'GPA[:\s]*([\d.]+/\d+)', line, re.IGNORECASE)
                if gpa_match:
                    current.gpa = gpa_match.group(1)
                    continue

                # Achievement detection
                if line.lower().startswith("achievements"):
                    ach = re.sub(r'achievements[:\s]*', '', line, flags=re.IGNORECASE)
                    if ach:
                        current.achievements.append(ach)
                    continue

                # Degree detection
                if not current.degree and any(
                    kw in line.lower()
                    for kw in ["bachelor", "higher secondary", "certificate"]
                ):
                    if "|" in line:
                        parts = [p.strip() for p in line.split("|", 1)]
                        current.degree = parts[0]
                        current.location = parts[1] if len(parts) > 1 else ""
                    else:
                        current.degree = line
                    continue

                # Handle project achievement with GitHub link
                if "github repository" in line.lower():
                    ach = line.replace("| Github Repository", "").strip()
                    current.achievements.append(ach)
                    if github_index < len(github_links):
                        current.project_github_url = github_links[github_index]
                        github_index += 1
                elif len(line) > 20:
                    current.achievements.append(line)

        if current:
            edus.append(current)

        self.data.education = edus

    def parse_certifications(self, lines, credential_links):
        certs = []
        i = 0
        credential_index = 0

        while i < len(lines):
            line = self.clean(lines[i])

            if "|" in line and re.search(r'(20\d{2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', line):
                parts = [p.strip() for p in line.split("|")]
                cert = Certification(
                    name=parts[0],
                    issuer=parts[1] if len(parts) > 1 else "",
                    date=parts[2] if len(parts) > 2 else ""
                )

                if i + 1 < len(lines):
                    nxt = self.clean(lines[i + 1])
                    if "credential" in nxt.lower():
                        cert.details = nxt.replace("Credential", "").replace("|", "").strip()
                        if credential_index < len(credential_links):
                            cert.credential_url = credential_links[credential_index]
                            credential_index += 1
                        i += 1

                certs.append(cert)

            i += 1

        self.data.certifications = certs

    def parse_languages(self, lines):
        self.data.languages = [self.clean(l) for l in lines if len(l.strip()) > 2]


    def parse(self, pdf_path: str) -> Dict[str, Any]:
        lines = self.extract_text(pdf_path)
        self.extract_links(pdf_path)  # Extract embedded links
        self.parse_header(lines)

        # Filter specific links
        github_links = [link['url'] for link in self.links if 'github.com' in link['url'].lower() and 'repository' in link['text'].lower()]
        credential_links = [link['url'] for link in self.links if 'credential' in link['text'].lower()]

        current_section = None
        buffer = []

        for line in lines:
            sec = self.identify_section(line)
            if sec:
                if current_section:
                    self.dispatch(current_section, buffer, github_links, credential_links)
                current_section = sec
                buffer = []
            else:
                if current_section:
                    buffer.append(line)

        if current_section:
            self.dispatch(current_section, buffer, github_links, credential_links)

        return self.to_dict()

    def dispatch(self, section, lines, github_links, credential_links):
        if section == "summary":
            self.parse_summary(lines)
        elif section == "skills":
            self.parse_skills(lines)
        elif section == "experience":
            self.parse_experience(lines)
        elif section == "projects":
            self.parse_projects(lines, github_links)
        elif section == "education":
            self.parse_education(lines, github_links)
        elif section == "certifications":
            self.parse_certifications(lines, credential_links)
        elif section == "languages":
            self.parse_languages(lines)

    def to_dict(self):
        return {
            "name": self.data.name,
            "title": self.data.title,
            "contact": asdict(self.data.contact),
            "summary": self.data.summary,
            "experience": [asdict(e) for e in self.data.experience],
            "skills": [asdict(s) for s in self.data.skills],
            "projects": [asdict(p) for p in self.data.projects],
            "education": [asdict(e) for e in self.data.education],
            "certifications": [asdict(c) for c in self.data.certifications],
            "languages": self.data.languages,
        }


if __name__ == "__main__":
    parser = ResumeParser(debug=True)
    data = parser.parse("Hasan_Mahmood_Resume.pdf")

    with open("resume_parsed_V2.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Resume parsed successfully")