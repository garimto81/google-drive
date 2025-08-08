#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6개월 이상 사용하지 않은 구글 드라이브 파일 분석
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

# JWT 토큰
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54RU5xSWR2bUVKM25FM29TeU1Bb0pNUTlWcGVwNlRIaWU0a1JTT0NhYzQ1TXlrVkVQMXd6NG51T0RMZjdHdC1tN3RYeGNERVlNaTlrYVFodl9CMjhDenUtQS04REFTN0lLeUZuRXB4X3RTZ1FPTjFJVXJpN0xPQ1hkZ1g4REFVWk1XNVhEWkJjbzQzRXFZQ1gtR1M1bGt6bmpiREFobXRoclphQ2dZS0FWOFNBUThTRlFIR1gyTWk4aVlRMEFRM1ZRYnpkNE5jRTRTM1NRMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVrUzQyWWRZTUk3UUNnWUlBUkFBR0E0U053Ri1MOUlyQU80RHNCeS1nOTNvTjhFaGxEbzZEMjEzaHpvV3pfTEJrRnJNWl9iUVZuTnlSblJ3NmZNSlpGSFBqX0JtMF9fY0RDQSIsImV4cCI6MTc1NDcyMDEzOH0.M6l5tbB4txnIQqjKbfdXiqbTGpiecc-Ied-Dgr-Ktvc"

BASE_URL = "http://127.0.0.1:8888"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 기준 날짜들
SIX_MONTHS_AGO = datetime(2025, 2, 8)  # 6개월 전
THREE_MONTHS_AGO = datetime(2025, 5, 8)  # 3개월 전
ONE_MONTH_AGO = datetime(2025, 7, 8)  # 1개월 전

print("=" * 70)
print("Google Drive File Age Analysis")
print("=" * 70)
print(f"Today: 2025-08-08")
print(f"6 months ago: {SIX_MONTHS_AGO.strftime('%Y-%m-%d')}")
print(f"3 months ago: {THREE_MONTHS_AGO.strftime('%Y-%m-%d')}")
print("-" * 70)

# 파일 목록 조회
print("\nFetching all files...")
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
print(f"Total items found: {len(files)}")

# 파일 분석
categories = {
    'over_6_months': [],
    'over_3_months': [],
    'over_1_month': [],
    'recent': [],
    'no_date': []
}

file_types = defaultdict(int)
total_sizes = defaultdict(int)

for file_info in files:
    modified_str = file_info.get('modifiedTime', '')
    name = file_info.get('name', '')
    mime_type = file_info.get('mimeType', '')
    size = int(file_info.get('size', 0))
    
    # 파일 타입 카운트
    if 'folder' in mime_type:
        file_types['Folders'] += 1
    elif 'spreadsheet' in mime_type:
        file_types['Spreadsheets'] += 1
    elif 'presentation' in mime_type:
        file_types['Presentations'] += 1
    elif 'document' in mime_type:
        file_types['Documents'] += 1
    elif 'video' in mime_type:
        file_types['Videos'] += 1
    elif 'image' in mime_type:
        file_types['Images'] += 1
    elif 'colaboratory' in mime_type:
        file_types['Colab'] += 1
    else:
        file_types['Others'] += 1
    
    if not modified_str:
        categories['no_date'].append(name)
        continue
    
    try:
        # 날짜 파싱
        modified_date = datetime.fromisoformat(modified_str.replace('Z', '+00:00'))
        modified_date = modified_date.replace(tzinfo=None)
        
        file_data = {
            'name': name,
            'id': file_info.get('id'),
            'modified': modified_str[:10],
            'size_mb': round(size / (1024*1024), 2),
            'type': mime_type,
            'parents': file_info.get('parents', [])
        }
        
        # 기간별 분류
        if modified_date < SIX_MONTHS_AGO:
            categories['over_6_months'].append(file_data)
            total_sizes['over_6_months'] += size
        elif modified_date < THREE_MONTHS_AGO:
            categories['over_3_months'].append(file_data)
            total_sizes['over_3_months'] += size
        elif modified_date < ONE_MONTH_AGO:
            categories['over_1_month'].append(file_data)
            total_sizes['over_1_month'] += size
        else:
            categories['recent'].append(file_data)
            total_sizes['recent'] += size
            
    except Exception as e:
        categories['no_date'].append(name)

