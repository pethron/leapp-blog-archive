---
title: "Increase AWS Security Posture with IAM Roles and Policies"
author: "Alessandro Gaggia"
date: 2023-08-03
tags: ["iam"]
description: "Tips and tricks to master the AWS IAM"
cover: images/2a94284f-34ad-43e2-b2b2-bb128f77e96d.png
original_url: https://blog.leapp.cloud/increase-aws-security-posture-with-iam-roles-and-policies
---

# Increase AWS Security Posture with IAM Roles and Policies

In this article we will discuss identity and access management (IAM) within Amazon Web Services (AWS), focusing on the similarities and differences between IAM roles and policies.

This article will provide examples of both roles and policies and explains how they relate to IAM roles, users, and groups.

By the end, you will have a clear understanding of IAM within AWS and be better equipped to manage access and identity needs on the platform.

## What is an IAM Policy in AWS?

An IAM policy is a document that **defines permissions for AWS resources**. It is an essential component of AWS identity and access management (IAM) that provides fine-grained control over who can access specific resources in your AWS account.

IAM policies **are used to grant or deny access to AWS resources** such as Amazon S3 buckets, EC2 instances, and RDS databases.

IAM policies are written in JSON format and consist of one or more statements. Each statement contains a set of permissions for a specific resource or set of resources. For example, you might use an IAM policy to grant read-only access to a particular S3 bucket, or to allow a user to start and stop an EC2 instance.

## Elements of an IAM Policy

An IAM policy is comprised of the following main elements:

| Element | Description |
| --- | --- |
| Version | The version of the IAM policy language used. |
| Statement | A list of one or more statements that define the permissions for the policy. |
| Effect | Specifies whether the statement allows or denies access to the resource. |
| Action | The specific actions that are allowed or denied for the resource. |
| Resource | The AWS resource that the policy applies to. |
| Principal | The entity that the policy applies to. |

### Version

The Version element specifies the version of the IAM policy language used in the policy.

The current version of the policy language is October 17, 2012.

Example:

```json
{
    "Version": "2012-10-17",
    ...
}
```

### Statement

The Statement element is a list of one or more statements that define the permissions for the policy.

Example:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            ...
        },
        {
            ...
        }
    ]
}
```

### Effect

The Effect element specifies whether the statement allows or denies access to the resource.

The values for Effect are `Allow` and `Deny`.

Example:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            ...
        },
        {
            "Effect": "Deny",
            ...
        }
    ]
}
```

### Action

The Action element specifies the specific actions that are allowed or denied for the resource.

Example:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            ...
        },
        {
            "Effect": "Deny",
            "Action": "ec2:*",
            ...
        }
    ]
}
```

### Resource

The Resource element specifies the AWS resource that the policy applies to.

Example:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::example-bucket/*",
            ...
        },
        {
            "Effect": "Deny",
            "Action": "ec2:*",
            "Resource": "*",
            ...
        }
    ]
}
```

### Principal

The Principal element specifies the entity that the policy applies to.

