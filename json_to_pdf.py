# import json
# from fpdf import FPDF

# class ResumePDF(FPDF):
#     def header(self):
#         # We don't use a fixed header per page to allow flow, 
#         # but you could add a recurring name here if desired.
#         pass

#     def footer(self):
#         # Position at 1.5 cm from bottom
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.set_text_color(128)
#         self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

#     def section_title(self, title):
#         """Creates a Section Header with a line underneath"""
#         self.ln(5)
#         self.set_font('Arial', 'B', 14)
#         self.set_text_color(0, 0, 0) # Black
#         self.cell(0, 8, title.upper(), 0, 1, 'L')
#         # Draw a line below the title
#         self.line(self.get_x(), self.get_y(), 200, self.get_y())
#         self.ln(2)

#     def chapter_body(self, body):
#         self.set_font('Arial', '', 11)
#         self.set_text_color(50, 50, 50)
#         self.multi_cell(0, 6, body)
#         self.ln()

#     def add_bullet(self, text):
#         """Adds a bullet point with proper indentation"""
#         self.set_font('Arial', '', 10)
#         self.set_text_color(0, 0, 0)
        
#         # Calculate height to see if we need a page break
#         # We check if 1 line fits, otherwise add page
#         if self.get_y() > 270:
#             self.add_page()
            
#         # Bullet char
#         self.cell(5, 5, chr(149), 0, 0, 'R') 
#         self.multi_cell(0, 5, text)

# def create_resume_pdf(json_file, output_file):
#     # 1. Load Data
#     try:
#         with open(json_file, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#     except FileNotFoundError:
#         print("❌ Error: resume.json not found.")
#         return

#     pdf = ResumePDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     # --- 1. HEADER SECTION (Name & Contact) ---
#     pdf.set_font('Arial', 'B', 24)
#     pdf.cell(0, 10, data.get('name', 'Name'), ln=True, align='C')
    
#     pdf.set_font('Arial', '', 14)
#     pdf.set_text_color(100, 100, 100) # Grey
#     pdf.cell(0, 8, data.get('title', 'Title'), ln=True, align='C')
    
#     # Contact Row
#     pdf.set_font('Arial', '', 9)
#     pdf.set_text_color(0, 0, 0)
    
#     c = data.get('contact', {})
#     contact_line = f"{c.get('phone', '')} | {c.get('email', '')} | {c.get('address', '')}"
#     pdf.cell(0, 6, contact_line, ln=True, align='C')
    
#     # Links Row
#     links = []
#     if c.get('linkedin'): links.append(c['linkedin'])
#     if c.get('github'): links.append(c['github'])
#     if links:
#         pdf.set_font('Arial', 'U', 9) # Underline for links
#         pdf.set_text_color(0, 0, 255) # Blue
#         pdf.cell(0, 6, " | ".join(links), ln=True, align='C')

#     pdf.ln(5)

#     # --- 2. SUMMARY / ABOUT ME ---
#     if data.get('summary'):
#         pdf.section_title("About Me")
#         pdf.set_font('Arial', '', 11)
#         pdf.set_text_color(0)
#         pdf.multi_cell(0, 6, data['summary'])

#     # --- 3. EXPERIENCE ---
#     if data.get('experience'):
#         pdf.section_title("Experience")
        
#         for job in data['experience']:
#             # Line 1: Company & Date (Justified)
#             pdf.set_font('Arial', 'B', 12)
#             pdf.cell(130, 7, job.get('company', ''), 0, 0)
            
#             pdf.set_font('Arial', 'I', 10)
#             pdf.cell(0, 7, job.get('duration', ''), 0, 1, 'R')
            
#             # Line 2: Role & Location
#             pdf.set_font('Arial', 'I', 11)
#             pdf.cell(130, 6, job.get('role', ''), 0, 0)
            
#             pdf.set_font('Arial', '', 9)
#             pdf.set_text_color(100)
#             pdf.cell(0, 6, job.get('location', ''), 0, 1, 'R')
            
#             # Details (Bullets)
#             pdf.set_text_color(0)
#             pdf.ln(2)
#             for detail in job.get('details', []):
#                 pdf.add_bullet(detail)
            
#             pdf.ln(4) # Spacing between jobs

#     # --- 4. PROJECTS ---
#     if data.get('projects'):
#         pdf.section_title("Projects")
        
