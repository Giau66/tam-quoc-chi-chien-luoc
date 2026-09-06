# -*- coding: utf-8 -*-
import os
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
uploads_dir = "uploads"
files = sorted([f for f in os.listdir(uploads_dir) if f.endswith('.png')])

print(f"Total uploaded png files: {len(files)}")

# Group by original screenshot name
seen_timestamps = {}
for f in files:
    # Example: 021335c6_Screenshot 2026-09-05 195935.png
    parts = f.split('_', 1)
    orig_name = parts[1] if len(parts) > 1 else f
    if orig_name not in seen_timestamps:
        seen_timestamps[orig_name] = os.path.join(uploads_dir, f)

print(f"Unique screenshots: {len(seen_timestamps)}")

for orig_name, path in seen_timestamps.items():
    res, _ = engine(path)
    if res:
        texts = [line[1] for line in res]
        full_text = " | ".join(texts)
        # Check if 'đoạt' or 'hồn' or 'phách' or any tactic words exist
        matched = [t for t in texts if any(k in t.lower() for k in ['đoạt', 'doat', 'hồn', 'hon', 'phách', 'phach', 'thái bình', 'quân dân', 'thảo thuyền'])]
        if matched or 'doat' in full_text.lower() or 'hon' in full_text.lower():
            print(f"\nFOUND in {orig_name}:")
            print(f"   Matched: {matched}")
            print(f"   Sample text: {full_text[:200]}")
