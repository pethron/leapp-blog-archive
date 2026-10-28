---
title: "What is an IAM Principal?"
author: "Alessandro Gaggia"
date: 2023-06-07
tags: ["iam"]
description: "A brief explanation"
cover: images/d66f0d45-cb88-4aff-83ea-d963a9fa024b.png
original_url: https://blog.leapp.cloud/what-is-an-iam-principal
---

# What is an IAM Principal?

Whenever you find yourself working with the AWS access model, being a newbie or an experienced DevOps, there is a lot of terminology to digest and learn.

Users, Roles and Policies are terms that we learn pretty early in our career, however, there is one concept that has a lot of meaning behind it and, in my opinion, deserves a little more explanation: **IAM Principal**!

## IAM Principal: definition

Let’s start by giving a standard definition: *a principal is a human user or workload that can make a request for an action or operation on an AWS resource.*

Moreover, a principal is anything, AWS related, that can *send a request to AWS, via the* **Management Console**, **the AWS API**, or **the AWS CLI.**

## IAM Principal: actors

In AWS **What** or **Who** are the “actors” that can be referred as Principals?

* Root User
    
* IAM Users
    
* IAM Roles/Temporary Security Tokens
    

The main differences among them are **Who can impersonate them**, and **What credentials they are granted**.

**Users** are impersonated by human users while **Roles** by services, or workloads in general.

Also, while the first actors are granted **long-lived credentials**, Roles use **temporary credentials**.

**Root user**

The Root user is the owner of the AWS main Account, and it should be protected by **MFA** and a **strong password** right after registering. We **should avoid using the Root user as a Principal**, for security reasons, and instead use IAM Users and Roles.

He accesses AWS with email and password: that is why we must avoid using it for operation work!

---

**IAM Users**

an IAM user is a **persistent** entity that is given a set of credentials to manage services on AWS. The IAM User can be associated with both long or short-lived credentials (tough short-lived ones are **much preferred**).

An IAM User can be authorized to perform actions directly via an AWS Policy attached to it, or via a Group Policy.

An IAM User is created through:

* AWS Management Console
    
* CLI
    
* SDKs
    

---

**IAM Role**

an IAM Role is a Principal **associated directly with AWS Resources** or assumed by an IAM User, the AWS CLI, or one of the AWS SDKs available. It has **permissions granted via temporary credentials**. It has one or more Policies attached to it.

Some use cases related to IAM Roles involve:

* **Amazon EC2 Roles**: grant permissions to **applications running on an Amazon EC2 instance**.
    
* **Cross-Account Access**: grant permissions to **users from other AWS accounts**, whether in control of those accounts or not.
    

**Temporary Security Tokens:**

Temporary Security Tokens are obtained from the AWS Security Token Service (STS).

They always have an expiration date and time, and have a lifespan between **15 minutes** and **up to 36 hours**.

These tokens are usually obtained through a **Federation Process**, which involves granting permissions to users **authenticated by a trusted external system**.

Here is a summary from AWS showing some types of Roles/Temporary Security Tokens and from what they are obtained:

