from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
import datetime
import time

# leave window open when done
options = Options()
options.add_experimental_option("detach", True)
driver = uc.Chrome()

# *** SET LOGIN DETAILS HERE ***
username = "82094541"
password = "t0404934e"

# *** CUSTOMIZE BOOKING HERE ***
total_courts = [1, 2, 3, 4, 5, 6, 7, 8]
courts = [1]
total_time_slots = ["7am", "8am", "9am", "10am", "11am", "12pm",
                    "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm"]
# total_time_slots = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm"]
time_slots = ["7am", "8am"]
# Only badminton @ bedok heartbeat for now (1181 - bukit canberra, 895 - bedok heartbeat, 560 - northland secondary school)
activity_id = 18
venue_id = 1181
now = datetime.datetime.now()
d = datetime.timedelta(days=16)
time_stamp = int((now + d).timestamp())


# get time_index for xpath in select_bookings
time_index = []
for i in time_slots:
    index = total_time_slots.index(i) + 1
    time_index.append(index)


def select_bookings():
    for i in courts:
        for j in time_index:
            xpath = (
                '/html/body/div[3]/main/div[3]/div/article/section[4]/div/div[1]/form/div[1]/div[{court}]/div/div[{time}]/label')

            params = {
                'court': i,
                'time': j, }
            xpath = xpath.format(**params)
            slot = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", slot)


# go to bookings
driver.get("https://members.myactivesg.com/auth?redirect=%2Fprofile")
driver.maximize_window()
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[3]/div/div[1]/div/article/div[2]/div/form/fieldset/div/div[1]/div[2]/div[1]/input"))).click()
driver.find_element(
    By.XPATH, "/html/body/div[3]/div/div[1]/div/article/div[2]/div/form/fieldset/div/div[1]/div[2]/div[1]/input").send_keys(username)
driver.find_element(
    By.XPATH, "/html/body/div[3]/div/div[1]/div/article/div[2]/div/form/fieldset/div/div[1]/div[2]/div[2]/input").send_keys(password)
driver.find_element(
    By.XPATH, "/html/body/div[3]/div/div[1]/div/article/div[2]/div/form/fieldset/div/div[1]/div[2]/div[5]/input").click()
wait.until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[3]/main/div[3]/div/div[1]/div/p/a")))
# url = (
#     'https://members.myactivesg.com/facilities/view/activity/{activity_id}/venue/{venue_id}?time_from={time}')
url = (
    'https://members.myactivesg.com/facilities/quick-booking')
params = {
    'activity_id': activity_id,
    'venue_id': venue_id,
    'time': time_stamp
}
url = url.format(**params)
driver.get(url)
print(url)
time.sleep(2)


wait.until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[3]/div/form/fieldset[1]/div/a"))).click()
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[3]/div/form/fieldset[1]/div/div/ul/li[2]").click()
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[3]/div/form/fieldset[2]/div/a/span").click()
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[3]/div/form/fieldset[2]/div/div/ul/li[13]").click()
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[3]/div/form/fieldset[3]/input").click()
driver.find_element(
    By.XPATH, "/html/body/div[4]/table/tbody/tr[4]/td[5]").click()
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[3]/div/form/fieldset[4]/input").click()


# refresh till bookings selected
while True:
    try:
        select_bookings()
        driver.find_element(By.ID, "addtocartbtn").click()
        break
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print("Bookings not found, refreshing page...")
        driver.refresh()
        time.sleep(2)

# get past speed detector
print("Bookings found!")
# time.sleep(2)
# ok = driver.find_element(By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[4]/div/div[1]/form/div[2]/div/input")
# driver.execute_script("arguments[0].click();", ok)
# time.sleep(1)
# print("Speed detector bypassed")

# # actual add to cart
# select_bookings()
# time.sleep(1)
# select_bookings()
# time.sleep(3)
# driver.find_element(By.ID, "addtocartbtn").click()
# time.sleep(2)
# driver.find_element(
#     By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[3]/div[4]/div/form/div[2]/div/input").click()
# if UnexpectedAlertPresentException:
#     time.sleep(100)
print("Added to cart")


try:
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[4]/div/div[1]/form/div[2]/div/input"))).click()
except UnexpectedAlertPresentException:
    cart_url = "https://members.myactivesg.com/cart"
    driver.get(cart_url)
    print("unexpectedAlertException: Proceeding to cart")

#TOC bs check
# wait.until(EC.element_to_be_clickable(
#     (By.XPATH, "/html/body/div[9]/div/div/div[2]/button")))
# driver.find_element(
#     By.XPATH, "/html/body/div[9]/div/div/div[2]/button").click()
# time.sleep(10)

# # select debit
# driver.find_element(
#     By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[1]/div/ul/li[1]/input").click()

# # pay
# driver.find_element(
#     By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[2]/div/div/input").click()

# enter pin
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[1]/div/div/div[1]/input[1]").sendkeys("0")
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[1]/div/div/div[1]/input[1]").sendkeys("4")
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[1]/div/div/div[1]/input[1]").sendkeys("0")
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[1]/div/div/div[1]/input[1]").sendkeys("4")
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[1]/div/div/div[1]/input[1]").sendkeys("9")
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[1]/div/div/div[1]/input[1]").sendkeys("3")
driver.find_element(
    By.XPATH, "/html/body/div[3]/main/div[3]/div/article/section[2]/form/div[2]/div/div/input").click()