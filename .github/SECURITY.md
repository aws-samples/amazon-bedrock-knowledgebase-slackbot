# 🛡️ Security Policy & Guidelines

이 문서는 프로젝트의 보안 정책, 취약점 대응 절차, 그리고 개발 가이드라인을 정의합니다.
이 리포지토리는 내부 전용(Internal Only)이며, 모든 기여자는 아래의 보안 표준(OWASP, ISMS-P)을 준수해야 합니다.

---

## 🚨 1. 취약점 신고 및 대응 (Vulnerability Reporting)

보안 취약점을 발견했을 경우, 공개된 Issue 트래커에 올리는 것을 **금지**합니다. 대신 아래 절차를 따라주세요.

### 신고 채널
* **담당자 이메일**: `twodragon114@gmail.com` (또는 담당자 사내 메신저)
* **GitHub**: `Security` 탭 > `Report a vulnerability` (Private Reporting)

### 대응 타임라인 (SLA)
심각도에 따라 다음 기한 내에 패치를 완료해야 합니다.

| 심각도 (Severity) | 초기 응답 | 해결 목표 (Fix Timeline) | 예시 |
| :--- | :--- | :--- | :--- |
| **Critical** | 24시간 이내 | **7일 이내** | RCE, SQL Injection, 인증 우회 |
| **High** | 48시간 이내 | **14일 이내** | 민감 데이터 노출, 권한 상승 |
| **Medium** | 3일 이내 | **30일 이내** | CSRF, XSS (제한적) |
| **Low** | 7일 이내 | **90일 이내** | 보안 설정 미흡, 정보 누출(사소) |

---

## 🔒 2. 보안 표준 (Security Standards)

본 프로젝트는 다음 두 가지 주요 보안 프레임워크를 준수합니다.

### 🌐 OWASP Top 10 (2025 기준)
어플리케이션 개발 시 가장 치명적인 10가지 취약점을 방어합니다.
* **Broken Access Control**: 최소 권한 원칙 적용
* **Cryptographic Failures**: 모든 민감 정보 암호화 (전송/저장)
* **Injection**: 입력값 검증 및 파라미터화된 쿼리 사용

### 🏛️ ISMS-P (정보보호 관리체계)
국내 정보보호 인증 기준을 준수하여 운영합니다.
* **접근 통제 (AC)**: RBAC 기반 접근 제어, MFA 적용
* **암호화 (CR)**: AES-256 저장 암호화, TLS 1.2+ 전송 암호화
* **취약점 관리 (VM)**: 정기적 스캔 및 의존성 업데이트

---

## 💻 3. 개발 가이드라인 (Development Guidelines)

개발 시 AI 도구(Cursor)와 자동화 도구가 이 규칙을 강제합니다.

### 🤖 AI Coding Assistant (`.cursorrules`)
이 프로젝트는 **`.cursorrules`** 파일을 통해 AI가 보안 코딩을 하도록 설정되어 있습니다.
* Cursor가 생성한 코드는 기본적으로 이 보안 정책을 따릅니다.
* AI의 제안이라도 보안 위배 사항(하드코딩 등)이 보이면 즉시 거부하십시오.

### 🚫 절대 금지 사항 (Prohibited)
다음 항목 발견 시 **Code Review에서 즉시 거절(Reject)** 됩니다.
1.  **Secret 하드코딩**: API Key, Password, Token을 코드에 직접 작성
2.  **HTTP 사용**: 모든 통신은 `HTTPS` 필수
3.  **로그 내 민감 정보**: 비밀번호, 주민번호, 토큰 등을 마스킹 없이 로깅
4.  **검증 없는 입력 사용**: `eval()`, `exec()` 사용 및 SQL String Concat

### 🔑 주요 언어별 보안 수칙
> 자세한 코딩 패턴은 `.cursorrules` 파일을 참조하세요.

* **Python**: `os.getenv()`로 환경변수 확인, `pydantic`으로 입력 검증
* **Java**: `BCrypt`로 비밀번호 해싱, `@Valid` 어노테이션 사용
* **Infra (TF/K8s)**: S3 퍼블릭 차단, Pod `runAsNonRoot: true` 설정

---

## ☁️ 4. 인프라 보안 (Infrastructure Security)

