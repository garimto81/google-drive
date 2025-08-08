#!/usr/bin/env python3
"""
1년 이상 된 구글 드라이브 파일 분석 및 삭제 대상 목록 생성
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

# JWT 토큰
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54RU5xSWR2bUVKM25FM29TeU1Bb0pNUTlWcGVwNlRIaWU0a1JTT0NhYzQ1TXlrVkVQMXd6NG51T0RMZjdHdC1tN3RYeGNERVlNaTlrYVFodl9CMjhDenUtQS04REFTN0lLeUZuRXB4X3RTZ1FPTjFJVXJpN0xPQ1hkZ1g4REFVWk1XNVhEWkJjbzQzRXFZQ1gtR1M1bGt6bmpiREFobXRoclphQ2dZS0FWOFNBUThTRlFIR1gyTWk4aVlRMEFRM1ZRYnpkNE5jRTRTM1NRMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVrUzQyWWRZTUk3UUNnWUlBUkFBR0E0U053Ri1MOUlyQU80RHNCeS1nOTNvTjhFaGxEbzZEMjEzaHpvV3pfTEJrRnJNWl9iUVZuTnlSblJ3NmZNSlpGSFBqX0JtMF9fY0RDQSIsImV4cCI6MTc1NDcyMDEzOH0.M6l5tbB4txnIQqjKbfdXiqbTGpiecc-Ied-Dgr-Ktvc"

# API 설정
BASE_URL = "http://127.0.0.1:8888"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 기준 날짜 (1년 전)
ONE_YEAR_AGO = datetime.now() - timedelta(days=365)
print(f"기준 날짜: {ONE_YEAR_AGO.strftime('%Y-%m-%d')} 이전 파일 분석")

def get_all_files():
    """모든 파일 목록 조회"""
    try:
        response = requests.get(
            f"{BASE_URL}/files/list",
            headers=HEADERS,
            params={"include_folders": "true", "page_size": "1000"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API 오류: {response.status_code}")
            return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def analyze_old_files(data):
    """1년 이상 된 파일 분석"""
    if not data or 'files' not in data:
        return None
    
    old_files = {
        'delete_immediately': [],  # 즉시 삭제 가능
        'review_needed': [],        # 검토 필요
        'keep_important': [],       # 보존 필요
        'statistics': {
            'total_old_files': 0,
            'total_size_mb': 0,
            'by_type': defaultdict(int)
        }
    }
    
    for file_info in data['files']:
        # 수정 날짜 파싱
        modified_str = file_info.get('modifiedTime', '')
        if not modified_str:
            continue
            
        try:
            # ISO 형식 날짜 파싱
            modified_date = datetime.fromisoformat(modified_str.replace('Z', '+00:00'))
            
            # 1년 이상 된 파일인지 확인
            if modified_date.replace(tzinfo=None) < ONE_YEAR_AGO:
                name = file_info.get('name', '')
                mime_type = file_info.get('mimeType', '')
                size = int(file_info.get('size', 0))
                size_mb = size / (1024 * 1024)
                
                file_data = {
                    'name': name,
                    'id': file_info.get('id'),
                    'type': mime_type,
                    'modified': modified_str,
                    'size_mb': round(size_mb, 2),
                    'parents': file_info.get('parents', [])
                }
                
                # 파일 분류
                name_lower = name.lower()
                
                # 즉시 삭제 가능 (임시, 테스트, 스크린샷 등)
                if any(keyword in name_lower for keyword in ['temp', 'test', '임시', 'sample', 'screenshot', '화면', 'copy', '사본']):
                    old_files['delete_immediately'].append(file_data)
                # 중요 파일 (보존 필요)
                elif any(keyword in name_lower for keyword in ['계약', 'contract', 'license', 'okr', '보고서', 'wsop', 'ggpoker']):
                    old_files['keep_important'].append(file_data)
                # 검토 필요
                else:
                    old_files['review_needed'].append(file_data)
                
                # 통계 업데이트
                old_files['statistics']['total_old_files'] += 1
                old_files['statistics']['total_size_mb'] += size_mb
                
                # 파일 타입별 카운트
                if 'spreadsheet' in mime_type:
                    old_files['statistics']['by_type']['스프레드시트'] += 1
                elif 'presentation' in mime_type:
                    old_files['statistics']['by_type']['프레젠테이션'] += 1
                elif 'document' in mime_type:
                    old_files['statistics']['by_type']['문서'] += 1
                elif 'video' in mime_type:
                    old_files['statistics']['by_type']['동영상'] += 1
                elif 'image' in mime_type:
                    old_files['statistics']['by_type']['이미지'] += 1
                elif 'folder' in mime_type:
                    old_files['statistics']['by_type']['폴더'] += 1
                else:
                    old_files['statistics']['by_type']['기타'] += 1
                    
        except Exception as e:
            print(f"날짜 파싱 오류: {e}")
            continue
    
    return old_files

def delete_files(file_ids):
    """파일 삭제 실행"""
    deleted = []
    failed = []
    
    for file_id in file_ids:
        try:
            response = requests.delete(
                f"{BASE_URL}/files/{file_id}",
                headers=HEADERS
            )
            if response.status_code == 200:
                deleted.append(file_id)
            else:
                failed.append({'id': file_id, 'error': response.status_code})
        except Exception as e:
            failed.append({'id': file_id, 'error': str(e)})
    
    return {'deleted': deleted, 'failed': failed}

# 메인 실행
print("=" * 80)
print("구글 드라이브 1년 이상 파일 분석 시작")
print("=" * 80)

# 사용자 확인
try:
    response = requests.get(f"{BASE_URL}/auth/me", headers=HEADERS)
    if response.status_code == 200:
        user_info = response.json()
        print(f"[OK] 인증 성공: {user_info.get('email')}")
    else:
        print(f"[FAIL] 인증 실패: {response.status_code}")
        exit(1)
except Exception as e:
    print(f"[ERROR] 연결 오류: {e}")
    exit(1)

# 파일 목록 조회
print("\n파일 목록 조회 중...")
data = get_all_files()

if not data:
    print("파일 목록 조회 실패")
    exit(1)

# 오래된 파일 분석
print(f"[OK] 총 {len(data.get('files', []))}개 파일 발견")
print("\n1년 이상 된 파일 분석 중...")

old_files = analyze_old_files(data)

if not old_files:
    print("분석 실패")
    exit(1)

# 결과 출력
print("\n" + "=" * 80)
print("분석 결과")
print("=" * 80)

stats = old_files['statistics']
print(f"\n[전체 통계]")
print(f"  • 1년 이상 된 파일: {stats['total_old_files']}개")
print(f"  • 총 용량: {stats['total_size_mb']:.2f} MB ({stats['total_size_mb']/1024:.2f} GB)")
print(f"\n[파일 타입별]")
for file_type, count in stats['by_type'].items():
    print(f"  • {file_type}: {count}개")

print(f"\n[즉시 삭제 가능]: {len(old_files['delete_immediately'])}개")
if old_files['delete_immediately']:
    print("  상위 10개:")
    for i, f in enumerate(old_files['delete_immediately'][:10], 1):
        print(f"  {i:2d}. {f['name'][:50]} ({f['size_mb']} MB)")

print(f"\n[검토 필요]: {len(old_files['review_needed'])}개")
if old_files['review_needed']:
    print("  상위 10개:")
    for i, f in enumerate(old_files['review_needed'][:10], 1):
        print(f"  {i:2d}. {f['name'][:50]} ({f['size_mb']} MB)")

print(f"\n[보존 필요 (중요)]: {len(old_files['keep_important'])}개")
if old_files['keep_important']:
    print("  상위 5개:")
    for i, f in enumerate(old_files['keep_important'][:5], 1):
        print(f"  {i:2d}. {f['name'][:50]}")

# 삭제 목록 저장
with open('C:\\claude02\\delete_candidates.json', 'w', encoding='utf-8') as f:
    json.dump({
        'delete_immediately': old_files['delete_immediately'],
        'total_count': len(old_files['delete_immediately']),
        'total_size_mb': sum(f['size_mb'] for f in old_files['delete_immediately'])
    }, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 80)
print("권장사항")
print("=" * 80)
print(f"""
1. 즉시 삭제 가능한 {len(old_files['delete_immediately'])}개 파일 삭제
   → 약 {sum(f['size_mb'] for f in old_files['delete_immediately']):.2f} MB 공간 확보

