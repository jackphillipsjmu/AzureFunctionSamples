# Azure Function Samples
Repository contains different solutions that can be solved using Azure Functions.

## What is an Azure Function?
_"Azure Functions is a cloud service available on-demand that provides all the continually updated infrastructure and resources needed to run your applications. You focus on the pieces of code that matter most to you, and Functions handles the rest. Functions provides serverless compute for Azure. You can use Functions to build web APIs, respond to database changes, process IoT streams, manage message queues, and more._"

## Samples in this Repository
| Function | Description |
|----------|-------------|
| GrayscaleImages | Example HTTP Azure Function that will take in either a URL form encoded request payload containing `1..N` images or a single image using binary data. The function will transform the data into a gray scale image(s), and respond with an in-memory `zip` file that contains the results. These outputs could be stored to a local filesystem, ingested by another function or service and more! |

## Prerequisites
- Download [.NET Core](https://dotnet.microsoft.com/download) if you do not have it already and install it.
- Install [Azure Function Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash#v2) to your local machine.
- For testing out using cURL make sure you have a terminal capable of running `curl` commands. If you don't your could utilize something such as Postman or other ways to send HTTP requests.
