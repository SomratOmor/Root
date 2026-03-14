
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from SmritiCloudEngine import SmritiCloudEngine

app = Flask(__name__)
CORS(app)

# ১. সরাসরি এনভায়রনমেন্ট ভেরিয়েবল থেকে API KEY নেওয়া
# MASTER_API_KEY (immortalize এর জন্য) এবং SMRITI_KEY (sync-registry এর জন্য)
API_KEY = os.environ.get("MASTER_API_KEY")
SMRITI_SECRET_KEY = "Samrat_Omor_16_Year_Gift" # তোমার সেই ১৬ বছরের সিগনেচার কি

# ২. স্টোরেজ পাথ সেটআপ (নিশ্চিত করা যে ফোল্ডারগুলো আছে)
PHOTO_STORAGE = "Storage/User/File/Photo"
CORE_STORAGE = "Storage/Core"

os.makedirs(PHOTO_STORAGE, exist_ok=True)
os.makedirs(CORE_STORAGE, exist_ok=True)

engine = SmritiCloudEngine()

@app.route('/')
def home():
    return jsonify({
        "status": "Online", 
        "existence": "Verified", 
        "owner": "Somrat",
        "system": "Smriti Godday Engine",
        "security": "Active (ENV Mode)"
    })

# --- নতুন রুট: SmritiName ডোমেইন সিঙ্ক করার জন্য ---
@app.route('/api/v1/sync-registry', methods=['POST'])
def sync_registry():
    data = request.json
    auth_key = request.headers.get("X-Smriti-Key")
    
    # ১৬ বছরের সিক্রেট কি দিয়ে ভেরিফাই করা
    if auth_key != SMRITI_SECRET_KEY:
        return jsonify({"status": "failed", "message": "Unauthorized Access"}), 403
    
    if not data:
        return jsonify({"status": "failed", "message": "No data provided"}), 400

    # ডোমেইন লিস্ট মাস্টার ফাইলে অমর করা
    registry_file = os.path.join(CORE_STORAGE, "domain_registry_master.json")
    
    try:
        with open(registry_file, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        return jsonify({
            "status": "success", 
            "message": "Registry Immortalized in Master Host!",
            "file": "domain_registry_master.json"
        })
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

# --- বিদ্যমান রুট: ডেটা অমর (Immortalize) করার জন্য ---
@app.route('/api/v1/immortalize', methods=['POST'])
def process_data():
    # ৩. হেডার থেকে এপিআই কি যাচাই
    incoming_key = request.headers.get('X-API-KEY')
    
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
    full_path = os.path.join(PHOTO_STORAGE, json_filename)
    
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)