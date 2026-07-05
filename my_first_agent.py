from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

myEndpoint = "https://sathya-first-agentic-pr-resource.services.ai.azure.com/api/projects/sathya-first-agentic-project"

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
