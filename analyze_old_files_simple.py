#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1년 이상 된 구글 드라이브 파일 분석
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

# JWT 토큰
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54RU5xSWR2bUVKM25FM29TeU1Bb0pNUTlWcGVwNlRIaWU0a1JTT0NhYzQ1TXlrVkVQMXd6NG51T0RMZjdHdC1tN3RYeGNERVlNaTlrYVFodl9CMjhDenUtQS04REFTN0lLeUZuRXB4X3RTZ1FPTjFJVXJpN0xPQ1hkZ1g4REFVWk1XNVhEWkJjbzQzRXFZQ1gtR1M1bGt6bmpiREFobXRoclphQ2dZS0FWOFNBUThTRlFIR1gyTWk4aVlRMEFRM1ZRYnpkNE5jRTRTM1NRMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVrUzQyWWRZTUk3UUNnWUlBUkFBR0E0U053Ri1MOUlyQU80RHNCeS1nOTNvTjhFaGxEbzZEMjEzaHpvV3pfTEJrRnJNWl9iUVZuTnlSblJ3NmZNSlpGSFBqX0JtMF9fY0RDQSIsImV4cCI6MTc1NDcyMDEzOH0.M6l5tbB4txnIQqjKbfdXiqbTGpiecc-Ied-Dgr-Ktvc"

BASE_URL = "http://127.0.0.1:8888"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 기준 날짜 (1년 전: 2024년 8월 8일)
ONE_YEAR_AGO = datetime(2024, 8, 8)

print("=" * 70)
print("Google Drive Old Files Analysis")
print("=" * 70)
print(f"Cutoff Date: {ONE_YEAR_AGO.strftime('%Y-%m-%d')}")
print("-" * 70)

# 파일 목록 조회
print("\nFetching file list...")
response = requests.get(
    f"{BASE_URL}/files/list",
    headers=HEADERS,
    params={"include_folders": "true", "page_size": "1000"}
)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit(1)

data = response.json()
files = data.get('files', [])
print(f"Total files found: {len(files)}")

# 오래된 파일 분석
old_files = []
delete_candidates = []
important_files = []
total_size = 0

for file_info in files:
    modified_str = file_info.get('modifiedTime', '')
    if not modified_str:
        continue
    
    try:
        # 날짜 파싱
        modified_date = datetime.fromisoformat(modified_str.replace('Z', '+00:00'))
        
        # 1년 이상 된 파일 체크
        if modified_date.replace(tzinfo=None) < ONE_YEAR_AGO:
            name = file_info.get('name', '')
            mime_type = file_info.get('mimeType', '')
            size = int(file_info.get('size', 0))
            
            old_files.append({
                'name': name,
                'id': file_info.get('id'),
                'modified': modified_str[:10],
                'size_mb': round(size / (1024*1024), 2),
                'type': mime_type
            })
            
            total_size += size
            
            # 분류
            name_lower = name.lower()
            if any(word in name_lower for word in ['temp', 'test', 'copy', 'screenshot']):
                delete_candidates.append(name)
            elif any(word in name_lower for word in ['contract', 'wsop', 'ggpoker', 'okr']):
                important_files.append(name)
                
    except Exception as e:
        continue

# 결과 출력
print("\n" + "=" * 70)
print("ANALYSIS RESULTS")
print("=" * 70)

print(f"\nOld Files (1+ year): {len(old_files)}")
print(f"Total Size: {total_size/(1024*1024):.2f} MB ({total_size/(1024*1024*1024):.2f} GB)")

print(f"\nDelete Candidates: {len(delete_candidates)}")
if delete_candidates:
    print("Top 10:")
    for i, name in enumerate(delete_candidates[:10], 1):
        print(f"  {i}. {name[:60]}")

print(f"\nImportant Files (Keep): {len(important_files)}")
if important_files:
    print("Top 5:")
    for i, name in enumerate(important_files[:5], 1):
        print(f"  {i}. {name[:60]}")

# 파일별 상세 정보
print("\n" + "=" * 70)
print("DETAILED LIST (Top 20 oldest files)")
print("=" * 70)

# 날짜순 정렬
old_files.sort(key=lambda x: x['modified'])

for i, f in enumerate(old_files[:20], 1):
    print(f"{i:2}. [{f['modified']}] {f['name'][:50]} ({f['size_mb']} MB)")

# JSON 저장
with open('C:\\claude02\\old_files_report.json', 'w', encoding='utf-8') as f:
    json.dump({
        'summary': {
            'total_old_files': len(old_files),
            'total_size_mb': round(total_size/(1024*1024), 2),
            'delete_candidates': len(delete_candidates),
            'important_files': len(important_files)
        },
        'files': old_files[:50]  # 상위 50개만 저장
    }, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 70)
print("Report saved to: old_files_report.json")
print("=" * 70)