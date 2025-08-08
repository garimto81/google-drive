#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 구글 드라이브 자동 정리
"""

import requests
import json
import time

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54RU5xSWR2bUVKM25FM29TeU1Bb0pNUTlWcGVwNlRIaWU0a1JTT0NhYzQ1TXlrVkVQMXd6NG51T0RMZjdHdC1tN3RYeGNERVlNaTlrYVFodl9CMjhDenUtQS04REFTN0lLeUZuRXB4X3RTZ1FPTjFJVXJpN0xPQ1hkZ1g4REFVWk1XNVhEWkJjbzQzRXFZQ1gtR1M1bGt6bmpiREFobXRoclphQ2dZS0FWOFNBUThTRlFIR1gyTWk4aVlRMEFRM1ZRYnpkNE5jRTRTM1NRMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVrUzQyWWRZTUk3UUNnWUlBUkFBR0E0U053Ri1MOUlyQU80RHNCeS1nOTNvTjhFaGxEbzZEMjEzaHpvV3pfTEJrRnJNWl9iUVZuTnlSblJ3NmZNSlpGSFBqX0JtMF9fY0RDQSIsImV4cCI6MTc1NDcyMDEzOH0.M6l5tbB4txnIQqjKbfdXiqbTGpiecc-Ied-Dgr-Ktvc"

BASE_URL = "http://127.0.0.1:8888"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("=" * 70)
print("Google Drive Auto Organization")
print("=" * 70)

# 1. 드라이브 분석
print("\n[1] Analyzing Drive...")
response = requests.get(f"{BASE_URL}/files/analyze", headers=HEADERS)

if response.status_code == 200:
    analysis = response.json()
    print(f"Total files: {analysis.get('analysis', {}).get('totalFiles', 0)}")
    print(f"Unorganized: {analysis.get('analysis', {}).get('unorganized', 0)}")
else:
    print(f"Analysis failed: {response.status_code}")

# 2. 자동 정리 시작
print("\n[2] Starting Organization...")

organize_data = {
    "auto_mode": True,
    "confidence_threshold": 0.7,
    "max_files": 100,
    "create_folders": True
}

response = requests.post(
    f"{BASE_URL}/organize/start",
    headers=HEADERS,
    json=organize_data
)

if response.status_code == 200:
    result = response.json()
    job_id = result.get('job_id')
    print(f"Job started: {job_id}")
    
    # 3. 진행 상황 모니터링
    print("\n[3] Monitoring Progress...")
    print("-" * 40)
    
    for i in range(60):  # 최대 2분 대기
        time.sleep(2)
        
        status_response = requests.get(
            f"{BASE_URL}/organize/status/{job_id}",
            headers=HEADERS
        )
        
        if status_response.status_code == 200:
            status = status_response.json()
            
            if status.get('status') == 'completed':
                print(f"\n[COMPLETED]")
                print(f"Processed: {status.get('processed_files', 0)} files")
                print(f"Organized: {status.get('organized_files', 0)} files")
                print(f"Errors: {len(status.get('errors', []))} files")
                break
            elif status.get('status') == 'failed':
                print(f"\n[FAILED] {status.get('error', 'Unknown error')}")
                break
            else:
                print(f"\rProgress: {status.get('progress', 0):.1f}%", end="")
        else:
            print(f"\n[ERROR] Status check failed: {status_response.status_code}")
            break
else:
    print(f"Failed to start: {response.status_code}")
    if response.text:
        print(f"Error: {response.text}")

print("\n" + "=" * 70)
print("Process Complete")
print("=" * 70)