#!/usr/bin/env python3
"""
Generate architecture diagram for Amazon Bedrock Knowledge Base Slackbot
This script creates a visual architecture diagram using the diagrams library.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.database import OpenSearch
from diagrams.aws.ml import Bedrock
from diagrams.aws.security import SecretsManager, IAM
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import User
from diagrams.onprem.chat import Slack

def generate_architecture_diagram():
    """Generate the architecture diagram for the Slackbot application."""
    
    graph_attr = {
        "fontsize": "16",
        "bgcolor": "white",
        "pad": "0.5"
    }
    
    with Diagram(
        "Amazon Bedrock Knowledge Base Slackbot Architecture",
        filename="docs/architecture-diagram",
        show=False,
        direction="LR",
        graph_attr=graph_attr
    ):
        # User and Slack
        user = User("Slack User")
        slack = Slack("Slack Workspace")
        
        # API Gateway
        api = APIGateway("API Gateway\n/slack/ask-aws")
        
        # Lambda Functions
        with Cluster("AWS Lambda"):
            slackbot_lambda = Lambda("BedrockKbSlackbotFunction\n(Python 3.12)")
            create_index_lambda = Lambda("CreateIndexFunction\n(Custom Resource)")
        
        # Secrets Management
        with Cluster("Secrets Management"):
            secrets = SecretsManager("Secrets Manager\n(Slack Bot Token\n& Signing Secret)")
            ssm = IAM("SSM Parameter Store\n(Parameter References)")
        
        # Bedrock Services
        with Cluster("Amazon Bedrock"):
            bedrock_kb = Bedrock("Knowledge Base\n(AWS Well-Architected\nFramework)")
            bedrock_guardrails = Bedrock("Guardrails\n(Content Filtering)")
            bedrock_model = Bedrock("Claude 3.5 Sonnet\n(RAG Model)")
            bedrock_embedding = Bedrock("Titan Embeddings\n(Embedding Model)")
        
        # Vector Database
        with Cluster("OpenSearch Serverless"):
            vector_db = OpenSearch("Vector Collection\n(slack-bedrock-vector-db)")
            vector_index = OpenSearch("Vector Index\n(slack-bedrock-os-index)")
        
        # Storage
        s3_bucket = S3("S3 Bucket\n(Knowledge Base\nDocuments)")
        
        # Monitoring
        cloudwatch = Cloudwatch("CloudWatch Logs\n(Monitoring & Logging)")
        
        # Connections
        user >> Edge(label="Slash Command\n/ask-aws") >> slack
        slack >> Edge(label="POST Request") >> api
        api >> Edge(label="Invoke") >> slackbot_lambda
        
        slackbot_lambda >> Edge(label="Read Secrets") >> secrets
        slackbot_lambda >> Edge(label="Read Parameters") >> ssm
        slackbot_lambda >> Edge(label="Retrieve & Generate") >> bedrock_kb
        
        bedrock_kb >> Edge(label="Query") >> vector_db
        bedrock_kb >> Edge(label="Apply Guardrails") >> bedrock_guardrails
        bedrock_kb >> Edge(label="Generate Response") >> bedrock_model
        bedrock_kb >> Edge(label="Embed Documents") >> bedrock_embedding
        
        # Note: vector_index is part of vector_db collection, no direct connection needed
        # vector_db >> vector_index  # Removed: Statement has no effect
        
        bedrock_kb >> Edge(label="Ingest Documents") >> s3_bucket
        
        create_index_lambda >> Edge(label="Create Index") >> vector_index
        
        slackbot_lambda >> Edge(label="Logs") >> cloudwatch
        api >> Edge(label="Access Logs") >> cloudwatch
        
        slackbot_lambda >> Edge(label="Response") >> api
        api >> Edge(label="Response") >> slack
        slack >> Edge(label="Display Answer") >> user

if __name__ == "__main__":
    print("Generating architecture diagram...")
    print("Installing required packages if needed...")
    print("Run: pip install diagrams")
    print("\nGenerating diagram...")
    generate_architecture_diagram()
    print("✓ Architecture diagram generated: docs/architecture-diagram.png")

