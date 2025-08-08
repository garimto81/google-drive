#!/usr/bin/env python3
"""
Google Drive 구조 분석 스크립트
"""

import requests
import json
from collections import defaultdict
from datetime import datetime

def get_drive_data(token):
    """Google Drive 데이터 조회"""
    url = "http://127.0.0.1:8888/files/list"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"include_folders": "true", "page_size": "1000"}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API 오류: {response.status_code} - {response.text}")
        return None

def analyze_structure(data):
    """드라이브 구조 분석"""
    if not data or 'files' not in data:
        return None
    
    files = data['files']
    
    # 분석 결과
    analysis = {
        'total_files': len(files),
        'root_files': [],
        'folders': [],
        'file_types': defaultdict(int),
        'folder_hierarchy': defaultdict(list),
        'project_patterns': defaultdict(list)
    }
    
    # 파일 분석
    for file_info in files:
        mime_type = file_info.get('mimeType', '')
        name = file_info.get('name', '')
        parents = file_info.get('parents', [])
        
        # 파일 타입 분류
        if 'folder' in mime_type:
            analysis['folders'].append({
                'name': name,
                'id': file_info.get('id'),
                'parents': parents
            })
        else:
            # 파일 타입 카운트
            if 'spreadsheet' in mime_type:
                analysis['file_types']['스프레드시트'] += 1
            elif 'presentation' in mime_type:
                analysis['file_types']['프레젠테이션'] += 1
            elif 'document' in mime_type:
                analysis['file_types']['문서'] += 1
            elif 'video' in mime_type:
                analysis['file_types']['동영상'] += 1
            elif 'colaboratory' in mime_type:
                analysis['file_types']['Colab 노트북'] += 1
            else:
                analysis['file_types']['기타'] += 1
        
        # 루트 파일 식별 (parents가 없거나 "0ANnZEeohyvlsUk9PVA"인 경우)
        if not parents or (len(parents) == 1 and parents[0] == "0ANnZEeohyvlsUk9PVA"):
            analysis['root_files'].append({
                'name': name,
                'type': mime_type,
                'modified': file_info.get('modifiedTime', ''),
                'size': file_info.get('size', 0)
            })
    
    return analysis

def identify_project_patterns(analysis):
    """프로젝트 패턴 식별"""
    patterns = {
        'WSOP 관련': [],
        'GGPoker/GGM 관련': [],
        'Corey YouTube': [],
        '장비/인력 관리': [],
        '데이터 분석': [],
        '보고서/회의': [],
        'Colab 개발': [],
        '기타': []
    }
    
    for file_info in analysis['root_files'] + [{'name': f['name'], 'type': 'folder'} for f in analysis['folders']]:
        name = file_info['name'].lower()
        
        if any(keyword in name for keyword in ['wsop', 'cyprus', 'wsope']):
            patterns['WSOP 관련'].append(file_info['name'])
        elif any(keyword in name for keyword in ['gg', 'poker', 'ggm', 'tournament']):
            patterns['GGPoker/GGM 관련'].append(file_info['name'])
        elif 'corey' in name:
            patterns['Corey YouTube'].append(file_info['name'])
        elif any(keyword in name for keyword in ['장비', '인력', '견적', '구매', '충원']):
            patterns['장비/인력 관리'].append(file_info['name'])
        elif any(keyword in name for keyword in ['data', '분석', 'sorting', 'profile']):
            patterns['데이터 분석'].append(file_info['name'])
        elif any(keyword in name for keyword in ['보고서', '회의', 'okr', 'meeting']):
            patterns['보고서/회의'].append(file_info['name'])
        elif 'colab' in name or file_info.get('type', '') == 'application/vnd.google.colaboratory':
            patterns['Colab 개발'].append(file_info['name'])
        else:
            patterns['기타'].append(file_info['name'])
    
    return patterns

def suggest_structure():
    """최적화된 폴더 구조 제안"""
    return {
        "01_프로젝트": {
            "WSOP": {
                "2024_WSOPE": "유럽 월드시리즈 관련 파일",
                "2025_WSOP": "2025년 메인 이벤트",
                "Creator_Program": "크리에이터 프로그램 관련",
                "체크리스트": "이벤트별 체크리스트"
            },
            "GGPoker_Production": {
                "LiveStream": "라이브 스트리밍 관련",
                "Marketing": "마케팅 자료 및 프레젠테이션",
                "Performance": "성과 분석 및 리포트",
                "방송설계": "방송 시스템 설계 문서"
            },
            "YouTube_Content": {
                "Corey_Channel": "Corey 채널 관련",
                "Shorts_Production": "쇼츠 제작",
                "PPT_Materials": "프레젠테이션 자료"
            }
        },
        "02_운영관리": {
            "인력관리": {
                "채용": "인력 충원 관련",
                "OKR": "목표 관리",
                "회의록": "정기 회의 기록"
            },
            "장비관리": {
                "견적서": "장비 구매 견적",
                "불출대장": "장비 대여 기록",
                "구독계정": "서비스 구독 관리"
            },
            "보고서": {
                "주간보고": "주간 업무 보고",
                "월간분석": "월간 성과 분석",
                "대표보고": "대표님 보고용 문서"
            }
        },
        "03_개발_및_데이터": {
            "Colab_Notebooks": "모든 Colab 노트북",
            "데이터분석": {
                "포커데이터": "포커 관련 데이터 분석",
                "성과분석": "비즈니스 성과 데이터",
                "Player_Profile": "플레이어 프로필 데이터"
            },
            "Archive_MAM": "미디어 자산 관리 시스템"
        },
        "04_미디어_자료": {
            "동영상": {
                "원본소스": "편집 전 원본 영상",
                "편집완료": "최종 편집본",
                "샘플영상": "테스트용 샘플"
            },
            "이미지": "스크린샷 및 이미지 파일",
            "오디오": "음성 및 음향 파일"
        },
        "05_외부협업": {
            "NSUSLAB": "NSUSLAB 관련 프로젝트",
            "외주업체": "외주 관련 문서 및 견적",
            "파트너": "비즈니스 파트너 자료"
        },
        "99_임시": "정리 예정인 임시 파일들"
    }

