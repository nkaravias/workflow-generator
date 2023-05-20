import logging


def setup_logger(logger_name, log_file=None, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create and configure the console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create and configure the file handler if log_file is provided
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# Create a logger instance for the workflow
workflow_logger = setup_logger("workflow", log_file="workflow.log")
