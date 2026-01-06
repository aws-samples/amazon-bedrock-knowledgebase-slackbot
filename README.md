# Amazon Bedrock Knowledge Base Slack Chat Bot

[![Security](https://img.shields.io/badge/security-hardened-green.svg)](.github/SECURITY.md)
[![License](https://img.shields.io/badge/license-MIT--0-blue.svg)](LICENSE)
[![CDK](https://img.shields.io/badge/CDK-2.189.0-orange.svg)](https://aws.amazon.com/cdk/)

A production-ready Slack chatbot integration powered by Amazon Bedrock Knowledge Base, enabling teams to query AWS Well-Architected Framework documentation and best practices directly from Slack using natural language.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage](#usage)
- [Security](#security)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project deploys a serverless Slack chatbot that integrates with Amazon Bedrock Knowledge Base to provide intelligent answers about AWS architecture, security, and best practices. The solution uses Retrieval-Augmented Generation (RAG) to answer questions based on the AWS Well-Architected Framework documentation.

### Key Technologies

- **Amazon Bedrock**: Foundation models (Claude 3.5 Sonnet) and Knowledge Base
- **OpenSearch Serverless**: Vector database for semantic search
- **AWS Lambda**: Serverless compute for Slack integration
- **API Gateway**: RESTful API endpoint
- **AWS CDK**: Infrastructure as Code (TypeScript)
- **Slack Bolt**: Python framework for Slack apps

## 🏗️ Architecture

### System Architecture

```mermaid
graph TB
    subgraph "User Interface"
        SU[Slack User]
        SW[Slack Workspace]
    end
    
    subgraph "API Layer"
        AG[API Gateway<br/>/slack/ask-aws<br/>POST Method]
    end
    
    subgraph "Compute Layer"
        LF1[BedrockKbSlackbotFunction<br/>Python 3.12<br/>Slack Integration]
        LF2[CreateIndexFunction<br/>Custom Resource<br/>OpenSearch Setup]
    end
    
    subgraph "Secrets Management"
        SM[Secrets Manager<br/>Slack Bot Token<br/>Signing Secret]
        SSM[SSM Parameter Store<br/>Parameter References]
    end
    
    subgraph "Amazon Bedrock"
        KB[Knowledge Base<br/>AWS Well-Architected<br/>Framework Docs]
        GR[Guardrails<br/>Content Filtering<br/>PII Protection]
        FM[Foundation Models<br/>Claude 3.5 Sonnet<br/>RAG Generation]
        EM[Embedding Model<br/>Titan Embeddings v2<br/>Vector Generation]
    end
    
    subgraph "Vector Database"
        OSS[OpenSearch Serverless<br/>Collection: slack-bedrock-vector-db<br/>Index: slack-bedrock-os-index]
        VS[Vector Search<br/>1024 dimensions<br/>HNSW Algorithm]
    end
    
    subgraph "Storage"
        S3[S3 Bucket<br/>Knowledge Base Documents<br/>Encrypted SSE-S3]
    end
    
    subgraph "Monitoring"
        CW[CloudWatch Logs<br/>API Gateway Logs<br/>Lambda Logs]
    end
    
    SU -->|Slash Command<br/>/ask-aws| SW
    SW -->|POST Request| AG
    AG -->|Invoke| LF1
    
    LF1 -->|Read Secrets| SM
    LF1 -->|Read Parameters| SSM
    LF1 -->|RetrieveAndGenerate| KB
    
    KB -->|Query Vectors| OSS
    KB -->|Apply Filters| GR
    KB -->|Generate Response| FM
    KB -->|Create Embeddings| EM
    
    OSS --> VS
    KB -->|Ingest Documents| S3
    
    LF2 -->|Create Index| OSS
    
    LF1 -->|Log Events| CW
    AG -->|Access Logs| CW
    
    LF1 -->|Response| AG
    AG -->|Response| SW
    SW -->|Display Answer| SU
    
    style LF1 fill:#e1f5ff
    style KB fill:#fff4e1
    style OSS fill:#ffe1f5
    style SM fill:#e8f5e9
    style GR fill:#e8f5e9
    style CW fill:#f3e5f5
```

### Data Flow

```mermaid
sequenceDiagram
    participant SU as Slack User
    participant SW as Slack Workspace
    participant AG as API Gateway
    participant LF as Lambda Function
    participant SM as Secrets Manager
    participant KB as Bedrock KB
    participant GR as Guardrails
    participant OSS as OpenSearch Serverless
    participant FM as Claude 3.5 Sonnet
    participant S3 as S3 Bucket
    participant CW as CloudWatch
    
    SU->>SW: /ask-aws "What are S3 security best practices?"
    SW->>AG: POST /slack/ask-aws (Signed Request)
    
    AG->>AG: Verify Slack Signing Secret
    AG->>LF: Invoke Lambda Function
    
    LF->>SM: Retrieve Slack Bot Token
    SM-->>LF: Bot Token
    
    LF->>LF: Validate Slack Request
    LF->>LF: Extract User Query
    
    LF->>KB: RetrieveAndGenerate(query)
    
    KB->>OSS: Query Vector Database
    OSS-->>KB: Relevant Document Chunks
    
    KB->>GR: Apply Content Filtering
    GR-->>KB: Filtered Content
    
    KB->>FM: Generate Response with Context
    FM-->>KB: Generated Answer
    
    KB-->>LF: Response Text
    
    LF->>LF: Format Slack Response
    LF->>SW: POST Response (Slack API)
    SW-->>SU: Display Answer
    
    LF->>CW: Log Request/Response
    AG->>CW: Log API Gateway Events
    
    Note over KB,S3: Document Ingestion (Background)
    S3->>KB: Sync Documents
    KB->>OSS: Index Embeddings
```

### Architecture Diagram (ASCII)

```
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
       │ POST Request (Signed)
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
```

### Detailed Data Flow Steps

1. **User Interaction**: User sends `/ask-aws` slash command in Slack with a question
2. **Slack → API Gateway**: Slack sends POST request to API Gateway endpoint with signed payload
3. **API Gateway Verification**: API Gateway verifies Slack signing secret
4. **API Gateway → Lambda**: API Gateway invokes Lambda function with request
5. **Secrets Retrieval**: Lambda retrieves Slack credentials from Secrets Manager/SSM
6. **Request Validation**: Lambda validates Slack request signature
7. **Query Extraction**: Lambda extracts user query from Slack payload
8. **Bedrock Query**: Lambda calls Bedrock Knowledge Base `RetrieveAndGenerate` API
9. **Vector Search**: Bedrock queries OpenSearch Serverless vector database for relevant chunks
10. **Content Filtering**: Bedrock applies Guardrails for content safety and PII protection
11. **Response Generation**: Bedrock generates response using Claude 3.5 Sonnet model with retrieved context
12. **Response Formatting**: Lambda formats response for Slack
13. **Response Delivery**: Response is returned to Slack and displayed to user
14. **Logging**: All events are logged to CloudWatch for monitoring and audit

### Components

| Component | Description |
|-----------|-------------|
| **API Gateway** | RESTful API endpoint (`/slack/ask-aws`) that receives Slack webhook requests |
| **Lambda Functions** | Serverless compute for processing Slack commands and creating OpenSearch indices |
| **Bedrock Knowledge Base** | RAG service that retrieves relevant documents and generates answers |
| **OpenSearch Serverless** | Vector database for semantic search (1024-dimensional embeddings) |
| **S3 Bucket** | Storage for Knowledge Base documents (AWS Well-Architected Framework PDFs) |
| **Secrets Manager** | Secure storage for Slack Bot Token and Signing Secret |
| **Bedrock Guardrails** | Content filtering and PII protection |
| **CloudWatch Logs** | Centralized logging and monitoring |

## ✨ Features

### Core Functionality

- **Natural Language Queries**: Ask questions about AWS architecture and best practices in plain English
- **RAG-Powered Responses**: Answers are generated based on AWS Well-Architected Framework documentation
- **Slack Integration**: Native Slack slash command (`/ask-aws`) for easy access
- **Content Safety**: Built-in Guardrails for filtering inappropriate content and protecting PII

### Security Features

- **Secrets Management**: Slack credentials stored in AWS Secrets Manager (encrypted)
- **IAM Least Privilege**: Minimal IAM permissions following security best practices
- **Encryption**: All data encrypted at rest (S3, OpenSearch) and in transit (TLS)
- **Access Control**: API Gateway request signing verification
- **Audit Trail**: Comprehensive CloudWatch Logs for security monitoring

### Operational Features

- **Serverless Architecture**: Fully serverless, pay-per-use model
- **Auto-scaling**: Automatically scales based on demand
- **Monitoring**: CloudWatch integration for metrics and logs
- **Infrastructure as Code**: CDK for reproducible deployments

## 📋 Prerequisites

### Required

- **AWS Account** with appropriate permissions
- **Node.js** 18.x or higher
- **Python** 3.12 or higher
- **AWS CDK CLI** 2.156.0 or higher
- **AWS CLI** configured with appropriate credentials
- **Slack Workspace** with admin permissions

### AWS Permissions

Your AWS credentials need permissions for:
- CloudFormation (CDK stack management)
- Lambda, API Gateway, S3, Bedrock, OpenSearch Serverless
- IAM (role and policy creation)
- Secrets Manager, SSM Parameter Store
- CloudWatch Logs

### Slack Setup

1. Create a Slack App at [api.slack.com](https://api.slack.com/apps)
2. Enable Slash Commands
3. Configure OAuth & Permissions (Bot Token Scopes: `commands`, `chat:write`)
4. Install the app to your workspace
5. Note the Bot User OAuth Token and Signing Secret

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Twodragon0/amazon-bedrock-knowledgebase-slackbot.git
cd amazon-bedrock-knowledgebase-slackbot
```

### 2. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies (for Lambda functions)
cd lambda/BedrockKbSlackbotFunction
pip install -r requirements.txt -t .
cd ../..
```

### 3. Build the Project

```bash
npm run build
```

## ⚙️ Configuration

### Environment Variables

Before deploying, you need to provide Slack credentials via CDK context:

```bash
cdk deploy \
  --context slackBotToken=xoxb-your-bot-token \
  --context slackSigningSecret=your-signing-secret
```

**⚠️ Security Note**: Never commit secrets to version control. Use CDK context or environment variables.

### Customization Options

Edit `lib/amazon-bedrock-knowledgebase-slackbot-stack.ts` to customize:

- **Slash Command**: Change `SLACK_SLASH_COMMAND` (default: `/ask-aws`)
- **Bedrock Model**: Change `RAG_MODEL_ID` (default: Claude 3.5 Sonnet)
- **Embedding Model**: Change `EMBEDDING_MODEL` (default: Titan Embeddings v2)
- **Lambda Memory**: Change `LAMBDA_MEMORY_SIZE` (default: 265 MB)

## 📦 Deployment

### 1. Bootstrap CDK (First Time Only)

```bash
cdk bootstrap
```

### 2. Deploy the Stack

```bash
cdk deploy \
  --context slackBotToken=xoxb-your-bot-token \
  --context slackSigningSecret=your-signing-secret
```

### 3. Configure Slack App

After deployment, update your Slack App configuration:

1. Go to your Slack App settings → **Slash Commands**
2. Edit the `/ask-aws` command
3. Set **Request URL** to: `https://<api-id>.execute-api.<region>.amazonaws.com/prod/slack/ask-aws`
   - You can find the API Gateway URL in the CDK output or AWS Console

### 4. Load Knowledge Base Documents

After deployment, load AWS Well-Architected Framework documents:

```bash
# Get Knowledge Base ID and Data Source ID from CDK output or AWS Console
./scripts/load-kb.sh <KB_ID> <DATA_SOURCE_ID> s3://<bucket-name>/aws-war-bot/
```

The script will:
- Download AWS Well-Architected Framework PDFs
- Upload them to S3
- Trigger Knowledge Base sync

## 💬 Usage

### Basic Usage

1. In Slack, type: `/ask-aws`
2. Enter your question, for example:
   - "What are the security best practices for S3 buckets?"
   - "How should I design for high availability?"
   - "What is the cost optimization pillar?"

3. The bot will respond with an answer based on AWS Well-Architected Framework documentation

### Example Interaction

```
User: /ask-aws What are the key principles of the security pillar?

Bot: Based on the AWS Well-Architected Framework Security Pillar, the key 
principles include:

1. Implement a strong identity foundation
2. Apply security at all layers
3. Enable traceability
4. Automate security best practices
5. Protect data in transit and at rest
6. Keep people away from data
7. Prepare for security events

[Additional context from the framework documentation...]
```

## 🔒 Security

This project follows security best practices:

### Implemented Security Measures

- ✅ **OWASP Top 10 2025 Compliance**
- ✅ **AWS Security Best Practices**
- ✅ **IAM Least Privilege Principle**
- ✅ **Secrets Management** (AWS Secrets Manager)
- ✅ **Data Encryption** (at rest and in transit)
- ✅ **Content Filtering** (Bedrock Guardrails)
- ✅ **Security Scanning** (CodeQL, Dependabot)
- ✅ **Audit Logging** (CloudWatch Logs)

### Security Features

- **No Hardcoded Secrets**: All credentials stored in Secrets Manager
- **Encrypted Storage**: S3 buckets encrypted with SSE-S3
- **Network Security**: API Gateway with request signing verification
- **Content Safety**: Bedrock Guardrails filter inappropriate content
- **PII Protection**: Automatic PII detection and anonymization
- **Access Control**: IAM roles with minimal required permissions

For more details, see [SECURITY.md](.github/SECURITY.md).

## 📊 Monitoring

### CloudWatch Logs

- **API Gateway Logs**: `/aws/apigateway/bedrock-kb-slackbot-api`
- **Lambda Logs**: `/aws/lambda/BedrockKbSlackbotFunction`

### Key Metrics

Monitor these CloudWatch metrics:

- **API Gateway**: Request count, latency, error rate
- **Lambda**: Invocations, duration, errors, throttles
- **Bedrock**: Token usage, API calls
- **OpenSearch**: Query latency, index size

### Alarms

Set up CloudWatch Alarms for:
- High error rates
- Unusual latency spikes
- Lambda function failures
- API Gateway 5xx errors

## 🔧 Troubleshooting

### Common Issues

#### 1. Slack Command Not Responding

**Symptoms**: `/ask-aws` command doesn't respond in Slack

**Solutions**:
- Verify API Gateway URL is correctly configured in Slack App settings
- Check API Gateway logs in CloudWatch
- Verify Slack Signing Secret matches in Secrets Manager
- Check Lambda function logs for errors

#### 2. "Knowledge Base Not Found" Error

**Symptoms**: Lambda returns error about Knowledge Base

**Solutions**:
- Verify Knowledge Base ID in Lambda environment variables
- Check Bedrock Knowledge Base status in AWS Console
- Ensure Knowledge Base has completed initial sync

#### 3. "Access Denied" Errors

**Symptoms**: Lambda cannot access Bedrock or OpenSearch

**Solutions**:
- Verify IAM role has required permissions
- Check Bedrock model access in AWS Console
- Verify OpenSearch Serverless access policy

#### 4. Slow Response Times

**Symptoms**: Bot takes too long to respond

**Solutions**:
- Increase Lambda memory size
- Check OpenSearch Serverless performance
- Monitor Bedrock API latency
- Review CloudWatch metrics for bottlenecks

### Debug Mode

Enable debug logging:

1. Set Lambda environment variable: `LOG_LEVEL=DEBUG`
2. Check CloudWatch Logs for detailed output
3. Review API Gateway request/response logs

### Getting Help

- Check [GitHub Issues](https://github.com/Twodragon0/amazon-bedrock-knowledgebase-slackbot/issues)
- Review [CONTRIBUTING.md](CONTRIBUTING.md)
- See [AWS Documentation](https://docs.aws.amazon.com/bedrock/)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `npm test`
5. Run security checks: `npm audit`
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to the branch: `git push origin feature/your-feature`
8. Open a Pull Request

### Code Standards

- Follow TypeScript/JavaScript best practices
- Follow Python PEP 8 style guide
- Write tests for new features
- Update documentation
- Ensure security best practices

## 📄 License

This project is licensed under the MIT-0 License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- AWS Well-Architected Framework team for comprehensive documentation
- Slack for the Bolt framework
- Amazon Bedrock team for RAG capabilities
- Original authors: Barry Conway and Dean Colcott

## 📚 Additional Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/)
- [Slack Bolt for Python](https://slack.dev/bolt-python/)
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [Blog Post: Create a generative AI assistant with Slack and Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/create-a-generative-ai-assistant-with-slack-and-amazon-bedrock/)

---

**Made with ❤️ using AWS Bedrock and Slack**

For security issues, please see [SECURITY.md](.github/SECURITY.md).
