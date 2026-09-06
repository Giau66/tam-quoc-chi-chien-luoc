# -*- coding: utf-8 -*-
from rapidocr_onnxruntime import RapidOCR
import glob
import os

engine = RapidOCR()
uploads = sorted(glob.glob("d:/TamQuocChiChienLuoc/uploads/*.png"))

print(f"Found {len(uploads)} uploads.")
for p in uploads[-5:]:
    print(f"\n=======================================================")
    print(f"OCR Testing: {os.path.basename(p)}")
    print(f"=======================================================")
    res, elapse = engine(p)
    if res:
        for box, text, score in res:
            sc = float(score)
            if sc > 0.4:
                print(f"  [{sc:.2f}] {text}")
    else:
        print("  (No text detected)")
