# AWS CDK

# Install CDK
 - npm install -g aws-cdk ( for cli)
 - pip install  aws-cdk-lib ( python module )

# Boot Strap CDK
cdk bootstrap aws://011755346992/eu-west-2 --tags CDK_TOLLKIT=dvCDK

- another way to get aws account id
 ```aws sts get-caller-identity --profile dev```

- another way to get aws region
    ```aws configure get region```

# Create Hello-CDK App
 - mkdir hello-cdk
 - cdk init app --lanuage python
 - add aws_cdk.core in requirements.txt
 - pip install -r requirements.txt ( this will take a while about 10-15 minutes atleast)
