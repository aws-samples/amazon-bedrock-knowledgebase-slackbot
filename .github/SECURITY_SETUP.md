# Security Setup Guide

이 문서는 프로젝트에 설정된 보안 기능들을 설명합니다.

## 🔒 설정된 보안 기능

### 1. Dependabot
- **파일**: `.github/dependabot.yml`
- **기능**:
  - npm, pip, GitHub Actions 의존성 자동 모니터링
  - 주간 자동 업데이트 (매주 월요일 9시)
  - 보안 패치 자동 감지 및 알림
  - PR 자동 생성

### 2. CodeQL Analysis
- **파일**: `.github/workflows/codeql.yml`, `.github/codeql-config.yml`
- **기능**:
  - JavaScript/TypeScript 및 Python 코드 정적 분석
  - 보안 취약점 자동 감지
  - 주간 자동 스캔

### 3. Security Scanning
- **파일**: `.github/workflows/security.yml`
- **기능**:
  - npm audit (의존성 취약점 검사)
  - pip-audit (Python 의존성 취약점 검사)
  - Secret scanning (Gitleaks, TruffleHog)
  - CDK NAG (CDK 보안 검사)
  - ESLint 보안 플러그인

### 4. Dependency Review
- **파일**: `.github/workflows/dependency-review.yml`
- **기능**:
  - PR에서 의존성 변경 자동 검토
  - 취약점이 있는 의존성 차단
  - CVSS 점수 기반 필터링

### 5. Secret Scanning
- **파일**: `.github/workflows/secret-scanning.yml`
- **기능**:
  - 코드에 노출된 시크릿 자동 감지
  - Gitleaks 및 TruffleHog 사용
  - 주간 자동 스캔

### 6. Dependabot Auto-merge
- **파일**: `.github/workflows/dependabot-auto-merge.yml`
- **기능**:
  - 보안 패치 자동 병합 (선택적)
  - 상태 검사 통과 후 자동 병합

### 7. Security Policy
- **파일**: `.github/SECURITY.md`
- **기능**:
  - 보안 취약점 보고 프로세스
  - 보안 팀 연락처
  - 보안 체크리스트

### 8. Pull Request Template
- **파일**: `.github/PULL_REQUEST_TEMPLATE.md`
- **기능**:
  - 보안 체크리스트 포함
  - PR 제출 시 자동으로 보안 검토 요청

### 9. CODEOWNERS
- **파일**: `.github/CODEOWNERS`
- **기능**:
  - 보안 관련 파일에 대한 자동 리뷰어 지정
  - 코드 소유권 관리

### 10. Security Issue Template
- **파일**: `.github/ISSUE_TEMPLATE/security-vulnerability.md`
- **기능**:
  - 보안 취약점 보고 템플릿
  - 구조화된 취약점 보고

## 🚀 사용 방법

### Dependabot 활성화
1. GitHub 저장소 설정에서 Dependabot 활성화
2. `.github/dependabot.yml` 파일이 자동으로 인식됨
3. 주간 자동 스캔 시작

### CodeQL 활성화
1. GitHub 저장소 설정 > Security > Code scanning
2. "Set up" 클릭
3. "CodeQL" 선택
4. `.github/workflows/codeql.yml` 파일이 자동으로 인식됨

### Secret Scanning 활성화
1. GitHub 저장소 설정 > Security > Secret scanning
2. "Set up" 클릭
3. 자동으로 활성화됨 (GitHub 기본 기능)

### Dependency Review 활성화
1. GitHub 저장소 설정 > Security > Dependency review
2. "Set up" 클릭
3. `.github/workflows/dependency-review.yml` 파일이 자동으로 인식됨

## 📋 보안 체크리스트

배포 전 확인사항:

- [ ] 모든 Dependabot 알림 확인 및 해결
- [ ] CodeQL 스캔 결과 확인
- [ ] Secret scanning 결과 확인
- [ ] npm audit 및 pip-audit 결과 확인
- [ ] CDK NAG 위반 사항 확인
- [ ] PR 보안 체크리스트 완료
- [ ] 보안 리뷰 완료

## 🔧 커스터마이징

### Dependabot 설정 변경
`.github/dependabot.yml` 파일을 수정하여:
- 스캔 주기 변경
- 특정 패키지 제외
- 자동 병합 규칙 변경

### CodeQL 쿼리 추가
`.github/codeql-config.yml` 파일을 수정하여:
- 추가 보안 쿼리 포함
- 특정 쿼리 제외

### 보안 워크플로우 수정
`.github/workflows/security.yml` 파일을 수정하여:
- 추가 보안 도구 통합
- 스캔 주기 변경

## 📚 참고 자료

- [GitHub Security Documentation](https://docs.github.com/en/code-security)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [CodeQL Documentation](https://docs.github.com/en/code-security/code-scanning)
- [Secret Scanning Documentation](https://docs.github.com/en/code-security/secret-scanning)

---

**마지막 업데이트**: 2025-01-XX

