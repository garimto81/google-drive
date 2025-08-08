#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
구글 드라이브 폴더 구조 직접 생성
Google Drive API를 사용한 직접 폴더 생성
"""

import requests
import json
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# JWT 토큰에서 Google 토큰 추출
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54RU5xSWR2bUVKM25FM29TeU1Bb0pNUTlWcGVwNlRIaWU0a1JTT0NhYzQ1TXlrVkVQMXd6NG51T0RMZjdHdC1tN3RYeGNERVlNaTlrYVFodl9CMjhDenUtQS04REFTN0lLeUZuRXB4X3RTZ1FPTjFJVXJpN0xPQ1hkZ1g4REFVWk1XNVhEWkJjbzQzRXFZQ1gtR1M1bGt6bmpiREFobXRoclphQ2dZS0FWOFNBUThTRlFIR1gyTWk4aVlRMEFRM1ZRYnpkNE5jRTRTM1NRMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVrUzQyWWRZTUk3UUNnWUlBUkFBR0E0U053Ri1MOUlyQU80RHNCeS1nOTNvTjhFaGxEbzZEMjEzaHpvV3pfTEJrRnJNWl9iUVZuTnlSblJ3NmZNSlpGSFBqX0JtMF9fY0RDQSIsImV4cCI6MTc1NDcyMDEzOH0.M6l5tbB4txnIQqjKbfdXiqbTGpiecc-Ied-Dgr-Ktvc"

# JWT 디코드 (간단한 방법)
import base64
jwt_payload = JWT_TOKEN.split('.')[1]
jwt_payload += '=' * (4 - len(jwt_payload) % 4)  # 패딩 추가
decoded = json.loads(base64.b64decode(jwt_payload))

GOOGLE_TOKEN = decoded['google_token']
REFRESH_TOKEN = decoded['google_refresh_token']

print("=" * 70)
print("Google Drive Folder Structure Creation")
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
    print("[OK] Google Drive API connected")
except Exception as e:
    print(f"[ERROR] Failed to connect: {e}")
    exit(1)

# 폴더 구조 정의
FOLDER_STRUCTURE = {
    "01_프로젝트": {
        "WSOP": {
            "2024_WSOPE": {},
            "2025_WSOP": {},
            "Creator_Program": {},
            "체크리스트": {},
            "예산계획": {},
            "현장자료": {}
        },
        "GGPoker_Production": {
            "LiveStream": {
                "방송계획": {},
                "기술문서": {},
                "성과분석": {}
            },
            "Marketing": {
                "프레젠테이션": {},
                "캠페인": {},
                "분석리포트": {}
            },
            "Performance": {
                "주간리포트": {},
                "월간분석": {},
                "KPI추적": {}
            },
            "방송설계": {
                "시스템구성도": {},
                "장비명세": {},
                "운영매뉴얼": {}
            }
        },
        "YouTube_Content": {
            "Corey_Channel": {},
            "Shorts": {},
            "Thumbnails": {}
        }
    },
    "02_운영관리": {
        "인력관리": {
            "채용": {},
            "성과평가": {},
            "교육자료": {}
        },
        "장비관리": {
            "구매": {},
            "운영": {},
            "유지보수": {}
        },
        "보고서": {
            "일일보고": {},
            "주간보고": {},
            "월간보고": {},
            "대표보고": {}
        },
        "문서보관": {
            "계약서": {},
            "법적문서": {},
            "기타문서": {}
        }
    },
    "03_개발_및_데이터": {
        "Colab_Notebooks": {
            "AI_프로젝트": {},
            "데이터분석": {},
            "자동화스크립트": {}
        },
        "데이터분석": {
            "포커데이터": {},
            "성과분석": {},
            "Player_Profile": {}
        },
        "Archive_MAM": {}
    },
    "04_미디어_자료": {
        "동영상": {
            "원본소스": {},
            "편집완료": {},
            "샘플영상": {}
        },
        "이미지": {
            "스크린샷": {},
            "디자인": {},
            "로고": {}
        },
        "오디오": {}
    },
    "05_외부협업": {
        "NSUSLAB": {},
        "Corey_Channel": {},
        "외주업체": {},
        "파트너": {}
    },
    "99_임시": {
        "정리예정": {},
        "테스트": {}
    }
}

created_folders = {}

def create_folder(name, parent_id=None):
    """Google Drive에 폴더 생성"""
    try:
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = service.files().create(
            body=file_metadata,
            fields='id, name'
        ).execute()
        
        print(f"  [CREATED] {name}")
        return folder.get('id')
    except HttpError as error:
        print(f"  [ERROR] {name}: {error}")
        return None

def create_folder_structure(structure, parent_id=None, path=""):
    """재귀적으로 폴더 구조 생성"""
    for folder_name, subfolders in structure.items():
        current_path = f"{path}/{folder_name}" if path else folder_name
        print(f"\nCreating: {current_path}")
        
        # 폴더 생성
        folder_id = create_folder(folder_name, parent_id)
        
        if folder_id:
            created_folders[current_path] = folder_id
            
            # 하위 폴더 생성
            if subfolders:
                create_folder_structure(subfolders, folder_id, current_path)
        
        time.sleep(0.3)  # API 제한 방지

# 메인 실행
print("\n[STARTING FOLDER CREATION]")
print("-" * 40)

create_folder_structure(FOLDER_STRUCTURE)

# 결과 출력
print("\n" + "=" * 70)
print("FOLDER CREATION COMPLETE")
print("=" * 70)
print(f"\nTotal folders created: {len(created_folders)}")

print("\n[CREATED FOLDER STRUCTURE]")
for path in sorted(created_folders.keys()):
    depth = path.count('/')
    indent = "  " * depth
    folder_name = path.split('/')[-1]
    print(f"{indent}{folder_name}/")

# 생성된 폴더 ID 저장
with open('C:\\claude02\\created_folders.json', 'w', encoding='utf-8') as f:
    json.dump(created_folders, f, ensure_ascii=False, indent=2)

print("\n[SAVED] Folder IDs saved to created_folders.json")
print("\n" + "=" * 70)
print("All folders have been created in your Google Drive!")
print("Check: https://drive.google.com")
print("=" * 70)