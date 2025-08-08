# 🤝 Contributing to Google Drive AI Organizer

우선, 이 프로젝트에 기여하려는 시간을 내주셔서 감사합니다! 

## 목차
- [행동 강령](#행동-강령)
- [기여 방법](#기여-방법)
- [개발 환경 설정](#개발-환경-설정)
- [코드 스타일](#코드-스타일)
- [커밋 메시지 규칙](#커밋-메시지-규칙)
- [Pull Request 프로세스](#pull-request-프로세스)

## 행동 강령

이 프로젝트는 [Contributor Covenant](https://www.contributor-covenant.org/) 행동 강령을 따릅니다.
프로젝트에 참여함으로써 이 규칙을 준수할 것에 동의하는 것입니다.

## 기여 방법

### 버그 신고

버그를 발견하셨다면:

1. 먼저 [이슈 목록](https://github.com/garimto81/google-drive/issues)을 확인하여 이미 보고되지 않았는지 확인
2. 새 이슈를 생성할 때 다음 정보 포함:
   - 버그에 대한 명확한 설명
   - 재현 단계
   - 예상 동작
   - 실제 동작
   - 스크린샷 (해당되는 경우)
   - 환경 정보 (OS, Python 버전 등)

### 기능 제안

새로운 기능을 제안하려면:

1. [이슈 목록](https://github.com/garimto81/google-drive/issues)에서 유사한 제안이 있는지 확인
2. 새 이슈 생성 시 `enhancement` 라벨 사용
3. 기능의 목적과 사용 사례를 명확히 설명

## 개발 환경 설정

### 1. 저장소 Fork 및 Clone

```bash
# Fork 후 clone
git clone https://github.com/YOUR_USERNAME/google-drive.git
cd google-drive
```

### 2. 가상환경 설정

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 개발 의존성
```

### 3. 브랜치 생성

```bash
git checkout -b feature/your-feature-name
# 또는
git checkout -b fix/your-bug-fix
```

## 코드 스타일

### Python

- [PEP 8](https://www.python.org/dev/peps/pep-0008/) 준수
- Black 포매터 사용
- Type hints 사용 권장

```bash
# 코드 포맷팅
black .

# 린팅
flake8 .
mypy .
```

### JavaScript/TypeScript

- ESLint + Prettier 설정 준수
- React Hooks 규칙 준수

```bash
# 프론트엔드 디렉토리에서
npm run lint
npm run format
```

## 커밋 메시지 규칙

[Conventional Commits](https://www.conventionalcommits.org/) 스펙을 따릅니다:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서만 변경
- `style`: 코드 의미에 영향을 주지 않는 변경 (공백, 포맷팅 등)
- `refactor`: 버그 수정이나 기능 추가가 아닌 코드 변경
- `perf`: 성능 개선
- `test`: 테스트 추가 또는 수정
- `chore`: 빌드 프로세스 또는 보조 도구 변경

### 예시

```bash
feat(auth): Google OAuth 2.0 로그인 구현

- OAuth 2.0 플로우 구현
- JWT 토큰 생성 및 검증
- 세션 관리 추가

Closes #123
```

## Pull Request 프로세스

### 1. PR 체크리스트

- [ ] 코드가 프로젝트 스타일 가이드를 따름
- [ ] 모든 테스트가 통과함
- [ ] 새로운 기능에 대한 테스트 추가됨
- [ ] 문서가 업데이트됨
- [ ] 커밋 메시지가 규칙을 따름

### 2. PR 템플릿

```markdown
## 설명
변경 사항에 대한 간단한 설명

## 변경 유형
- [ ] 버그 수정
- [ ] 새 기능
- [ ] Breaking change
- [ ] 문서 업데이트

## 테스트
테스트 방법 설명

## 체크리스트
- [ ] 코드 리뷰 요청 전 자체 리뷰 완료
- [ ] 관련 이슈 링크 추가
- [ ] 변경 로그 업데이트
```

### 3. 리뷰 프로세스

1. PR 생성 후 최소 1명의 리뷰어 할당
2. 모든 피드백 해결
3. 승인 받은 후 merge

## 테스트

### 단위 테스트

```bash
# 백엔드 테스트
pytest tests/

# 커버리지 확인
pytest --cov=backend tests/
```

### 통합 테스트

```bash
# Docker Compose로 전체 스택 실행
docker-compose up -d

# 통합 테스트 실행
pytest tests/integration/
```

### 프론트엔드 테스트

```bash
cd frontend
npm test
npm run test:coverage
```

## 문서화

### 코드 문서화

```python
def classify_file(file_info: FileInfo) -> Classification:
    """
    파일을 분류하여 적절한 폴더를 결정합니다.
    
    Args:
        file_info: 파일 메타데이터를 포함한 객체
        
    Returns:
        Classification: 분류 결과 및 신뢰도
        
    Raises:
        ClassificationError: 분류 실패 시
        
    Example:
        >>> file = FileInfo(name="report.pdf", type="application/pdf")
        >>> result = classify_file(file)
        >>> print(result.folder_path)
        "02_운영관리/보고서"
    """
```

### API 문서화

FastAPI는 자동으로 OpenAPI 문서를 생성합니다:
- 개발 서버 실행 후 `/docs` 접속

## 릴리즈 프로세스

1. 버전 번호 업데이트 (SemVer 준수)
2. CHANGELOG.md 업데이트
3. 릴리즈 브랜치 생성
4. 테스트 및 검증
5. main 브랜치로 merge
6. 태그 생성 및 릴리즈 발행

## 도움 요청

질문이나 도움이 필요하신 경우:

1. [Discussions](https://github.com/garimto81/google-drive/discussions) 활용
2. [이슈](https://github.com/garimto81/google-drive/issues) 생성
3. 이메일: aiden.kim@ggproduction.net

## 라이선스

이 프로젝트에 기여함으로써, 귀하의 기여가 MIT 라이선스 하에 라이선스될 것에 동의합니다.

---

감사합니다! 🙏