2. 검토 필요한 {len(old_files['review_needed'])}개 파일 수동 확인
   → 추가 {sum(f['size_mb'] for f in old_files['review_needed']):.2f} MB 확보 가능

3. 중요 파일 {len(old_files['keep_important'])}개는 보존 권장

삭제를 진행하시겠습니까? (y/n)
""")

# 사용자 확인
confirm = input("삭제 진행 (즉시 삭제 가능 파일만)? (y/n): ").strip().lower()

if confirm == 'y':
    print("\n파일 삭제 시작...")
    delete_ids = [f['id'] for f in old_files['delete_immediately']]
    
    # 배치 삭제 (10개씩)
    batch_size = 10
    total_deleted = 0
    
    for i in range(0, len(delete_ids), batch_size):
        batch = delete_ids[i:i+batch_size]
        print(f"  삭제 중... {i+1}-{min(i+batch_size, len(delete_ids))}/{len(delete_ids)}")
        result = delete_files(batch)
        total_deleted += len(result['deleted'])
        
        if result['failed']:
            print(f"  [WARNING] {len(result['failed'])}개 삭제 실패")
    
    print(f"\n[COMPLETE] 삭제 완료: {total_deleted}개 파일")
    print(f"   확보된 공간: {sum(f['size_mb'] for f in old_files['delete_immediately'][:total_deleted]):.2f} MB")
else:
    print("\n삭제 취소됨. 'delete_candidates.json' 파일에 삭제 대상 목록이 저장되었습니다.")

print("\n" + "=" * 80)
print("작업 완료!")
print("=" * 80)