Example:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::example-bucket/*",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::123456789012:user/Bob",
                    "arn:aws:iam::123456789012:role/DevOps"
                ]
            },
            ...
        },
        {
            "Effect": "Deny",
            "Action": "ec2:*",
            "Resource": "*",
            "Principal": "*",
            ...
        }
    ]
}
```

## What is an IAM Role in AWS?

**An IAM role is an AWS identity with permission policies that determine what the identity can and cannot do in AWS**.

IAM roles are similar to IAM users, but with some important differences.

IAM roles are not associated with a specific user or group. Instead, they are intended to be assumed by anyone who needs the permissions associated with the role.

**IAM roles are a way to delegate access to AWS resources without the need to create and manage long-term AWS credentials**.

For example, you might create an IAM role that grants access to an S3 bucket, and then allow a Lambda function to assume that role when it needs to access the bucket.

This way, you don't need to manage access keys for the Lambda function, and you can maintain tighter control over who has access to the S3 bucket.

### Main Elements of an IAM Role

| Element | Description |
| --- | --- |
| Role Name | The name assigned to the role. |
| Role ARN | The Amazon Resource Name (ARN) assigned to the role. |
| Assume Role Policy | The policy document that grants permission to assume the role. |
| Inline Policies | One or more inline policies that are attached to the role. |
| Managed Policies | One or more managed policies that are attached to the role. |

## Assuming an AWS IAM Role

Assuming an AWS IAM Role means **temporarily taking on the permissions and policies associated with that role**. This is done by using the **AWS Security Token Service (STS)** API to obtain temporary security credentials, which include an access key, a secret access key, and a security token.

The **user who is assuming the role must have permission to do so**, which is granted **by the role's trust policy**. The trust policy specifies which users or services are allowed to assume the role.

There are several ways to assume an IAM Role in AWS, including using the AWS Management Console, AWS CLI, AWS SDKs, and the AssumeRole API.

When using the **AssumeRole API, the user must provide their own security credentials and the ARN of the role they want to assume**. The API then returns temporary security credentials that can be used to access AWS resources associated with the role.

Once the user has obtained temporary security credentials, they can use them to access AWS resources associated with the role until the credentials expire. **The length of time that the credentials are valid can be set in the role's session duration policy. By default, this is set to one hour but can be increased up to 12 hours**.

## How is an IAM Policy different from an IAM Role?

An IAM policy and an IAM role are both used to control access to AWS resources. However, they serve different purposes.

**An IAM policy is used to define permissions** for a specific AWS resource or set of resources. It is **attached to a user, group, or role** to **grant or deny access** to those resources.

IAM policies **are static and do not change based on the user, group, or role** that is accessing the resources.

In contrast, **an IAM role is a set of permissions that can be assumed by a user, group, or service**.

**It is a way to delegate access to AWS resources without the need to share long-term security credentials such as access keys**.

When a **user** (or a service) assumes an IAM role, they inherit the permissions associated with the role. **IAM roles are dynamic** (opposed to policies) and can change based on the user, group, or service that is assuming the role.

**IAM roles are useful for scenarios where you need to grant temporary access to a resource**.

For example, you might have a script that needs to access an S3 bucket to upload a file. Instead of embedding AWS credentials in the script, you can create an IAM role that has permission to access the S3 bucket and then assume that role in the script.

## Examples of IAM Policies

Here are some examples of simple IAM policies for common use cases:

### Allow read-only access to an S3 bucket

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::example-bucket",
                "arn:aws:s3:::example-bucket/*"
            ]
        }
    ]
}
```

This policy allows a user to read objects from the `example-bucket` S3 bucket and list the contents of the bucket, but does not allow them to upload or modify objects.

### Allow full access to an EC2 instance

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:*",
            "Resource": "*"
        }
    ]
}
```

This policy allows a user to perform any action on any EC2 instance in the account.

### Allow read-only access to an RDS instance

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "rds:DescribeDBInstances",
                "rds:DescribeDBSnapshots",
                "rds:DownloadDBLogFilePortion"
            ],
            "Resource": [
                "arn:aws:rds:us-west-2:123456789012:db:mysql-db",
                "arn:aws:rds:us-west-2:123456789012:snapshot:mysql-db-snapshot"
            ]
        }
    ]
}
```

This policy allows a user to view information about the `mysql-db` RDS instance and download log files, but does not allow them to perform any modifications.

### Allow read-only access to an SQS queue

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sqs:GetQueueUrl",
                "sqs:ReceiveMessage"
            ],
            "Resource": "arn:aws:sqs:us-west-2:123456789012:example-queue"
        }
    ]
}
```

This policy allows a user to retrieve the URL of the `example-queue` SQS queue and receive messages from the queue, but does not allow them to send messages or modify the queue in any way.

### Allow read-only access to a DynamoDB table

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:DescribeTable",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan"
            ],
            "Resource": "arn:aws:dynamodb:us-west-2:123456789012:table/example-table"
        }
    ]
}
```

This policy allows a user to view the schema of the `example-table` DynamoDB table and read items from the table, but does not allow them to modify the table in any way.

## Increase AWS Security Posture with IAM Roles and Policies

Using a combination of IAM roles and policies is an effective way to **increase the security posture** of an AWS account. Here are some best practices to follow:

### Use Least Privilege

When creating IAM policies, it's important to **use the principle of least privilege**. This means granting users and roles **only the permissions they need to perform their job functions and no more**.

For example, if a user only needs read access to an S3 bucket, don't grant them write or delete access.

### Rotate Credentials

AWS recommends **regularly rotating access keys and secret access keys for IAM users and roles**. This helps to reduce the risk of unauthorized access to your resources in the event that credentials are compromised.

### Use IAM Roles Instead of Access Keys

**IAM roles are a more secure way to grant temporary access to AWS resources than using access keys**.

When a user assumes an IAM role, they get temporary security credentials that expire after a specified amount of time. This minimizes the risk of credentials being compromised and reduces the need to manage long-term access keys.

### Use Managed Policies

AWS provides a number of managed policies that can be used to grant permissions to users and roles.

**These policies are created and maintained by AWS and are designed to follow best practices for security and compliance**.

By using managed policies, you can be sure that your users and roles have the appropriate permissions without having to create and maintain policies yourself.

### Use Conditions in IAM Policies

**IAM policies can include conditions that further restrict the permissions granted to users and roles**.

For example, you can create a policy that only allows access to a resource during certain hours of the day or only from certain IP addresses.

**Using conditions can help to further reduce the risk of unauthorized access** to your resources.

### Use Multi-Factor Authentication (MFA)

**Enabling multi-factor authentication (MFA) for IAM roles is an effective way to increase the security** of your AWS account.

MFA requires users to provide a second form of authentication, such as a hardware token or a mobile app, in addition to their password.

This makes it much more difficult for an attacker to gain unauthorized access to your resources even if they have obtained the user's password.

By following these best practices, you can significantly increase the security posture of your AWS account and better protect your resources from unauthorized access.

## What have we seen

In this article, we explored the differences and similarities between IAM roles and policies in AWS.

IAM policies define permissions for AWS resources and are used to grant or deny access to specific resources in your AWS account.

IAM roles, on the other hand, are AWS identities with permission policies that determine what the identity can and cannot do in AWS. IAM roles are a way to delegate access to AWS resources without the need to create and manage long-term AWS credentials.

We also discussed the main elements of an IAM policy, including the version, statement, effect, action, resource, and principal. Additionally, we explained how to assume an IAM role in AWS using the AWS Security Token Service (STS) API.

To increase the security posture of an AWS account, we recommended using a combination of IAM roles and policies and following best practices such as using least privilege, rotating credentials, using managed policies, using conditions in IAM policies, and enabling multi-factor authentication (MFA) for IAM roles.

Overall, by understanding the differences between IAM roles and policies and following best practices, you will be better equipped to manage access and identity needs on the AWS platform.

I really hope that this little article has been of help for all of you, and as always, feel free to comment and reach us on our [community slack](https://join.slack.com/t/noovolari/shared_invite/zt-opn8q98k-HDZfpJ2_2U3RdTnN~u_B~Q).

Until next time, stay safe and see you in the next article, in which we’ll discuss about IAM Users and Groups! 😉
