# import json
# import resume_pb2
# import qrcode
# import zlib
# import base64
# from google.protobuf.json_format import ParseDict

# def generate_qr_from_json(json_file, output_image="resume_qr.png"):
#     print(f"Reading data from {json_file}...")
    
#     # 1. Load JSON Data
#     try:
#         with open(json_file, 'r') as f:
#             data_dict = json.load(f)
#     except FileNotFoundError:
#         print("Error: resume.json file not found.")
#         return

#     # 2. Convert JSON to Protobuf Object
#     # ParseDict automatically handles the mapping if keys match the proto schema
#     try:
#         resume_proto = resume_pb2.Resume()
#         ParseDict(data_dict, resume_proto)
#     except Exception as e:
#         print(f"Error mapping JSON to Protobuf: {e}")
#         return

#     # 3. Serialize & Compress
#     binary_data = resume_proto.SerializeToString()
#     compressed_data = zlib.compress(binary_data)
#     final_payload = base64.b64encode(compressed_data).decode('utf-8')

#     # Stats
#     original_size = len(str(data_dict))
#     proto_size = len(binary_data)
#     compressed_size = len(final_payload)
    
#     print(f"🔸 Original JSON size: {original_size} bytes")
#     print(f"🔸 Binary Protobuf size: {proto_size} bytes")
#     print(f"🔸 Final QR Payload size: {compressed_size} bytes")
#     print(f"🔻 Compression Ratio: {round((1 - compressed_size/original_size)*100, 1)}% reduction")

#     # 4. Generate QR Code
#     qr = qrcode.QRCode(
#         version=None, # Auto-size
#         error_correction=qrcode.constants.ERROR_CORRECT_M,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(final_payload)
#     qr.make(fit=True)

#     img = qr.make_image(fill_color="black", back_color="white")
#     img.save(output_image)
#     print(f"Success! QR Code saved as '{output_image}'")

# if __name__ == "__main__":
#     generate_qr_from_json("resume.json", "Hasan_Resume_QR.png")





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
CHUNK_SIZE = 800  # Bytes per QR code

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

    # 2. Split into Chunks
    total_len = len(full_payload)
    num_chunks = math.ceil(total_len / CHUNK_SIZE)
    
    print(f"🔸 Total Data Size: {total_len} bytes")
    print(f"🔸 Splitting into {num_chunks} QR codes")

    chunks = []
    for i in range(num_chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        header = f"{i+1}/{num_chunks}|" 
        chunk_data = header + full_payload[start:end]
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
        
        # FIX: Add .convert('RGB') to ensure compatibility with the background
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_images.append(img)

    # 4. Create the Grid Image
    grid_size = math.ceil(math.sqrt(num_chunks))
    qr_w, qr_h = qr_images[0].size
    
    padding = 20 
    final_w = (qr_w * grid_size) + (padding * (grid_size + 1))
    final_h = (qr_h * grid_size) + (padding * (grid_size + 1))
    
    # White Background
    bg_color = (255, 255, 255)
    grid_img = Image.new('RGB', (final_w, final_h), bg_color)
    
    print(f"🔹 Assembling {grid_size}x{grid_size} grid...")

    for idx, img in enumerate(qr_images):
        row = idx // grid_size
        col = idx % grid_size
        x = padding + col * (qr_w + padding)
        y = padding + row * (qr_h + padding)
        
        # Paste works now because img is explicitly RGB
        grid_img.paste(img, (x, y))

    # 5. Save
    grid_img.save(output_image)
    print(f"Success! Saved grid image to: {output_image}")

if __name__ == "__main__":
    generate_grid_qr("resume_parsed_V2.json", "Hasan_Resume_Grid_QR.png")