# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import os
from rapidocr_onnxruntime import RapidOCR
from recognition.vision_service import VisionService

vs = VisionService('database')
engine = RapidOCR()
uploads = sorted(glob.glob('uploads/*.png'))

print(f"Total uploads: {len(uploads)}")

found_count = 0
for p in uploads:
    res, _ = engine(p)
    if res:
        lines = [line[1] for line in res]
        full_text = " ".join(lines)
        if any(w in full_text.lower() for w in ["doat", "đoạt", "hon", "hồn", "phach", "phách"]):
            found_count += 1
            print(f"\nFOUND MATCH in {os.path.basename(p)}:")
            for l in lines:
                if any(w in l.lower() for w in ["doat", "đoạt", "hon", "hồn", "phach", "phách"]):
                    print(f"  Line: '{l}'")
            matched = vs.recognize_with_local_ocr(p)
            print(f"  VisionService tactics detected: {matched['tactics']}")

print(f"\nTotal files with Đoạt Hồn / Hiệp Phách: {found_count}")

