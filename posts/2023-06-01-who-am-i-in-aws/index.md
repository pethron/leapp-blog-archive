---
title: "Who am I in AWS?"
author: "Eric Villa"
date: 2023-06-01
tags: ["aws"]
description: "Presenting IAM STS get-caller-identity"
cover: images/43ae958c-6e96-45e6-91da-b8cb47967150.png
original_url: https://blog.leapp.cloud/who-am-i-in-aws
---

# Who am I in AWS?

Have you ever been in a situation in which you were about to forward a critical API request to AWS but you were not sure what was the target of your request?

It’s always a best practice to check if the API request target is the one that you expect, especially if the operations that are about to be performed may have major repercussions on your AWS accounts.

## Who am I in the context of AWS?

When it comes generate temporary credentials and get information about them, AWS Security Token Service (AWS STS) comes to the rescue.

“Who am I in the context of AWS” is exactly the question the AWS STS GetCallerIdentity API provides an answer to. The answer tells you what is the account affected by the next API call if credentials are not going to change in the meanwhile.

Yes, I mentioned AWS STS. Indeed, this is the service that I should call upon to get that information. To interface with the GetCallerIdentity API, two requirements must be fulfilled:

* network connectivity;
    
* a valid set of AWS Credentials, placed in one of the locations the client that you’re using expects them to be (environment variables, shared configuration files, etcetera). As you can see on [this](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html) documentation page, authentication information is added to the request via the Authorization Header.
    

The reference client used in this article is the AWS CLI (Command Line Interface). The AWS CLI command that you should issue to get this information is the following:

```bash
aws sts get-caller-identity
```

## aws sts get-caller-identity response structure

Regardless of the IAM identity used to authenticate the request, the API response always contains three fields:

* UserId - the unique identifier of the calling entity;
    
* Account - the AWS Account ID number of the account that owns or contains the calling entity;
    
* Arn - the Amazon Resource Name associated with the calling identity.
    

While the Account field is always a 12-digits number, Arn and UserId depend on the principal that initiated the request.

In this blog post, we’ll focus on two categories of principals: User and AssumedRole.

The User category simply corresponds to the IAM User principal.

The AssumedRole category covers more principals, but we’ll focus on SAML federated user (assumed via AssumeRoleWithSAML API), assumed role (assumed via AssumeRole API), and role assigned to an Amazon EC2 instance.

For a complete overview of principals, please refer to the [documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html#principaltable).

Now, let’s deepen the UserId and Arn fields for each of the previously cited principals.

### IAM User

```json
{
	"UserId": "AIDACKCEVSQ6C2EXAMPLE",
	"Account": "123456789012",
	"Arn": "arn:aws:iam::123456789012:user/JohnDoe"
}
```

The UserId corresponds to the [unique ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-unique-ids) of the IAM User.

The Arn field adheres to the following template: *arn:aws:iam::&lt;account-id&gt;:user/&lt;user-name-with-path&gt;*.

### SAML federated user

```json
{
	"UserId": "AROACKCEVSQ6C2EXAMPLE:johndoe@example.com",
	"Account": "123456789012",
	"Arn": "arn:aws:sts::123456789012:assumed-role/john.doe/johndoe@example.com"
}
```

The UserId consists of the unique ID of the role (AROACKCEVSQ6C2EXAMPLE) and the caller specified role name (johndoe@example.com).

The caller specified role name corresponds to the RoleSessionName attribute that is part of the SAML assertion.

The SAML assertion is an authentication response forwarded by the external IdP to the https://region-code.signin.aws.amazon.com/saml endpoint. The SAML assertion contains a set of claims; the RoleSessionName is one of them.

Typically, the value of the RoleSessionName attribute is a user ID or an email address. As explained in [this](https://blog.leapp.cloud/how-to-saml-federate-your-aws-account-with-g-suite) blog post by my fellow colleague [Nicolò Marchesi](https://twitter.com/NicoloMarchesi), when it comes to federating a G Suite IdP to an AWS account, the RoleSessionName SAML attribute is mapped to the G Suite user’s Primary Email.

The Arn field adheres to the following template: *arn:aws:iam::&lt;account-id&gt;:assumed-role/&lt;role-name&gt;/&lt;role-session-name&gt;*. The Principal Type is not a *user* - as for the IAM User - but an *assumed-role*. Indeed, the SAML-based federation allows a user - managed by the external IdP - to assume an AWS Role via the STS assumeRoleWithSAML API.

### Assumed role

This principal corresponds to an IAM Role assumed via the AssumeRole API. Using this API, an IAM Role can be assumed by either an IAM User, an AWS IAM Identity Center user, or another IAM Role (the last configuration is called role chaining).

All these configurations provide the same GetCallerIdentity API response structure.

```json
{
	"UserId": "AROACKCEVSQ6C2EXAMPLE:FakeRoleSessionName",
	"Account": "123456789012",
	"Arn": "arn:aws:sts::123456789012:assumed-role/FakeRoleName/FakeRoleSessionName"
}
```

As for the SAML federated user scenario, the Arn field adheres to the following template: *arn:aws:iam::&lt;account-id&gt;:assumed-role/&lt;role-name&gt;/&lt;role-session-name&gt;*.

The UserId field is composed of the unique id of the role and the caller specified role name that is specified by the RoleSessionName parameter passed to the AssumeRole request.

### Role assigned to an Amazon EC2 instance

When you launch an Amazon EC2 instance, you specify an IAM role to associate with the instance. Applications that run on the instance can then use the role-supplied temporary credentials to sign API requests. To be precise, the IAM Role is encapsulated in an Instance Profile which can provide the role’s temporary credentials to an application that runs on the instance.

When you call the AWS STS GetCallerIdentity API, the request is signed using the temporary credentials supplied via the Instance Profile. The following is an example response.

```json
{
	"Account": "123456789012",
	"UserId": "AROACKCEVSQ6C2EXAMPLE:i-1234567890abcdef0",
	"Arn": "arn:aws:sts::123456789012:assumed-role/iam-role-name/i-1234567890abcdef0"
}
```

The UserId field is composed of the unique id of the role (AROACKCEVSQ6C2EXAMPLE) and the unique identifier of the EC2 instance (i-1234567890abcdef0).

The Arn field adheres to the following template: *arn:aws:iam::&lt;account-id&gt;:assumed-role/&lt;role-name&gt;/&lt;role-session-name&gt;*. The *&lt;role-name&gt;* corresponds to iam-role-name while the *&lt;role-session-name&gt;* corresponds to the unique identifier of the EC2 instance.

## That’s all Folks!

In this blog post, I’ve provided you with a description of the API that you can consume to answer the question “Who am I in the context of AWS?”. The answer to that question can vary, depending on the Principal associated with the IAM Credentials used to sign the GetCallerIdentity API.

Reach out to [me](https://twitter.com/herr_villa), if you want to enrich the list of most common scenarios where you can find yourself in.

Stay tuned for new publications!
