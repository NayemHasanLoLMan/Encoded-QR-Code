# import pdfplumber
# import json
# import re


# def clean_text(text):
#     """Removes bullets and extra whitespace"""
#     if not text: return ""
#     # Remove bullet points (●, •, etc.)
#     text = re.sub(r'[\u25cf\u2022\u25aa\-\*]', '', text)
#     return text.strip()

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#     return text

# def parse_resume_text(text):
#     # Initialize the empty structure
#     data = {
#         "name": "", "title": "",
#         "contact": {"phone": "", "email": "", "linkedin": "", "github": "", "address": ""},
#         "summary": "",
#         "experience": [],
#         "skills": [],
#         "projects": [],
#         "education": [],
#         "certifications": [],
#         "languages": []
#     }

#     lines = text.split('\n')
#     lines = [line.strip() for line in lines if line.strip()] # Remove empty lines

#     # --- 1. BASIC INFO (First few lines) ---
#     # Usually Line 1 is Name, Line 2 is Title
#     if len(lines) > 0: data["name"] = lines[0]
#     if len(lines) > 1: data["title"] = lines[1]

#     # --- 2. CONTACT PARSING (Regex) ---
#     # We scan the first chunk of text for contact info
#     header_chunk = " ".join(lines[:10])
    
#     email_match = re.search(r'[\w\.-]+@[\w\.-]+', header_chunk)
#     if email_match: data["contact"]["email"] = email_match.group(0)

#     phone_match = re.search(r'(\+880|01)[0-9\-\s]+', header_chunk)
#     if phone_match: data["contact"]["phone"] = phone_match.group(0).strip()

#     if "linkedin.com" in header_chunk:
#         link = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+', header_chunk)
#         if link: data["contact"]["linkedin"] = link.group(0)

#     if "github.com" in header_chunk:
#         git = re.search(r'(https?://)?(github\.com/[a-zA-Z0-9%_-]+)', header_chunk)
#         if git: data["contact"]["github"] = git.group(0)
    
#     # Address (heuristic: look for "Dhaka" or specific keywords)
#     if "Dhaka" in header_chunk:
#         data["contact"]["address"] = "Dhaka, Bangladesh"

#     # --- 3. SECTION PARSING ---
#     # We define keywords to split the text into blocks
#     current_section = None
#     buffer = []
    
#     # Keywords that start new sections
#     HEADERS = {
#         "ABOUT ME": "summary",
#         "EXPERIENCE": "experience",
#         "SKILLS": "skills",
#         "PROJECTS": "projects",
#         "EDUCATION": "education",
#         "CERTIFICATIONS": "certifications",
#         "ACHIEVEMENTS": "achievements", # Sometimes mapped to others
#         "LANGUAGES": "languages",
#         "LAGUAGES": "languages"
#     }

#     for line in lines[3:]: # Skip header lines
#         # Check if line is a Header (Uppercase + specific words)
#         clean_line = line.upper().replace(":", "").strip()
        
#         # Heuristic: Headers are often short (< 3 words) and in our list
#         is_header = False
#         for header, key in HEADERS.items():
#             if header in clean_line and len(clean_line.split()) < 4:
#                 # Process the PREVIOUS section before switching
#                 process_section(current_section, buffer, data)
                
#                 # Start NEW section
#                 current_section = key
#                 buffer = []
#                 is_header = True
#                 break
        
#         if not is_header:
#             buffer.append(line)

#     # Process the final section caught in buffer
#     process_section(current_section, buffer, data)

#     return data

# def process_section(section, lines, data):
#     """Parses specific section blocks into structured lists"""
#     if not section or not lines: return

#     if section == "summary":
#         data["summary"] = " ".join(lines)

#     elif section == "skills":
#         # Group skills by lines (heuristic)
#         for line in lines:
#             if ":" in line:
#                 cat, items = line.split(":", 1)
#                 data["skills"].append({
#                     "category": cat.strip(),
#                     "items": [i.strip() for i in items.split(",")]
#                 })

#     elif section == "experience":
#         # Heuristic: Company name usually comes before Date
#         # This is tricky without AI, but we try to group by blocks
#         # We assume a new job starts when we see a Date (Dec 2024 - Present)
#         job_entry = {}
#         details = []
        
#         for line in lines:
#             # Check for date pattern (e.g., "Dec 2024 - Present")
#             date_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}', line)
            
#             if date_match and len(line) < 50: # Likely a header line for the job
#                 # Save previous job if exists
#                 if job_entry:
#                     job_entry["details"] = details
#                     data["experience"].append(job_entry)
#                     details = []
#                     job_entry = {}
                
#                 parts = line.split("|")
#                 if len(parts) > 1:
#                     job_entry["duration"] = parts[-1].strip()
#                     job_entry["company"] = parts[0].strip()
#                 else:
#                     job_entry["duration"] = line
#                     job_entry["company"] = "Unknown Company" # Placeholder if parsing fails
            
