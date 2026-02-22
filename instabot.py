import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random

def setup_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Uncomment for headless mode
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def random_sleep(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def login(driver, username, password):
    driver.get("https://www.instagram.com/")
    random_sleep(2, 4)
    driver.delete_all_cookies()
    driver.get("https://www.instagram.com/accounts/login/")
    random_sleep(3, 5) # Wait for page load
    
    try:
        # Enter Username
        user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username' or @name='email']"))
        )
        user_input.send_keys(username)
        random_sleep(1, 2)
        
        # Enter Password
        pass_input = driver.find_element(By.XPATH, "//input[@name='password' or @name='pass']")
        pass_input.send_keys(password)
        random_sleep(1, 2)
        
        # Click Login
        try:
            # Try to click the actual login div or button
            login_btn = driver.find_element(By.XPATH, "//*[text()='Log in' or text()='Log In']")
            login_btn.click()
        except Exception:
            # Fallback to Enter key
            pass_input.send_keys(Keys.RETURN)
        
        random_sleep(3, 5)
        
        # Wait for login to complete
        try:
            WebDriverWait(driver, 15).until(
                lambda d: "accounts/login" not in d.current_url
            )
            print(f"Successfully logged in as {username}")
        except Exception as e:
            driver.save_screenshot(f"login_timeout_{username}.png")
            print(f"Login timed out or failed for {username}. See login_timeout_{username}.png")
            return False
            
        random_sleep(3, 5)
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        driver.save_screenshot(f"error_{username}.png")
        print(f"Login failed for {username}: {e}")
        return False

def like_post(driver, post_url):
    from selenium.webdriver.common.action_chains import ActionChains
    driver.get(post_url)
    random_sleep(5, 8)
    
    try:
        # Check if already liked first
        try:
            driver.find_element(By.XPATH, "//svg[@aria-label='Unlike']")
            print(f"Post already liked: {post_url}")
            return
        except:
            pass
            
        # Look for the main post image or video to double click
        # We wait for at least one image to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
        
        # Find the largest visible image or video (this is typically the main post content)
        media_elements = driver.find_elements(By.TAG_NAME, "img") + driver.find_elements(By.TAG_NAME, "video")
        
        main_media = None
        max_area = 0
        
        for media in media_elements:
            try:
                if media.is_displayed():
                    size = media.size
                    area = size['width'] * size['height']
                    if area > max_area:
                        max_area = area
                        main_media = media
            except:
                pass
                
        if main_media and max_area > 10000: # Ensure it's reasonably large (e.g. 100x100+)
            # Double click to like!
            ActionChains(driver).double_click(main_media).perform()
            print(f"Double-clicked main media for post: {post_url}")
        else:
            raise Exception("Could not find a large enough main media element to double-click.")
            
        random_sleep(3, 5)
    except Exception as e:
        import traceback
        traceback.print_exc()
        driver.save_screenshot(f"like_failed_{post_url[-15:-1]}.png")
        with open("failed_post.html", "w") as f:
            f.write(driver.page_source)
        print(f"Could not like post {post_url}: {e}")

def main():
    csv_file = "credentials.csv"
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Please create it first.")
        return

    for index, row in df.iterrows():
        driver = None
        try:
            print(f"Processing user: {row['username']}")
            driver = setup_browser()
            
            if login(driver, row['username'], row['password']):
                # Optional: Navigate to profile first as requested
                if 'profile_url' in row and pd.notna(row['profile_url']):
                    driver.get(row['profile_url'])
                    random_sleep(2, 4)
                
                # Navigate to post and like
                if 'post_url' in row and pd.notna(row['post_url']):
                    like_post(driver, row['post_url'])
            
            print(f"Finished session for {row['username']}\n")
            
        except Exception as e:
            print(f"Error processing {row['username']}: {e}")
        finally:
            if driver:
                driver.quit()
            random_sleep(5, 10) # Heavy delay between accounts

if __name__ == "__main__":
    main()