#         for proj in data['projects']:
#             # Project Name & Link
#             pdf.set_font('Arial', 'B', 12)
#             name_text = proj.get('name', '')
#             if proj.get('link'):
#                 name_text += f" ({proj.get('link')})"
#             pdf.cell(140, 7, name_text, 0, 0)
            
#             # Duration
#             pdf.set_font('Arial', 'I', 10)
#             pdf.cell(0, 7, proj.get('duration', ''), 0, 1, 'R')
            
#             # Description
#             pdf.set_font('Arial', '', 10)
#             pdf.multi_cell(0, 6, proj.get('description', ''))
#             pdf.ln(3)

#     # --- 5. SKILLS ---
#     if data.get('skills'):
#         pdf.section_title("Skills")
#         pdf.set_font('Arial', '', 10)
        
#         for skill_group in data['skills']:
#             # Bold Category Name
#             pdf.set_font('Arial', 'B', 10)
#             pdf.write(6, f"{skill_group['category']}: ")
            
#             # Normal Items
#             pdf.set_font('Arial', '', 10)
#             items = ", ".join(skill_group['items'])
#             pdf.write(6, items)
#             pdf.ln(6)

#     # --- 6. EDUCATION ---
#     if data.get('education'):
#         pdf.section_title("Education")
        
#         for edu in data['education']:
#             pdf.set_font('Arial', 'B', 12)
#             pdf.cell(140, 7, edu.get('school', ''), 0, 0)
            
#             pdf.set_font('Arial', 'I', 10)
#             pdf.cell(0, 7, edu.get('year', ''), 0, 1, 'R')
            
#             pdf.set_font('Arial', '', 11)
#             degree_line = edu.get('degree', '')
#             if edu.get('gpa'):
#                 degree_line += f" (GPA: {edu['gpa']})"
#             pdf.cell(0, 6, degree_line, ln=True)
            
#             if edu.get('achievements'):
#                 pdf.set_font('Arial', 'I', 10)
#                 pdf.multi_cell(0, 5, f"Achievement: {edu['achievements']}")
            
#             pdf.ln(3)

#     # --- 7. CERTIFICATIONS ---
#     if data.get('certifications'):
#         pdf.section_title("Certifications")
        
#         for cert in data['certifications']:
#             pdf.set_font('Arial', 'B', 10)
#             # Bullet point for certs
#             pdf.cell(5, 5, chr(149), 0, 0, 'R')
            
#             text = f"{cert.get('name')} - {cert.get('issuer')} ({cert.get('date')})"
#             pdf.cell(0, 5, text, ln=True)

#     # --- 8. LANGUAGES ---
#     if data.get('languages'):
#         pdf.section_title("Languages")
#         pdf.set_font('Arial', '', 10)
#         lang_str = " | ".join(data['languages'])
#         pdf.multi_cell(0, 6, lang_str)

#     # Save
#     pdf.output(output_file)
#     print(f"PDF generated successfully: {output_file}")

# if __name__ == "__main__":
#     create_resume_pdf("resume_parsed.json", "Reconstructed.pdf")


# my V2 dont know if the shit works or not 

import json
from fpdf import FPDF

# --- CONFIGURATION ---
FONT_MAIN = 'Arial'
COLOR_HEADER = (0, 51, 102)   # Dark Blue headers
COLOR_TEXT = (0, 0, 0)        # Black text
COLOR_GREY = (100, 100, 100)  # Grey for metadata

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT_MAIN, 'I', 8)
        self.set_text_color(150)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, 'C')

    def section_title(self, label):
        self.ln(5)
        self.set_font(FONT_MAIN, 'B', 12)
        self.set_text_color(*COLOR_HEADER)
        self.cell(0, 7, label.upper(), 0, 1, 'L')
        self.set_draw_color(*COLOR_HEADER)
        self.line(self.get_x(), self.get_y(), 200, self.get_y())
        self.ln(3)

    def draw_bullet(self, text):
        self.set_font(FONT_MAIN, '', 10)
        self.set_text_color(*COLOR_TEXT)
        if self.get_y() > 270: self.add_page()
        
        current_x = self.get_x()
        self.set_x(current_x + 5)
        self.cell(5, 5, chr(149), 0, 0, 'L') 
        self.set_x(current_x + 10) 
        self.multi_cell(0, 5, text)
        self.ln(1)

    def write_link(self, text, url):
        """Writes an underlined link in black text"""
        self.set_text_color(*COLOR_TEXT) # Black
        self.set_font(FONT_MAIN, 'U', 10) # Underline
        self.cell(0, 5, text, link=url, ln=True)
        # Reset
        self.set_font(FONT_MAIN, '', 10)

