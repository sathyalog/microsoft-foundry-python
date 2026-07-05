# Azure AI Foundry - Agent Framework Comparison

This project demonstrates two different approaches to connecting and communicating with an AI Agent hosted in Azure AI Foundry using Python:
1. **Azure AI Projects SDK** (Original implementation)
2. **Microsoft Agent Framework (MAF)** (New, asynchronous, enterprise-ready orchestration framework)

---

## Project Structure

* `agent.py` - Core implementation using the legacy Azure AI Projects SDK.
* `agent_maf.py` - Modernized implementation using the Microsoft Agent Framework (MAF).
* `.env` - Local environment configuration file.

---

# Use a Microsoft Foundry Agent with Python

This guide explains how to create and configure an agent in **Microsoft Foundry**, connect your local machine to the same project, and use Python to retrieve that agent and send prompts to an LLM through your Foundry project. It is written for first-time users, so it includes the Azure portal setup, VS Code setup, Azure authentication, Python environment setup, and a full example based on the `azure-ai-projects` SDK.[web:12][page:1]

## What this guide covers

By following this README, you will learn how to:

- Create an Azure account and sign in to Microsoft Foundry.
- Create a Foundry project.
- Deploy a model in that project.
- Create an agent inside Foundry.
- Install Azure and Python tooling on your machine.
- Authenticate locally with Azure.
- Use Python to retrieve an existing Foundry agent.
- Use the project client to obtain an authenticated OpenAI client.
- Send a prompt to the model and print the response.[web:12][page:1]

## How this approach works

This README follows a pattern where the agent is created and managed in Microsoft Foundry first, and Python connects to that project later. Your Python code does not create the model deployment itself; instead, it connects to the Foundry project endpoint, checks whether the named agent exists, and then uses `get_openai_client()` to send a request to the deployed model through the same project.[page:1][web:13]

That means the portal handles project-level setup such as models, agents, and project resources, while Python acts as the client application that authenticates with Azure and communicates with the LLM.[page:1]

## Prerequisites

Before starting, make sure you have:

