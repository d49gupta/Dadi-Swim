from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

def getDay():
    today = datetime.datetime.today().weekday()  # Monday=0, Sunday=6
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return day_names[(today + 2) % 7]

email = "gupta.swaran@gmail.com"
# email = "dharma.anita@gmail.com"
timeslot = "8:30 AM"
day = getDay()
# day = 'Thursday'

def book():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--headless')  # Uncomment if running on EC2 without GUI
    # options.add_argument('--headless=new')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://reservation.frontdesksuite.ca/rcfs/pinecrest/Home/Index?Culture=en&PageId=d2e84295-c4e0-490a-861b-f99e10636ab2&ShouldStartReserveTimeFlow=False&ButtonId=00000000-0000-0000-0000-000000000000")

    try:
        # Step 1: Click "Aqua general shallow"
        aqua_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//div[text()='Aqua general shallow']]"))
        )
        aqua_link.click()
        print("✅ Clicked 'Aqua general shallow'")

        # Step 2: Set number of people
        count_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "reservationCount"))
        )
        count_input.clear()
        count_input.send_keys("1")
        print("✅ Set number of people to 1")

        # Step 3: Confirm initial form
        initial_confirm = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit-btn"))
        )
        initial_confirm.click()
        print("✅ Clicked initial Confirm button")

        # Step 4: Expand Tuesday's rows
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//a[contains(@aria-label, '{day}')]"))
            )
            buttons = driver.find_elements(By.XPATH, f"//a[contains(@aria-label, '{day}')]")
            for btn in buttons:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                except:
                    continue
            print("✅ Expanded Tuesday rows")
        except Exception as e:
            print("❌ Couldn't expand day sections:", e)

        # Step 5: Pick 7:30 AM slot
        try:
            slots = driver.find_elements(By.XPATH, "//a[contains(@aria-label, {timeslot})]")
            print(f"🔍 Found {len(slots)} 7:30 AM slot(s)")
            if slots:
                slots[0].click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "field2021")))
                print("✅ Selected 7:30 AM and loaded contact form")
            else:
                print("❌ No 7:30 AM slot found.")
        except Exception as e:
            print("❌ Error selecting time slot:", e)

        # Step 6: Fill in contact form
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "field2021"))).send_keys("Swaran Gupta")
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys("dharma.anita@gmail.com")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "telephone"))).send_keys("6137984810")
            print("✅ Filled in name, email, and phone")
        except Exception as e:
            print("❌ Error filling in contact info:", e)

        # Find the actual submit button
        try:
            # Wait for final confirm button
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "submit-btn"))
            )

            # Dispatch a real click
            driver.execute_script("""
                let btn = arguments[0];
                let event = new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                btn.dispatchEvent(event);
            """, submit_button)
            print("✅ Real DOM click dispatched to Final Submit button")

            # Give time for async JS
            time.sleep(2)

            # Fallback: explicitly trigger submitCommand in case form isn't submitted yet
            driver.execute_script("submitCommand();")
            print("✅ submitCommand() triggered as fallback")

            # Wait again for JS to finish
            time.sleep(2)

            # Check for any validation errors
            errors = driver.execute_script("""
                return Array.from(document.querySelectorAll(".field-validation-error, .validation-summary-errors"))
                            .map(e => e.innerText.trim()).filter(Boolean);
            """)
            if errors:
                print("❌ Validation errors found:")
                for e in errors:
                    print("   ➤", e)
            else:
                print("✅ No visible validation errors — form may have submitted successfully")

        except Exception as e:
            print("❌ Final submission step failed:", e)

    except Exception as e:
        print("❌ Error in booking process:", e)

    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    book()