def sanitize(text):
    if not text: return ""
    replacements = {
        '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '', '\uf0b7': ''
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

def reconstruct_sentences(raw_list):
    if not raw_list: return []
    if isinstance(raw_list, str): return [raw_list]
    cleaned = []
    buffer = ""
    connectors = ('and', 'or', 'with', 'using', 'in', 'to', ',', 'of', 'for', 'models', 'frameworks')
    for item in raw_list:
        item = item.strip()
        if not item: continue
        if buffer and (item[0].islower() or buffer.strip().endswith(connectors)):
            buffer += " " + item
        else:
            if buffer: cleaned.append(buffer)
            buffer = item
    if buffer: cleaned.append(buffer)
    return cleaned

def create_resume(json_path, output_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return

    pdf = PDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- 1. HEADER ---
    pdf.set_font(FONT_MAIN, 'B', 22)
    pdf.set_text_color(*COLOR_TEXT)
    pdf.cell(0, 10, sanitize(data.get('name', '')).upper(), ln=True, align='C')
    
    pdf.set_font(FONT_MAIN, '', 12)
    pdf.set_text_color(*COLOR_GREY)
    pdf.cell(0, 6, sanitize(data.get('title', '')), ln=True, align='C')

    # Contact Info
    pdf.set_font(FONT_MAIN, '', 9)
    pdf.set_text_color(*COLOR_TEXT)
    c = data.get('contact', {})
    contact_parts = [c.get('phone'), c.get('email'), c.get('address')]
    contact_str = "  |  ".join(filter(None, contact_parts))
    pdf.cell(0, 6, sanitize(contact_str), ln=True, align='C')

    # Links (Underlined, Centered)
    links = []
    if c.get('linkedin'): links.append(("LinkedIn", c['linkedin']))
    if c.get('github'): links.append(("GitHub", c['github']))
    
    if links:
        pdf.set_font(FONT_MAIN, 'U', 9) # Underline
        pdf.set_text_color(*COLOR_TEXT) # Black
        
        # Center the links manually
        total_width = sum(pdf.get_string_width(l[0]) for l in links) + (len(links)-1)*5
        start_x = (210 - total_width) / 2
        pdf.set_x(start_x)
        
        for i, (name, url) in enumerate(links):
            pdf.write(6, name, url)
            if i < len(links) - 1:
                pdf.set_font(FONT_MAIN, '', 9) # Turn off underline for separator
                pdf.write(6, "  |  ")
                pdf.set_font(FONT_MAIN, 'U', 9) # Turn on for next link
        pdf.ln(8)

    # --- 2. SUMMARY ---
    if data.get('summary'):
        pdf.section_title("Summary")
        pdf.set_font(FONT_MAIN, '', 10)
        pdf.set_text_color(*COLOR_TEXT)
        pdf.multi_cell(0, 5, sanitize(data['summary']))

    # --- 3. EXPERIENCE ---
    if data.get('experience'):
        pdf.section_title("Experience")
        for job in data['experience']:
            pdf.set_font(FONT_MAIN, 'B', 11)
            pdf.set_text_color(*COLOR_TEXT)
            pdf.cell(140, 6, sanitize(job.get('company', '')), 0, 0)
            
            pdf.set_font(FONT_MAIN, 'I', 9)
            pdf.cell(0, 6, sanitize(job.get('duration', '')), 0, 1, 'R')
            
            pdf.set_font(FONT_MAIN, 'I', 10)
            pdf.cell(140, 5, sanitize(job.get('role', '')), 0, 0)
            
            pdf.set_font(FONT_MAIN, '', 9)
            pdf.set_text_color(*COLOR_GREY)
            pdf.cell(0, 5, sanitize(job.get('location', '')), 0, 1, 'R')
            
            pdf.ln(1)
            clean_details = reconstruct_sentences(job.get('details', []))
            for d in clean_details:
                pdf.draw_bullet(sanitize(d))
            pdf.ln(3)

    # --- 4. PROJECTS ---
    if data.get('projects'):
        pdf.section_title("Projects")
        for proj in data['projects']:
            pdf.set_font(FONT_MAIN, 'B', 11)
            pdf.set_text_color(*COLOR_TEXT)
            
            # Name (Underlined if linked)
            name = sanitize(proj.get('name', ''))
            link = proj.get('github_url') or proj.get('link')
            
            if link and link.startswith('http'):
                pdf.set_font(FONT_MAIN, 'BU', 11) # Bold + Underline
                pdf.cell(140, 6, name, link=link, ln=0)
                pdf.set_font(FONT_MAIN, 'B', 11)  # Reset
            else:
                pdf.cell(140, 6, name, ln=0)
            
            pdf.set_font(FONT_MAIN, 'I', 9)
            pdf.cell(0, 6, sanitize(proj.get('duration', '')), 0, 1, 'R')
            
            pdf.set_font(FONT_MAIN, '', 10)
            pdf.multi_cell(0, 5, sanitize(proj.get('description', '')))
            pdf.ln(3)

    # --- 5. SKILLS ---
    if data.get('skills'):
        pdf.section_title("Skills")
        pdf.set_text_color(*COLOR_TEXT) # Ensure text is black
        
        for cat in data['skills']:
            category_name = sanitize(cat.get('category', ''))
            clean_items = reconstruct_sentences(cat.get('items', []))
            items_str = ", ".join(clean_items)
            
            pdf.set_font(FONT_MAIN, 'B', 10)
            pdf.write(6, f"{category_name}: ")
            
            pdf.set_font(FONT_MAIN, '', 10)
            pdf.write(6, sanitize(items_str))
            pdf.ln(5)

    # --- 6. EDUCATION ---
    if data.get('education'):
        pdf.section_title("Education")
        for edu in data['education']:
            pdf.set_font(FONT_MAIN, 'B', 11)
            pdf.set_text_color(*COLOR_TEXT)
            pdf.cell(140, 6, sanitize(edu.get('school', '')), 0, 0)
            
            pdf.set_font(FONT_MAIN, 'I', 9)
            pdf.cell(0, 6, sanitize(edu.get('year', '')), 0, 1, 'R')
            
            degree = sanitize(edu.get('degree', ''))
            if edu.get('gpa'): degree += f" (GPA: {edu.get('gpa')})"
            
            pdf.set_font(FONT_MAIN, '', 10)
            pdf.cell(0, 5, degree, ln=True)
            
            # Achievements formatting
            achievements = edu.get('achievements', [])
            if achievements:
                cleaned_ach = reconstruct_sentences(achievements)
                for ach in cleaned_ach:
                     pdf.draw_bullet(f"Achievement: {sanitize(ach)}")

            # Project Link (Underlined)
            if edu.get('project_github_url'):
                 pdf.set_font(FONT_MAIN, 'U', 9)
                 pdf.cell(0, 5, "Final Year Project Link", link=edu['project_github_url'], ln=True)

            pdf.ln(3)

    # --- 7. CERTIFICATIONS ---
    if data.get('certifications'):
        pdf.section_title("Certifications")
        for cert in data['certifications']:
            text = f"{cert.get('name')} - {cert.get('issuer')}"
            if cert.get('date'): text += f" ({cert.get('date')})"
            
            url = cert.get('credential_url')
            
            # Bullet
            pdf.set_font(FONT_MAIN, '', 10)
            pdf.set_x(20)
            pdf.cell(5, 5, chr(149), 0, 0, 'R')
            
            # Text (Underlined if linked)
            if url:
                pdf.set_font(FONT_MAIN, 'U', 10)
                pdf.cell(0, 5, sanitize(text), link=url, ln=True)
                pdf.set_font(FONT_MAIN, '', 10)
            else:
                pdf.cell(0, 5, sanitize(text), ln=True)

    # --- 8. LANGUAGES (Updated to List) ---
    if data.get('languages'):
        pdf.section_title("Languages")
        pdf.set_text_color(*COLOR_TEXT)
        
        for lang in data['languages']:
            # Use the bullet function for vertical listing
            pdf.draw_bullet(sanitize(lang))

    pdf.output(output_path)
    print(f"Generated updated resume: {output_path}")

if __name__ == "__main__":
    create_resume("resume_parsed_V2.json", "Fixed_Resume.pdf")