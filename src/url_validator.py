import validators
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)
def validate_url(url):
    """
    Validate the given URL.
    
    Args:
        url (str): URL to validate
    
    Returns:
        bool: True if URL is valid, False otherwise
    """
    logging.info(" *****      1      ***** ")
    return validators.url(url) is True