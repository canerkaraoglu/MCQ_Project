# Logger file for the project. Whenever we execute a code, during the different phases of the code, 
# we need to log that information.

import logging
import os
from datetime import datetime

# Log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Store the log file
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Create the object of logging
# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(level=logging.INFO,
        filename=LOG_FILEPATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

# To call import this file and logging.info("Hi, I'm going to start my execution...")