if __name__ == "__main__":
    # JWT 토큰
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFpZGVuLmtpbUBnZ3Byb2R1Y3Rpb24ubmV0IiwibmFtZSI6IkFpZGVuIEtpbSIsImdvb2dsZV90b2tlbiI6InlhMjkuYTBBUzNINk54Y08wYXp1Z2VmdXVIeFpzbXRwM0luSnoxdDN1SW5YTGttRVlRcGhVNjVEam9iM0tFNXBac0FZeDBNMXRmUThfZHBobUlzcnlsMlZCdzk4M2dPaXhveHhUR1ZDSmJUTGN0RUNDaWdQdGJkZlE4R2kxR015TjI1UjFzSWVxT3FLWk1iZ0ptTHFtck0xdkRRNlFlNmtfdmQ2eEx1OEVqeFY4Nm1hQ2dZS0FmVVNBUThTRlFIR1gyTWktcDFUU3JVbnNlMlFMQjdPa0lZQmRnMDE3NSIsImdvb2dsZV9yZWZyZXNoX3Rva2VuIjoiMS8vMGVKeFBOUHd2eXVTRkNnWUlBUkFBR0E0U053Ri1MOUlyNFhCdm5qMlJFRUNpRXJvdVY5VEhURnd5Z1gtcVY0b0NYNWtwT1EwODJ0cW85QURKeWM5VXk2cC1iaWR3bzVjSm45NCIsImV4cCI6MTc1NDcxNzYxNn0.KHzS5zdZFSaw6_wIy3ErxtiKHwChMIUetnvex2lWEzo"
    
    print("Google Drive 구조 분석 중...")
    
    # 데이터 조회
    data = get_drive_data(token)
    if not data:
        print("데이터 조회 실패")
        exit(1)
    
    # 구조 분석
    analysis = analyze_structure(data)
    patterns = identify_project_patterns(analysis)
    suggested_structure = suggest_structure()
    
    print("=" * 80)
    print("GOOGLE DRIVE 구조 분석 결과")
    print("=" * 80)
    
    print(f"\n[전체 통계]:")
    print(f"  - 총 파일 수: {analysis['total_files']}개")
    print(f"  - 총 폴더 수: {len(analysis['folders'])}개")
    print(f"  - 루트 폴더 파일 수: {len(analysis['root_files'])}개")
    
    print(f"\n[파일 타입별 분포]:")
    for file_type, count in analysis['file_types'].items():
        print(f"  - {file_type}: {count}개")
    
    print(f"\n[루트 폴더 정리 대상 (상위 20개)]:")
    root_files = sorted(analysis['root_files'], 
                       key=lambda x: x.get('modified', ''), reverse=True)
    for i, file_info in enumerate(root_files[:20], 1):
        name = file_info['name'][:50] + "..." if len(file_info['name']) > 50 else file_info['name']
        print(f"  {i:2d}. {name}")
    
    print(f"\n[프로젝트 패턴 분석]:")
    for pattern, files in patterns.items():
        if files:
            print(f"  - {pattern}: {len(files)}개")
            for file_name in files[:3]:  # 상위 3개만 표시
                print(f"    * {file_name}")
            if len(files) > 3:
                print(f"    ... 외 {len(files)-3}개")
    
    print(f"\n[제안된 최적화 구조]:")
    
    def print_structure(structure, indent=0):
        for key, value in structure.items():
            if isinstance(value, dict):
                print("  " * indent + f"[폴더] {key}/")
                print_structure(value, indent + 1)
            else:
                print("  " * indent + f"[파일] {key} - {value}")
    
    print_structure(suggested_structure)
    
    print(f"\n[주요 개선사항]:")
    print("  1. 루트 폴더 95개 파일 -> 0개 (완전 정리)")
    print("  2. 프로젝트별 명확한 분류 체계 구축")
    print("  3. 업무 프로세스 기반 폴더 구조")
    print("  4. 확장 가능하고 유지보수 용이한 구조")
    print("  5. 미디어 파일 전용 관리 영역 분리")
    
    print(f"\n[구현 우선순위]:")
    print("  1단계: 메인 폴더 구조 생성")
    print("  2단계: 프로젝트별 파일 분류 및 이동")
    print("  3단계: 루트 폴더 완전 정리")
    print("  4단계: 명명 규칙 통일")
    print("  5단계: 정기적 유지보수 체계 구축")
    
    print("=" * 80)