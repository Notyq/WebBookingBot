from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import capsolver
import datetime


# leave window open when done
options = Options()
options.add_argument('--user-data-dir=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
options.add_experimental_option("detach", True)
driver = uc.Chrome()

websiteURL = 'https://www.google.com/recaptcha/api2/demo'
driver.get(websiteURL)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
print("Opened website")
# iframe = driver.find_element(By.XPATH('/html/body/div[1]/div/div[2]'))
# captcha_site_key = iframe.get_attribute('data-sitekey')
# print(captcha_site_key)
captcha_element = driver.find_element(By.CLASS_NAME, "g-recaptcha")
data_sitekey = captcha_element.get_attribute("data-sitekey")
print(data_sitekey)

def main():
    # Solve CAPTCHA
    driver.get(websiteURL)
    wait = WebDriverWait(driver, 10)
    driver.maximize_window()
    token = get_token(websiteURL, data_sitekey)
    post_data(token, websiteURL)
    print("Submitted form")



def get_token(websiteURL, websiteKey):
    # Your CapSolver API key
    capsolver.api_key = 'CAP-8E7E60DF49320EA19B99D3EDEF3FF155'

    # Parameters for the reCAPTCHA v2 (proxyless) task
    solution = capsolver.solve({
        "type": "ReCaptchaV2TaskProxyLess",
        "websiteURL": websiteURL,
        "websiteKey": websiteKey
    })

    print('CAPTCHA solution:', solution)
    
    token = solution['gRecaptchaResponse']



    # payload = {
    #     'g-recaptcha-response': token,
    #     # Include any other necessary data
    # }

    # # Send a POST request to the endpoint with the token in the payload
    # solved_captcha = requests.post(websiteURL, data=payload)

    # print("solved captcha: ", solved_captcha)

    return token

def post_data(token, websiteURL):
    driver.get(websiteURL)
    # Find the reCAPTCHA form field (replace 'g-recaptcha-response' with the actual field ID)
    recaptcha_response_field = driver.find_element(By.ID, 'g-recaptcha-response')
    # Inject the token into the field
    driver.execute_script("arguments[0].value = arguments[1]", recaptcha_response_field, token)
    # Submit the form
    form = driver.find_element(By.ID, "recaptcha-demo-submit")
    form.submit()


# def post_data(token, websiteURL):
#     cookies = {
#         '_ga': 'GA1.1.917993207.1709800797',
#         '_ga_70K7MBE4SF': 'GS1.1.1709803121.2.1.1709803122.59.0.0',
#     }

#     headers = {
#         'authority': 'nopecha.com',
#         'accept': '*/*',
#         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#         'content-type': 'application/json',
#         # 'cookie': '_ga=GA1.1.917993207.1709800797; _ga_70K7MBE4SF=GS1.1.1709803121.2.1.1709803122.59.0.0',
#         'origin': 'https://nopecha.com',
#         'referer': 'https://nopecha.com/demo/recaptcha',
#         'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#     }

#     json_data = {
#         'token': token,
#         'type': 'moderate',
#     }

#     response = requests.post(websiteURL, cookies=cookies, headers=headers, json=json_data)
#     print(response)

#     return response

main()