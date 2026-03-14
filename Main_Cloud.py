import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from SmritiCloudEngine import SmritiCloudEngine

app = Flask(__name__)
CORS(app)

# ১. সরাসরি এনভায়রনমেন্ট ভেরিয়েবল থেকে API KEY নেওয়া
# কোডে কোনো ডিফল্ট পাসওয়ার্ড রাখা হয়নি
API_KEY = os.environ.get("MASTER_API_KEY")

# ২. স্টোরেজ পাথ সেটআপ (নিশ্চিত করা যে ফোল্ডারটি আছে)
STORAGE_PATH = "Storage/User/File/Photo"
os.makedirs(STORAGE_PATH, exist_ok=True)

engine = SmritiCloudEngine()

@app.route('/')
def home():
    return jsonify({
        "status": "Online", 
        "existence": "Verified", 
        "owner": "Somrat",
        "security": "Active (ENV Mode)"
    })

@app.route('/api/v1/immortalize', methods=['POST'])
def process_data():
    # ৩. হেডার থেকে এপিআই কি যাচাই
    incoming_key = request.headers.get('X-API-KEY')
    
    # যদি ENV সেট না থাকে বা কি না মিলে তবে ৪০১ এরর দিবে
    if not API_KEY or incoming_key != API_KEY:
        return jsonify({"error": "Unauthorized: API Key mismatch or missing in ENV"}), 401

    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request body"}), 400

    pic_name = data.get("name")
    
    # ৪. ১.২ বাইট ইঞ্জিন প্রসেসিং
    processed_index = engine.generate_byte_index(pic_name)

    # ৫. মেটাডেটা ফাইল হিসেবে সেভ করা
    json_filename = f"{pic_name}.json"
    full_path = os.path.join(STORAGE_PATH, json_filename)
    
    metadata = {
        "name": pic_name,
        "index": processed_index,
        "status": "Immortal",
        "timestamp": "2026-03-14",
        "cloud_type": "Master_Host"
    }
    
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
    except Exception as e:
        return jsonify({"error": f"Storage Write Failed: {str(e)}"}), 500

    return jsonify({
        "status": "Success", 
        "index": processed_index, 
        "saved_at": json_filename
    })

if __name__ == "__main__":
    # রেন্ডার অটোমেটিক পোর্ট ভেরিয়েবল দেয়
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)