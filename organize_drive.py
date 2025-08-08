#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
구글 드라이브 정리 실행 스크립트
"""

import requests
import json
import time
from datetime import datetime

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54RU5xSWR2bUVKM25FM29TeU1Bb0pNUTlWcGVwNlRIaWU0a1JTT0NhYzQ1TXlrVkVQMXd6NG51T0RMZjdHdC1tN3RYeGNERVlNaTlrYVFodl9CMjhDenUtQS04REFTN0lLeUZuRXB4X3RTZ1FPTjFJVXJpN0xPQ1hkZ1g4REFVWk1XNVhEWkJjbzQzRXFZQ1gtR1M1bGt6bmpiREFobXRoclphQ2dZS0FWOFNBUThTRlFIR1gyTWk4aVlRMEFRM1ZRYnpkNE5jRTRTM1NRMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVrUzQyWWRZTUk3UUNnWUlBUkFBR0E0U053Ri1MOUlyQU80RHNCeS1nOTNvTjhFaGxEbzZEMjEzaHpvV3pfTEJrRnJNWl9iUVZuTnlSblJ3NmZNSlpGSFBqX0JtMF9fY0RDQSIsImV4cCI6MTc1NDcyMDEzOH0.M6l5tbB4txnIQqjKbfdXiqbTGpiecc-Ied-Dgr-Ktvc"

BASE_URL = "http://127.0.0.1:8888"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

print("=" * 70)
print("GOOGLE DRIVE ORGANIZATION PROCESS")
print("=" * 70)
print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 70)

# 1단계: 메인 폴더 구조 생성
print("\n[STEP 1] Creating Main Folder Structure")
print("-" * 40)

main_folders = [
    {"name": "01_프로젝트", "subfolders": ["WSOP", "GGPoker_Production", "YouTube_Content"]},
    {"name": "02_운영관리", "subfolders": ["인력관리", "장비관리", "보고서", "문서보관"]},
    {"name": "03_개발_및_데이터", "subfolders": ["Colab_Notebooks", "데이터분석", "Archive_MAM"]},
    {"name": "04_미디어_자료", "subfolders": ["동영상", "이미지", "오디오"]},
    {"name": "05_외부협업", "subfolders": ["NSUSLAB", "외주업체", "파트너", "Corey_Channel"]},
    {"name": "99_임시", "subfolders": []}
]

created_folders = {}

def create_folder(name, parent_id=None):
    """폴더 생성 함수"""
    try:
        data = {"name": name}
        if parent_id:
            data["parent_id"] = parent_id
            
        response = requests.post(
            f"{BASE_URL}/folders/create",
            headers=HEADERS,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            folder_id = result.get('folder', {}).get('id')
            print(f"  [OK] Created: {name}")
            return folder_id
        else:
            print(f"  [FAIL] {name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
        return None

# 메인 폴더 생성
for folder_info in main_folders:
    main_name = folder_info["name"]
    print(f"\nCreating: {main_name}")
    
    # 메인 폴더 생성
    main_id = create_folder(main_name)
    if main_id:
        created_folders[main_name] = main_id
        
        # 서브 폴더 생성
        for sub_name in folder_info["subfolders"]:
            sub_id = create_folder(sub_name, main_id)
            if sub_id:
                created_folders[f"{main_name}/{sub_name}"] = sub_id
            time.sleep(0.5)  # API 호출 제한 방지

# 2단계: WSOP 하위 폴더 생성
print("\n[STEP 2] Creating WSOP Subfolders")
print("-" * 40)

wsop_id = created_folders.get("01_프로젝트/WSOP")
if wsop_id:
    wsop_subfolders = [
        "2024_WSOPE",
        "2025_WSOP", 
        "Creator_Program",
        "체크리스트",
        "예산계획",
        "현장자료"
    ]
    
    for subfolder in wsop_subfolders:
        sub_id = create_folder(subfolder, wsop_id)
        if sub_id:
            created_folders[f"01_프로젝트/WSOP/{subfolder}"] = sub_id
        time.sleep(0.5)

# 3단계: GGPoker 하위 폴더 생성
print("\n[STEP 3] Creating GGPoker Subfolders")
print("-" * 40)

ggpoker_id = created_folders.get("01_프로젝트/GGPoker_Production")
if ggpoker_id:
    ggpoker_subfolders = {
        "LiveStream": ["방송계획", "기술문서", "성과분석"],
        "Marketing": ["프레젠테이션", "캠페인", "분석리포트"],
        "Performance": ["주간리포트", "월간분석", "KPI추적"],
        "방송설계": ["시스템구성도", "장비명세", "운영매뉴얼"]
    }
    
    for main_sub, sub_subs in ggpoker_subfolders.items():
        main_sub_id = create_folder(main_sub, ggpoker_id)
        if main_sub_id:
            created_folders[f"01_프로젝트/GGPoker_Production/{main_sub}"] = main_sub_id
            
            for sub_sub in sub_subs:
                sub_sub_id = create_folder(sub_sub, main_sub_id)
                if sub_sub_id:
                    created_folders[f"01_프로젝트/GGPoker_Production/{main_sub}/{sub_sub}"] = sub_sub_id
                time.sleep(0.5)

# 4단계: 파일 목록 조회
print("\n[STEP 4] Fetching Files to Organize")
print("-" * 40)

response = requests.get(
    f"{BASE_URL}/files/list",
    headers=HEADERS,
    params={"include_folders": "true", "page_size": "1000"}
)

if response.status_code != 200:
    print(f"[ERROR] Failed to fetch files: {response.status_code}")
    exit(1)

data = response.json()
files = data.get('files', [])
print(f"Total files found: {len(files)}")

# 5단계: 파일 분류 및 이동 규칙
print("\n[STEP 5] Organizing Files")
print("-" * 40)

move_rules = {
    # WSOP 관련
    "wsop": "01_프로젝트/WSOP",
    "wsope": "01_프로젝트/WSOP/2024_WSOPE",
    "cyprus": "01_프로젝트/WSOP/2024_WSOPE",
    "bahamas": "01_프로젝트/WSOP/2025_WSOP",
    "checklist": "01_프로젝트/WSOP/체크리스트",
    
    # GGPoker 관련
    "ggpoker": "01_프로젝트/GGPoker_Production",
    "ggm": "01_프로젝트/GGPoker_Production",
    "performance": "01_프로젝트/GGPoker_Production/Performance",
    "livestream": "01_프로젝트/GGPoker_Production/LiveStream",
    "방송": "01_프로젝트/GGPoker_Production/방송설계",
    
    # YouTube/Corey
    "corey": "05_외부협업/Corey_Channel",
    "youtube": "01_프로젝트/YouTube_Content",
    
    # 보고서
    "보고서": "02_운영관리/보고서",
    "report": "02_운영관리/보고서",
    "okr": "02_운영관리/보고서",
    
    # 인력/장비
    "인력": "02_운영관리/인력관리",
    "충원": "02_운영관리/인력관리",
    "장비": "02_운영관리/장비관리",
    "견적": "02_운영관리/장비관리",
    
    # 데이터/개발
    "colab": "03_개발_및_데이터/Colab_Notebooks",
    ".ipynb": "03_개발_및_데이터/Colab_Notebooks",
    "data": "03_개발_및_데이터/데이터분석",
    "player": "03_개발_및_데이터/데이터분석",
    
    # PDF 문서
    ".pdf": "02_운영관리/문서보관",
    
    # 미디어
    ".mp4": "04_미디어_자료/동영상",
    ".jpg": "04_미디어_자료/이미지",
    ".png": "04_미디어_자료/이미지",
    
    # 외부협업
    "nsuslab": "05_외부협업/NSUSLAB",
}

def move_file(file_id, folder_id, file_name):
    """파일 이동 함수"""
    try:
        response = requests.post(
            f"{BASE_URL}/files/move",
            headers=HEADERS,
            json={
                "file_id": file_id,
                "folder_id": folder_id
            }
        )
        
        if response.status_code == 200:
            print(f"  [MOVED] {file_name[:50]}")
            return True
        else:
            print(f"  [FAIL] {file_name[:50]}: {response.status_code}")
            return False
    except Exception as e:
        print(f"  [ERROR] {file_name[:50]}: {e}")
        return False

# 루트 폴더의 파일들만 정리
root_files = [f for f in files 
              if 'folder' not in f.get('mimeType', '') 
              and (not f.get('parents') or f.get('parents') == ['0ANnZEeohyvlsUk9PVA'])]

print(f"\nFiles in root folder: {len(root_files)}")

moved_count = 0
failed_count = 0

for file_info in root_files[:100]:  # 안전을 위해 100개만 먼저 처리
    file_name = file_info.get('name', '')
    file_id = file_info.get('id')
    file_name_lower = file_name.lower()
    
    # 이동할 폴더 결정
    target_folder = None
    for keyword, folder_path in move_rules.items():
        if keyword in file_name_lower:
            if folder_path in created_folders:
                target_folder = created_folders[folder_path]
                break
    
    # 매치되지 않은 파일은 임시 폴더로
    if not target_folder and "99_임시" in created_folders:
        target_folder = created_folders["99_임시"]
    
    # 파일 이동
    if target_folder:
        if move_file(file_id, target_folder, file_name):
            moved_count += 1
        else:
            failed_count += 1
        time.sleep(0.3)  # API 제한 방지

# 6단계: 불필요한 파일 삭제
print("\n[STEP 6] Deleting Unnecessary Files")
print("-" * 40)

delete_keywords = ["untitled", "copy of copy", "test_", "temp_", "_backup_backup"]
deleted_count = 0

for file_info in files:
    file_name = file_info.get('name', '').lower()
    file_id = file_info.get('id')
    
    # 삭제 대상 확인
    should_delete = any(keyword in file_name for keyword in delete_keywords)
    
    if should_delete and 'folder' not in file_info.get('mimeType', ''):
        try:
            response = requests.delete(
                f"{BASE_URL}/files/{file_id}",
                headers=HEADERS
            )
            if response.status_code == 200:
                print(f"  [DELETED] {file_info.get('name')[:50]}")
                deleted_count += 1
        except:
            pass
        
        if deleted_count >= 5:  # 안전을 위해 5개만 삭제
            break

# 결과 요약
print("\n" + "=" * 70)
print("ORGANIZATION COMPLETE")
print("=" * 70)
print(f"\nFolders created: {len(created_folders)}")
print(f"Files moved: {moved_count}")
print(f"Files failed to move: {failed_count}")
print(f"Files deleted: {deleted_count}")
print(f"\nRoot folder files remaining: {len(root_files) - moved_count - deleted_count}")

print("\n[FOLDER STRUCTURE CREATED]")
for path in sorted(created_folders.keys()):
    depth = path.count('/')
    indent = "  " * depth
    folder_name = path.split('/')[-1]
    print(f"{indent}{folder_name}/")

print("\n" + "=" * 70)
print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)