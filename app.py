# -*- coding: utf-8 -*-
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import aws_cdk as cdk
from demo_pipeline import CDKDemoPipeline

env_EU = cdk.Environment(region="eu-west-2")

app = cdk.App()

CDKDemoPipeline(app, "cdk-demo-pipeline", env=env_EU)

app.synth()
