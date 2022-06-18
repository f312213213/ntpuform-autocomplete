from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import os

StudentId = '410874230'
StudentPasswd = 'David-04190975'

os.chmod('./msedgedriver', 0o755)
ser = Service('./msedgedriver')
op = webdriver.EdgeOptions()
driver = webdriver.Edge(service=ser, options=op)

# driver = webdriver.Edge(executable_path='/Users/david/Downloads/edgedriver_arm64/msedgedriver.exe')


driver.get("https://cof.ntpu.edu.tw/student_new.htm")

input_name = driver.find_element(By.NAME, 'stud_num')
input_pwd = driver.find_element(By.NAME, 'passwd')

input_name.send_keys(StudentId)
input_pwd.send_keys(StudentPasswd)

login_btn = driver.find_element(By.ID, 'loginBtn1')
login_btn.click()

driver.get("https://cof.ntpu.edu.tw/pls/univer/query_all_course.judge?year1=110")
tr = driver.find_elements(By.XPATH, '//table[1]/tbody/tr')

formDriver = webdriver.Chrome(service=ser, options=op)
formDriver.get("https://cof.ntpu.edu.tw/student_new.htm")
input_name = formDriver.find_element(By.NAME, 'stud_num')
input_pwd = formDriver.find_element(By.NAME, 'passwd')
login_btn = formDriver.find_element(By.ID, 'loginBtn1')
input_name.send_keys(StudentId)
input_pwd.send_keys(StudentPasswd)
login_btn.click()
formDriver.get("https://cof.ntpu.edu.tw/pls/univer/query_all_course.judge?year1=110")

for index, classData in enumerate(tr):
    if index == 0:
        pass
    else:
        classNum = classData.find_element(By.XPATH, '//tr['+str(index+1)+']/td[1]')
        classID = classData.find_element(By.XPATH, '//tr['+str(index+1)+']/td[2]')
        className = classData.find_element(By.XPATH, '//tr['+str(index+1)+']/td[3]')
        classTeacher = classData.find_element(By.XPATH, '//tr['+str(index+1)+']/td[4]')
        classType = classData.find_element(By.XPATH, '//tr['+str(index+1)+']/td[5]')
        classStatus = classData.find_element(By.XPATH, '//tr['+str(index+1)+']/td[6]')
        if classStatus.text == '尚未填寫':
            # print('由 ' + classTeacher.text + ' 老師開的 ' + classType.text + ' 修課程：' + classNameAndLink.text + ' 問卷還沒填寫過。')
            classLink = className.find_element(By.TAG_NAME, 'a')
            formDriver.get(classLink.get_attribute('href'))
            # 進到問卷系統
            formDriver.find_element(By.XPATH, '/html/body/center/form/center[1]/table[1]/tbody/tr[4]/th[2]/input[@type="radio"]').click()
            form_tr = formDriver.find_elements(By.XPATH, '/html/body/center/form/center[1]/table[2]/tbody/tr')
            for index_in, clickable_tr in enumerate(form_tr):
                if index_in in [0, 1, 2, 17, 18, 19, 20, 24]:
                    pass
                elif index_in in [6, 13]:
                    clickable_tr.find_element(By.XPATH, '/html/body/center/form/center[1]/table[2]/tbody/tr['+str(index_in+1)+']/th[6]/input[@type="radio"]').click()
                elif index_in == 27:
                    clickable_tr.find_element(By.XPATH, '/html/body/center/form/center[1]/table[2]/tbody/tr['+str(index_in+1)+']/th[1]/div/input[1][@type="checkbox"]').click()
                    clickable_tr.find_element(By.XPATH, '/html/body/center/form/center[1]/table[2]/tbody/tr[' + str(
                        index_in + 1) + ']/th[1]/div/input[2][@type="checkbox"]').click()
                elif index_in in [28, 29]:
                    clickable_tr.find_element(By.XPATH, '/html/body/center/form/center[1]/table[2]/tbody/tr[' + str(
                        index_in + 1) + ']/th[1]/div/input[2][@type="radio"]').click()
                elif index_in == 30:
                    clickable_tr.find_element(By.XPATH, '/html/body/center/form/center[1]/table[2]/tbody/tr[' + str(
                        index_in + 1) + ']/th[1]/div/input[4][@type="radio"]').click()
                else:
                    clickable_tr.find_element(By.XPATH, '/html/body/center/form/center[1]/table[2]/tbody/tr['+str(index_in+1)+']/th[2]/input[@type="radio"]').click()
            formDriver.find_element(By.XPATH, '/html/body/center/form/center[2]/table/tbody/tr[2]/td/textarea').send_keys('謝謝老師！')
            try:
                formDriver.find_element(By.XPATH, '/html/body/center/form/center[2]/table[2]/tbody/tr/td/b/input[4]').click()
                formDriver.find_element(By.XPATH, '/html/body/center/form/center[2]/input').click()
            except:
                formDriver.find_element(By.XPATH, '/html/body/center/form/center[2]/input[2]').click()
            formDriver.switch_to.alert.accept()
            print('由 ' + classTeacher.text + ' 老師開的 ' + classType.text + ' 修課程：' + className.text + ' 問卷填寫完成。')
        else:
            print('由 '+classTeacher.text+' 老師開的 '+classType.text+' 修課程：'+className.text+' 問卷已經填寫過。')
formDriver.close()
driver.close()
