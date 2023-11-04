import logging

# Create a logger instance
logger = logging.getLogger('bot_logger')
logger.setLevel(logging.DEBUG)  # Set the desired log level

# Create a console handler and set its log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set the desired log level

# Create a formatter and attach it to the console handler
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)
