from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

driver = webdriver.Chrome(chrome_options=options)

wait = WebDriverWait(driver, 5)

driver.get("http://localhost/IDM2008/SmartView.aspx?mid=10&svid=49&mode=minimal&linkId=29")

# Login
driver.find_element_by_id("txtUsername").send_keys("Frank_Gallagher")
# Password
driver.find_element_by_id("txtPassword").send_keys("Master_Password_Here")
# Log in button (localhost)
driver.find_element_by_id("cmdOK_CMD").click()     

wait.until(EC.title_is("User Management"))

# Choosing 'Create New User' Smart Binder
driver.find_element_by_id("SVT_ctl12_ctl02_IMG").click()
driver.find_element_by_css_selector("td.idocBtnItm").click()

# Find and switch to frame              
driver.switch_to.frame("MyIndex")

# driver.switch_to_default_content() - after finishing with this frame

wait.until(EC.presence_of_element_located((By.ID, "MyIndex")))
wait.until(EC.presence_of_element_located((By.ID, "Grid___edt_8_7_0_10_0_Association_10_19_1_0_listValue___Img")))

# Choosing Location
driver.find_element_by_id("Grid___edt_8_7_0_10_0_Association_10_19_1_0_listValue___Img").click()
driver.find_element_by_link_text("Chicago").click()

# First Name
driver.find_element_by_id("Grid___edt_8_7_0_10_0_Record_UAA_22_8_textValue").send_keys("Name")

# Last Name
driver.find_element_by_id("Grid___edt_8_7_0_10_0_Record_UAA_23_10_textValue").send_keys("Surname")

# THE LIST OF LIGINS TO CHECK
incorrect_logins = ["john smith", "jöhnsmith", "johnsmïth", "jоhnsmith", "johnсmith", "jänsmith", "ülrichsmith", "çaytest", "Ceskátest", "johnsmith!", "johnsmith,", "johnsmith#", "johnsmith$", "johnsmith%", "johnsmith^", "johnsmith&", "johnsmith*", "johnsmith=", "johnsmith+", "johnsmith?", "johnsmith;", "johnsmith:", "johnsmith<", "johnsmith>", "johnsmith(", "johnsmith)", "johnsmith[", "johnsmith]", "johnsmith{", "johnsmith}"]

# THE LIST OF PASSWORDS TO CHECK
incorrect_password = ["123456a", "12345678", "qwertyu", "333qwerty", "112233nnn", "pässword", "passwörd", "passwörd123", "passwordï123", "passwordü123", "passwоrdn123,", "paссword123", "passwordç123", "päссвöрд132", "johnsmith^", "123 qwerty  321"]

# Start loop test for incorrect symbols in Login
def check_login(login):
    driver.find_element_by_id("Grid___edt_8_7_0_10_0_Record_UAA_9_12_textValue").send_keys(login)
    driver.find_element_by_id("Grid_buttonSend_CMD").click()
    print("Checked - OK")
    print(login)
    time.sleep(3) #Need to wait for some DB load issues may happen on the remote server
    driver.find_element_by_id("MyIndex")
    wait.until(EC.presence_of_element_located((By.ID, "Grid_labelWarnings")))
    driver.find_element_by_id("Grid___edt_8_7_0_10_0_Record_UAA_9_12_textValue").clear() # Clear the input field
[check_login(incorrect_login) for incorrect_login in incorrect_logins]

print("Test for incorrect symbols in Login is finished!")      

driver.find_element_by_id("Grid___edt_8_7_0_10_0_Record_UAA_9_12_textValue").send_keys("testuserlogin3000")

# Start loop test for incorrect symbols in Password
def check_password(password):
    driver.find_element_by_id("Grid___edt_8_7_0_10_0_Record_UAA_27_13_textValue").clear()
    driver.find_element_by_id("Grid___edt_8_7_0_10_0_Record_UAA_27_13_textValue").send_keys(password)
    driver.find_element_by_id("Grid_buttonSend_CMD").click()
    print("Checked - OK")
    print(password)
    driver.find_element_by_id("MyIndex")
    time.sleep(3)
[check_password(incorrect_password) for incorrect_password in incorrect_password]

print("Test for incorrect symbols in Password is finished!")      

driver.quit