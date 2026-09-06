# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import glob
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
files = sorted(glob.glob('uploads/*.png'))
unique_by_size = {}
for f in files:
    sz = os.path.getsize(f)
    if sz not in unique_by_size:
        unique_by_size[sz] = f

print(f"Scanning {len(unique_by_size)} unique screenshots...")
sys.stdout.flush()

for sz, f in unique_by_size.items():
    res, _ = engine(f)
    if res:
        lines = [line[1] for line in res]
        full_text = " ".join(lines)
        # Check if Đoạt Hồn or similar
        keywords = [l for l in lines if any(w in l.lower() for w in ["doat", "đoạt", "hon", "hồn", "phach", "phách", "doạt", "đoat"])]
        if keywords:
            print(f"\n[!!!] KEYWORD MATCH in {os.path.basename(f)}:")
            print("   Lines:", keywords)
        
        # Also print what this screenshot seems to be
        tactic_headers = [l for l in lines if any(w in l.lower() for w in ["chu dong", "bi dong", "dot kich", "binh chung", "phap tran", "chi huy"])]
        if len(tactic_headers) >= 3:
            # This is a tactic screenshot
            print(f"\nTactic Screen: {os.path.basename(f)}")
            print("   Sample lines:", lines[10:25])
    sys.stdout.flush()