#             elif "Developer" in line or "Intern" in line or "Engineer" in line:
#                 job_entry["role"] = line
#             elif "Dhaka" in line:
#                 job_entry["location"] = line
#             else:
#                 details.append(line)
        
#         # Append the last job found
#         if job_entry:
#             job_entry["details"] = details
#             data["experience"].append(job_entry)

#     elif section == "education":
#         # Similar logic to experience
#         edu_entry = {}
#         for line in lines:
#             if "B.Sc" in line or "HSC" in line:
#                 if edu_entry: data["education"].append(edu_entry)
#                 edu_entry = {"degree": line}
#             elif "University" in line or "College" in line:
#                 edu_entry["school"] = line
#             elif "GPA" in line:
#                 edu_entry["gpa"] = line.replace("GPA:", "").strip()
#             elif re.search(r'\d{4}-\d{4}', line):
#                 edu_entry["year"] = line
#         if edu_entry: data["education"].append(edu_entry)

#     elif section == "languages":
#         data["laguages"] = lines

#     elif section == "projects":
#         # Simple list append for projects
#         proj_entry = {}
#         for line in lines:
#             if "GitHub" in line or "Repository" in line:
#                 if proj_entry: data["projects"].append(proj_entry)
#                 proj_entry = {"name": line.split("|")[0].strip(), "link": "GitHub"}
#             elif proj_entry:
#                 current_desc = proj_entry.get("description", "")
#                 proj_entry["description"] = current_desc + " " + line
#         if proj_entry: data["projects"].append(proj_entry)

#     elif section == "certifications":
#         for line in lines:
#             if "|" in line:
#                 parts = line.split("|")
#                 data["certifications"].append({
#                     "name": parts[0].strip(),
#                     "issuer": parts[1].strip() if len(parts)>1 else "",
#                     "date": parts[-1].strip() if len(parts)>2 else ""
#                 })

# def main():
#     pdf_path = "Hasan_Mahmood_Resume.pdf"
    
#     print(f"Extracting text from {pdf_path}...")
#     try:
#         raw_text = extract_text_from_pdf(pdf_path)
#     except FileNotFoundError:
#         print("Error: PDF file not found. Please ensure 'Hasan_Mahmood_Resume.pdf' is in the folder.")
#         return

#     print("Parsing data...")
#     resume_json = parse_resume_text(raw_text)
    
#     output_file = "resume_test.json"
#     with open(output_file, "w", encoding='utf-8') as f:
#         json.dump(resume_json, f, indent=4)
        
#     print(f"JSON created successfully: {output_file}")
#     print("   (You can now run 'json_to_qr.py' to generate the code)")

# if __name__ == "__main__":
#     main()




import pdfplumber
import json
import re

def clean_text(text):
    """Removes bullets and extra whitespace"""
    if not text: return ""
    # Remove bullet points (●, •, etc.)
    text = re.sub(r'[\u2022\u25cf\u25aa\-\*]', '', text)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_resume_text(text):
    data = {
        "name": "", "title": "",
        "contact": {"phone": "", "email": "", "linkedin": "", "github": "", "address": ""},
        "summary": "",
        "experience": [],
        "skills": [],
        "projects": [],
        "education": [],
        "certifications": [],
        "languages": []
    }

    lines = text.split('\n')
    # Pre-clean lines to remove empty strings
    lines = [line.strip() for line in lines if line.strip()]

    # --- 1. BASIC INFO ---
    if len(lines) > 0: data["name"] = clean_text(lines[0])
    if len(lines) > 1: data["title"] = clean_text(lines[1])

    # --- 2. CONTACT ---
    header_chunk = " ".join(lines[:12]) # Scan first 12 lines
    
    # Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', header_chunk)
    if email_match: data["contact"]["email"] = email_match.group(0)

    # Phone
    phone_match = re.search(r'(\+880|01)[\d\-\s]+', header_chunk)
    if phone_match: data["contact"]["phone"] = phone_match.group(0).strip()

    # LinkedIn / GitHub Links
    # We look for the actual URL patterns
    linkedin = re.search(r'linkedin\.com/in/[\w-]+', header_chunk)
    if linkedin: data["contact"]["linkedin"] = "https://" + linkedin.group(0)

    github = re.search(r'github\.com/[\w-]+', header_chunk)
    if github: data["contact"]["github"] = "https://" + github.group(0)

    if "Dhaka" in header_chunk:
        data["contact"]["address"] = "Dhaka, Bangladesh"

    # --- 3. SECTION PARSING ---
    current_section = None
    buffer = []
    
    # Updated Headers Map (Includes the Typo "LAGUAGES")
    HEADERS = {
        "ABOUT ME": "summary",
        "EXPERIENCE": "experience",
        "SKILLS": "skills",
        "PROJECTS": "projects",
        "EDUCATION": "education",
        "CERTIFICATIONS": "certifications",
        "ACHIEVEMENTS": "achievements",
        "LANGUAGES": "languages",
        "LAGUAGES": "languages"  # <--- FIX: Added to catch the typo in PDF
    }

    for line in lines[3:]:
        # normalize line for header check
        upper_line = line.upper().replace(":", "").strip()
        
        # Check if line is a header
        is_header = False
        # We check if the line matches a header exactly or is very close
        for header, key in HEADERS.items():
            if header == upper_line or (header in upper_line and len(upper_line.split()) < 3):
                # Save previous section
                process_section(current_section, buffer, data)
                
                # Start new section
                current_section = key
                buffer = []
                is_header = True
                break
        
        if not is_header:
            buffer.append(line)

    # Process last section
    process_section(current_section, buffer, data)

    return data

