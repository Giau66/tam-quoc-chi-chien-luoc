# -*- coding: utf-8 -*-
import os
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')
from rapidocr_onnxruntime import RapidOCR
from recognition.vision_service import VisionService

vs = VisionService()
engine = RapidOCR()
uploads_dir = "uploads"

# Focus on screenshots from 1959 to 2001 (which are tactics screenshots)
tac_files = [f for f in os.listdir(uploads_dir) if any(ts in f for ts in ["1958", "1959", "2000", "2001", "tactic"])]
# Group unique
seen = set()
unique_files = []
for f in tac_files:
    suffix = f.split('_', 1)[1] if '_' in f else f
    if suffix not in seen:
        seen.add(suffix)
        unique_files.append((suffix, os.path.join(uploads_dir, f)))

print(f"Testing {len(unique_files)} tactic screenshots...")
sys.stdout.flush()

for suffix, path in unique_files:
    res, _ = engine(path)
    if res:
        raw_texts = [line[1] for line in res]
        matched = vs.match_entities(raw_texts)
        # Check if Đoạt Hồn or similar appears in raw_texts
        keywords = [t for t in raw_texts if any(k in t.lower() for k in ['đoạt', 'doat', 'hồn', 'hon', 'phách', 'phach', 'thái bình', 'quân dân', 'thảo thuyền'])]
        print(f"\n--- File: {suffix} ---")
        if keywords:
            print(f"  * RAW KEYWORDS: {keywords}")
        print(f"  * Detected tactics ({len(matched['tactics'])}): {matched['tactics']}")
        print(f"  * All raw texts: {raw_texts[:15]}")
        sys.stdout.flush()