### 🔐 AWS Best Practices
* **IAM**: User 사용을 지양하고 **Role** 기반 접근을 사용합니다.
  * **GitHub Actions**: OIDC Provider를 통한 Role 기반 인증 (`github-oidc.tf`)
  * **EKS Pod Identity**: IRSA 대신 Pod Identity 사용으로 자동 자격 증명 주입 (`pod-identity.tf`)
  * **최소 권한 원칙**: 각 Role은 필요한 권한만 부여 (S3, EKS 등)
* **S3 보안**:
  * `server_side_encryption = "AES256"` 필수
  * `block_public_acls = true`, `block_public_policy = true` 설정
  * 버전 관리 및 수명 주기 정책 적용
* **EKS 보안**:
  * **GuardDuty**: Control Plane 로깅 대신 AWS GuardDuty를 사용하여 EKS 보안 모니터링 (비용 최적화)
  * Secrets Encryption 활성화 (KMS)
  * Network Policy로 Pod 간 통신 제한

### ☸️ Kubernetes (EKS) Security
* **Pod Security**:
  * 모든 Pod에 `SecurityContext` 필수 적용:
    ```yaml
    securityContext:
      runAsNonRoot: true
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
    ```
  * **Resource Limits**: `requests`와 `limits` 명시 (노이지 네이버 방지)
* **Network Policy**:
  * 기본 정책: Deny All
  * 필요한 Pod 간 통신만 명시적으로 허용 (`k8s/network-policy/`)
* **RBAC**:
  * ServiceAccount별 최소 권한 부여
  * ClusterRole 사용 최소화, Namespace-scoped Role 우선
* **Secrets 관리**:
  * Kubernetes Secrets 암호화 (KMS)
  * 민감 정보는 External Secrets Operator 또는 AWS Secrets Manager 사용

### 🔄 ArgoCD 보안
* **RBAC**: ArgoCD Application별 최소 권한 부여
* **Git Credentials**: SSH Key 또는 GitHub App Token 사용 (HTTPS 인증)
* **Sync Policy**: 자동 Sync 비활성화, 수동 승인 후 배포
* **Source Control**: GitOps Repository에 대한 접근 제어 및 감사 로그

### 🔑 Okta 통합 보안
* **OIDC 인증**: kubectl 접근 시 Okta OIDC Provider 사용
* **MFA 강제**: 모든 관리자 계정에 MFA 필수
* **세션 관리**: 토큰 만료 시간 설정 및 자동 갱신
* **포트 관리**: OIDC 로그인 콜백 포트(8000, 8080) 충돌 방지

### 🛡️ GitHub Security
* **Branch Protection**: `main` 브랜치에 필수 설정
  * Require pull request reviews (최소 1명)
  * Require status checks to pass before merging
  * Require branches to be up to date before merging
* **Secret Scanning**: GitHub Advanced Security 활성화
  * Dependabot alerts 자동 생성
  * Secret scanning 결과 즉시 알림
* **Dependabot**: 자동 의존성 업데이트 및 취약점 알림
* **Code Scanning**: GitHub CodeQL 또는 외부 SAST 도구 통합

### 💰 비용 최적화 (FinOps)
* **스토리지**: S3 버킷에는 수명 주기(Lifecycle) 정책을 걸어 오래된 로그를 Glacier로 보냅니다.
* **컴퓨팅**: 개발(Dev) 환경은 가능한 **Spot Instance**를 활용합니다.
* **삭제**: 사용하지 않는 리소스(EIP, EBS, LB)는 즉시 삭제합니다.

---

## ✅ 5. 배포 체크리스트 (Checklist)

PR 생성 및 배포 전 다음 항목을 확인해 주세요.

### 🔴 Pre-Commit (개발자 확인)
- [ ] `.env` 파일이나 시크릿 키가 커밋에 포함되지 않았는가?
- [ ] 입력값 검증(Validation) 로직이 존재하는가?
- [ ] 불필요한 디버그 로그(`console.log`, `print`)를 제거했는가?

### 🟠 Pre-Deployment (배포 전 확인)
- [ ] CI/CD 파이프라인의 보안 스캔(Trivy/Snyk)을 통과했는가?
- [ ] 변경된 인프라(Terraform)가 퍼블릭 접근을 허용하지 않는가?
- [ ] DB 마이그레이션 시 데이터 백업 대책이 있는가?

---

## 📚 참고 자료
* [OWASP Top 10](https://owasp.org/www-project-top-ten/)
* [프로젝트 .cursorrules 설정 파일](./.cursorrules)
* [AWS Well-Architected Framework - Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
* [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
* [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---
**Last Updated**: 2026-01-06
**Maintainer**: DevSecOps