def process_section(section, lines, data):
    if not section or not lines: return

    if section == "summary":
        # Join lines and clean bullets
        full_text = " ".join(lines)
        data["summary"] = clean_text(full_text)

    elif section == "skills":
        for line in lines:
            line = clean_text(line)
            if ":" in line:
                cat, items = line.split(":", 1)
                data["skills"].append({
                    "category": cat.strip(),
                    "items": [i.strip() for i in items.split(",")]
                })

    elif section == "experience":
        job_entry = {}
        details = []
        for line in lines:
            line = clean_text(line)
            # Date detection
            if re.search(r'\d{4}', line) and ("Present" in line or "-" in line):
                if job_entry: 
                    job_entry["details"] = details
                    data["experience"].append(job_entry)
                    details = []
                    job_entry = {}
                
                # Try to split "Company | Date" or "Date"
                if "|" in line:
                    parts = line.split("|")
                    job_entry["company"] = parts[0].strip()
                    job_entry["duration"] = parts[-1].strip()
                else:
                    job_entry["company"] = line # Fallback
                    job_entry["duration"] = "" # Fallback
            
            elif "Developer" in line or "Intern" in line:
                job_entry["role"] = line
            else:
                details.append(line)
        
        if job_entry:
            job_entry["details"] = details
            data["experience"].append(job_entry)

    elif section == "education":
        edu_entry = {}
        for line in lines:
            line = clean_text(line)
            if "B.Sc" in line or "HSC" in line:
                if edu_entry: data["education"].append(edu_entry)
                edu_entry = {"degree": line, "school": "", "year": "", "gpa": ""}
            elif "University" in line or "College" in line:
                if not edu_entry: edu_entry = {} 
                edu_entry["school"] = line
            elif re.search(r'\d{4}.*\d{4}', line):
                if not edu_entry: edu_entry = {}
                edu_entry["year"] = line
            elif "GPA" in line:
                if not edu_entry: edu_entry = {}
                edu_entry["gpa"] = line
            
        if edu_entry: data["education"].append(edu_entry)

    elif section == "languages":
        # Simply clean the lines and add them
        cleaned_langs = [clean_text(l) for l in lines]
        data["languages"] = cleaned_langs

    elif section == "projects":
        proj_entry = {}
        for line in lines:
            line = clean_text(line)
            # Detect GitHub link or Repository keyword
            if "GitHub" in line or "Repository" in line:
                if proj_entry: data["projects"].append(proj_entry)
                proj_entry = {
                    "name": line.split("|")[0].replace("GitHub Repository", "").strip(),
                    "link": "GitHub",
                    "description": ""
                }
            elif proj_entry:
                proj_entry["description"] += line + " "
        
        if proj_entry: data["projects"].append(proj_entry)

    elif section == "certifications":
        for line in lines:
            line = clean_text(line)
            if "|" in line:
                parts = line.split("|")
                name = parts[0].strip()
                date = parts[-1].strip() if len(parts) > 1 else ""
                data["certifications"].append({"name": name, "issuer": "", "date": date})
            # Fallback for lines that might look like "Name - Issuer"
            elif " - " in line:
                parts = line.split(" - ")
                data["certifications"].append({"name": parts[0].strip(), "issuer": parts[1].strip(), "date": ""})
            elif len(line) > 5 and "Credential" not in line: 
                # Avoid adding the word "Credential" as a cert
                data["certifications"].append({"name": line, "issuer": "", "date": ""})

def main():
    pdf_path = "Hasan_Mahmood_Resume.pdf"
    print(f"Processing {pdf_path}...")
    
    try:
        raw_text = extract_text_from_pdf(pdf_path)
        resume_json = parse_resume_text(raw_text)
        
        output_file = "resume_test2.json"
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(resume_json, f, indent=4)
            
    except FileNotFoundError:
        print("Error: PDF not found.")

if __name__ == "__main__":
    main()