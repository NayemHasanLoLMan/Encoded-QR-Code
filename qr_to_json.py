import resume_pb2
from pyzbar.pyzbar import decode
from PIL import Image
import zlib
import base64
from google.protobuf.json_format import MessageToJson

def decode_qr_to_json(image_path):
    print(f"🔹 Scanning {image_path}...")
    
    # 1. Read QR
    img = Image.open(image_path)
    decoded_objects = decode(img)
    
    if not decoded_objects:
        print("No QR code found.")
        return

    payload = decoded_objects[0].data.decode('utf-8')

    # 2. Decompress & Deserialize
    try:
        compressed_data = base64.b64decode(payload)
        binary_data = zlib.decompress(compressed_data)
        
        resume_proto = resume_pb2.Resume()
        resume_proto.ParseFromString(binary_data)
        
        # 3. Convert back to JSON for display
        json_output = MessageToJson(resume_proto, preserving_proto_field_name=True)
        print("decoded Successfully! Here is the data:")
        print(json_output)
        
    except Exception as e:
        print(f"Error decoding: {e}")

if __name__ == "__main__":
    decode_qr_to_json("Hasan_Resume_QR.png")