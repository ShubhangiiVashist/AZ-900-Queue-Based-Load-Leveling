# Rate limiting - Queue-Based Load Leveling pattern in cloud

Implement a sample architecture to understand [Queue-Based Load Leveling pattern](https://shubhangivashist.medium.com/queue-based-load-leveling-pattern-in-cloud-hosted-applications-039b2ad8f378) leveraging Azure cloud platform. 

## Architecture 

![diagram](architecture.jpg)

- GitHub for Version control.
- Azure Blob Storage to store our documents.
- Azure Queue Storage to implement rate limiting.
- Azure Table Storage to store documents and associated metadata. 
- [Python](https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview) for our Infrastructure as Code.

## You'll need

- [Azure account](azure.com/free)
- [GitHub account](github.com/join)

For local developer environment

- VS Code
- Docker

## How to get started

### Get the code and environment

1. [Fork the repository](https://docs.github.com/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) so you can have your own copy of it. 
2. FOR CLOUDSPACES: Click on the `Code` button, click on `Codespaces` tab, and click on `Create Codespaces on main`. I've provided a [`devcontainer.json`](https://code.visualstudio.com/docs/devcontainers/create-dev-container) file with the configuration needed for this project.
3. Once your Codespace has loaded, in the Explorer, expand the `src` folder and rename `local.settings.sample.json` to `local.settings.json`
4. FOR LOCAL DEV: Clone the code, open it with VS Code and Launch in the dev container. More info [here](https://code.visualstudio.com/docs/devcontainers/containers)

### Authenticate your Environment with Azure
1. In the Terminal, type `az login --use-device-code` to log into your Azure account from the az cli in your Codespace.
2. In the Terminal, type `az account list --output table` to get a list of Azure subscriptions you have available to you and make note of the name you want to use. 
3. In the Terminal, type `az account set --name "name-of-subscription"` with the name of the subscription you want to use.
4. In the Terminal, type `az account show` and make sure it's set to the subscription you want to work in.

### Provision resources in Azure

> **NOTE:** I've set the resource group name to be `rg-serverlessresumeapi`

1. I've provided Infrastructure as Code (IaC) files, you can find them in the `infra` folder. Now we need to use those files to create a deployment in Azure, in the Terminal, type: 
    ```sh
    az deployment sub create --template-file ./infra/main.bicep -l <your-region>   
    ```
2. In the Terminal, run the following command to see the values for your storage account name and function:
    ```sh
    az deployment group show -g rg-serverlessresumeapi -n resources --query properties.outputs 
    ```
3. Now let's save that output into individual variables. Run the Azure CLI command and capture the output:
    ```sh
    output=$(az deployment group show -g rg-serverlessresumeapi -n resources --query properties.outputs)
    ```
4. Since the output has several values, we need to arse the output and store each value in a variable
    ```sh
    functionAppName=$(echo $output | jq -r '.functionAppName.value')
    functionUri=$(echo $output | jq -r '.functionUri.value')
    storageAccountName=$(echo $output | jq -r '.storageAccountName.value')
    ```
5. Now we can Echo (print to screen) the variables to verify
    ```sh
    echo "Function App Name: $functionAppName"
    echo "Function URI: $functionUri"
    echo "Storage Account Name: $storageAccountName"
    ```
6. Upload `myresume.json` to that newly created blob container. 
    ```sh
    az storage blob upload --account-name $storageAccountName --container-name resume --name myresume.json --file myresume.json 
    ```
7. In your `local.settings.json` add the Storage Account Connection String to the `AzureWebJobsStorage` value. You can get that value by running this command: 
    ```sh
    az storage account show-connection-string --name $storageAccountName --resource-group rg-serverlessresumeapi   
    ```
8. You can now run and debug (F5) your Function in your environment or run this command in the terminal: 
    ```sh
    cd src
    func start host
    ```

## Configure CI/CD with GitHub actions

1. In the .github folder, edit your `build.yml` and update the `AZURE_FUNCTIONAPP_NAME` value with the name of your function app.
2. We'll need to get our Function's Publish Profile, run the following command in the terminal and copy the output:
    ```sh
    az functionapp deployment list-publishing-profiles --name $functionAppName --resource-group rg-serverlessresumeapi --xml
    ```
3. In your GitHub repo, go to settings > secrets and variables > actions > create a secret named `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` with the contents of your publish profile you just copied.
4. Head to Actions tab on your Repo and manually run the workflow. 
5. Once it's complete. Your resume api is now in production. We can view it in 3 ways:
    - Using curl in the terminal: 
        ```sh
        curl $functionUri/getresume
        ```
    - Using the browser: open a new tab with your function URI and add `/api/getresume` at the end.
    - Use the thunderclient extension in VS Code with your function URI and add `/api/getresume` at the end.
        
