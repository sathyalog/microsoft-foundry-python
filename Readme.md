Create an azure account
goto URL: ai.azure.com(microsoft foundry)
create a project
choose a model and deploy it

Install azure resources extension in vscode
Install foundry toolkit extension in vscode

Install azure cli in your machine(mac/windows)
I am using mac so my command is `brew install azure-cli`

sign into azure with your account
after sign in you will see your subscription name(eg: Azure subscription1)
Inside that choose microsoft foundry and open your project(which you created in ai.azure.com(foundry))
then foundry extension gets linked with your project so you can access and work on it.

install python3
check python3 -v
create virtual env with `python3 -m venv myenv`
run this command to start virtual env `source myenv/bin/activate`

Everytime you do not need to run virtual environment with above commands

In vscode run cmd+shift+p type python and choose "select interpreter" and choose your version then vscode remembers virtual env. when you open a new terminal it will remember your virtual environment.

uv also manages complex projects with virtual environments

now lets install necessary python libraries
`pip install azure-ai-projects azure-identity`
if python3 version then use pip3 and it will be like `pip3 install azure-ai-projects azure-identity`

After this azure login using `az login` and login into browser to choose your azure portal login, after that it will show subscription in terminal

choose 1(top in the list) and it will be selected default

then to see whether we connected python environment with azure type
`az account show`

Now created a new python file called my_first_agent.py and provided our agent name to retrieve my configured agent and using agent model, we can give prompt in my python file and get response. Usually we will configure api keys and model names etc in .env file right? instead of that process, we used agent end point to communicate with LLM. check the code.






