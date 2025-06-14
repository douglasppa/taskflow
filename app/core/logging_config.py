import logging.config
import json_log_formatter

class CustomJsonFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra['level'] = record.levelname
        extra['logger'] = record.name
        return extra

def setup_logging():
    formatter = CustomJsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)