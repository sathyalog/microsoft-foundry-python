import os
import asyncio
from dotenv import load_dotenv
from azure.identity import AzureCliCredential

# Import MAF specific modules
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient

load_dotenv(override=True)

PROMPT = "Hello, how are you?"


def normalize_endpoint(endpoint: str | None) -> str:
    if not endpoint:
        return "https://sathya-first-agentic-pr-resource.services.ai.azure.com/api/projects/sathya-first-agentic-project"

    endpoint = endpoint.rstrip("/")
    if "/api/projects/" in endpoint:
        return endpoint

    project_name = os.getenv("Azure_AI_Project_Name") or "sathya-first-agentic-project"
    return f"{endpoint}/api/projects/{project_name}"


async def main():
    # 1. Resolve configuration values
    endpoint = normalize_endpoint(os.getenv("Azure_AI_Project_Endpoint"))
    agent_name = os.getenv("Azure_AI_Agent_ID") or "first-foundry-agent"

    print(f"Using endpoint: {endpoint}")
    print(f"Using agent: {agent_name}")

    # 2. Initialize the MAF Foundry Client with proper parameters
    client = FoundryChatClient(
        project_endpoint=endpoint,
        credential=AzureCliCredential(),
        model="gpt-4.1-mini",
    )

    # 3. Define the MAF Agent wrapping the client configuration
    agent = Agent(
        name=agent_name, client=client, instructions="You are a helpful assistant."
    )

    print(f"Retrieved Agent Name: {agent.name}")

    # 4. Invoke the agent asynchronously
    response = await agent.run(PROMPT)

    # MAF directly returns the result message string/object
    print(f"Agent Response: {response}")


if __name__ == "__main__":
    # Run the async main loop
    asyncio.run(main())