import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Load local quiz_form.html directly via file:// URI
html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_form.html")
file_url = f"file:///{html_path.replace(os.sep, '/')}"

options = Options()
# Run headless automatically in GitHub Actions CI; visible locally unless HEADLESS=1
if os.getenv("CI") == "true" or os.getenv("HEADLESS") == "1":
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# 5 test cases: (input_value, expected_prefix)
test_cases = [
    ("-1", "Rejected"),
    ("0", "Accepted"),
    ("1", "Accepted"),
    ("10", "Accepted"),
    ("11", "Rejected"),
]

print(f"{'Input':<8} | {'Expected':<10} | {'Actual Result':<45} | {'Status'}")
print("-" * 80)

all_passed = True

try:
    for value, expected_prefix in test_cases:
        driver.get(file_url)
        input_box = driver.find_element(By.ID, "markInput")
        submit_btn = driver.find_element(By.ID, "submitBtn")

        input_box.clear()
        input_box.send_keys(value)
        submit_btn.click()

        actual_text = driver.find_element(By.ID, "result").text.strip()
        passed = actual_text.startswith(expected_prefix)
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False

        print(f"{value:<8} | {expected_prefix:<10} | {actual_text:<45} | {status}")
finally:
    driver.quit()

if not all_passed:
    sys.exit(1)