# 결과 출력
print("\n" + "=" * 70)
print("FILE AGE DISTRIBUTION")
print("=" * 70)

print(f"\nOver 6 months old: {len(categories['over_6_months'])} files")
print(f"  Total size: {total_sizes['over_6_months']/(1024*1024):.2f} MB")

print(f"\n3-6 months old: {len(categories['over_3_months'])} files")
print(f"  Total size: {total_sizes['over_3_months']/(1024*1024):.2f} MB")

print(f"\n1-3 months old: {len(categories['over_1_month'])} files")
print(f"  Total size: {total_sizes['over_1_month']/(1024*1024):.2f} MB")

print(f"\nLess than 1 month: {len(categories['recent'])} files")
print(f"  Total size: {total_sizes['recent']/(1024*1024):.2f} MB")

print(f"\nNo date info: {len(categories['no_date'])} items")

# 파일 타입별 통계
print("\n" + "=" * 70)
print("FILE TYPE DISTRIBUTION")
print("=" * 70)
for ftype, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
    print(f"{ftype}: {count}")

# 6개월 이상 된 파일 중 삭제 대상 분석
print("\n" + "=" * 70)
print("DELETE CANDIDATES (6+ months old)")
print("=" * 70)

delete_candidates = []
keep_important = []

for f in categories['over_6_months']:
    name_lower = f['name'].lower()
    
    # 삭제 대상 패턴
    if any(word in name_lower for word in ['temp', 'test', 'copy', 'backup', 'old', 'screenshot', 'untitled']):
        delete_candidates.append(f)
    # 중요 파일 패턴
    elif any(word in name_lower for word in ['contract', 'wsop', 'ggpoker', 'okr', 'report', 'budget']):
        keep_important.append(f)
    # 나머지는 검토 필요
    else:
        pass

print(f"\nRecommended for deletion: {len(delete_candidates)} files")
if delete_candidates:
    print("Top 10 delete candidates:")
    # 크기 순으로 정렬
    delete_candidates.sort(key=lambda x: x['size_mb'], reverse=True)
    for i, f in enumerate(delete_candidates[:10], 1):
        print(f"  {i}. {f['name'][:50]} ({f['size_mb']} MB) - {f['modified']}")
    
    total_delete_size = sum(f['size_mb'] for f in delete_candidates)
    print(f"\n  Total size to free up: {total_delete_size:.2f} MB")

print(f"\nImportant files to keep: {len(keep_important)} files")
if keep_important:
    print("Top 5 important files:")
    for i, f in enumerate(keep_important[:5], 1):
        print(f"  {i}. {f['name'][:50]} - {f['modified']}")

# 최근 수정 파일
print("\n" + "=" * 70)
print("RECENTLY MODIFIED FILES (Last month)")
print("=" * 70)
if categories['recent']:
    # 날짜순 정렬
    categories['recent'].sort(key=lambda x: x['modified'], reverse=True)
    print(f"Top 10 recently modified:")
    for i, f in enumerate(categories['recent'][:10], 1):
        print(f"  {i}. [{f['modified']}] {f['name'][:50]}")

# 루트 폴더에 있는 6개월 이상 파일
print("\n" + "=" * 70)
print("OLD FILES IN ROOT FOLDER (6+ months)")
print("=" * 70)
root_old_files = [f for f in categories['over_6_months'] 
                  if not f['parents'] or f['parents'] == ['0ANnZEeohyvlsUk9PVA']]
print(f"Files in root: {len(root_old_files)}")
if root_old_files:
    for i, f in enumerate(root_old_files[:10], 1):
        print(f"  {i}. {f['name'][:60]} - {f['modified']}")

# JSON 저장
report = {
    'summary': {
        'total_files': len(files),
        'over_6_months': len(categories['over_6_months']),
        'over_3_months': len(categories['over_3_months']),
        'over_1_month': len(categories['over_1_month']),
        'recent': len(categories['recent']),
        'delete_candidates': len(delete_candidates),
        'size_to_free_mb': sum(f['size_mb'] for f in delete_candidates)
    },
    'delete_candidates': delete_candidates[:20],
    'root_old_files': root_old_files[:20]
}

with open('C:\\claude02\\6months_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 70)
print("Report saved to: 6months_analysis.json")
print("=" * 70)