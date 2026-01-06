# Pull Request

## 📋 Description

<!-- Provide a clear description of what this PR does -->

## 🔒 Security Checklist

<!-- Please check all that apply -->

- [ ] No hardcoded secrets, credentials, or API keys in code
- [ ] All sensitive data is stored in AWS Secrets Manager or SSM Parameter Store
- [ ] IAM policies follow least privilege principle (no wildcards without conditions)
- [ ] All user inputs are validated and sanitized
- [ ] No SQL/NoSQL injection vulnerabilities
- [ ] No OS command injection vulnerabilities (no `exec`, `eval`, `os.system` without proper sanitization)
- [ ] S3 buckets have public access blocked
- [ ] All data is encrypted (at rest and in transit)
- [ ] API Gateway has proper authentication/authorization
- [ ] CloudWatch Logs do not contain sensitive information
- [ ] Security groups restrict access appropriately
- [ ] Bedrock Guardrails are properly configured (if applicable)
- [ ] All dependencies are up-to-date and free of known vulnerabilities
- [ ] Dependabot alerts have been reviewed and addressed (if any)
- [ ] Code has been reviewed for security best practices

## 🛡️ Security Review

<!-- Security team review checklist -->

- [ ] Security review completed
- [ ] No security vulnerabilities identified
- [ ] All security concerns addressed

## 📦 Dependencies

<!-- List any new dependencies added -->

- [ ] New npm dependencies: `package.json` updated
- [ ] New Python dependencies: `requirements.txt` updated
- [ ] All dependencies reviewed for security vulnerabilities
- [ ] Dependabot alerts checked and resolved

## 🧪 Testing

<!-- Describe the tests you ran -->

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Security tests pass
- [ ] Manual testing completed

## 📝 Type of Change

<!-- Mark the relevant option with an 'x' -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Security fix
- [ ] Dependency update

## 🔍 Related Issues

<!-- Link related issues here -->

Closes #<!-- issue number -->

## 📸 Screenshots (if applicable)

<!-- Add screenshots to help explain your changes -->

## ✅ Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## 🚨 Security Notes

<!-- If this PR addresses a security issue, describe it here. Do NOT include sensitive details. -->

## 📚 Additional Context

<!-- Add any other context about the PR here -->

---

**⚠️ Security Reminder**: If this PR contains security-related changes, please ensure all security checklist items are completed and reviewed by the security team.

