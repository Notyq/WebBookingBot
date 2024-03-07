from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import capsolver


# leave window open when done
options = Options()
options.add_argument('--user-data-dir=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
options.add_experimental_option("detach", True)
driver = uc.Chrome()

websiteURL = 'https://nopecha.com/demo/recaptcha#moderate'
iframe = driver.find_element(By.XPATH('/html/body/div[1]/div/div[2]'))
captcha_site_key = iframe.get_attribute('data-sitekey')
print(captcha_site_key)


# def main():
#     # Solve CAPTCHA
#     driver.get(websiteURL)
#     solve_captcha(websiteURL, websiteKey)
#     driver.maximize_window()
#     wait = WebDriverWait(driver, 10)

# def solve_captcha(websiteURL, websiteKey):
#     # Your CapSolver API key
#     capsolver.api_key = 'CAP-8E7E60DF49320EA19B99D3EDEF3FF155'

#     # # CapSolver API endpoint
#     capSolver_api_url = 'https://api.capsolver.com/createTask'

#     # Parameters for the reCAPTCHA v2 (proxyless) task
#     solution = capsolver.solve({
#         "type": "ReCaptchaV2TaskProxyLess",
#         "websiteURL": websiteURL,
#         "websiteKey": websiteKey
#     })

#     print('CAPTCHA solution:', solution)

#     # # Send HTTP POST request to CapSolver API
#     # response = requests.post(capSolver_api_url, data=params)

#     # # Check if request was successful
#     # if response.status_code == 200:
#     #     # Parse response JSON
#     #     response_json = response.json()

#     #     # Check if solution is available
#     #     if response_json['status'] == 1:
#     #         # Solution found
#     #         solution = response_json['solution']
#     #         print('CAPTCHA solution:', solution)
#     #     else:
#     #         # No solution found or error occurred
#     #         error_message = response_json['error']
#     #         print('Error:', error_message)
#     # else:
#     #     # Request failed
#     #     print('Failed to connect to CapSolver API')

# main()