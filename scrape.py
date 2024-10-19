import config
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException
import time

def get_end_page(driver):
    try:
        
        last_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolderBody_fvBottom_lBtnLast')
        last_button.click()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table_rows = soup.find_all('tr')
        sno_values = []
        
       
        if len(table_rows) > 2:
            for row in table_rows[1:]:
                cells = row.find_all('td')
                if cells:
                    sno_text = cells[0].get_text(strip=True)
                    try:
                        sno = int(sno_text)
                        sno_values.append(sno)
                    except ValueError:
                        continue

        
        if sno_values:
            max_sno = max(sno_values)
            end_page_number = (max_sno - 1) // 30 + 1

        else:
            print("[DEBUG] No SNo values found on the last page.")
            end_page_number = None

       
        if end_page_number is not None:
            first_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolderBody_fvBottom_lBtnFirst')
            first_button.click()
            time.sleep(3)

        return end_page_number
    except Exception as e:
        print(f"[DEBUG] Error while detecting end page: {e}")
        return None

def navigate_to_start_page(driver, start_page):
   
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table_rows = soup.find_all('tr')
        current_page = 1 

        if len(table_rows) > 2:
            first_data_row_tds = table_rows[2].find_all('td')
            if len(first_data_row_tds) > 0:
                sno_text = first_data_row_tds[0].get_text(strip=True)
                try:
                    sno = int(sno_text)
                    current_page = (sno - 1) // 30 + 1  
                except ValueError:
                    print("[DEBUG] SNo text could not be converted to integer.")

        
        if start_page != current_page:
            while current_page < start_page:
                try:
                    next_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolderBody_fvBottom_lBtnNext')
                    if next_button.is_enabled():
                        next_button.click()
                        time.sleep(3)
                        current_page += 1
                    else:
                        print("[DEBUG] 'Next' button is disabled. Cannot navigate forward.")
                        break
                except NoSuchElementException as e:
                    print(f"[DEBUG] Error while navigating to page {start_page}: {e}")
                    break
                except Exception as e:
                    print(f"[DEBUG] Unexpected error: {e}")
                    break

            while current_page > start_page:
                try:
                    prev_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolderBody_fvBottom_lBtnPrevious')
                    if prev_button.is_enabled():
                        prev_button.click()
                        time.sleep(3)
                        current_page -= 1
                    else:
                        print("[DEBUG] 'Previous' button is disabled. Cannot navigate backward.")
                        break
                except NoSuchElementException as e:
                    print(f"[DEBUG] Error while navigating to page {start_page}: {e}")
                    break
                except Exception as e:
                    print(f"[DEBUG] Unexpected error: {e}")
                    break

        return current_page 

    except Exception as e:
        print(f"[DEBUG] Error while navigating to start page: {e}")
        return None
        

def main():
    all_data = []
    driver=None
    try:
        year = int(input("Enter the year you want info: "))

        if year < 2022:
            print("Error: Data not available for the entered year.")
            return

        url = config.URL_TEMPLATE.format(year, year)

        
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={config.USER_AGENT}")
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, config.TIMEOUT)

        try:
            driver.get(url)
        except NoSuchWindowException:
            print("Target window is already closed. Restarting the browser session.")
            driver.quit()
            driver = webdriver.Chrome(options=options)
            driver.get(url)

        
        end_page = get_end_page(driver)
        
        if end_page is None:
            print("[ERROR] Failed to retrieve the end page number.")
            driver.quit()
            return
        
        
        user_start_page = int(input(f"Enter the start page number (1-{end_page}): "))
        user_end_page = int(input(f"Enter the end page number (1-{end_page}, 0 for all pages): "))

        if user_start_page < config.DEFAULT_START_PAGE or user_start_page > end_page:
            print(f"[ERROR] Start page must be between {config.DEFAULT_START_PAGE} and {end_page}.")
            driver.quit()
            return

        if user_end_page == 0:
            user_end_page = end_page
        elif user_end_page < user_start_page or user_end_page > end_page:
            print(f"[ERROR] End page must be between {user_start_page} and {end_page}.")
            driver.quit()
            return
        
        page = navigate_to_start_page(driver, user_start_page)

        
        while page <= user_end_page or user_end_page == 0:
            try:
                
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table_rows = soup.find_all('tr')
                rows_to_scrape = table_rows[1:-1] if len(table_rows) > 2 else []
                for row in rows_to_scrape:
                    cells = row.find_all('td')
                    if cells:
                        row_data = [cell.text.strip() for cell in cells]
                        all_data.append(row_data)
                print(f"[DEBUG] Scraped data from page {page}.")

                
                if user_end_page == 0 or page < user_end_page:
                    try:
                        next_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolderBody_fvBottom_lBtnNext')
                        if next_button.is_enabled():
                           next_button.click()
                           time.sleep(config.SLEEP_BETWEEN_REQUESTS)  # Allow time for the page to load
                           page += 1
                        else:
                            print("[DEBUG] 'Next' button is disabled. No more pages to scrape.")
                            break
                    except NoSuchElementException as e:
                        print(f"[DEBUG] Next button not found or an error occurred: {e}")
                        break
                    except Exception as e:
                        print(f"[DEBUG] Unexpected error while clicking 'Next' button: {e}")
                        break
                else:
                    print("[DEBUG] Reached the user-specified end page.")
                    break
            except NoSuchWindowException as e:
                print(f"[ERROR] Window was closed unexpectedly: {e}")
                print("[DEBUG] Attempting to restart browser session")
                driver.quit()
                driver = webdriver.Chrome(options=options)
                driver.get(url)
                print(f"[DEBUG] Reopened URL and attempting to resume from page {page}.")
                continue

            except Exception as e:
                print(f"[DEBUG] Error occurred while processing page {page}: {e}")
                break

    finally:
        if driver is not None:
            driver.quit()
            print("[DEBUG] Browser session closed.")

    
        if config.SAVE_TO_CSV and all_data:
            df = pd.DataFrame(all_data,columns=['SNo.', 'Name of the student', 'FIITJEE Enrollment No.','Programme Name','AIR'])
            df.to_csv(f'scraped_data_{year}.csv',index=False)
            print("[DEBUG] Scraping completed and data saved to CSV.")
        else:
            print("[DEBUG] No data was scraped.")

if __name__ == "__main__":
    main()



