#!/usr/bin/env python3
"""
Generate a simple ASCII/text-based architecture diagram
This doesn't require external dependencies and can be included in README
"""

def generate_ascii_diagram():
    """Generate ASCII architecture diagram."""
    
    diagram = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Amazon Bedrock Knowledge Base Slackbot                    │
│                              Architecture Diagram                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│ Slack User  │
└──────┬───────┘
       │ Slash Command: /ask-aws
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Slack Workspace                                    │
└──────┬──────────────────────────────────────────────────────────────────────┘
       │ POST Request
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         API Gateway                                          │
│                    Endpoint: /slack/ask-aws                                 │
│                    Method: POST                                             │
│                    Authentication: Slack Signing Secret                    │
└──────┬──────────────────────────────────────────────────────────────────────┘
       │ Invoke Lambda
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AWS Lambda Functions                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ BedrockKbSlackbotFunction (Python 3.12)                            │   │
│  │ • Handles Slack slash commands                                      │   │
│  │ • Processes user queries                                           │   │
│  │ • Calls Bedrock Knowledge Base                                     │   │
│  │ • Returns responses to Slack                                       │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ CreateIndexFunction (Custom Resource)                               │   │
│  │ • Creates OpenSearch Serverless index                              │   │
│  │ • Configures vector search settings                                │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────┬──────────────────────────────────────────────────────────────────────┘
       │
       ├─────────────────────────────────────────────────────────────────┐
       │                                                                 │
       ▼                                                                 ▼
┌──────────────────────────┐                              ┌──────────────────────────┐
│   Secrets Management     │                              │   Amazon Bedrock         │
├──────────────────────────┤                              ├──────────────────────────┤
│                          │                              │                          │
│ • Secrets Manager        │                              │ • Knowledge Base         │
│   - Slack Bot Token      │                              │   - AWS Well-Architected │
│   - Signing Secret       │                              │     Framework Docs       │
│                          │                              │                          │
│ • SSM Parameter Store    │                              │ • Guardrails             │
│   - Parameter References │                              │   - Content Filtering    │
│                          │                              │   - PII Protection       │
│                          │                              │                          │
│                          │                              │ • Foundation Models      │
│                          │                              │   - Claude 3.5 Sonnet   │
│                          │                              │   - Titan Embeddings    │
│                          │                              │                          │
└──────────────────────────┘                              └──────┬───────────────────┘
                                                                   │
                                                                   │ Query & Embed
                                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OpenSearch Serverless (Vector DB)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Collection: slack-bedrock-vector-db                                        │
│  Index: slack-bedrock-os-index                                              │
│                                                                              │
│  • Vector Search (1024 dimensions)                                          │
│  • HNSW Algorithm (Faiss engine)                                           │
│  • Encrypted at rest (AWS Managed Keys)                                     │
│                                                                              │
└──────┬──────────────────────────────────────────────────────────────────────┘
       │
       │ Ingest Documents
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Amazon S3                                           │
│                    Knowledge Base Documents                                 │
│                    • Encrypted (SSE-S3)                                     │
│                    • Versioning Enabled                                     │
│                    • Public Access Blocked                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         CloudWatch Logs                                     │
│                    • API Gateway Access Logs                                │
│                    • Lambda Function Logs                                   │
│                    • Error Tracking                                         │
└─────────────────────────────────────────────────────────────────────────────┘

Data Flow:
1. User sends /ask-aws command in Slack
2. Slack sends POST request to API Gateway
3. API Gateway invokes Lambda function
4. Lambda retrieves secrets from Secrets Manager/SSM
5. Lambda calls Bedrock Knowledge Base RetrieveAndGenerate API
6. Bedrock queries OpenSearch Serverless vector database
7. Bedrock applies Guardrails for content filtering
8. Bedrock generates response using Claude 3.5 Sonnet
9. Response is returned to Slack and displayed to user

Security Features:
• Secrets stored in AWS Secrets Manager (encrypted)
• IAM roles with least privilege access
• Bedrock Guardrails for content filtering
• S3 bucket encryption and public access blocking
• CloudWatch Logs for audit trail
• API Gateway request signing verification
"""
    
    return diagram

if __name__ == "__main__":
    diagram = generate_ascii_diagram()
    print(diagram)
    
    # Save to file
    with open("docs/architecture-diagram.txt", "w") as f:
        f.write(diagram)
    
    print("\n✓ ASCII diagram saved to: docs/architecture-diagram.txt")