| Principal | Type | Docs & Links |
| --- | --- | --- |
| Federated User (Login via custom proxy architecture) | FederatedUser |  |
| Web Federated User (Login with Amazon, Amazon Cognito, Facebook, Google) | AssumedRole | [https://docs.aws.amazon.com/IAM/latest/UserGuide/id\_roles\_providers\_oidc\_user-id.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc_user-id.html) |
| SAML 2.0 Federated User | AssumedRole | [https://docs.aws.amazon.com/IAM/latest/UserGuide/id\_roles\_providers\_saml.html#CreatingSAML-userid](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html#CreatingSAML-userid) |
| AWS SSO User | AssumedRole | [https://dev.to/aws-heroes/adding-aws-sso-and-controlling-permissions-56ga](https://dev.to/aws-heroes/adding-aws-sso-and-controlling-permissions-56ga) |

A special mention goes to **AWS SSO Users** that are **configured via IAM Identity Center permission sets** to access different **accounts with different roles**. When a user lands on an account **a role is given transparently** to access services and resources according to the policies set up by the administrator.

IAM Roles, AWS SSO, and Temporary Security Tokens are meant for advanced AWS IAM usage and have always a **limited set duration of time**.

Because these Principals are **extremely important and versatile**, I strongly advise reading more on the argument, starting from [this article](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) and also this [one](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html#principaltable), concluding with this [one](https://dev.to/aws-heroes/adding-aws-sso-and-controlling-permissions-56ga) from AWS Hero [**Matt Lewis**](https://aws.amazon.com/it/developer/community/heroes/matt-lewis/).

## IAM Principal: authentication, requests, and authorization

When working with Principals we must understand the two actions that must be taken to finally obtain a set of valid Credentials.

First **Authentication** of the subject against AWS or a valid Identity Provider, and then **Authorization** to be able to perform actions and access specific resources.

### IAM Principal: Authentication

A Principal must always authenticate to send AWS requests.

Only Amazon S3, SQS, SNS, and AWS STS allow limited (and specific) requests from anonymous users, **but they're the exception**.

To log in as a **Root User on the console**, use your **email and password**.

As a **Federated User**, you can access AWS resources through **IAM roles granted by your identity provider's authentication**.

Enter your Access Key ID and Secret Access Key to authenticate as an **IAM user**.

To authenticate workloads, use **temporary** or long-term credentials (always preferring the first).

DevOps’ best practices recommend using MFA and temporary credentials to keep your account secure.

### IAM Principal: Request

When a principal tries to do something with AWS using the AWS Management Console, an SDK, or the CLI, it sends a *request* to AWS with the following information:

* **Actions or operations:** the actions to perform.
    
* **Resources:** the AWS services or objects to manipulate.
    
* **Principal:** and now we know what they can be 😀!
    
* **Environment data:** various metadata, like IP address, User agent, etc.
    
* **Resource data:** metadata depending on the specific AWS resource.
    

AWS puts all of these in a *request context*, which is used to evaluate and authorize the request.

### IAM Principal: Authorization

After Authentication, you must also be authorized to complete your request.

During the authorization process, AWS uses the *request context* to check for **policies that conform to the request**.

It then **parses the policies to determine whether to allow or deny the request**.

Most policies are stored in AWS as [JSON documents](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json) and specify the permissions for principal entities. There are [several types of policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) that can affect the outcome of the request.

If a single permissions policy **includes a denied action**, **AWS denies the entire request and stops evaluating**.

Because requests are *denied by default*, they can complete only if every part of the request is allowed by the permissions policies.

The general rules to understand how the authorization works are the following:

* **By default, all requests are denied**.
    
* **An explicit allow** (identity-based or resource-based) **overrides the default deny**.
    
* **Organizations' SCPs, IAM permissions boundaries, or session policies override the allow**. But **if there is more than one of these policies, they all need to allow the request**.
    
* An **explicit denial in any policy overrides any allows**.
    

To learn more about how this process is evaluated, see [Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).

## IAM Principal: Credentials

As we have seen there are two types of credentials granted to a Principal: **long-lived** and **temporary short-lived**.

Long-lived credentials last until an administrator **explicitly removes them** from a Principals and usually, are applied to **Root Users** and **IAM Users/Groups**.

**Short-lived credentials are temporary**, and have an explicit expiration date and time.

**They are generated through AWS STS Service** and a**re associated with IAM Roles, Assumed Roles**, or even **Federated Identities** (AWS SSO, Web, SAML, OIDC, OAuth, Cognito, Azure AD, etc.)

## IAM Principal: Best Practices

As short-lived credentials can also be applied to a Group or a User thanks to the Assume Role action, I **strongly recommend adhering to DevOps best practices and always using short-lived credentials whenever possible.**

It is preferable to use temporary credentials **because they reduce the potential damage done by an attacker stealing them** (they are limited in time).

It is also savvy to **narrow down policies associated with users and roles to the bare minimum set of resources** that you need for your work. Always take advantage of the Deny First rules!

With the Introduction of **IAM Identity Center is always preferable for administrators to use it for creating new Users** as they will also benefit from a landing panel to choose the account and role from.

## Sum Up

In this short article, we learned about AWS IAM Principals, how they are categorized, and what they stand for.

We have learned that IAM Principals have to deal with both an Authentication and an Authorization process to be able to operate successfully on AWS.

We have seen what a request, made to AWS by a Principal, contains.

We have seen what a Root account and an IAM User are, how they differ from IAM Roles, and moreover from Temporary Security Tokens.

We have analyzed the differences between Long and Short-lived Credentials, and why the latter are preferable and more secure.

We have proposed some basic best practices to follow to better use your AWS Principals.

So, thank you all for reaching the end of the article!

As always, if you have suggestions or questions, feel free to come and have a chat with us on our [Slack](https://join.slack.com/t/noovolari/shared_invite/zt-opn8q98k-HDZfpJ2_2U3RdTnN~u_B~Q) community.

Until next time, see ya and stay safe! 🙂
