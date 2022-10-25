# Imports
import os, logging
from gaiasdk import sdk

# Funtion to generate a basic config file.
def get_template(args):
    # listing which arguments are valid.
    acceptable_args = ["dev", "staging", "prod"]

    # Have to loop through the arguments
    for x in args:
        # remove empty entry
        if x == "":
            pass
        else:
            # Ensure environment is valid
            if x.value not in acceptable_args:
                logging.error(f"Unsupported environment selected: {x.value}")
                exit(1)
            else:
                logging.info(f"Environment selected: {x.value}")
                # Multi line which will be my config file.
                my_config = """
                    monitoring-server: {env}-grafana.com
                    key-store:  {env}-vault.com
                    web-service-frontend: {env}-frontend.com
                    db-service-backend: {env}-db.com""".format(env=x.value)
                # Write to that file
                try:
                    config= open("/tmp/config.yaml","a+")
                    config.write(my_config)
                    # for f in my_config:
                    #     config.write(f)
                    config.close()
                    logging.info("Created the config file successfully")
                except:
                    logging.error("Failed to create config")
                    exit(1)
            # read the file to the logs for us to check it out.
            config_read = os.popen('cat /tmp/config.yaml').read()
            logging.info(config_read)
            # remove that temoporary file.
            os.remove('/tmp/config.yaml')

def main():
    # Configure logging.
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Define our argument input
    argParam = sdk.Argument("Type in your environment. It must be dev, staging or prod (Lowercase):", sdk.InputType.TextFieldInp, "Environment")
    # Configure our job with the args.
    configjob = sdk.Job("Generating config", "Creating the config", get_template, None, [argParam])
    # Run the job
    sdk.serve([configjob])