#  FIITJEE Scraper: Dynamic Data Scraper

This project automates the extraction of FIITJEE exam results from the official results page, available at FIITJEE Results Page. Using Selenium, it allows users to specify the starting page, year, and the number of pages to scrape, offering flexibility and control over the scraping process. If the year entered is earlier than 2022, the scraper displays an error message, ensuring accurate input. The scraper is designed to handle dynamic page navigation, starting from the selected page regardless of the initially opened one, and it offers the option to scrape either a limited range of pages or all available pages. This tool is ideal for students, parents, and researchers looking to quickly access FIITJEE-related results without manual browsing. Additionally, developers can use this as a base project for web scraping tasks, given its customizable Selenium-based architecture.


## Features

**Dynamic URL Generation**: Easily create and modify URLs based on user input to target specific data ranges.

**Flexible Page Scraping**: Choose to scrape either a specific range of pages or all available pages with seamless transitions.

**Error Handling**: Built-in mechanisms to handle common issues, such as unavailable data for certain years, ensuring smooth operation.

**Retry Mechanism**: Automatically retries failed requests, minimizing interruptions due to temporary issues.

**User-Friendly Interface**: Clear prompts and error messages guide users through the scraping process.

## Tech Stack


**Server:** Python, Selenium WebDriver

**Dependencies**: ChromeDriver (or other WebDriver), Python libraries (as specified in requirements.txt)

## Installation

Follow these steps to install and set up the WebPulse project :

1.**Clone the repository**:
```bash
  git clone https://github.com/yourusername/webpulse.git
cd webpulse
```
2. **Install the required Python packages**:
```bash
    pip install -r requirements.txt
```
3. **Download and set up the WebDriver**:
     
->      Download **ChromeDriver** (or the appropriate WebDriver for your browser).


    
## Usage/Examples

To use the WebPulse scraper, follow these steps:

1. **Run the Script**:
    ```bash
        python scrape.py
    ```
2. **Enter the required parameters when prompted, such as the year and page range.** 
