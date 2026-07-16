# Bedrock Managed Knowledge Base Support

## Changes
- CDK stack updated to create managed KB via `addPropertyOverride` with `type: MANAGED`
- Added `MANAGED_KNOWLEDGE_BASE_CONNECTOR` data source for managed ingestion
- Slackbot Lambda retrieval function updated to use `managedSearchConfiguration`
- Added `KNOWLEDGE_BASE_TYPE` environment variable to Lambda configuration
- Retrieval logic branches on KB type for correct search config shape

## Design
- VECTOR is the default; MANAGED via --context knowledgeBaseType=MANAGED
- CDK `addPropertyOverride` used since L2 constructs don't support managed type natively
- AgenticRetrieveStream available for enhanced Slack response quality
- Backward compatible: existing VECTOR Slackbot deployments set env var to retain behavior

## API Shapes
- KB Creation: `type: MANAGED` + `managedKnowledgeBaseConfiguration.embeddingModelType: MANAGED`
- Data Source: `type: MANAGED_KNOWLEDGE_BASE_CONNECTOR`
- Retrieval: `managedSearchConfiguration` (not `vectorSearchConfiguration`)
- Agentic: `AgenticRetrieveStream` with `foundationModelType: MANAGED`, `rerankingModelType: MANAGED`

## Configuration
| Variable | Description | Default |
|---|---|---|
| KNOWLEDGE_BASE_TYPE | MANAGED or VECTOR | VECTOR |
| USE_AGENTIC_RETRIEVAL | Enable agentic retrieval | true |
| KNOWLEDGE_BASE_ID | Slackbot KB ID (CDK output) | (required) |

## SDK Requirements
- boto3 >= 1.43 for managed search and agentic retrieval
- aws-cdk-lib >= 2.170.0 for KB L1 constructs

## Required IAM Permissions
```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:Retrieve",
    "bedrock:AgenticRetrieveStream"
  ],
  "Resource": "arn:aws:bedrock:<region>:<account-id>:knowledge-base/<kb-id>"
}
```
