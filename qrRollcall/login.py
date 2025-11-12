import time
import requests
from tkinter import Tk, Label
from PIL import ImageTk, Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def login(url, driver, status, username, password):
    if not status:
        print("登录无需验证,正在登录...")
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.ID, "userNameLogin_a"))
        ).click()
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login_submit").click()
        time.sleep(5)
        driver.get(url)
        res = requests.get(url, cookies={c['name']: c['value'] for c in driver.get_cookies()})
        if res.status_code == 200:
            verified_cookies = {c['name']: c['value'] for c in driver.get_cookies()}
            return True, verified_cookies

    print("账号密码登录暂时不可用，请用企业微信扫码登录。")
    driver.find_element(By.ID, "qrLogin_a").click()
    time.sleep(1)
    driver.set_window_size(1920, 1080)
    elem = driver.find_element(By.ID, "qr_img")
    elem.screenshot("cache/qr_code.png")
    root = Tk()
    img = Image.open("cache/qr_code.png")
    tk_img = ImageTk.PhotoImage(img)
    Label(root, image=tk_img).pack()
    root.mainloop()
    res = requests.get(url, cookies={c['name']: c['value'] for c in driver.get_cookies()})
    if res.status_code == 200:
        verified_cookies = {c['name']: c['value'] for c in driver.get_cookies()}
        return True, verified_cookies

    return False, None