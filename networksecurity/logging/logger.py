import logging
import os
from datetime import datetime

# Create a logs folder
LOGS_FOLDER = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGS_FOLDER, exist_ok=True)

# Create a log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOGS_FOLDER, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
