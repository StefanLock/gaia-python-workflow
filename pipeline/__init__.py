from gaiasdk import sdk
import logging
from jinja2 import Environment, FileSystemLoader
import yaml
from os import system

def get_template(env):
    ## Open up our yaml file which will map any services depending on the environment.
    with open('.envConfigValues.yaml', 'r') as file:
        svc_conf = yaml.safe_load(file)
    
    logging.info("Gathering contents for our config file.")
    ## Pulling the values from the service discovery yaml and assigning them to variables.
    monitoringserver = svc_conf[env]['monitoring-server']
    keystore = svc_conf[env]['key-store']
    webservicefrontend = svc_conf[env]['web-service-frontend']
    dbservicebackend = svc_conf[env]['db-service-backend']

    ## Load the templates directory.
    file_loader = FileSystemLoader('templates')
    ## Create our Jinja environment
    jinja_env = Environment(loader=file_loader)
    ## Get our template config file.
    template = jinja_env.get_template("config.yaml")
    ## Create the config file using are variables from the service-discovery yaml.
    outputText = template.render(
        monitoringserver = monitoringserver,
        keystore = keystore,
        webservicefrontend = webservicefrontend,
        dbservicebackend = dbservicebackend
    )

    ## Write the new file
    f = open(f"output/{env}Config.yaml", "w")
    f.write(outputText)
    f.close()

def show_new_config(env):
    system(f"cat output/{env}Config.yaml")


def main():
    logging.basicConfig(level=logging.INFO)
    # Instead of sdk.InputType.TextFieldInp you can also use sdk.InputType.TextAreaInp
    # for a text area or sdk.InputType.BoolInp for boolean input.
    argParam = sdk.Argument("Type in your environment:", sdk.InputType.TextFieldInp, "environment")
    configjob = sdk.Job("Generating config", "Creating the config", get_template, None, [argParam])
    printjob = sdk.Job("Getting config contents", "Printing config", show_new_config, ["Generating config"], [argParam])
    sdk.serve([configjob, printjob])