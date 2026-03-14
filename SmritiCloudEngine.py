import hashlib

class SmritiCloudEngine:
    def __init__(self):
        pass

    def generate_byte_index(self, input_string):
        # ১.২ বাইট লেভেলের ইউনিক আইডি জেনারেটর
        hash_object = hashlib.md5(input_string.encode())
        return hash_object.hexdigest()[:8]
