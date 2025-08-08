#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
루트 폴더 파일들을 적절한 폴더로 이동
"""

import json
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# JWT 토큰에서 Google 토큰 추출
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54RU5xSWR2bUVKM25FM29TeU1Bb0pNUTlWcGVwNlRIaWU0a1JTT0NhYzQ1TXlrVkVQMXd6NG51T0RMZjdHdC1tN3RYeGNERVlNaTlrYVFodl9CMjhDenUtQS04REFTN0lLeUZuRXB4X3RTZ1FPTjFJVXJpN0xPQ1hkZ1g4REFVWk1XNVhEWkJjbzQzRXFZQ1gtR1M1bGt6bmpiREFobXRoclphQ2dZS0FWOFNBUThTRlFIR1gyTWk4aVlRMEFRM1ZRYnpkNE5jRTRTM1NRMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVrUzQyWWRZTUk3UUNnWUlBUkFBR0E0U053Ri1MOUlyQU80RHNCeS1nOTNvTjhFaGxEbzZEMjEzaHpvV3pfTEJrRnJNWl9iUVZuTnlSblJ3NmZNSlpGSFBqX0JtMF9fY0RDQSIsImV4cCI6MTc1NDcyMDEzOH0.M6l5tbB4txnIQqjKbfdXiqbTGpiecc-Ied-Dgr-Ktvc"

# JWT 디코드
import base64
jwt_payload = JWT_TOKEN.split('.')[1]
jwt_payload += '=' * (4 - len(jwt_payload) % 4)
decoded = json.loads(base64.b64decode(jwt_payload))

GOOGLE_TOKEN = decoded['google_token']
REFRESH_TOKEN = decoded['google_refresh_token']

print("=" * 70)
print("MOVING FILES TO ORGANIZED FOLDERS")
print("=" * 70)

# Google Drive API 서비스 생성
creds = Credentials(
    token=GOOGLE_TOKEN,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id="15001647688-7mmotpki7kpgd4rcdgn3onfialsu716b.apps.googleusercontent.com",
    client_secret="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"
)

try:
    service = build('drive', 'v3', credentials=creds)
    print("[OK] Connected to Google Drive")
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

# 생성된 폴더 ID 로드
try:
    with open('C:\\claude02\\created_folders.json', 'r', encoding='utf-8') as f:
        created_folders = json.load(f)
    print(f"[OK] Loaded {len(created_folders)} folder IDs")
except:
    print("[ERROR] created_folders.json not found")
    exit(1)

# 파일 이동 규칙 정의
MOVE_RULES = {
    # WSOP 관련
    'wsop': '01_프로젝트/WSOP',
    'wsope': '01_프로젝트/WSOP/2024_WSOPE',
    'cyprus': '01_프로젝트/WSOP/2024_WSOPE',
    'bahamas': '01_프로젝트/WSOP/2025_WSOP',
    'paradise': '01_프로젝트/WSOP/2025_WSOP',
    'circuit': '01_프로젝트/WSOP',
    'checklist': '01_프로젝트/WSOP/체크리스트',
    'budget': '01_프로젝트/WSOP/예산계획',
    
    # GGPoker 관련
    'ggpoker': '01_프로젝트/GGPoker_Production',
    'ggproduction': '01_프로젝트/GGPoker_Production',
    'ggm': '01_프로젝트/GGPoker_Production',
    'performance': '01_프로젝트/GGPoker_Production/Performance/주간리포트',
    'livestream': '01_프로젝트/GGPoker_Production/LiveStream',
    'comparelivesstream': '01_프로젝트/GGPoker_Production/LiveStream/성과분석',
    '방송': '01_프로젝트/GGPoker_Production/방송설계',
    
    # YouTube/Corey
    'corey': '05_외부협업/Corey_Channel',
    'youtube': '01_프로젝트/YouTube_Content',
    'pokerstorycircle': '01_프로젝트/YouTube_Content',
    
    # 보고서
    '보고서': '02_운영관리/보고서/대표보고',
    'report': '02_운영관리/보고서',
    'okr': '02_운영관리/인력관리/성과평가',
    'pm okr': '02_운영관리/인력관리/성과평가',
    
    # 인력/장비
    '인력': '02_운영관리/인력관리/채용',
    '충원': '02_운영관리/인력관리/채용',
    '장비': '02_운영관리/장비관리/구매',
    '견적': '02_운영관리/장비관리/구매',
    '불출': '02_운영관리/장비관리/운영',
    
    # 데이터/개발
    'gemini': '03_개발_및_데이터/Colab_Notebooks/AI_프로젝트',
    'player': '03_개발_및_데이터/데이터분석/Player_Profile',
    'sorting': '03_개발_및_데이터/데이터분석/포커데이터',
    '포커 토너먼트': '03_개발_및_데이터/데이터분석/포커데이터',
    
    # 미디어
    'archive-mam': '03_개발_및_데이터/Archive_MAM',
    'thumbnail': '01_프로젝트/YouTube_Content/Thumbnails',
    
    # 외부협업
    'nsuslab': '05_외부협업/NSUSLAB',
    
    # 문서
    'trello': '02_운영관리/문서보관/기타문서',
    'cbas': '02_운영관리/문서보관/기타문서',
    'gog': '02_운영관리/문서보관/기타문서',
}

# 루트 폴더의 파일 조회
def get_root_files():
    """루트 폴더의 파일 목록 조회"""
    try:
        results = service.files().list(
            q="'root' in parents and mimeType != 'application/vnd.google-apps.folder'",
            pageSize=500,
            fields="files(id, name, mimeType, parents)"
        ).execute()
        
        files = results.get('files', [])
        print(f"\n[FOUND] {len(files)} files in root folder")
        return files
    except HttpError as error:
        print(f"[ERROR] {error}")
        return []

# 파일 이동 함수
def move_file(file_id, file_name, target_folder_id):
    """파일을 지정된 폴더로 이동"""
    try:
        # 현재 부모 폴더 가져오기
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents', []))
        
        # 파일 이동
        file = service.files().update(
            fileId=file_id,
            addParents=target_folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        
        return True
    except HttpError as error:
        print(f"    [ERROR] {error}")
        return False

# 파일명 기반 폴더 매칭
def match_folder(file_name):
    """파일명을 분석하여 적절한 폴더 찾기"""
    file_name_lower = file_name.lower()
    
    # 파일 확장자 확인
    if file_name.endswith('.pdf'):
        # PDF는 문서보관으로
        if any(k in file_name_lower for k in ['주민', '등본', '증명']):
            return '02_운영관리/문서보관/법적문서'
        else:
            return '02_운영관리/문서보관/기타문서'
    
    # 규칙 기반 매칭
    for keyword, folder_path in MOVE_RULES.items():
        if keyword in file_name_lower:
            if folder_path in created_folders:
                return folder_path
    
    # Colab 노트북
    if file_name.endswith('.ipynb'):
        if 'untitled' in file_name_lower:
            return '99_임시/테스트'
        else:
            return '03_개발_및_데이터/Colab_Notebooks'
    
    # 미디어 파일
    if any(ext in file_name_lower for ext in ['.mp4', '.mov', '.avi']):
        return '04_미디어_자료/동영상/원본소스'
    if any(ext in file_name_lower for ext in ['.jpg', '.png', '.gif']):
        return '04_미디어_자료/이미지'
    
    # 매칭 안된 파일은 임시 폴더로
    return '99_임시/정리예정'

# 메인 실행
print("\n[STEP 1] Getting root files...")
root_files = get_root_files()

if not root_files:
    print("[INFO] No files in root folder")
    exit(0)

# 파일 분류
print("\n[STEP 2] Classifying files...")
file_moves = []
unmatched = []

for file in root_files:
    file_name = file['name']
    file_id = file['id']
    
    # 적절한 폴더 찾기
    target_folder_path = match_folder(file_name)
    
    if target_folder_path in created_folders:
        target_folder_id = created_folders[target_folder_path]
        file_moves.append({
            'id': file_id,
            'name': file_name,
            'target_path': target_folder_path,
            'target_id': target_folder_id
        })
    else:
        unmatched.append(file_name)

print(f"\n[CLASSIFIED]")
print(f"  Files to move: {len(file_moves)}")
print(f"  Unmatched: {len(unmatched)}")

# 분류 결과 출력
if file_moves:
    print("\n[MOVE PLAN]")
    # 폴더별로 그룹화
    moves_by_folder = {}
    for move in file_moves:
        path = move['target_path']
        if path not in moves_by_folder:
            moves_by_folder[path] = []
        moves_by_folder[path].append(move['name'])
    
    for folder_path, files in sorted(moves_by_folder.items())[:10]:
        print(f"\n  -> {folder_path}/")
        for fname in files[:3]:
            print(f"     - {fname[:50]}")
        if len(files) > 3:
            print(f"     ... and {len(files)-3} more")

# 파일 이동 실행
print("\n[STEP 3] Moving files...")
print("-" * 40)

moved_count = 0
failed_count = 0

for i, move in enumerate(file_moves, 1):
    print(f"\r  Moving {i}/{len(file_moves)}: {move['name'][:40]}...", end="")
    
    if move_file(move['id'], move['name'], move['target_id']):
        moved_count += 1
    else:
        failed_count += 1
    
    time.sleep(0.2)  # API 제한 방지

print(f"\n\n[COMPLETE]")
print(f"  Moved: {moved_count} files")
print(f"  Failed: {failed_count} files")

# 남은 파일 확인
remaining = len(root_files) - moved_count
print(f"  Remaining in root: {remaining} files")

# 이동 로그 저장
move_log = {
    'total_files': len(root_files),
    'moved': moved_count,
    'failed': failed_count,
    'remaining': remaining,
    'moves': file_moves[:50],  # 상위 50개만 저장
    'unmatched': unmatched[:20]  # 상위 20개만 저장
}

with open('C:\\claude02\\move_log.json', 'w', encoding='utf-8') as f:
    json.dump(move_log, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 70)
print("FILE ORGANIZATION COMPLETE!")
print("=" * 70)
print("\nYour Google Drive is now organized!")
print("Check: https://drive.google.com")
print("\nMove log saved to: move_log.json")