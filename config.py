# Configuration file for the web scraper

# User agent string to mimic a real browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# URL template for constructing the target URL
URL_TEMPLATE = "http://jeemain.iitjeetoppers.com/{}/CompleteResult{}.aspx"

# Default settings
DEFAULT_START_PAGE = 1  # The default page number to start scraping from
MAX_RETRIES = 3  # Number of times to retry a failed request

# Other settings
TIMEOUT = 10  # Maximum time to wait for a page to load (in seconds)
SLEEP_BETWEEN_REQUESTS = 3  # Time to wait between requests to avoid overwhelming the server

# Optional configurations for specific needs
SAVE_TO_CSV = True  # Whether to save the scraped data to a CSV file
DEBUG_MODE = True  # Enable debug mode to get detailed log outputs


