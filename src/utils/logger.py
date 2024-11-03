import logging

class Logger:
    @staticmethod
    def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
        """Setup a logger with the specified name and level."""
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add handler to the logger
        logger.addHandler(ch)
        return logger

# Example usage
if __name__ == "__main__":
    logger = Logger.setup_logger("MyLogger")
    logger.info("This is an info message.")
    logger.error("This is an error message.")
