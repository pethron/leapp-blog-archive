---
title: "IAM Users vs Roles"
author: "Eric Villa"
date: 2023-08-17
tags: ["iam"]
description: "In this blog post, we will cover IAM User and IAM Role concepts, focusing on best practices and access patterns.If you are already familiar with IAM User…"
cover: images/330396f1-8235-4960-a036-03a7be54dd32.png
original_url: https://blog.leapp.cloud/iam-users-vs-roles
---

# IAM Users vs Roles

In this blog post, we will cover IAM User and IAM Role concepts, focusing on best practices and access patterns.  
If you are already familiar with IAM User and Role concepts and just want to know what you should opt for based on your use case, feel free to skip to the last section: "*When should I go for IAM Users and when for IAM Roles?*".

## What is an IAM User?

When you create your first AWS account, you sign in with an identity that has full access to all the services and resources in your account. That identity is called the AWS account root user. As soon as you log into the AWS Console with the AWS account root user, you’ve to find a safer pattern to access it. Why? Because credentials associated with the AWS account root user are not disposable; in case of credentials theft, there is no way to invalidate them. That said, you can implement a safer access pattern by creating an IAM Identity called IAM User.

> An AWS Identity and Access Management (IAM) user is an entity that you create in AWS. The IAM user represents the human user or workload who uses the IAM user to interact with AWS. A user in AWS consists of a name and credentials.

A brand-new IAM User has, by default, no permissions. To allow an IAM User to access services and resources in the AWS account in which it was created, you’ve to assign an IAM Policy and one or more credentials to it.

