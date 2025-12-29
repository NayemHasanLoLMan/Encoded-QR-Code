
# fuck its new 


import json
import zlib
import base64
import math
import qrcode
from PIL import Image
from google.protobuf.json_format import ParseDict
import resume_pb2 

# --- CONFIGURATION ---
FIXED_GRID_COUNT = 9  # Force exactly 9 QR codes (3x3)

def normalize_data(data):
    """Ensures data types match Protobuf schema."""
    if 'education' in data:
        for edu in data['education']:
            if isinstance(edu.get('achievements'), str):
                edu['achievements'] = [edu['achievements']]
            elif edu.get('achievements') is None:
                 edu['achievements'] = []
    if 'projects' in data:
        for proj in data['projects']:
            if isinstance(proj.get('technologies'), str):
                proj['technologies'] = [proj['technologies']]
            elif proj.get('technologies') is None:
                proj['technologies'] = []
    return data

def generate_grid_qr(json_file, output_image="Resume_Grid_QR.png"):
    print(f"🔹 Processing {json_file}...")
    
    # 1. Load & Process Data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return

    data = normalize_data(raw_data)
    
    try:
        resume_proto = resume_pb2.Resume()
        ParseDict(data, resume_proto, ignore_unknown_fields=True)
        binary_data = resume_proto.SerializeToString()
        compressed = zlib.compress(binary_data, level=9)
        full_payload = base64.b64encode(compressed).decode('utf-8')
    except Exception as e:
        print(f"Data processing error: {e}")
        return

    # 2. Split into EXACTLY 9 Chunks
    total_len = len(full_payload)
    # Calculate how many bytes per QR to fill exactly 9 spots
    chunk_size = math.ceil(total_len / FIXED_GRID_COUNT)
    
    print(f"🔸 Total Data Size: {total_len} bytes")
    print(f"🔸 Forcing 3x3 Grid (9 QRs)")
    print(f"🔸 Data per QR: ~{chunk_size} bytes (Very high readability)")

    chunks = []
    for i in range(FIXED_GRID_COUNT):
        start = i * chunk_size
        end = start + chunk_size
        
        # Safety check for last chunk
        if start >= total_len:
            payload_part = "" # Should not happen with math.ceil, but safe to handle
        else:
            payload_part = full_payload[start:end]

        header = f"{i+1}/{FIXED_GRID_COUNT}|" 
        chunk_data = header + payload_part
        chunks.append(chunk_data)

    # 3. Generate Individual QR Images
    qr_images = []
    for chunk in chunks:
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(chunk)
        qr.make(fit=True)
        # Convert to RGB to ensure Pillow compatibility
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_images.append(img)

    # 4. Create the 3x3 Grid Image
    grid_side = 3 # 3x3
    qr_w, qr_h = qr_images[0].size
    
    padding = 20 
    final_w = (qr_w * grid_side) + (padding * (grid_side + 1))
    final_h = (qr_h * grid_side) + (padding * (grid_side + 1))
    
    bg_color = (255, 255, 255)
    grid_img = Image.new('RGB', (final_w, final_h), bg_color)
    
    print(f"🔹 Assembling 3x3 grid...")

    for idx, img in enumerate(qr_images):
        row = idx // grid_side
        col = idx % grid_side
        x = padding + col * (qr_w + padding)
        y = padding + row * (qr_h + padding)
        
        grid_img.paste(img, (x, y))

    # 5. Save
    grid_img.save(output_image)
    print(f"Success! Saved 3x3 Grid QR to: {output_image}")

if __name__ == "__main__":
    generate_grid_qr("resume_parsed_V2.json", "Hasan_Resume_Grid_QR.png")