#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aws_cdk as cdk

from cdk_poc.cdk_poc_stack import CdkPocStack


app = cdk.App()
CdkPocStack(app, "cdk-poc")

app.synth()
