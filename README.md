# Rate limiting - Queue-Based Load Leveling pattern on cloud

Implement a simple architecture using python SDK to understand the concept of [Rate limiting (Queue-Based Load Leveling pattern)](https://shubhangivashist.medium.com/queue-based-load-leveling-pattern-in-cloud-hosted-applications-039b2ad8f378) leveraging Azure cloud platform.  

## Architecture 

![diagram](architecture.jpg)

- GitHub for Version control.
- Azure Blob Storage to store our documents.
- Azure Queue Storage to implement rate limiting.
- Azure Table Storage to store URL for the uploaded documents and associated metadata. 
- [Python](https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview) for our Infrastructure as Code.

## You'll need

- [Azure account](azure.com/free)
- [GitHub account](github.com/join)
- Prerequisite: Create a resource group if you don't have an existing one. 

For local developer environment

- VS Code/ Jupyter notebook
- Docker (optional)

## How to get started

### Authenticate your Environment with Azure
In the Terminal, type `az login --use-device-code` to log into your Azure account from the az cli.

### Get the code and environment

1. [Fork the repository](https://docs.github.com/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) so you can have your own copy of it. 
2. If you don't already have Jupyter notebook installed, navigate to [python](https://jupyter.org/) and download the latest version. Follow the installation instructions for the setup.
3. Launch Jupyter notebook and open [main.py](main.py) and [defaults.py](defaults.py). 
4. Replace the parameters in [defaults.py](defaults.py) with your own subscription ID, principle ID and resource-group name. You can modify the other default parameters or leave them as it is(your choice).
5. Now execute main.py to build the sample architecture.

### How the codebase works
Refer my [blog](https://shubhangivashist.medium.com/queue-based-load-leveling-pattern-in-cloud-hosted-applications-039b2ad8f378) to understand the working of the codebase.
        
