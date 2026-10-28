---
title: "10 best practices to secure your AWS environment"
author: "Alessandro Gaggia"
date: 2022-03-10
tags: ["aws"]
description: "10 best practices to help put your mind at peace when working with AWS"
cover: images/4c4f3656-b2f6-4abd-bde0-e12576a4556f.png
original_url: https://blog.leapp.cloud/10-best-practices-to-secure-your-aws-environment
---

# 10 best practices to secure your AWS environment

You registered to AWS. You are eager to start using it.

You want to solve the problem that drove you to Amazon Web Services in the first place.

However, when starting to use a Cloud Environment for work, **security must be addressed first**.

You need to secure your AWS resources, especially your accounts, from possible attacks. In this article, I want to describe 10 **best practices to follow** to help you put your mind at peace when working with AWS.

Let’s start!

## Create Strong, Secure Password

Always use **randomly-generated solid** passwords with at least **24-30 characters, symbols, uppercase letters, and numbers.**

Because these passwords are complex, always use a secure vault to store and retrieve them easily. Something like [LastPass](https://www.lastpass.com/) or [BitWarden](https://bitwarden.com/) can help! Give it a try.

## Multi-Factor Authentication Everywhere

AWS allows for Multi-Factor Authentication for the root account (**indispensable**) and other accounts. Try to consistently enforce MFA whenever possible if you don’t want your account hacked, [or else](https://www.reddit.com/r/aws/comments/rvi9a8/thanks_to_all_of_the_my_account_was_hacked_posts/)...

To enable MFA for **the root account**, follow this [guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html#enable-virt-mfa-for-root). To enforce MFA for IAM users, follow this [guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html#enable-virt-mfa-for-iam-user) instead.

If you are a developer and need to access programmatically, you can use [Leapp](https://github.com/Noovolari/leapp) to access with MFA.

Remember also that:

- You can add more than one device (or virtual device) per account or user.
- You can [replace or “rotate”](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html#replace-virt-mfa) a device.

## Remove credentials from your root account

Your root account must be used only once to register to AWS and must NOT be used for anything else, as it can access everything in your environment. One of the first step**s** is removing **programmatic access from it**.

Create an IAM user and grant that user only the permissions needed for the APIs you plan to call.

Follow this [guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials) to understand how to do it.

## Enable CloudTrail logging, store trails into separated account

Log everything that happens in your AWS environment for security breach detection and investigation with CloudTrail.

The following **best practices are general guidelines**: you can tweak them as you see fit!

- **Apply trails to all AWS Regions:** ensure that all events that occur in your AWS account are logged.
- **Enable CloudTrail log file integrity:** lets you know if a log file has been deleted or changed.
- **Always store the logs in a separate account**: enforce strict security controls, access, and segregation of duties.
- **Use AWS KMS managed keys instead of standard S3-SSE: t**o provide a directly manageable security layer.

Get started with this [guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-tutorial.html).

## Operate with IAM users, groups, and roles

**Don’t use the root user for your everyday routine.**

Instead, citing AWS: *adhere to the [best practice of using the root user only to create your first IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#create-iam-users)*.

Then you can safely store away access and secret credentials. You’ll generally not be needing them unless there are a few specific [tasks](https://docs.aws.amazon.com/general/latest/gr/root-vs-iam.html#aws_tasks-that-require-root).

**IAM users** represent an IAM identity capable of doing operations on AWS resources. **User Groups** are collections of IAM users seen as a unit. Finally, a role is attached directly to a resource and allows it to perform operations on other resources.

By exploiting these instruments, you can isolate and manage who or what is doing something in your environment in a more structured way.

## Apply the Least Privilege Principle on IAM policies

Avoid policies with Administrator access for everything!

Start with a **Deny All permission** and slowly add permissions for specific services you need for the task: this way, you’ll adhere to the Least Privilege principle.

This is a [small list of tricks](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege) that you can use to define the perfect policy for your service!

Also, there is [an open-source tool](https://github.com/iann0036/iamlive) you can use to define your policy.

## Use AWS Organizations to set up your project accounts

AWS Organizations is an account management service that enables the central management of multiple accounts. You can define your organizational structure to better sort and scope account usage with Organizational Units.

Also, AWS Organizations include consolidated billing to see the overall breakdown of expenses. This helps you find anomalies quicker.

If you have AWS Single Sign-On enabled in your Organization, you can access programmatically your [eligible roles through Leapp](https://docs.leapp.cloud/0.9.0/configuring-integration/configure-aws-single-sign-on-integration/).

AWS Organization uses **[Service Control Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)** for security purposes, which act on top of IAM Policies across all accounts, limiting their maximum available permissions. Applied to Organizational Units help define permission boundaries in different company areas.

Follow this guide to help you correctly set up your landing zone and your project’s accounts.

## Enable AWS Config rules and Billing Alarms

AWS has instruments to **verify tampering or unwanted use of AWS Resources**.

AWS Config provides a detailed view of AWS resources’ configurations in your account. This includes how they are related to each other and how they were configured in the past. AWS Config allows us to understand how they have changed over time.

Setting up AWS Config is an excellent way for **proactive and detective** actions. Use this [guide](https://docs.aws.amazon.com/config/latest/developerguide/getting-started.html) to configure it and remember to **enable AWS Config in all accounts and Regions.**

This is an industry best practice recommended by the [Center for Internet Security](https://aws.amazon.com/blogs/security/announcing-industry-best-practices-for-securing-aws-resources/).

**Billing alarms and Billing thresholds** are another great way to be notified if something is not right in your account. Configure them like this [guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html), remembering to **apply clean and meaningful TAGs** to all resources.

## Apply security at all layers

When building a project with AWS, always strive to secure all layers of your application and your environment:

- Apply HTTPS as protocol; you can do it with services like API Gateway, CloudFront, LoadBalancers, even with plain EC2 instances; also remember [mutual TLS authentication](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html) if you are developing a B2B application.
- Apply security groups to your resources to manage carefully what CIDR, specific IP addresses, and Ports can communicate in and out of your environment.
- Try to apply a good network design, isolating all the resources that don’t need direct Internet access in private VPCs, thus reducing ingress to selected Gateways that are easy to monitor.
- Always apply **encryption in transit and at rest whenever possible.** Remember that AWS offers direct encryption in S3, KMS for key management, and the ability to encrypt EBS volumes directly.

## Use temporary generated credentials

**Credentials and .aws folder are possible vectors of malicious attacks.**

To secure all your credentials and remove the hassle of creating temporary credentials via IAM Simple Token Service, I would suggest the **open-source project [Leapp](https://www.leapp.cloud/).**

Some of its features at a glance:

- **Cloud credentials generation in 1 click**
- **Data [stored locally encrypted](https://docs.leapp.cloud/latest/security/system-vault/) in the OS System Vault**
- **Multiple Cloud-Access supported [strategies](https://docs.leapp.cloud/latest/configuration/)**
- **Automatic [short-lived credentials rotation](https://docs.leapp.cloud/latest/security/credentials-generation/aws/)**
- **Automated provisioning of [Sessions](https://docs.leapp.cloud/latest/sessions/) from [AWS Single Sign-on](https://docs.leapp.cloud/latest/configuring-integration/configure-aws-single-sign-on-integration/)**
- A friendly and slick user interface 🙂

## Conclusions

With all these tips and tricks, I hope to have shown you how you can enhance the security posture of your AWS Cloud Environment.

Until next time, stay safe, and thanks for reading.

Noovolari team.
