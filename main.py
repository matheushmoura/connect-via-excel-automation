from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import time

email = input('Digite seu email:')
senha = input('Digite sua senha:')

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

df = pd.read_csv('linkedinmbausp.csv', header=0)
driver.get('https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'username')))
driver.find_element(By.ID, 'username').send_keys(email)
driver.find_element(By.ID, 'password').send_keys(senha)
driver.find_element(By.CSS_SELECTOR, '.btn__primary--large').click()
time.sleep(4)
for item in df.index:
    try:
        conta = df['Linkedin'][item]
        if conta is not None and 'linkedin' in conta:
            conta = "https://www.linkedin.com" + conta.split('linkedin.com')[1]
            driver.get(str(conta))
            try:
                """ Primeira forma de clicar em Conectar """
                WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH,  "//div[@class='pvs-profile-actions ']/button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action']")))
                driver.find_element(By.XPATH, "//div[@class='pvs-profile-actions ']/button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action']").click()
                time.sleep(1)
                WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,  "/html/body/div[3]/div/div/div[3]/button[2]")))
                driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]").click()
                time.sleep(1)
            except:
                try:
                    """ Se não conseguir da primeira forma, tentar a segunda, que é clicando em 'Mais' e depois achar a linha onde está o Conectar """
                    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,  "//div[@class='pvs-profile-actions ']//span[.='Mais']")))
                    driver.find_element(By.XPATH, "//div[@class='pvs-profile-actions ']//span[.='Mais']").click()
                    for x in range(0, 10):
                        try:
                            texto = driver.find_element(By.XPATH, "//div[@class='pvs-profile-actions ']//li[" + str(x) + "]//span[@class='display-flex t-normal flex-1']").text
                            if texto == "Conectar":
                                driver.find_element(By.XPATH, "//div[@class='pvs-profile-actions ']//li[" + str(x) + "]//span[@class='display-flex t-normal flex-1']").click()
                                time.sleep(1)
                                WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,  "/html/body/div[3]/div/div/div[3]/button[2]")))
                                driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]").click()
                                time.sleep(1)
                        except:
                            print('não passou')
                except Exception as e:
                    print('erro', e)
        time.sleep(6)
        """ Diminuição do time.sleep pode ocasionar bloqueios em plataformas """
    except Exception as e:
        print('erro', e)
