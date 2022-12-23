# -*- coding: utf-8 -*-
from constructs import Construct

from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    CfnOutput,
    aws_iam as iam,
    aws_kms as kms,
    aws_s3 as s3,
    aws_codebuild as codebuild,
)


class CDKDemoPipeline(Stack):
    def __init__(self, scope: Construct, construct_id: str, props={}, **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        self.stack_data = props.copy()

        self.pipeline_role(scope, construct_id, **kwargs)
        self.pipeline_bucket(scope, construct_id, **kwargs)
        self.pipeline_codebuild(scope, construct_id, **kwargs)

    def pipeline_role(self, scope, construct_id, **kwargs):

        role = iam.Role(
            self,
            f"{construct_id}-Role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("s3.amazonaws.com"),
                iam.ServicePrincipal("codebuild.amazonaws.com"),
                iam.ServicePrincipal("codepipeline.amazonaws.com"),
                iam.ServicePrincipal("cloudformation.amazonaws.com"),
                iam.ServicePrincipal("codecommit.amazonaws.com"),
                iam.ServicePrincipal("codestar.amazonaws.com"),
            ),
            description=f"{construct_id} Role for Bucket and Codebuild",
        )

        """
        Github Connection policy statement
        """
        codestart_connection_policy_statement = iam.PolicyStatement(
            actions=[
                "codestar-connections:CreateConnection",
                "codestar-connections:DeleteConnection",
                "codestar-connections:GetConnection",
                "codestar-connections:ListConnections",
                "codestar-connections:GetInstallationUrl",
                "codestar-connections:GetIndividualAccessToken",
                "codestar-connections:ListInstallationTargets",
                "codestar-connections:StartOAuthHandshake",
                "codestar-connections:UpdateConnectionInstallation",
                "codestar-connections:UseConnection",
                "codestar-connections:TagResource",
                "codestar-connections:ListTagsForResource",
                "codestar-connections:UntagResource",
                "iam:PassRole",
                "s3:GetObject",
                "s3:PutObject",
                "s3:GetObjectVersion",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation",
                "codebuild:*",
            ],
            resources=["*"],
        )

        role.add_to_policy(codestart_connection_policy_statement)

        """
        Some informative outputs to cloudformation stack
        """
        CfnOutput(
            self,
            f"{construct_id}-Role-ARN",
            description=f"{construct_id} Role ARN",
            value=role.role_arn,
            export_name=f"{construct_id}-Role-ARN",
        )

        CfnOutput(
            self,
            f"{construct_id}-RoleName",
            description=f"{construct_id} Role Name",
            value=role.role_name,
            export_name=f"{construct_id}-RoleName",
        )

        self.stack_data.update({"role": role})

    def pipeline_bucket(self, scope, construct_id, **kwargs):
        """
        bucket key
        """
        key = kms.Key(
            self,
            f"{construct_id}-Key",
            removal_policy=RemovalPolicy.DESTROY,
            pending_window=Duration.days(10),
            description=f"{construct_id} Bucket Key",
        )

        """
        s3 bucket creation
        """
        bucket = s3.Bucket(
            self,
            f"{construct_id}-Bucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            encryption_key=key,
        )

        """
        Output
        """
        CfnOutput(
            self,
            f"{construct_id}-BucketName",
            description=f"{construct_id} Bucket Name",
            value=bucket.bucket_name,
            export_name=f"{construct_id}-BucketName",
        )

        CfnOutput(
            self,
            f"{construct_id}-BucketARN",
            description=f"{construct_id} Bucket ARN",
            value=bucket.bucket_arn,
            export_name=f"{construct_id}-BucketARN",
        )

        bucket.grant_read_write(self.stack_data["role"])
        self.stack_data.update({"bucket": bucket})

    def pipeline_codebuild(self, scope, construct_id, **kwargs):

        code_build = codebuild.Project(
            self,
            f"{construct_id}-codebuild",
            role=self.stack_data["role"],
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "build": {
                            "commands": [
                                f"echo 'Hello from {construct_id} CodeBuild'",
                                "ls -la",
                                "pwd",
                                "env",
                            ]
                        }
                    },
                }
            ),
        )

        """
        Output
        """
        CfnOutput(
            self,
            f"{construct_id}-CodeBuildName",
            description=f"{construct_id} Codebuild Project Name",
            value=code_build.project_name,
            export_name=f"{construct_id}-BuildName",
        )
