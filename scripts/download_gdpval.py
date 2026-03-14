#!/usr/bin/env python3
"""
Download GDPVal dataset from HuggingFace.
Places the parquet file at ./gdpval/data/train-00000-of-00001.parquet
as expected by the ClawWork LiveBench system.
"""
import os
import sys

DEST = "./gdpval/data/train-00000-of-00001.parquet"
URL = "https://huggingface.co/datasets/openai/gdpval/resolve/main/data/train-00000-of-00001.parquet"

def main():
    if os.path.exists(DEST) and os.path.getsize(DEST) > 10000:
        print(f"✅ GDPVal dataset already exists at {DEST}")
        return True
    
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    print(f"📥 Downloading GDPVal dataset from HuggingFace...")
    print(f"   URL: {URL}")
    print(f"   Destination: {DEST}")
    
    try:
        import urllib.request
        
        def progress(block_num, block_size, total_size):
            if total_size > 0:
                pct = min(100, block_num * block_size * 100 // total_size)
                sys.stdout.write(f"\r   Progress: {pct}%")
                sys.stdout.flush()
        
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(URL, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as response:
            with open(DEST, "wb") as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        
        print(f"\n✅ GDPVal dataset downloaded successfully ({os.path.getsize(DEST) / 1024 / 1024:.1f} MB)")
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to download via urllib: {e}")
        
        # Try with requests library
        try:
            import requests
            print("⏳ Trying with requests library...")
            r = requests.get(URL, stream=True, timeout=120)
            r.raise_for_status()
            with open(DEST, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ GDPVal dataset downloaded successfully ({os.path.getsize(DEST) / 1024 / 1024:.1f} MB)")
            return True
        except Exception as e2:
            print(f"❌ Also failed with requests: {e2}")
            return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
