---
title: "Enhanced Serverless GitHub Metrics"
author: "Nicolò Marchesi"
date: 2021-03-11
tags: ["serverless"]
description: "Measure what matters with Lambda, TypeScript, and Terraform"
cover: images/dd477e73-a9d7-4ebc-be83-698c64d9361b.png
original_url: https://blog.leapp.cloud/enhanced-serverless-github-metrics
---

# Enhanced Serverless GitHub Metrics

Since we started [Leapp](https://github.com/Noovolari/leapp) a few months ago, we wanted to steadily improve our open-source project to engage better all people interested in working fast and safely in the cloud.

But to improve on something, you need to be aware of what you want to improve. So the first thing we noticed was the Insight page inside our GitHub repository. You can find a ton of useful information there, but it's limited to 1 month of data, so my thought was: let's fix that!

## Meanwhile...

What better chance to learn something new? Since the project was simple enough, I decided to take a little extra time to study and research new technologies that could come in handy for future projects. I like to learn new things consistently to keep up with our ever-changing world... and while having fun too!

I wanted to share the whole process and my takeout at the end, so if you're searching for inspiration, I hope you're in the right place!

# Requisites

So, before writing even a few code lines, I want to have a clear overview of how I would build my project. Here's my thought process.

## Choosing the framework and language

My drive here is to do some research to evaluate technologies for other projects to use in production. Since this is an easy goal, it's perfect to avoid incurring major technical issues while having the opportunity to dive deep enough to discover any significant flaws I can encounter in the future.

For a few months, I wanted to try out **TypeScript** and check if the Twitter hype was right for once, while for infrastructure as code (IaC), I never had the chance to research **Terraform**. In the end, this was an excellent use-case to finally do some serious research and development with a clear goal.

As for deployment and data persistence, I want to use something that I'm confident in; since I'm already adding uncertainty with a new programming language and deployment frameworks, it's better to stop here with the novelty and avoid delays.

## Choosing the data-persistence layer

For this, I need something inexpensive and with good filtering capabilities since I'm going to query for dates. Moreover, I don't want to pay for idle, so the choice is between DynamoDB and Aurora Serverless. Since I don't forecast to access this data a lot, I think DynamoDB is a better fit. For the filtering part, I learned the hard way that it's always better to devise your queries first; I took some time to forecast what kind of questions I would run to retrieve my data, and i's something like:

- How many GitHub stars did we have on that date?
- How many Contributors did we have on that date?
- Plot all Stargazers that were present between those dates

It's pretty clear that I wanted all data divided by date, so I designed the table to have the date set as my primary key. Unfortunately, the date range query was applicable only in two scenarios: secondary indexes or scans. But the data I'm expecting to store and search for is tiny, so I can safely ignore the mantra "**never use scans"** and use the date as my primary key.

## Other considerations

Since I want complete automation and daily granularity, the best thing to do is fire off my Lambda on a daily cron job. To maintain the serverless spirit, CloudWatch Alarms is a perfect fit for that.

## Final choice

So, with the final choice, I went with:

- Platform: **AWS Lambda**
- Language: **TypeScript**
- Infrastructure as Code: **Terraform**
- Data Persistence: **DynamoDB**
- Events: **CloudWatch Alarm**

# Developing

Once settled with the whole technology stack, it was time to do some testing and development.

## Extracting data

The first thing I did was use the GitHub SDK with Octokit to query for data and start defining the data structure. I will later save this to DynamoDB.

This thing would be as fast as lightning to implement, but I made an encounter with the most dreaded thing of the whole JavaScript engine... the Promise! Octokit only provides a client that could be interacted only with asynchronous interfaces.

[Thanks to MDN for the clear explanation.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

After that, it was pretty easy. Put await in front of each promise to make them synchronous and extract a bunch of data to store in an Object:

```tsx
async scrape(): Metrics {
        const s = await this.get_social()
        const cic = await this.get_issues_count(IssueState.Closed)
        const opc = await this.get_pulls_count(IssueState.Open)
        const cpc = await this.get_pulls_count(IssueState.Closed)
        const r = await this.get_releases()

        const g: Globals = {
            closed_issues_count: cic,
            closed_pulls_count: cpc,
            forks_count: s.forks_count,
            open_issues_count: s.open_issues_count,
            open_pulls_count: opc,
            stargazers_count: s.stargazers_count,
            subscribers_count: s.subscribers_count,
            total_issues_count: cic + s.open_issues_count,
            total_pulls_count: cpc + opc,
            watchers_count: s.watchers_count
        }

        const m: Metrics = {
            globals: g,
            releases: r
        }

        return m
    }
```

As you can see, I divided the metrics into **globals** and **releases.** The first contains all data tied to the repository (Stars, Contributors, Traffic, etc.), while the latter will store all releases versions and the number of times each file has been downloaded.

## Writing data

The writing part was the most tricky... guess why? Again the Promise!

Since I already created the Lambda handler, it took me few attempts to return the Promise to be resolved.

```tsx
import { DynamoDB } from 'aws-sdk';
import { Metrics } from "./scrape/dto";

export async function write(table: string, metrics: Metrics): Promise<any> {
    const today = new Date()
    const calendar = { date: today.toISOString().substring(0,10) }

    const item = { ...calendar, ...metrics.globals }
    const dynamo = new DynamoDB.DocumentClient({apiVersion: '2012-08-10', region: 'eu-west-1'});
    return dynamo.put({
        TableName: table,
        Item: item
    }).promise();
}
```

## The lambda handler

And here, for the sake of completeness, the handler:

```tsx
import {Scraper} from "./scrape/scrape";
import {write} from "./writer";

export const handler = async (event: any = {}): Promise<any> => {
    const scraper = new Scraper(process.env.OWNER, process.env.REPO, process.env.AUTH);
    const metrics = await scraper.scrape();
    return write(process.env.TABLE, metrics);
}
```

Since the handler is a Promise, and the Lambda runtime environment has a wrapper that resolves it, you don't need to wait for the write function to complete before returning it. I'm returning the Promise directly from the DynamoDB put operation.

I know it's pretty dry, but I like to have *slim handlers to focus on the business logic* without worrying about how they will run in the Lambda environment.

# Building the infrastructure

After making everything work on the development side, I went to build and create the infrastructure. I set up everything in a folder named [terraform](https://github.com/pethron/serverless-github-metrics/tree/master/terraform) to generate a file for each infrastructure element. Something like:

- Terraform
    - cloudwatch
    - dynamo
    - iam
    - lambda
    - Etc.

## The variables

Since I want to consistently work between the local and cloud environments and always prefer to generalize and reuse my code when possible, I always start by forecasting the variables I need to pass to the function. Since I'm using CloudWatch Alarms to fire off Lambda those variables will be later transformed into environment variables.

```tsx
variable "aws_region" {
  type    = string
  default = "eu-west-1"
}

variable "aws_profile" {
  type    = string
  default = "default"
}

variable "vertical" { }
variable "stack" { }
variable "project" { }

variable "owner" { }
variable "repo" {}
variable "auth" { }

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}]
```

I would need the *owner* and *repo* to configure the data source and the *auth* token to establish the connection. Since I'm using [Leapp](https://github.com/Noovolari/leapp) to manage access to the cloud account, I've configured the *aws_profile* to pick it up from default.

## The .env

As we have previously seen, I want to populate the variables for Terraform automatically. For this, I think the [dotenv project](https://github.com/motdotla/dotenv#readme) is helpful. Set up a .env file to store your variables and, if there isn't an integration or you're a purist (like me), you can source the file and run any command you want like this: "*source .env && terraform plan."* It will export all variables, and Terraform will pick them up and assign them to the elements defined in the *variables* file.

The only downside here was to export manually with TF_VAR prepended to each variable. But you know, it should take about 10 seconds to do that. I think I can live with it. **

```bash
VERTICAL={my-vertical}
STACK={my-stack}
PROJECT={my-project}
OWNER=noovolari
REPO=leapp
AUTH={my-github-token}
TABLE={eddie-metrics-global-table}
AWS_SDK_LOAD_CONFIG=true

export TF_VAR_vertical=$VERTICAL
export TF_VAR_stack=$STACK
export TF_VAR_project=$PROJECT
export TF_VAR_owner=$OWNER
export TF_VAR_repo=$REPO
export TF_VAR_auth=$AUTH
export TF_VAR_table=$TABLE
```

## The locals

Here I put the local variable I will consistently use on my whole stack to avoid repeating them and clog the configuration files.

The vertical, stack and project variables are a 3-tier set of constants used to group and identify projects by name. I have defined a composite variable named *full* to avoid composing the full project name in the *locals* file.

Moreover setting the *tags* like a dictionary let me use them directly as a variable and forget completely about them, but still have them consistent.

```bash
locals {
  lambda_memory = 128
  full        = "${var.vertical}-${var.stack}-${var.project}"

  tags = {
    Vertical    = var.vertical
    Stack       = var.stack
    Project     = var.project
    Name        = local.full
    ManagedBy   = "terraform"
  }
}
```

## The DynamoDB table

I'm cheating a bit because I had already set up the DynamoDB table with Terraform... but it's really tiny so let's just ignore that. As you can see, the *tags* variables it is really handy!

```tsx
resource "aws_dynamodb_table" "dynamodb_table" {
  name           = "${local.full}-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "date"

  attribute {
    name = "date"
    type = "S"
  }

  tags = local.tags
}
```

## The Lambda

Here I'll break down things a bit to better explain.

### Archive Files

The archive files are just zip files that contain the function and the node_modules folders. The main things to notice here are:

- While there is a convenient function in Terraform that does the packaging for you, I needed a more custom approach, and thus there are two commands in the *package.json* for building the Lambda and the layer. They copy and zip a folder.
- Never forget to add the *source_code_hash* and the sha256 fingerprint! It allows Terraform to put a fingerprint on the package and automatically create new versions of the layer only if something is changed.

```bash
data "archive_file" "function_archive" {
  type        = "zip"
  source_dir  = "${path.module}/../dist/lambda"
  output_path = "${path.module}/../dist/lambda/lambda.zip"
}

resource "aws_lambda_layer_version" "layer" {
  filename            = "${path.module}/../dist/layers/layers.zip"
  layer_name          = "${local.full}-layer"
  compatible_runtimes = ["nodejs12.x"]
  source_code_hash    = filebase64sha256("${path.module}/../dist/layers/layers.zip")
}
```

### The function

The function again is pretty primary. As you can see, I have referenced the data archives containing the Lambda and the lambda layer resource name. I added the environmental variables to let me configure the function from Terraform. If I need to deploy this to track another GitHub repository, I only need to change the variables in the *.env* file, and everything will run the same.

```bash
resource "aws_lambda_function" "lambda" {
  filename      = data.archive_file.function_archive.output_path
  function_name = "${local.full}-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"

  # Lambda Runtimes can be found here: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
  layers = [aws_lambda_layer_version.layer.arn]
  runtime     = "nodejs12.x"
  timeout     = "30"
  memory_size = local.lambda_memory

  environment {
    variables = {
      OWNER = var.owner
      REPO = var.repo
      AUTH = var.auth
      TABLE = aws_dynamodb_table.dynamodb_table.name
    }
  }
}
```

# R&D conclusions

Here are my conclusion of my R&D on TypeScript and Terraform

TypeScript is a potent language. I've always had some problems with JavaScript and its lack of types, and with TypeScript, it feels like a complete experience. I still need to wrap my head around the async/await paradigm and Promise class on the downsides. It's not that they don't work, but, in my opinion, it adds unnecessary overhead while programming. Since TypeScript was an extension of JavaScript, which was designed for asynchronous operations and frontend, I think it's normal to shine in these environments. For backend, synchronous operations, and scripting, I think there are better choices.

**Terraform was mind-blowing.** What I conservatively forecast to take at least a day to get up and running was done in about an hour. The tooling was great, the documentation was clear, many examples around the internet and on the git repository... what more could I have to ask for?

There were some minor inconsistencies with the state management, though; just once something went wrong and generating the plan threw an unrecoverable error (probably due to my inexperience). In the end, I resolved pretty quickly by tearing all down and re-creating it, so no-big-deal.

# And what about metrics?

After some research around the best metrics to track for open-source projects, I set everything up to save:

- Open/Closed issues and pull requests
- Forks, Stargazers, Watchers, and Subscribers
- Total issues and pull requests

The idea was to get an overall feeling if we are sparking interest in other people and contributing with code or just with issues and enhancements. Those metrics proved very useful and gave us some insight, but after few months of running and reviewing them, we feel that something is missing along the lines.

Nonetheless, I'm happy we started collecting those metrics and weekly review them.

It's the drive to do better and improve our community and project.
