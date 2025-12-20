import json
from fpdf import FPDF

class ResumePDF(FPDF):
    def header(self):
        # We don't use a fixed header per page to allow flow, 
        # but you could add a recurring name here if desired.
        pass

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        """Creates a Section Header with a line underneath"""
        self.ln(5)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0) # Black
        self.cell(0, 8, title.upper(), 0, 1, 'L')
        # Draw a line below the title
        self.line(self.get_x(), self.get_y(), 200, self.get_y())
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, body)
        self.ln()

    def add_bullet(self, text):
        """Adds a bullet point with proper indentation"""
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        
        # Calculate height to see if we need a page break
        # We check if 1 line fits, otherwise add page
        if self.get_y() > 270:
            self.add_page()
            
        # Bullet char
        self.cell(5, 5, chr(149), 0, 0, 'R') 
        self.multi_cell(0, 5, text)

def create_resume_pdf(json_file, output_file):
    # 1. Load Data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: resume.json not found.")
        return

    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- 1. HEADER SECTION (Name & Contact) ---
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 10, data.get('name', 'Name'), ln=True, align='C')
    
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(100, 100, 100) # Grey
    pdf.cell(0, 8, data.get('title', 'Title'), ln=True, align='C')
    
    # Contact Row
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(0, 0, 0)
    
    c = data.get('contact', {})
    contact_line = f"{c.get('phone', '')} | {c.get('email', '')} | {c.get('address', '')}"
    pdf.cell(0, 6, contact_line, ln=True, align='C')
    
    # Links Row
    links = []
    if c.get('linkedin'): links.append(c['linkedin'])
    if c.get('github'): links.append(c['github'])
    if links:
        pdf.set_font('Arial', 'U', 9) # Underline for links
        pdf.set_text_color(0, 0, 255) # Blue
        pdf.cell(0, 6, " | ".join(links), ln=True, align='C')

    pdf.ln(5)

    # --- 2. SUMMARY / ABOUT ME ---
    if data.get('summary'):
        pdf.section_title("About Me")
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0)
        pdf.multi_cell(0, 6, data['summary'])

    # --- 3. EXPERIENCE ---
    if data.get('experience'):
        pdf.section_title("Experience")
        
        for job in data['experience']:
            # Line 1: Company & Date (Justified)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(130, 7, job.get('company', ''), 0, 0)
            
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 7, job.get('duration', ''), 0, 1, 'R')
            
            # Line 2: Role & Location
            pdf.set_font('Arial', 'I', 11)
            pdf.cell(130, 6, job.get('role', ''), 0, 0)
            
            pdf.set_font('Arial', '', 9)
            pdf.set_text_color(100)
            pdf.cell(0, 6, job.get('location', ''), 0, 1, 'R')
            
            # Details (Bullets)
            pdf.set_text_color(0)
            pdf.ln(2)
            for detail in job.get('details', []):
                pdf.add_bullet(detail)
            
            pdf.ln(4) # Spacing between jobs

    # --- 4. PROJECTS ---
    if data.get('projects'):
        pdf.section_title("Projects")
        
        for proj in data['projects']:
            # Project Name & Link
            pdf.set_font('Arial', 'B', 12)
            name_text = proj.get('name', '')
            if proj.get('link'):
                name_text += f" ({proj.get('link')})"
            pdf.cell(140, 7, name_text, 0, 0)
            
            # Duration
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 7, proj.get('duration', ''), 0, 1, 'R')
            
            # Description
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 6, proj.get('description', ''))
            pdf.ln(3)

    # --- 5. SKILLS ---
    if data.get('skills'):
        pdf.section_title("Skills")
        pdf.set_font('Arial', '', 10)
        
        for skill_group in data['skills']:
            # Bold Category Name
            pdf.set_font('Arial', 'B', 10)
            pdf.write(6, f"{skill_group['category']}: ")
            
            # Normal Items
            pdf.set_font('Arial', '', 10)
            items = ", ".join(skill_group['items'])
            pdf.write(6, items)
            pdf.ln(6)

    # --- 6. EDUCATION ---
    if data.get('education'):
        pdf.section_title("Education")
        
        for edu in data['education']:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(140, 7, edu.get('school', ''), 0, 0)
            
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 7, edu.get('year', ''), 0, 1, 'R')
            
            pdf.set_font('Arial', '', 11)
            degree_line = edu.get('degree', '')
            if edu.get('gpa'):
                degree_line += f" (GPA: {edu['gpa']})"
            pdf.cell(0, 6, degree_line, ln=True)
            
            if edu.get('achievements'):
                pdf.set_font('Arial', 'I', 10)
                pdf.multi_cell(0, 5, f"Achievement: {edu['achievements']}")
            
            pdf.ln(3)

    # --- 7. CERTIFICATIONS ---
    if data.get('certifications'):
        pdf.section_title("Certifications")
        
        for cert in data['certifications']:
            pdf.set_font('Arial', 'B', 10)
            # Bullet point for certs
            pdf.cell(5, 5, chr(149), 0, 0, 'R')
            
            text = f"{cert.get('name')} - {cert.get('issuer')} ({cert.get('date')})"
            pdf.cell(0, 5, text, ln=True)

    # --- 8. LANGUAGES ---
    if data.get('languages'):
        pdf.section_title("Languages")
        pdf.set_font('Arial', '', 10)
        lang_str = " | ".join(data['languages'])
        pdf.multi_cell(0, 6, lang_str)

    # Save
    pdf.output(output_file)
    print(f"PDF generated successfully: {output_file}")

if __name__ == "__main__":
    create_resume_pdf("resume_parsed.json", "Reconstructed.pdf")