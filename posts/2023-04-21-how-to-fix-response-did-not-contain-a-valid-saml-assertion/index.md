---
title: "How to fix response did not contain a valid saml assertion"
author: "Alessandro Gaggia"
date: 2023-04-21
tags: []
description: "How to investigate and fix one of the most common problem in managing IAM federated principals"
cover: images/7b984fa5-899c-4815-be51-da23fb8d78e6.png
original_url: https://blog.leapp.cloud/how-to-fix-response-did-not-contain-a-valid-saml-assertion
---

# How to fix response did not contain a valid saml assertion

If you read this article, you are managing user identities outside of AWS and using Identity Provider (IdP) Federation to give these external identities permission to use AWS resources in your account.

In this authentication process, one of the **most common errors** you may need to confront is "response did not contain a valid saml assertion," and in this article, I want to share with you some troubleshooting advice to solve it.

## **Investigating a No valid assertion found in SAML response**

### Checking the attribute name and attribute value on your IdP

If you are on AWS (but in general), invalid SAML assertion mainly occurs when the SAML response from the IdP does not include an attribute with the `Name` set to [`https://aws.amazon.com/SAML/Attributes/Role`](https://aws.amazon.com/SAML/Attributes/Role) . The attribute must also contain one or more `AttributeValue` elements, **each with these two strings**, separated by a comma:

* The ARN of a role that the user can be mapped to
    
* The ARN of the SAML provider
    

E.g.:

```markdown
<Attribute Name="<https://aws.amazon.com/SAML/Attributes/Role>">

<AttributeValue>arn:aws:iam::account-number:role/role-name1,arn:aws:iam::account-number:saml-provider/provider-name</AttributeValue>

</Attribute>
```

[Here](https://repost.aws/knowledge-center/iam-invalid-saml-response-okta) is also an example of a resolution for Okta.

### Time Synchronisation issues between IdP and Service Provider

[https://docs.pulsesecure.net/WebHelp/Content/PCS/PCS\_AdminGuide\_8.2/Investigating a No valid assertion.htm](https://docs.pulsesecure.net/WebHelp/Content/PCS/PCS_AdminGuide_8.2/Investigating%20a%20No%20valid%20assertion.htm)

**If the SAML IdP and SAML service provider (AWS, for example) clocks are not synchronized, the assertion can be determined invalid**, and authentication fails.

A possible solution is to verify that your IdP and Service provider **can share the same NTP server** or prove that your server's clock is up-to-date.

### Metadata.xml mismatch

**Data refreshes, and upgrades can cause the certificates to be no longer trusted by one side of the Federation process or the other**. Try to check and update the metadata.xml on both ends so the certificates will match again.

### **SAML message not properly formatted, with missing or invalid elements**

[https://stackoverflow.com/questions/64158310/aws-sso-your-request-included-an-invalid-saml-response](https://stackoverflow.com/questions/64158310/aws-sso-your-request-included-an-invalid-saml-response)

Sometimes the error occurs not only with the User attribute but in general if the message needs to include all the required information in the required format. For example:

* The message was signed, but **the signature could not be verified**.
    
* Assertion contains an unacceptable **Audience Restriction**.
    
* The assertion is no longer valid, or the message is expired, see **Time Synchronisation issues between IdP and Service Provider**.
    
* **SAML response contained an error** indicating that the Cloud Provider received a SAML message from an IdP with an error status code.
    

Remember that SAML is schema-compliant, so you must adhere to its standard when creating its XML request. Make sure to refer to this [document](http://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf) to see all the standard tags.

Some more examples of possible typos can be:

* Not including encoding at the beginning of the XML:
    

`<?xml version="1.0" encoding="UTF-8"?>`

* Typo in the Recipient of the **SubjectConfirmationData**: set it to "[https://signin.aws.amazon.com/saml](https://signin.aws.amazon.com/saml)."
    
* Not including an **AuthStatement**.
    

### **How to view a SAML response for troubleshooting**

[https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot\_saml.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_saml.html)

This article has several ideas to help you narrow down the exact cause of the issue. Still, I'd also like to give you some basic tips on debugging the SAML assertion you receive to find details that can point you to the root cause of your problem.

**Google Chrome and Firefox**

1. Press **F12** to start the **Developer Tools** console.
    
2. Select the **Network** tab, and then select **Preserve log** (Persist Log in Firefox)
    
3. Look for a **SAML Post**, then view the **Payload** tab at the top. Look for the **SAMLResponse** element that contains the Base64-encoded response.
    
4. Copy it.
    

<mark>💡 Security Note: as SAML assertions contain sensitive information, I discourage you from using&nbsp;</mark> *<mark>online base64 decoders</mark>* <mark>&nbsp;and using one of these simple scripts to do it from your local terminal.</mark>

**Windows systems (PowerShell):**

`PS C:\\>[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("base64encodedtext"))`

**MacOS and Linux systems:**

`$echo "base64encodedtext" | base64 --decode`

Also, if the attributes from your Identity Provider are **not encrypted**, the [Firefox browser SAML tracer Add-on](https://addons.mozilla.org/en-US/firefox/addon/saml-tracer) or [Chrome SAML Message Decoder](https://chrome.google.com/webstore/detail/saml-message-decoder/mpabchoaimgbdbbjjieoaeiibojelbhm?hl=en) can view these attributes.

### Tutorials

To help you further, here are two articles from our blog where we share some hints to configure SAML with GSuite (note that concepts and properties are similar to other IdPs).

* [https://blog.leapp.cloud/how-to-saml-federate-your-aws-account-with-g-suite](https://blog.leapp.cloud/how-to-saml-federate-your-aws-account-with-g-suite)
    
* [https://blog.leapp.cloud/how-to-update-in-bulk-g-suite-users-custom-attributes-with-google-admin-sdk](https://blog.leapp.cloud/how-to-update-in-bulk-g-suite-users-custom-attributes-with-google-admin-sdk)
    

## Conclusions

In this article, we have seen how to troubleshoot a very pesky error of the SAML Federation: "Response did not contain a valid SAML assertion."

We have shown that it can occur when:

* **Role attributes are not set correctly** in the SAML request - IdP side.
    
* There is a **time desynchronization** between the IdP and the Service Provider.
    
* There is a **Metadata.xml mismatch** between the actors, so the certificate doesn't match.
    
* There are **typos or an invalid SAML structure** in your request.
    

In general, I always return to [this](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_saml.html#troubleshoot_saml_invalid-response) link when I need to troubleshoot a SAML response, as the problem may lie on a different configuration depending on the IdP you're using.

This little article has been of help to all of you, and till next time, Happy SAML assertions, and see you in the next article! 😉
