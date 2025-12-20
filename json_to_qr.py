import json
import resume_pb2
import qrcode
import zlib
import base64
from google.protobuf.json_format import ParseDict

def generate_qr_from_json(json_file, output_image="resume_qr.png"):
    print(f"Reading data from {json_file}...")
    
    # 1. Load JSON Data
    try:
        with open(json_file, 'r') as f:
            data_dict = json.load(f)
    except FileNotFoundError:
        print("Error: resume.json file not found.")
        return

    # 2. Convert JSON to Protobuf Object
    # ParseDict automatically handles the mapping if keys match the proto schema
    try:
        resume_proto = resume_pb2.Resume()
        ParseDict(data_dict, resume_proto)
    except Exception as e:
        print(f"Error mapping JSON to Protobuf: {e}")
        return

    # 3. Serialize & Compress
    binary_data = resume_proto.SerializeToString()
    compressed_data = zlib.compress(binary_data)
    final_payload = base64.b64encode(compressed_data).decode('utf-8')

    # Stats
    original_size = len(str(data_dict))
    proto_size = len(binary_data)
    compressed_size = len(final_payload)
    
    print(f"🔸 Original JSON size: {original_size} bytes")
    print(f"🔸 Binary Protobuf size: {proto_size} bytes")
    print(f"🔸 Final QR Payload size: {compressed_size} bytes")
    print(f"🔻 Compression Ratio: {round((1 - compressed_size/original_size)*100, 1)}% reduction")

    # 4. Generate QR Code
    qr = qrcode.QRCode(
        version=None, # Auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(final_payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_image)
    print(f"Success! QR Code saved as '{output_image}'")

if __name__ == "__main__":
    generate_qr_from_json("resume.json", "Hasan_Resume_QR.png")