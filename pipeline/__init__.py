import os
from gaiasdk import sdk

import logging

def get_template(env):

    env = env.key

    mylist = f"""
        monitoring-server: {env}-grafana.com
        key-store:  {env}-vault.com
        web-service-frontend: {env}-frontend.com
        db-service-backend: {env}-db.com"""

    try:
        config= open("/tmp/config.yaml","a+")
        for f in mylist:
            config.write(f)
        config.close()
        logging.info("Created the config file successfully")
    except:
        logging.error("Failed to create config")
        exit(1)

    test = os.popen('cat /tmp/config.yaml').read()
    print(test)
    logging.info(test)
    


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Instead of sdk.InputType.TextFieldInp you can also use sdk.InputType.TextAreaInp
    # for a text area or sdk.InputType.BoolInp for boolean input.
    argParam = sdk.Argument("Type in your environment:", sdk.InputType.TextFieldInp, "environment")
    configjob = sdk.Job("Generating config", "Creating the config", get_template, None, [argParam])
    sdk.serve([configjob])