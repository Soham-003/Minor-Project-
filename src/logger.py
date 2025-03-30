import logging
import os
from datetime import datetime

log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logs_path = os.path.join(os.getcwd(),"LOGS",log_file)
os.makedirs(os.path.dirname(logs_path), exist_ok=True)

logging.basicConfig(
    filename = logs_path,
    level = logging.INFO,
    format = '%(asctime)s-%(name)s-%(levelname)s-%(message)s',
)

if __name__ == "__main__":
    logging.info("This is a test log")