---
title: "Toward IAM Collaboration: Introducing Workspaces"
author: "Nicolò Marchesi"
date: 2023-07-26
tags: []
description: "How collaboration is key to effectively handle, access, and safeguard every cloud environment."
cover: images/7b6c97d2-4641-4a67-873f-c9d89a99b2c8.png
original_url: https://blog.leapp.cloud/introducing-workspaces
---

# Toward IAM Collaboration: Introducing Workspaces

Hey everyone, Nicolò here. I’m excited to announce that Noovolari Leapp is finally taking its final steps toward our long-waited access collaboration platform, and today we are introducing the first building block of our solution: **Workspaces**.

You may have seen it in our desktop application, so *“What is this?”* should have already popped into your mind; if not, you’ll learn about this today… surprise! 😄

Workspaces are, as the name implies, logically separated environments where all Leapp access and configurations live. It contains all the relevant information about your Sessions, your Leapp setup, and your Plugins, so in simple terms, everything that is needed for Leapp to work correctly.

Workspaces are, at their essence, the places where all your configurations are stored and can be both **local** and **remote.**

### The default local workspace

Leapp client is, first and foremost, an open-source project designed to work with secured local data and automate temporary credentials generation. All data needed to generate credentials are stored locally in the Keychain or encrypted configuration files so no one other than the user can access them.

Other than that, we have a plethora of different configurations, such as your preferred terminal or web browser, installed and active plugins, profiles, and a bunch of other things needed for Leapp to work.

It started as a tool for single developers and worked locally, giving us a lot of early feedback until our users began to ask for ways to collaborate and work with their teams, which wasn’t enough.

### The zero-trust remote workspace

Working only locally isn't impossible once you start to tread the path of collaborating on access. All Leapp data that wasn’t tied to the single user needed a place to live since a critical Cloud aspect as access requires reliability and robustness.

So we just created a place for everything to be saved online. Easy peasy lemon squeezy, right? But of course not!

From the start, we had the problem of not being happy with doing server-side encryption. It’s ok, but we weren’t satisfied because we wanted something that even the most critical of us would not have a problem using.

Since we’re **dev-and-privacy-obsessed,** we thought, *“What would make our users feel safe storing sensitive data online?”*. And the best answer we came up with, together with our users, was to ensure that **we can never-ever-ever access your data, even if you ask us to**. Everything saved in our server is client-side encrypted; only the user possesses the key to decrypt it.

This enables us to manage your access data while never knowing anything about them, and that’s the reason it’s called **zero-knowledge encryption**. We don’t know, and can’t know, anything about the encryption key, but you can be at peace storing everything you need to collaborate online.

## The Importance of Leapp Collaboration

With persistence sorted out, we are now focusing on the collaborative aspects of Cloud access management. When wielded by an individual, **Leapp is a powerful tool**, but when groups of people collaborate using Leapp, they can achieve real, transformational benefits. We have always known collaboration is essential for managing, accessing, and securing each Cloud environment.

We’re working closely with Leapp's open-source user community, learning from our users working with Leapp in organizations large and small, and it’s common to find a big gap between the builder’s need for focusing on actual work and the controls needed by security and compliance team managing a cloud environment.

We love IAM, but it’s not quite in the spot to be developer-centric. Powerful and of critical importance, but with many rough edges, and as a central pillar of the Cloud, it’s everywhere. Way too many teams struggle to get their access right with reasonable effort when they need to manage their Cloud Operations at scale. And that’s where we’re looking for the months to come, make Identity and Access management simpler and automated:

* **Identity-centric Cloud Access**: Seamlessly integrate identities from AWS IAM Identity Center, Okta, Azure AD, Google Workspace, and more.
    
* **IAM Automation**: Streamline access management operation tasks and enhance control and visibility over permissions and policies following your organization's workflow and tools.
    
* **Dynamic Roles and Policies**: Leverage Leapp's capability to template policies and roles, enabling the effective deployment of different versions based on the environment and context.
    
* **Just-in-time Access**: Simplify temporary access management by automating cloud access definition and expiration.
    
* **Automated Least Privilege**: Ensure fine-grained permissions and minimize access privileges through Leapp's automation capabilities.
    
* **Zero-trust IAM**: Implement a zero-trust approach to identity and access management, enhancing security and reducing risks.
    

## Come to the dark side of IAM; we have cookies (the good ones)

All puns are intended.

This overview has provided some insights into the solution we are developing and the principles behind our choices. The underlying principle on which everything was built is the firm belief that the sole practical method for a Cloud organization to achieve and maintain security is by embracing a developer-led approach.

As we envision the future of this project, we are excited about the possibilities that lie ahead. Our team constantly strives to add new features and improve the user experience based on valuable user feedback. Their input is vital to us, as it helps shape the future of our software.

If you are intrigued by our work and want to join our **Closed Beta**, please [fill out this form](https://docs.google.com/forms/d/e/1FAIpQLSeznt30p3By3isRNcdUrdjjAaCF87q8HP6c1cwAfMcnmqlCNA/viewform?usp=sf_link) or reach out to me on our [Slack community](https://join.slack.com/t/noovolari/shared_invite/zt-opn8q98k-HDZfpJ2_2U3RdTnN~u_B~Q). We value the opportunity to collaborate with individuals who share our passion for Identity Access management and security.

Furthermore, we are commencing our **Early Adopter Program**, specifically designed for organizations that desire a more intimate feedback process and the opportunity to influence the software's development actively. This exclusive program comes with distinct advantages and privileges not accessible to other users, and it customizes our solution to cater to your organization's specific use cases. For this, [let’s have a chat](https://calendly.com/noovolari/meet-nicolo) or find me on [Linkedin](https://www.linkedin.com/in/nicolomarchesi/)!

So, I hope you like what you’re reading, and if you don't want to miss out on this exciting opportunity – reach out to us today! Together we will advance IAM by Leap(p)s and bounds.

![](images/f80517b7-d9b3-471f-bea7-52b967bbe212.png)
