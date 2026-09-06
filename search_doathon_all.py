# -*- coding: utf-8 -*-
import os
import sys
import glob
sys.stdout.reconfigure(encoding='utf-8')
from recognition.vision_service import VisionService

vs = VisionService('database')
all_pngs = sorted(glob.glob('uploads/*.png'))
print(f"Scanning {len(all_pngs)} uploads...")

found_files = []
for p in all_pngs:
    res = vs.recognize_with_local_ocr(p)
    # Check if Đoạt Hồn was detected
    if any("Đoạt Hồn" in t or "Hiệp Phách" in t for t in res.get("tactics", [])):
        found_files.append((p, res.get("tactics", [])))

print(f"\nFiles with Đoạt Hồn Hiệp Phách detected: {len(found_files)}")
for f, tacs in found_files[:10]:
    print(f"  * {os.path.basename(f)}: {tacs}")

# If none detected, check raw OCR on all uploads to see where Đoạt Hồn is
if len(found_files) == 0:
    print("\nScanning raw OCR text for 'đoạt' or 'hồn' or 'phách'...")
    for p in all_pngs:
        ocr_res, _ = vs.ocr_engine(p)
        if ocr_res:
            lines = [l[1] for l in ocr_res]
            for l in lines:
                if any(w in l.lower() for w in ['đoạt', 'doat', 'hồn', 'hon', 'phách', 'phach']):
                    print(f"  * RAW MATCH in {os.path.basename(p)}: '{l}'")
