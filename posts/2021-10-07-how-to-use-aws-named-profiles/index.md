---
title: "How to use AWS named profiles"
author: "Andrea Cavagna"
date: 2021-10-07
tags: ["aws"]
description: "Let's debunk the best use-cases for AWS named-profile"
cover: images/1022a16f-9b72-406d-9468-34305e6a4d8f.png
original_url: https://blog.leapp.cloud/how-to-use-aws-named-profiles
---

# How to use AWS named profiles

It doesn't matter what kind of service you're creating. If you're building it on Amazon Web Services, there's one thing you can't run away from: IAM.

AWS IAM (*Identity & Access Management*) is the gatekeeper of your AWS accounts. It says who can access your account and what this person/service can and cannot do.

With programmatic access, you can set a particular set of credentials in the ~/.aws/ files to access your resources from CLI and SDKs. A profile wraps a set of credentials locally, so users can invoke different AWS account by pointing to other profiles.

A *named profile* is a collection of settings and credentials to apply to an AWS CLI command. When you specify a profile to run a command, the settings and credentials run that command.

There are many reasons why you might have multiple sets of AWS credentials at the same time, and I'll try to demystify some of them, but in general:

> To me, the correct way to use this feature is to have multiple profiles for some specific use-cases active simultaneously and then other sets of credentials [stored in a more secure place](https://docs.leapp.cloud/contributing/system_vault/), like the System Vault.
> 


![Named_Profile.jpg](images/_WEGpd0Pb.jpeg)

Whenever a credential set is not needed, the associated profile **must be removed from the credentials file.**

It's essential to have all these profiles [constantly rotated](https://docs.leapp.cloud/concepts/) and available only when needed for security reasons.

That's all nice and good, but what are the best use-cases for using multiple AWS profiles?
## CodeCommit helper in a different account

With [the evolution of the AWS environment](https://medium.com/leapp-cloud/how-to-access-your-aws-accounts-73d090f8e99) at the AWS Organization level, I've seen an increasing number of AWS Account dedicated to protecting the actual value behind a company, the **code itself**.

It's becoming common to set up at least two accounts: one for storing code, isolated, and one for deploying the actual solution.

To commit to an AWS CodeCommit repository, a developer needs to set up a helper in the `.gitconfig` file; So an excellent way to manage this thing is to create a profile (Eg: CodeCommitProfile) for this purpose only, and add the following lines to the file:

```bash
[credential]
helper = !aws --profile CodeCommitProfile codecommit credential-helper $@
UseHttpPath = true
```

Now developers push code changes in an account and deploy that code in another one without switching the right set of credentials.

**Everything is secured and constantly rotated.**

## Use default profile as a Canary.

As described by Eric Hammond: one or more of the profiles (perhaps the default) can be a honeypot, so you get notified if somebody tries to use the credentials.

[https://twitter.com/esh/status/1294500886685704192](https://twitter.com/esh/status/1294500886685704192)
By doing so with a tool like [CanaryTokens,](https://canarytokens.org/generate) you can get notified if someone is trying to steal your set of credentials.

The typical use-case for managing local credentials is to use default profile only, so this is the information an attacker tries to steal firstly.

The canary token is triggered when someone uses this **fake** credential pair to access AWS programmatically: being the generated key unique, If this token fires, it is a clear indication that this set of keys has "leaked."

But what can we use it for in concrete?

- Monitor your DevOps and Sysadmins: If someone tries to access AWS with their credentials pair, the chances of a compromised account.
- Check if someone is accessing an important private repository without permission: place these fake credentials there as a honeypot.

The canary Token approach can protect from external attackers, but it can also be tedious to set up and use for DevOps that work mainly with CLI projects. It depends on what you want to achieve!

## direnv
[https://github.com/direnv/direnv](https://github.com/direnv/direnv)
[direnv](https://github.com/direnv/direnv) is an extension available for many different shells and compatible with all the primary OS. It allows to automatically load and unload environment variables from a **.envrc** file depending on the current directory.

Direnv can exploit AWS Named Profiles. We can easily set up the **.envrc** to support the [AWS credential chain.](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html) add the following line:

```json
 export AWS_PROFILE=<a_profile_name>
 
```

This line of code allows using standard CLI or SDK command without specifying the profile option (remember to run direnv let if requested).

Using NamedProfile with direnv ensure always using the correct set of credentials, despite remembering the *—profile* option, for a specific project with the added benefit of avoiding unwanted actions (for example, deploying an app or uploading a sensible file in wrong AWS accounts).

Protecting yourself from unwanted actions becomes crucial when working for **MSP companies**: when dealing with many clients' accounts, **it is essential to segregate your work accurately**; imagine pushing code or deploying a solution from a client to another client's account!

## Why can Leapp help in these scenarios?
[https://github.com/Noovolari/leapp](https://github.com/Noovolari/leapp)
[Leapp](https://www.leapp.cloud/) allows us to store all the available AWS sessions needed centrally and generates credentials only when required.

It allows specifying different Named Profile to identify each AWS session, following the principle that you need to **activate and use** a session only when necessary and remove it once required.

The credential file will be filled only with short-lived credentials, and as said, all the **sensitive information will be stored in a secure vault accessible only by Leapp**.

So how can you leverage our tool in all the proposed use cases? Here are some examples!

### **When using CodeCommitHelper**

No helper modification is needed! Just add a Session with a specific `codecommitHelper` name profile and turn it on when you need to work with Git.

### **Are you using a default profile or a specific profile as a canary?**

Switch the Leapp session you want from the app list, and you can switch between monitoring a canary honeypot or debugging your favorite app!

### **direnv and Leapp to manage different accounts at once**

~~S~~pecify a name profile for other accounts and switch between them from Leapp allowing to test or deploy the same codebase in every environment with almost no configuration.

To sum up, we have seen different use cases to leverage the potential of AWS Named Profiles in a good way and how they can simplify a DevOps working routine. If you have any questions, by any means, feel free to [contact me](https://twitter.com/a_cava94) or [join our slack community](https://join.slack.com/t/noovolari/shared_invite/zt-opn8q98k-HDZfpJ2_2U3RdTnN~u_B~Q).

Until next time, see you all 🙂.
