import logging


# Define color escape codes
COLORS = {
    logging.DEBUG: "\033[0m",         # Default color
    logging.INFO: "\033[94m",         # Blue
    logging.WARNING: "\033[93m",      # Yellow
    logging.ERROR: "\033[91m",        # Red
    logging.CRITICAL: "\033[95m"      # Magenta
}


class ColoredFormatter(logging.Formatter):
    ''' Custom log formatter to set output style per log level '''
    def format(self, record):
        # Get the log level and corresponding color code
        log_level = record.levelno
        color_code = COLORS.get(log_level, "")

        # Apply the color code to the log message
        log_message = super().format(record)
        colored_log_message = f"{color_code}{log_message}\033[0m"

        return colored_log_message


def setup_logger(logger_name, log_file=None, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create and configure the console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Set the custom log formatter
    console_formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")
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


# Create a logger instance
workflow_logger = setup_logger("workflow", log_file="workflow.log")
