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
            "DemoPipelineRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("s3.amazonaws.com"),
                iam.ServicePrincipal("codebuild.amazonaws.com"),
                iam.ServicePrincipal("codepipeline.amazonaws.com"),
            ),
            description="Pipeline Role for Bucket and Codebuild",
        )

        CfnOutput(
            self,
            "DemoPipelineRoleARN",
            description="Demo Pipeline Role ARN",
            value=role.role_arn,
            export_name="DemoPipelineRoleARN",
        )

        CfnOutput(
            self,
            "DemoPipelineRoleName",
            description="Demo Pipeline Role Name",
            value=role.role_name,
            export_name="DemoPipelineRoleName",
        )

        self.stack_data.update({"role": role})

    def pipeline_bucket(self, scope, construct_id, **kwargs):
        """
        bucket key
        """
        key = kms.Key(
            self,
            "DemoPipeLineKey",
            removal_policy=RemovalPolicy.DESTROY,
            pending_window=Duration.days(10),
            description="Demo Pipeline Bucket Key",
        )

        """
        s3 bucket creation
        """
        bucket = s3.Bucket(
            self,
            "DemoPipelineBucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            encryption_key=key,
        )

        """
        Output
        """
        CfnOutput(
            self,
            "DemoPipelineBucketName",
            description="Demo Pipeline Bucket Name",
            value=bucket.bucket_name,
            export_name="DemoPipelineBucketName",
        )

        CfnOutput(
            self,
            "DemoPipelineBucketARN",
            description="Demo Pipeline Bucket ARN",
            value=bucket.bucket_arn,
            export_name="DemoPipelineBucketARN",
        )

        bucket.grant_read_write(self.stack_data["role"])
        self.stack_data.update({"bucket": bucket})

    def pipeline_codebuild(self, scope, construct_id, **kwargs):

        code_build = codebuild.Project(
            self,
            "DemoCodeBuild-1",
            role=self.stack_data["role"],
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "build": {"commands": ["echo 'Hello from Demo CodeBuild 1'"]}
                    },
                }
            ),
        )

        """
        Output
        """
        CfnOutput(
            self,
            "DemoPipelineCodeBuildName",
            description="Codebuild Project Name",
            value=code_build.project_name,
            export_name="DemoPipelineCodeBuildName",
        )
