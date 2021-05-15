import subprocess
import logging
logger = logging.getLogger(__name__)

def runBashCommand(bashCommand):

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    logger.debug(output)
    logger.debug(error)

    return output, error
