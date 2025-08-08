#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
구글 드라이브 1년 이상 된 파일 식별 및 분석 스크립트 (간단 버전)
오늘 날짜: 2025-08-08
1년 기준: 2024-08-08 이전 파일
"""

import requests
import json
from datetime import datetime
import sys
import os

# 윈도우 콘솔 인코딩 문제 해결
if sys.platform == "win32":
    os.system("chcp 65001 >nul")

def get_all_files(token):
    """모든 파일 목록 조회"""
    url = "http://127.0.0.1:8888/files/list"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "include_folders": "true", 
        "page_size": "1000",
        "include_trashed": "false"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('files', [])
        else:
            print(f"파일 목록 조회 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return []
    except Exception as e:
        print(f"파일 목록 조회 오류: {e}")
        return []

def parse_date(date_string):
    """날짜 문자열을 datetime 객체로 변환"""
    if not date_string:
        return None
    try:
        if 'T' in date_string:
            date_string = date_string.split('T')[0]
        return datetime.strptime(date_string, '%Y-%m-%d')
    except:
        return None

def classify_file_type(mime_type, name):
    """파일 타입 분류"""
    if not mime_type:
        ext = os.path.splitext(name.lower())[1]
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return '이미지'
        elif ext in ['.mp4', '.avi', '.mov']:
            return '동영상'
        elif ext in ['.pdf']:
            return 'PDF'
        return '기타'
    
    if 'folder' in mime_type:
        return '폴더'
    elif 'document' in mime_type:
        return '구글문서'
    elif 'spreadsheet' in mime_type:
        return '스프레드시트'
    elif 'presentation' in mime_type:
        return '프레젠테이션'
    elif 'colaboratory' in mime_type:
        return 'Colab노트북'
    elif 'image' in mime_type:
        return '이미지'
    elif 'video' in mime_type:
        return '동영상'
    else:
        return '기타'

def format_size(size_str):
    """파일 크기 포맷팅"""
    try:
        size = int(size_str) if size_str else 0
        if size == 0:
            return '0B'
        elif size < 1024:
            return f'{size}B'
        elif size < 1024 * 1024:
            return f'{size/1024:.1f}KB'
        elif size < 1024 * 1024 * 1024:
            return f'{size/(1024*1024):.1f}MB'
        else:
            return f'{size/(1024*1024*1024):.1f}GB'
    except:
        return '크기불명'

def is_important_file(name):
    """중요 파일 판별 (간단 버전)"""
    name_lower = name.lower()
    important_keywords = [
        '계약', 'contract', '법적', '라이센스', '세금', '재무', '급여',
        'okr', '보고서', 'report', '중요', 'important', '백업', 'backup',
        'wsop', 'ggpoker', '프로덕션', 'production'
    ]
    return any(keyword in name_lower for keyword in important_keywords)

def main():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54Y08wYXp1Z2VmdXVIeFpzbXRwM0luSnoxdDN1SW5YTGttRVlRcGhVNjVEam9iM0tFNXBac0FZeDBNMXRmUThfZHBobUlzcnlsMlZCdzk4M2dPaXhveHhUR1ZDSmJUTGN0RUNDaWdQdGJkZlE4R2kxR005TjI1UjFzSWVxT3FLWk1iZ0ptTHFtck0xdkRRNlFlNmtfdmQ2eEx1OEVqeFY4Nm1hQ2dZS0FmVVNBUThTRlFIR1gyTWktcDFUU3JVbnNlMlFMQjdPa0lZQmRnMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVKeFBOUHd2eXVTRkNnWUlBUkFBR0E0U053Ri1MOUlyNFhCdm5qMlJFRUNpRXJvdVY5VEhURnd5Z1gtcVY0b0NYNWtwT1EwODJ0cW85QURKeWM5VXk2cC1iaWR3bzVjSm45NCIsImV4cCI6MTc1NDcxNzYxNn0.KHzS5zdZFSaw6_wIy3ErxtiKHwChMIUetnvex2lWEzo"
    
    cutoff_date = datetime(2024, 8, 8)  # 1년 기준일
    today = datetime(2025, 8, 8)
    
    print("=" * 60)
    print("구글 드라이브 1년 이상 된 파일 분석")
    print("=" * 60)
    print(f"기준일: {cutoff_date.strftime('%Y-%m-%d')} 이전")
    print(f"분석일: {today.strftime('%Y-%m-%d')}")
    print()
    
    # 파일 목록 조회
    print("파일 목록 조회 중...")
    all_files = get_all_files(token)
    
    if not all_files:
        print("파일 목록을 가져올 수 없습니다.")
        return
    
    print(f"총 {len(all_files)}개 파일/폴더 조회됨")
    
    # 분석
    old_files = []
    stats = {
        'total_files': 0,
        'old_files_count': 0,
        'by_type': {},
        'important_files': [],
        'safe_to_delete': [],
        'total_size': 0,
        'old_size': 0
    }
    
    for file_info in all_files:
        name = file_info.get('name', '')
        modified_time = file_info.get('modifiedTime', '')
        mime_type = file_info.get('mimeType', '')
        size = file_info.get('size', '0')
        
        # 폴더가 아닌 경우만 파일 통계에 포함
        if 'folder' not in mime_type:
            stats['total_files'] += 1
            stats['total_size'] += int(size) if size else 0
        
        # 수정일 확인
        modified_date = parse_date(modified_time)
        if not modified_date:
            continue
        
        # 1년 이상 된 파일인지 확인
        if modified_date < cutoff_date:
            file_type = classify_file_type(mime_type, name)
            is_important = is_important_file(name)
            age_days = (today - modified_date).days
            
            old_file = {
                'name': name,
                'modified_date': modified_date,
                'file_type': file_type,
                'size': size,
                'formatted_size': format_size(size),
                'is_important': is_important,
                'age_days': age_days
            }
            
            old_files.append(old_file)
            
            # 통계 업데이트
            if 'folder' not in mime_type:
                stats['old_files_count'] += 1
                stats['old_size'] += int(size) if size else 0
            
            # 타입별 통계
            if file_type in stats['by_type']:
                stats['by_type'][file_type] += 1
            else:
                stats['by_type'][file_type] = 1
            
            # 중요도별 분류
            if is_important:
                stats['important_files'].append(old_file)
            elif any(keyword in name.lower() for keyword in ['temp', '임시', 'test', 'sample']):
                stats['safe_to_delete'].append(old_file)
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("분석 결과")
    print("=" * 60)
    
    print(f"\n[전체 통계]")
    print(f"전체 파일 수: {stats['total_files']:,}개")
    print(f"1년 이상 된 파일: {stats['old_files_count']:,}개 ({stats['old_files_count']/stats['total_files']*100:.1f}%)")
    print(f"전체 용량: {format_size(str(stats['total_size']))}")
    print(f"1년 이상 된 파일 용량: {format_size(str(stats['old_size']))}")
    
    print(f"\n[파일 타입별 분포]")
    sorted_types = sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)
    for file_type, count in sorted_types:
        print(f"  {file_type}: {count:,}개")
    
    print(f"\n[중요 파일 - 보호 필요] ({len(stats['important_files'])}개)")
    for i, file_info in enumerate(stats['important_files'][:10], 1):
        print(f"  {i}. {file_info['name'][:50]}... ({file_info['age_days']}일 전)")
    
    print(f"\n[안전 삭제 대상] ({len(stats['safe_to_delete'])}개)")
    safe_size = sum(int(f['size']) if f['size'] else 0 for f in stats['safe_to_delete'])
    print(f"예상 절약 용량: {format_size(str(safe_size))}")
    for i, file_info in enumerate(stats['safe_to_delete'][:10], 1):
        print(f"  {i}. {file_info['name'][:50]}... ({file_info['formatted_size']}, {file_info['age_days']}일 전)")
    
    # 가장 오래된 파일들
    print(f"\n[가장 오래된 파일 10개]")
    oldest_files = sorted([f for f in old_files if not f['is_important']], 
                         key=lambda x: x['age_days'], reverse=True)
    for i, file_info in enumerate(oldest_files[:10], 1):
        print(f"  {i}. {file_info['name'][:50]}... ({file_info['age_days']}일 전, {file_info['formatted_size']})")
    
    # 권장사항
    print(f"\n" + "=" * 60)
    print("권장사항")
    print("=" * 60)
    
    print(f"\n[안전장치]")
    print(f"1. Google Takeout으로 전체 백업 생성")
    print(f"2. 중요 파일 {len(stats['important_files'])}개는 별도 폴더로 보호")
    print(f"3. 단계적 삭제 (테스트 파일 → 임시 파일 → 기타)")
    print(f"4. 30일 휴지통 보관 기간 활용")
    
    print(f"\n[삭제 우선순위]")
    print(f"1단계: 테스트/임시 파일 - {len(stats['safe_to_delete'])}개")
    print(f"2단계: 2년 이상 된 일반 파일")
    print(f"3단계: 1년 이상 된 기타 파일")
    print(f"보호: 중요 파일 - {len(stats['important_files'])}개")
    
    print(f"\n분석 완료!")
    
    # JSON 파일로 결과 저장
    try:
        output_file = f"drive_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # datetime 객체를 문자열로 변환
        json_data = {
            'analysis_date': today.isoformat(),
            'cutoff_date': cutoff_date.isoformat(),
            'stats': stats,
            'old_files_count': len(old_files),
            'old_files': []
        }
        
        # 파일 정보를 JSON 호환 형태로 변환
        for file_info in old_files:
            json_file = file_info.copy()
            json_file['modified_date'] = file_info['modified_date'].isoformat()
            json_data['old_files'].append(json_file)
        
        # 중요 파일과 안전 삭제 대상도 JSON 호환 형태로 변환
        json_data['stats']['important_files'] = []
        for file_info in stats['important_files']:
            json_file = file_info.copy()
            json_file['modified_date'] = file_info['modified_date'].isoformat()
            json_data['stats']['important_files'].append(json_file)
        
        json_data['stats']['safe_to_delete'] = []
        for file_info in stats['safe_to_delete']:
            json_file = file_info.copy()
            json_file['modified_date'] = file_info['modified_date'].isoformat()
            json_data['stats']['safe_to_delete'].append(json_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n상세 결과가 '{output_file}' 파일로 저장되었습니다.")
        
    except Exception as e:
        print(f"\n파일 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    main()