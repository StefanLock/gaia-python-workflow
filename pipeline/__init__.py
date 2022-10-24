from asyncore import write
from distutils.command.config import config
from fileinput import close
import sys
from gaiasdk import sdk
import logging

def get_template(env):

    mylist = [
        f"monitoring-server: {env}-grafana.com",
        f"key-store:  {env}-vault.com",
        f"web-service-frontend: {env}-frontend.com",
        f"db-service-backend: {env}-db.com"
    ]

    config= open("config.yaml","a+")

    for f in mylist:
        config.write(f)
    
    contents = config.read()
    print(contents)
    
    config.close()


def main():
    logging.basicConfig(level=logging.INFO)
    # Instead of sdk.InputType.TextFieldInp you can also use sdk.InputType.TextAreaInp
    # for a text area or sdk.InputType.BoolInp for boolean input.
    argParam = sdk.Argument("Type in your environment:", sdk.InputType.TextFieldInp, "environment")
    configjob = sdk.Job("Generating config", "Creating the config", get_template, None, [argParam])
    sdk.serve([configjob])