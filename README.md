# Encoded QR Code Resume System

<div align="center">

**A robust Python framework for encoding and decoding professional resume data through QR codes**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Protocol Buffers](https://img.shields.io/badge/Protocol_Buffers-3.0%2B-green.svg)](https://developers.google.com/protocol-buffers)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Detailed Usage](#detailed-usage)
- [Module Documentation](#module-documentation)
- [Protocol Buffer Schema](#protocol-buffer-schema)
- [Use Cases](#use-cases)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

The Encoded QR Code Resume System is a comprehensive toolkit designed to transform traditional resume documents into machine-readable QR codes and vice versa. By leveraging Protocol Buffers for efficient data serialization, this system enables the compact storage and rapid transmission of complete professional profiles through QR codes.

This solution bridges the gap between physical and digital resume presentation, allowing professionals to embed their entire career history in a scannable format suitable for business cards, portfolios, and digital platforms.

## Features

### Core Functionality

-  **PDF Processing**: Extract structured data from PDF resumes with high accuracy
-  **Bidirectional Conversion**: Seamlessly convert between PDF, JSON, and QR code formats
-  **Protocol Buffer Serialization**: Efficient binary encoding for minimal QR code complexity
-  **Link Extraction**: Automatically identify and process URLs from resume documents
-  **Skill Normalization**: Standardize technical skills using an intelligent ontology system
-  **Repository Matching**: Link GitHub repositories to portfolio projects automatically

### Advanced Features

- **Version Control**: Multiple PDF parsing implementations for different document structures
- **Ontology-Based Categorization**: Hierarchical skill classification system
- **Data Validation**: Ensure data integrity throughout the conversion pipeline
- **Extensible Schema**: Easily customizable Protocol Buffer definitions

## Architecture

```
┌─────────────┐
│   PDF       │
│  Document   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐        ┌──────────────┐
│  PDF Parser     │──────▶│    JSON      │
│  (v1 & v2)      │        │   Format     │
└─────────────────┘        └──────┬───────┘
                                  │
                                  ▼
                          ┌──────────────┐
                          │  Protobuf    │
                          │  Encoder     │
                          └──────┬───────┘
                                 │
                                 ▼
                          ┌──────────────┐
                          │   QR Code    │
                          │   Generator  │
                          └──────┬───────┘
                                 │
                                 ▼
                          ┌──────────────┐
                          │  QR Image    │
                          └──────────────┘
```

## Installation

### Prerequisites

Ensure you have Python 3.8 or higher installed on your system.

### Required Dependencies

```bash
# Core dependencies
pip install protobuf>=3.20.0
pip install qrcode[pil]>=7.4.0
pip install Pillow>=9.0.0

# PDF processing
pip install PyPDF2>=3.0.0
pip install pdfplumber>=0.9.0

# PDF generation
pip install reportlab>=4.0.0

# QR code scanning
pip install opencv-python>=4.7.0
pip install pyzbar>=0.1.9

# Additional utilities
pip install numpy>=1.24.0
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/NayemHasanLoLMan/Encoded-QR-Code.git
   cd Encoded-QR-Code
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Compile Protocol Buffers** (if modified)
   ```bash
   protoc --python_out=. resume.proto
   ```

## Quick Start

### Example Workflow

```bash
# Step 1: Convert PDF resume to JSON
python pdf_to_json.py sample_resume.pdf resume_data.json

# Step 2: Normalize skills and data
python skill_normalizer.py resume_data.json

# Step 3: Generate QR code
python json_to_qr.py resume_data.json resume_qr.png

# Step 4: Decode QR code back to JSON
python qr_to_json.py resume_qr.png decoded_resume.json

# Step 5: Generate PDF from decoded data
python json_to_pdf.py decoded_resume.json output_resume.pdf
```

## Detailed Usage

### PDF to JSON Conversion

**Version 1 (Basic)**
```python
from pdf_to_json import PDFToJSONConverter

converter = PDFToJSONConverter()
resume_data = converter.convert('input_resume.pdf')
converter.save_json(resume_data, 'output.json')
```

**Version 2 (Enhanced)**
```python
from pdf_to_json_V2 import EnhancedPDFConverter

converter = EnhancedPDFConverter()
resume_data = converter.extract_structured_data('input_resume.pdf')
converter.export_json(resume_data, 'output.json')
```

### JSON to QR Code

```python
from json_to_qr import ResumeQRGenerator

generator = ResumeQRGenerator()
generator.encode_resume('resume.json', 'output_qr.png', 
                       error_correction='H', 
                       box_size=10)
```

### QR Code to JSON

```python
from qr_to_json import QRResumeDecoder

decoder = QRResumeDecoder()
resume_data = decoder.decode_qr('resume_qr.png')
decoder.save_json(resume_data, 'decoded_resume.json')
```

### JSON to PDF Generation

```python
from json_to_pdf import ResumePDFGenerator

generator = ResumePDFGenerator()
generator.create_pdf('resume.json', 'output_resume.pdf',
                     template='professional',
                     font_size=11)
```

## Module Documentation

### Core Modules

#### `pdf_to_json.py`
Extracts resume data from PDF documents and converts it to a structured JSON format. Handles text extraction, section identification, and data parsing.

**Key Functions:**
- `extract_text(pdf_path)`: Extract raw text from PDF
- `parse_sections(text)`: Identify and parse resume sections
- `convert_to_json(pdf_path, output_path)`: Complete conversion pipeline

#### `json_to_qr.py`
Encodes JSON resume data into QR codes using Protocol Buffer serialization for optimal data compression.

**Key Functions:**
- `serialize_resume(json_data)`: Convert JSON to Protocol Buffer format
- `generate_qr(protobuf_data, output_path)`: Create QR code image
- `encode_resume(json_path, qr_output_path)`: End-to-end encoding

#### `qr_to_json.py`
Decodes QR codes containing resume data back into JSON format.

**Key Functions:**
- `scan_qr(image_path)`: Extract data from QR code image
- `deserialize_resume(protobuf_data)`: Convert Protocol Buffer to JSON
- `decode_resume(qr_path, json_output_path)`: Complete decoding pipeline

#### `json_to_pdf.py`
Generates professional PDF resumes from JSON data with customizable templates.

**Key Functions:**
- `load_template(template_name)`: Load PDF template
- `populate_data(template, json_data)`: Fill template with resume data
- `generate_pdf(json_path, pdf_output_path)`: Create final PDF

### Utility Modules

#### `link_extraction.py`
Extracts and validates URLs from resume documents, including email addresses, LinkedIn profiles, GitHub repositories, and portfolio websites.

#### `repo_matcher.py`
Matches GitHub repositories with projects listed in the resume using repository metadata and project descriptions.

#### `skill_normalizer.py`
Standardizes skill names to a canonical format (e.g., "JS" → "JavaScript", "React.js" → "React").

#### `skill_ontology.py`
Provides hierarchical categorization of technical skills into domains such as Programming Languages, Frameworks, Databases, and Tools.

## Protocol Buffer Schema

The `resume.proto` file defines the structured schema for resume data:

```protobuf
message Resume {
  PersonalInfo personal_info = 1;
  repeated Education education = 2;
  repeated Experience experience = 3;
  repeated Project projects = 4;
  SkillSet skills = 5;
  repeated Certification certifications = 6;
  repeated Language languages = 7;
  ContactLinks links = 8;
}

message PersonalInfo {
  string full_name = 1;
  string email = 2;
  string phone = 3;
  string location = 4;
  string summary = 5;
}

// Additional message definitions...
```

**Benefits of Protocol Buffers:**
- **Compact Size**: Binary encoding reduces QR code complexity
- **Type Safety**: Strongly typed data structures prevent errors
- **Version Compatibility**: Forward and backward compatible schema evolution
- **Cross-Platform**: Language-agnostic serialization format

## Use Cases

### Professional Networking
Embed complete resume data in business cards or conference badges for instant information sharing.

### Recruitment Technology
Enable rapid candidate profile scanning at career fairs and recruiting events.

### Portfolio Integration
Add machine-readable resume data to personal websites and online portfolios.

### ATS Compatibility
Generate standardized resume formats compatible with Applicant Tracking Systems.

### Data Portability
Transfer resume information seamlessly between different platforms and applications.

### Academic Applications
Share research profiles and academic CVs in a compact, scannable format.

## Contributing

We welcome contributions from the community! Please follow these guidelines:

### Development Process

1. **Fork the repository** and create your feature branch
   ```bash
   git checkout -b feature/YourFeatureName
   ```

2. **Make your changes** with clear, descriptive commits
   ```bash
   git commit -m "Add: Detailed description of your changes."
   ```

3. **Write or update tests** for your changes

4. **Ensure code quality**
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Update documentation as needed

5. **Push to your fork** and submit a pull request
   ```bash
   git push origin feature/YourFeatureName
   ```

### Code Style

- Use descriptive variable and function names
- Add type hints where appropriate
- Include error handling and logging
- Write comprehensive docstrings

### Reporting Issues

Please use the GitHub issue tracker to report bugs or suggest features. Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

**Nayem Hasan**

- GitHub: [@NayemHasanLoLMan](https://github.com/NayemHasanLoLMan)
- Project Link: [https://github.com/NayemHasanLoLMan/Encoded-QR-Code](https://github.com/NayemHasanLoLMan/Encoded-QR-Code)

## Acknowledgments

- **Google Protocol Buffers** for efficient data serialization
- **QR Code Libraries** for encoding and decoding functionality
- **PDF Processing Community** for parsing tools and techniques
- **Open Source Contributors** for continuous improvement and feedback

---

<div align="center">

**Built for the professional community**

Star this repository if you find it helpful!

</div>﻿# Encoded-QR-Code


