import PyPDF2

def extract_links(pdf_path):
    links = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            if '/Annots' in page:
                annotations = page['/Annots']
                for annot in annotations:
                    annot_obj = annot.get_object()
                    if annot_obj.get('/Subtype') == '/Link' and '/A' in annot_obj:
                        action = annot_obj['/A']
                        if '/URI' in action:
                            uri = action['/URI']
                            # Optionally, get the link's bounding box or nearby text for context
                            rect = annot_obj.get('/Rect')  # [x1, y1, x2, y2]
                            links.append({
                                'page': page_num + 1,
                                'url': uri,
                                'rect': rect
                            })
    return links

# Usage
pdf_file = 'Hasan_Mahmood_Resume.pdf'
extracted_links = extract_links(pdf_file)
for link in extracted_links:
    print(f"Page {link['page']}: {link['url']} at position {link['rect']}")