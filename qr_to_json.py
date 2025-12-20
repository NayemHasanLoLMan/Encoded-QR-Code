# import resume_pb2
# from pyzbar.pyzbar import decode
# from PIL import Image
# import zlib
# import base64
# from google.protobuf.json_format import MessageToJson

# def decode_qr_to_json(image_path):
#     print(f"🔹 Scanning {image_path}...")
    
#     # 1. Read QR
#     img = Image.open(image_path)
#     decoded_objects = decode(img)
    
#     if not decoded_objects:
#         print("No QR code found.")
#         return

#     payload = decoded_objects[0].data.decode('utf-8')

#     # 2. Decompress & Deserialize
#     try:
#         compressed_data = base64.b64decode(payload)
#         binary_data = zlib.decompress(compressed_data)
        
#         resume_proto = resume_pb2.Resume()
#         resume_proto.ParseFromString(binary_data)
        
#         # 3. Convert back to JSON for display
#         json_output = MessageToJson(resume_proto, preserving_proto_field_name=True)
#         print("decoded Successfully! Here is the data:")
#         print(json_output)
        
#     except Exception as e:
#         print(f"Error decoding: {e}")

# if __name__ == "__main__":
#     decode_qr_to_json("Hasan_Resume_QR.png")



# Mf its new too


import json
import zlib
import base64
from PIL import Image
from pyzbar.pyzbar import decode
from google.protobuf.json_format import MessageToDict
import resume_pb2

def decode_grid_qr(image_path):
    print(f"🔹 Scanning grid image: {image_path}...")
    
    try:
        img = Image.open(image_path)
        decoded_objects = decode(img)
    except Exception as e:
        print(f"Error reading image: {e}")
        return

    if not decoded_objects:
        print("No QR codes found.")
        return

    print(f"🔸 Found {len(decoded_objects)} QR code segments.")

    # 1. Extract and Sort Chunks
    segments = {}
    total_chunks = 0
    
    for obj in decoded_objects:
        raw_text = obj.data.decode('utf-8')
        
        # Parse Header "Index/Total|Data"
        try:
            if '|' in raw_text:
                header, content = raw_text.split('|', 1)
                index, total = map(int, header.split('/'))
                segments[index] = content
                total_chunks = total
            else:
                # Fallback for single QR if header is missing
                print("Warning: Found data without header. Assuming single QR.")
                segments[1] = raw_text
                total_chunks = 1
                
        except ValueError:
            continue

    # 2. Verification
    if len(segments) != total_chunks:
        print(f"Incomplete data! Found {len(segments)} of {total_chunks} parts.")
        return

    print("All segments present. Reassembling...")
    
    # 3. Reassemble
    full_payload_b64 = ""
    for i in range(1, total_chunks + 1):
        full_payload_b64 += segments[i]

    # 4. Decode & Decompress
    try:
        compressed_data = base64.b64decode(full_payload_b64)
        binary_data = zlib.decompress(compressed_data)
        
        resume_proto = resume_pb2.Resume()
        resume_proto.ParseFromString(binary_data)
        
        # FIX: Removed 'including_default_value_fields' to fix compatibility error
        resume_dict = MessageToDict(
            resume_proto, 
            preserving_proto_field_name=True
        )
        
        print(" RESUME RESTORED SUCCESSFULLY ")

        
        # Print basic stats to verify
        name = resume_dict.get('name', 'Unknown')
        print(f"Name: {name}")
        
        # Handle potential missing keys gracefully for display
        summary = resume_dict.get('summary', '')
        print(f"Summary Length: {len(summary)} chars")
        
        exp = resume_dict.get('experience', [])
        print(f"Experience Entries: {len(exp)}")
        
        # Save to file
        output_filename = "restored_full_resume.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(resume_dict, f, indent=2, ensure_ascii=False)
            print(f"\nFull data saved to '{output_filename}'")

    except Exception as e:
        print(f"Error during decompression/parsing: {e}")

if __name__ == "__main__":
    decode_grid_qr("Hasan_Resume_Grid_QR.png")