- An active Azure subscription.[page:1]
- Access to the [Microsoft Foundry portal](https://ai.azure.com/).[web:12]
- Python 3.9 or later installed.[page:1]
- Visual Studio Code installed.
- Azure CLI installed and available in your terminal.[page:1]
- Permission to access the Foundry project through Microsoft Entra ID, because the `azure-ai-projects` client currently supports Entra ID authentication rather than API-key-only access.[page:1]

## Step 1: Create an Azure account

If you do not already have an Azure account, create one first. After that, sign in with the same account you plan to use for Microsoft Foundry and local development.[web:12]

## Step 2: Open Microsoft Foundry

Go to [ai.azure.com](https://ai.azure.com/) and sign in. This is the main Microsoft Foundry portal where you create projects, deploy models, configure agents, and manage project resources.[web:12]

## Step 3: Create a Foundry project

Inside Microsoft Foundry:

1. Create a new project.
2. Choose the Azure subscription and resource settings required for the project.
3. Wait until the project is provisioned successfully.[web:12]

After the project is created, open its overview page and note the **project endpoint**. The Azure AI Projects SDK expects an endpoint in this format:

```text
https://your-ai-services-account-name.services.ai.azure.com/api/projects/your-project-name
```

This value is one of the most important details in the entire setup, because your Python code connects to the Foundry project by using this endpoint.[page:1]

## Step 4: Deploy a model

In your Foundry project, go to **Models + endpoints** and deploy a model that supports the type of interaction you want to perform. The Azure AI Projects SDK can work with deployed models in your Foundry project when using the authenticated OpenAI client returned by `get_openai_client()`.[page:1]

In your code example, you used `model="gpt-4.1-mini"` when creating the response request. That means your project must have a matching deployment available and accessible in the same Foundry project context.[page:1]

## Step 5: Create the agent in Foundry

Create an agent in the Foundry portal after the model is deployed. Give it a clear name, such as `first-foundry-agent`, because your Python code later retrieves the agent by name with:

```python
agent = project_client.agents.get(myAgent)
```

If the name does not match exactly, your code will raise `ResourceNotFoundError`, which is why your current script also lists available agents for debugging.[page:1]

When configuring the agent, make sure you review:

- Agent name.
- Agent instructions.
- Model configuration.
- Any tools or project resources the agent should use.

Even though your current script sends a prompt through `get_openai_client()`, validating that the agent exists is still useful because it confirms the project contains the configured Foundry agent you expect to work with.[page:1]

## Step 6: Install VS Code extensions

Install the extensions that make Azure and Foundry development easier in VS Code:

- Azure Resources extension.
- Microsoft Foundry or Foundry Toolkit extension, if available in your VS Code marketplace or environment.
- Python extension for VS Code.

These extensions help with authentication, project navigation, and interpreter management during local development.

## Step 7: Install Azure CLI

Install Azure CLI on your machine. If you are using macOS, one common installation method is:

```bash
brew install azure-cli
```

After installation, verify that it is working:

```bash
az version
```

Azure CLI matters here because local authentication is commonly satisfied by an Azure sign-in that `DefaultAzureCredential()` can detect as part of its credential chain.[page:1][page:2]

## Step 8: Sign in to Azure

Run the following command in your terminal:

```bash
az login
```

A browser window will open and ask you to sign in. After login succeeds, Azure CLI will know which account and subscription you are using locally.[page:1]

To confirm the selected subscription, run:

```bash
az account show
```

This is a good verification step because many connection issues happen simply because the wrong Azure account, tenant, or subscription is active.

## Step 9: Understand `DefaultAzureCredential()`

Your code uses:

```python
from azure.identity import DefaultAzureCredential
```

`DefaultAzureCredential()` tries multiple authentication sources in order, including environment credentials, managed identity, the VS Code Azure login, and the current Azure CLI login. That makes it a good choice for local development because it can often reuse the credentials you already established with VS Code or `az login`.[page:2]

For most first-time local setups, the Azure CLI sign-in is the easiest way to make this work.[page:1][page:2]

## Step 10: Install Python 3

Check your Python version:

```bash
python3 --version
```

The Azure AI Projects Python package requires Python 3.9 or later, so upgrade Python first if your local version is older.[page:1]

## Step 11: Create a virtual environment

Create a virtual environment for the project:

```bash
python3 -m venv myenv
```

Activate it on macOS or Linux:

```bash
source myenv/bin/activate
```

If you are on Windows, use the activation command that matches Command Prompt or PowerShell.

Why this step matters:

- It isolates project dependencies.
- It avoids version conflicts with other Python projects.
- It makes the setup cleaner for beginners.

## Step 12: Select the interpreter in VS Code

In VS Code:

1. Press `Cmd + Shift + P` on macOS, or `Ctrl + Shift + P` on Windows.
2. Search for **Python: Select Interpreter**.
3. Choose the interpreter from your virtual environment.

VS Code usually remembers this selection for the current workspace, which makes future runs easier.

## Step 13: Install the required Python packages

Install the SDK packages your code depends on:

```bash
pip install azure-ai-projects azure-identity openai
```

If your system requires `pip3`, run:

```bash
pip3 install azure-ai-projects azure-identity openai
```

These packages are needed for:

- `azure-ai-projects` for `AIProjectClient` and agent/project operations.[page:1]
- `azure-identity` for `DefaultAzureCredential()` authentication.[page:2]
- `openai` because `get_openai_client()` returns an authenticated OpenAI client from the `openai` package.[web:13][page:1]

## Step 14: Save your project endpoint

Your Python code currently hardcodes:

```python
myEndpoint = "https://xyz"
```

Replace that value with your real Foundry project endpoint from the project overview page. It should look similar to this:

```python
myEndpoint = "https://your-ai-services-account-name.services.ai.azure.com/api/projects/your-project-name"
```

Using the wrong endpoint is one of the most common setup mistakes, so copy it directly from Microsoft Foundry rather than typing it manually.[page:1]

## Step 15: Create your Python file

Create a new file called `my_first_agent.py` and add the following code:

```python
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

myEndpoint = "https://your-ai-services-account-name.services.ai.azure.com/api/projects/your-project-name"

project_client = AIProjectClient(
    endpoint=myEndpoint,
    credential=DefaultAzureCredential(),
    allow_preview=True,
)

myAgent = "first-foundry-agent"

try:
    agent = project_client.agents.get(myAgent)
except ResourceNotFoundError as exc:
    available_agents = [a.name for a in project_client.agents.list()]
    print(f"Agent '{myAgent}' was not found in this project.")
    print(f"Available agents: {available_agents if available_agents else 'None'}")
    raise SystemExit(1) from exc

print(f"Retrieved Agent Name: {agent.name}")

openai_client = project_client.get_openai_client(agent_name=myAgent)

response = openai_client.responses.create(
    model="gpt-4.1-mini",
    input="Hello, how are you?"
)

print(f"Agent Response: {response.output_text}")
```

This script does four important things:

1. Connects to your Foundry project using `AIProjectClient`.[page:1]
2. Authenticates with Azure using `DefaultAzureCredential()`.[page:2]
3. Checks whether the named agent exists in the project using the `.agents` client.[page:1]
4. Gets an authenticated OpenAI client and sends an LLM request using the Responses API.[web:13][page:1]

## Step 16: Run the script

Run your file from the terminal:

```bash
python my_first_agent.py
```

Or, if your environment requires it:

```bash
python3 my_first_agent.py
```

If everything is configured correctly, the script should:

- Connect to your Foundry project.
- Find the agent.
- Send the input prompt.
- Print the LLM response in your terminal.

whatever we developed so far is created using Azure AI Projects SDK.

Microsoft also provides another framework called MAF(Microsoft Agent Framework)
Microsoft Agent Framework (MAF) introduces a higher-level abstraction that unifies agents, personas, and memory tools natively. It relies on asynchronous execution via Python's asyncio loop to efficiently manage multi-agent architectures and high-performance streaming.

In order to use MAF and connect your agent from python we can can do the following..

`pip install agent-framework --pre`
`pip install python-dotenv`

also create an .env file now to move our Azure AI project end point and Agent name and model to .env file

Now create a file name agent_maf.py to access using MAF framework and communicate to LLM. Pls check the code to understand of using MAF framework.

Key Enhancements in MAF

    Asynchronous Design: Handled natively using asyncio for scalable execution.

    Streamlined Arguments: Uses unified project_endpoint and model initializers inside FoundryChatClient.

    Agent Encapsulation: Moves logic out of explicit client creation steps and abstracts interactions into a singular Agent.run() method execution.

## How your code works

### `AIProjectClient`

`AIProjectClient` is the main entry point for working with Azure AI Foundry project resources in Python. According to Microsoft documentation, it can be used to work with agents, deployments, connections, datasets, indexes, and authenticated OpenAI access within the same project.[page:1]

### `project_client.agents.get(myAgent)`

This line checks whether the agent exists in your project. In your code, this is a good safety step because it prevents the rest of the script from continuing with a wrong or missing agent name.[page:1]

### `project_client.agents.list()`

This is useful for beginners because, when the requested agent is missing, your script prints the available agent names. That makes debugging much easier than failing silently.

### `project_client.get_openai_client(agent_name=myAgent)`

The Azure AI Projects client can return an authenticated OpenAI client. Microsoft documents that `get_openai_client()` creates an OpenAI client configured for the project endpoint and backed by Azure token authentication rather than a manually pasted API key.[web:13][page:1]

### `responses.create(...)`

Your code then calls the Responses API using the OpenAI client. In your example, the request is sent with `model="gpt-4.1-mini"` and a simple prompt, and the final text is printed using `response.output_text`.[page:1]

## Why this is different from a normal `.env` setup

In many LLM tutorials, developers store an API key, endpoint, and model name in a `.env` file and call the model directly. In your setup, the project is authenticated through Microsoft Entra ID using `DefaultAzureCredential()`, and the application connects through the Foundry project client instead of manually building every authentication detail itself.[page:1][page:2]

That gives a cleaner Azure-native workflow for enterprise or team environments where project access is controlled centrally.

## Important beginner tips

These are the points first-time users usually miss:

- **Use the exact project endpoint** from the Foundry project overview page.[page:1]
- **Use the exact agent name** from the portal, including capitalization.[page:1]
- **Run `az login` before running Python** so `DefaultAzureCredential()` can find your Azure sign-in.[page:1][page:2]
- **Install `openai` as well** because `get_openai_client()` depends on the OpenAI Python package.[web:13]
- **Make sure the model name is valid in your project** when calling `responses.create(...)`.[page:1]
- **Check RBAC permissions** if authentication succeeds but access is denied, because Foundry project access depends on the correct Azure role assignments.[page:1]
- **Use Python 3.9 or newer** because the package requires it.[page:1]

## Troubleshooting

### Agent not found

If you see an error that your agent was not found:

- Verify that `myAgent` exactly matches the name in Foundry.
- Confirm you are pointing to the correct Foundry project endpoint.
- Use the printed `available_agents` list from your own script to check what exists in that project.

### Authentication failed

If authentication fails:

- Run `az login` again.
- Check `az account show`.
- Confirm that the signed-in account has permission to access the Foundry project.
- Confirm that `DefaultAzureCredential()` can use one of the available local credentials, such as Azure CLI or VS Code login.[page:2]

### Wrong model or response error

If the call fails at `responses.create(...)`:

- Check that `gpt-4.1-mini` is actually available to your project or connected resource.
- Confirm you are using a supported API path through the project client.
- Make sure package versions are up to date.

### Package import errors

If imports fail:

- Confirm your VS Code interpreter points to the same virtual environment where you installed the packages.
- Reinstall the dependencies inside the active virtual environment.

## Suggested project structure

A simple beginner-friendly folder structure can look like this:

```text
foundry-agent-python/
├── myenv/
├── my_first_agent.py
├── README.md
└── requirements.txt
```

Example `requirements.txt`:

```text
azure-ai-projects
azure-identity
openai
```

## Full workflow recap

1. Create an Azure account.
2. Open Microsoft Foundry at [ai.azure.com](https://ai.azure.com/).
3. Create a Foundry project.[web:12]
4. Copy the project endpoint from the project overview page.[page:1]
5. Deploy a model in **Models + endpoints**.[page:1]
6. Create an agent in Foundry.[page:1]
7. Install VS Code, Azure extensions, and Python extension.
8. Install Azure CLI.[page:1]
9. Run `az login`.[page:1]
10. Confirm the active Azure subscription.
11. Install Python 3.9 or later.[page:1]
12. Create and activate a virtual environment.
13. Select the interpreter in VS Code.
14. Install `azure-ai-projects`, `azure-identity`, and `openai`.[page:1][web:13]
15. Create `my_first_agent.py`.
16. Connect with `AIProjectClient` using `DefaultAzureCredential()`.[page:1][page:2]
17. Retrieve the agent using `project_client.agents.get(myAgent)`.[page:1]
18. Use `get_openai_client()` and `responses.create(...)` to communicate with the LLM.[web:13][page:1]
19. Print the response in the terminal.