As explained in [this](https://blog.leapp.cloud/increase-aws-security-posture-with-iam-roles-and-policies) article by my fellow colleague Alessandro Gaggia, an IAM Policy is a document that allows you to specify what an IAM Identity (in this case, an IAM User) can do on which resources or services, under what conditions. An IAM Policy is not enough to enable the IAM User permission to access resources or services; credentials must be associated with it.

Based on the way you want to access AWS, you have to use different kinds of credentials.

If you want to enable the IAM User to access the AWS Console, you’ve to assign a console password to the IAM User. The IAM User console password cannot be used to access AWS resources or services from the CLI or SDK.

Access to services or resources from the CLI or SDK is called programmatic access. To grant the IAM User programmatic access, you’ve to set up Access Keys; Access Keys that are created and assigned to an IAM User are long-term credentials. It means they’ve no expiration; you can use them to access your AWS account until they’re disabled or deleted. A common best practice to avoid long-term credentials is to rotate IAM User’s Access Keys periodically by deleting the old ones and replacing them with new ones created from scratch. In addition, IAM User Access Keys can be used to generate temporary credentials through the AWS Security Token Service GetSessionToken API.

Another important common best practice consists in requiring multi-factor authentication for all IAM users in your account. With MFA, users must provide two forms of identification: a console password or Access Keys, and a temporary numeric code that's generated on a hardware device or by an application on a smartphone, like Google Authenticator.

IAM Users are an effective instrument if you want to enable a human or application to access resources and services in a specific account, i.e. the one in which the IAM Users lives. But, there are many use cases that go beyond the possibilities of an IAM User. In particular, an IAM User does not fit a scenario in which we need to grant temporary permissions to trusted entities without sharing long-term credentials. Those trusted entities could be outside the boundary of my account (supposed that I have a single one), outside the boundary of AWS, or outside the boundary of my company.

At this point, you may wonder what kind of technology you can exploit to overcome these limits.

When it comes to granting temporary permissions to trusted entities without sharing long-term credentials, the IAM Identity that comes to the rescue is called IAM Role.

## IAM Role

An IAM Role is an Identity that you create in your AWS Account. Like an IAM User, an IAM Role has permissions defined in one or more IAM Access Policies associated with it. But, instead of being associated with one person or application, a Role is designed to be assumed by trusted entities. Assuming an IAM Role means generating temporary credentials associated with that IAM Role. These credentials allow us to perform operations against resources or services based on the permissions defined in the IAM Access Policy associated with the IAM Role.

You can define which trusted entities are allowed to assume the role and acquire temporary security credentials using a Trust Policy for an IAM Role. In addition, the trust policy of a role defines the conditions under which the role can be assumed. The trust policy is written in JSON format and is attached to the role.

Here's an example of what a trust policy for an IAM role might look like:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Replace `YOUR_ACCOUNT_ID` with your actual AWS account ID. In this trust policy, the `Principal` is set to the root user of the same AWS account (`arn:aws:iam::YOUR_ACCOUNT_ID:root`). This means that any entity within the account can assume the role.

Please note that while this example demonstrates granting access to any entity within the account, it's important to follow the principle of least privilege. Granting such broad permissions should be done with caution, as it might lead to unintended access and security risks. It's generally recommended to define more specific trust policies that only allow trusted entities that actually need the permissions provided by the role to assume it. It's important to craft trust policies carefully; trust policies, along with the permissions policies attached to the role, play a crucial role in controlling access to AWS resources in a secure and controlled manner.

Let’s deepen some access scenarios in which I can use IAM Roles to grant temporary permissions to trusted entities.

### **Federated Access from External Identity Provider (IdP)**

In some organizations, user identities are managed outside of AWS using an Identity Provider (IdP). To provide users with access to AWS resources, you can enable federated access. This allows users authenticated by the external IdP to access your AWS environment without needing to create IAM Users. Instead, they're granted temporary access using security tokens based on their IdP authentication. This enhances security and reduces the need for separate user accounts in AWS. There are different kinds of federated access protocol, based on the IdP you’re using.

**SAML Federated Access**

SAML (Security Assertion Markup Language) is a widely used protocol for SSO. When a user from your organization tries to access AWS resources, they authenticate with your external SAML-compatible IdP (such as Microsoft Active Directory Federation Services or Okta). After successful authentication, the IdP generates a SAML assertion, which is a digitally signed document containing the user's identity and attributes.

The SAML assertion is passed to AWS through the `AssumeRoleWithSAML` API call. This API call includes the Amazon Resource Name (ARN) of the IAM role the user wants to assume, along with the SAML assertion. AWS verifies the SAML assertion's signature and attributes with the trusted IdP metadata.

If everything checks out, AWS issues temporary security credentials associated with the IAM role specified in the request. These credentials enable the user to access AWS services and resources according to the permissions defined in the IAM role's policies.

**OpenID Connect Federated Access**

OpenID Connect (OIDC) is a modern protocol built on top of OAuth 2.0 that allows applications to authenticate users. When users want to access AWS resources, they authenticate with their OpenID Connect-compatible IdP. The IdP returns an ID token, which contains the user's identity and other relevant information.

To enable federated access in AWS, you create an IAM identity provider that points to your OIDC IdP. Then, you create an IAM role with a trust policy that allows the OIDC identity provider to assume the role. Users initiate federated access by signing in through the IdP, and the OIDC token is exchanged for temporary AWS credentials through the `AssumeRoleWithWebIdentity` API call.

**Web Identity Federated Access**

Web identity providers include well-known platforms like Amazon, Facebook, Google, and more. These providers offer their own authentication mechanisms for user sign-ins. When a user authenticates with one of these providers, they receive an identity token.

Similar to OIDC, you establish an IAM identity provider for the web identity provider. You create an IAM role with a trust policy allowing the web identity provider to assume the role. Users authenticated by the web identity provider can assume the role using the `AssumeRoleWithWebIdentity` API call, receiving temporary AWS credentials to access resources based on the role's permissions.

### **Cross-Account Access**

Traditionally, managing access to resources across different AWS accounts could be complex and potentially compromise security by sharing long-term credentials. However, AWS cross-account access with IAM roles simplifies this process while enhancing security and control. It empowers organizations to collaborate seamlessly, allowing users from one AWS account to access resources in another account with well-defined permissions.

This capability is particularly valuable for scenarios such as:

* **Organizational Collaboration**: different departments, teams, or external partners can work together effectively by granting controlled access to specific resources.
    
* **Managed Services**: organizations can centralize operations by providing external services, like managed security or analytics, and secure access to resources.
    
* **Consulting and Vendor Engagement**: consulting companies or vendors can access client resources while adhering to stringent security practices.
    

The core concept behind AWS cross-account access is the utilization of IAM roles. Instead of sharing credentials, a trusted relationship is established between accounts. The trusting account defines an IAM role with a Trust Policy that allows IAM Identities in the trusted account to assume that role.

Let's say Account A (123456789012) wants to allow users from Account B (987654321001) to access specific resources. Account A creates an IAM role named `CrossAccountRoleA` and attaches a Trust Policy that specifies that Account B is allowed to assume this role.

Trust Policy for `CrossAccountRoleA` in Account A:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::987654321001:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}
```

In Account B (987654321001), IAM users or roles can assume the `CrossAccountRoleA` role from Account A (123456789012) because Account A has defined a trust policy allowing it. Users in Account B can use the `AssumeRole` API call to acquire temporary credentials for the `CrossAccountRoleA` role.

Assuming `CrossAccountRoleA` in Account B using AWS CLI:

```json
aws sts assume-role --role-arn arn:aws:iam::123456789012:role/CrossAccountRoleA --role-session-name MySession
```

This will return temporary security credentials that can be used to access resources in Account A.

### **AWS Service-to-Service Access**

AWS services often need to interact with each other for various purposes. For example, you might want an AWS Lambda function to access data stored in Amazon S3. Instead of relying on long-term credentials, you can create an IAM role with the required permissions and allow the Lambda function to assume that role. This enables the Lambda function to securely access the necessary resources without exposing sensitive credentials.

Here's a concise breakdown of how AWS Service-to-Service Access works:

1. **Role Creation**: create an IAM role with necessary permissions for an AWS service to perform specific actions on other AWS resources.
    
2. **Trust Policy**: specify the AWS service's ARN in the role's trust policy, allowing it to assume the role.
    
3. **Role Assumption**: the AWS service requests temporary credentials from AWS STS by assuming the role.
    
4. **Temporary Credentials**: AWS STS provides temporary credentials, including the Access Key ID, the Secret Access Key, and the Session Token.
    
5. **Resource Access**: the AWS service uses temporary credentials to interact securely with other AWS resources.
    

### **EC2 Instance Access without Long-Term Credentials**

On 12 June 2014, Mike Pope announced a new, crucial AWS feature: [Granting Permission to Launch EC2 Instances with IAM Roles](https://aws.amazon.com/blogs/security/granting-permission-to-launch-ec2-instances-with-iam-roles-passrole-permission/)**.**

If you deploy a workload on an EC2 instance that requires access to AWS services, instead of embedding IAM User’s long-term credentials (Access Keys) directly into the instance, which can pose security risks, you can assign an IAM role to it. This role grants temporary permissions to the EC2 instance, ensuring that the workload running on this instance can interact with AWS services securely without exposing credentials. This dynamic and controlled approach simplifies management and enhances security.

When creating the IAM Role that has to be attached to the EC2 instance, remember to add a Trust Policy that allows the trusted entity (in this case, the EC2 service) to assume the role. In particular, you’ve to add `"Service": "`[`ec2.amazonaws.com`](http://ec2.amazonaws.com)`"` as the Principal in the Trust Policy.

The IAM Role can be attached to the instance during its creation or when it is already running.

When you assign an IAM role to an EC2 instance, an instance profile is automatically created. This instance profile is associated with the IAM role and acts as a container for temporary security credentials. The instance profile is managed by AWS and is not directly accessible from outside the instance.

When an application or process running on the EC2 instance needs to access AWS services, it makes an HTTP request to the metadata service, which is a web service that provides information about the instance's configuration and attributes. In this case, the [`http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>`](http://169.254.169.254/latest/meta-data/iam/security-credentials/%3Crole-name%3E) endpoint is invoked to retrieve temporary security credentials associated with the IAM role. These credentials include an Access Key ID, a Secret Access Key, a Session Token, and an Expiration Time. EC2 instances automatically renew the temporary credentials by periodically requesting updated credentials from the metadata service. This ensures uninterrupted access to AWS resources.

## Interaction between IAM Users and IAM Roles

As far as now, we didn’t take into account any possible interaction between IAM Users and IAM Roles. Well, IAM users can interact with IAM roles through the process of assuming roles. This allows IAM users to temporarily take on the permissions and privileges associated with an IAM role, granting them access to resources they might not have direct permissions. This interaction is commonly used to delegate access to specific resources without sharing long-term credentials.

An IAM User initiates the process by calling the `AssumeRole` API, specifying the ARN (Amazon Resource Name) of the IAM Role they want to assume. The IAM User must have the necessary permissions to assume the role in the first place. These permissions are defined by an IAM Access Policy attached to the user. The IAM Role’s Trust Policy must contain a statement that allows the IAM User to assume it. If the trust policy allows the IAM User to assume the role, AWS STS (Security Token Service) generates temporary credentials for the IAM User. The IAM User can use the temporary credentials to make requests to AWS services just like they would with their own IAM User credentials. The IAM User only has the permissions associated with the assumed role, not their original IAM User permissions.

As previously mentioned, it is possible to enable MFA for an IAM User. In the user's Access Policy, you can define actions that require MFA protection. This means that these actions can only be performed using IAM User credentials that include MFA information.

To generate credentials that include MFA information, you must call the STS GetSessionToken API and provide a valid MFA token associated with a hardware or virtual MFA device. You can then use the resulting credentials to call MFA-protected actions.

## **When should I go for IAM Users and when for IAM Roles?**

### **IAM Users**

IAM Users are well-suited for managing access within your AWS account, particularly for individuals and applications that require straightforward access to AWS services and resources. They offer personalized access control and are appropriate for the following scenarios:

* **Individuals**: If you have human users who need to interact with AWS services using the AWS Management Console, IAM Users provide a way to grant personalized access. You can assign permissions based on each user's roles and responsibilities.
    
* **Simple Application Access**: For applications running within your AWS account that require programmatic access to AWS services, IAM Users can be used. However, it's important to note that IAM Roles are often a better choice for applications, as they provide temporary access without exposing long-term credentials.
    

While IAM Users are useful for straightforward access requirements, they might not be the optimal solution for scenarios involving temporary access, cross-account access, or enhanced security.

### **IAM Roles**

IAM Roles offer a more comprehensive approach to access management, particularly when dealing with complex access patterns and security considerations. They are the recommended choice in the following situations:

* **Federated Access**: When you need to grant temporary access to users from external identity providers (IdPs) such as SAML, OpenID Connect, or web identity providers, IAM Roles provide a secure way to authenticate and access AWS resources without exposing long-term credentials.
    
* **Cross-Account Access**: IAM Roles excel at enabling secure collaboration between AWS accounts. This is crucial for scenarios like organizational partnerships, managed services, and consulting engagements.
    
* **Service-to-Service Access**: IAM Roles facilitate secure interactions between AWS services without relying on long-term credentials. This enhances security and adheres to the principle of least privilege.
    

IAM Roles streamline security, minimize long-term credential exposure, and provide controlled access. They're designed to address a wide range of security and access requirements.

In summary, while IAM Users are suitable for simpler access scenarios within an AWS account, IAM Roles offer a more advanced and secure approach for managing complex access patterns, temporary access needs, and cross-account collaboration. The choice between IAM Users and IAM Roles should align with the specific security requirements and complexity of the access scenario you're addressing.

# That’s all Folks!

In this blog post we have seen what are IAM Users and IAM Roles, what are the differences between them, and the use cases in which they’re used.

I hope you enjoyed this blog post and that you find it informative. Please, don’t hesitate to provide your feedback and share your thoughts about the topic. Feel free to reach out to us on our [Community Slack](https://join.slack.com/t/noovolari/shared_invite/zt-opn8q98k-HDZfpJ2_2U3RdTnN~u_B~Q)!

Stay tuned for new publications!
