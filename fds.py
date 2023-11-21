from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS
import time
from bs4 import BeautifulSoup
import requests
import re
from flask_socketio import SocketIO
from flask import Flask, request, render_template, jsonify
from threading import Thread, Lock    
from urllib.request import Request, urlopen
import random


urls = ['https://smstome.com/country/denmark', 'https://smstome.com/country/united-kingdom', 'https://smstome.com/country/finland']
app = Flask(__name__)
socketio = SocketIO(app)
codigos = ''
numeros = []
verify = False

CORS(app)
        
@app.route("/")
def teste():
    return render_template('index.html')


@app.route('/driver', methods=['POST'])
def telegram():
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://web.telegram.org/k/")

    try:
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[2]/button[1]')))
        driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[2]/button[1]').click()
    except Exception as e:
        driver.close()
        print(e)
        telegram()
    
    return json('Em Funcionamento!', '')

        
@app.route('/task3', methods=['POST'])
def task():
    try:
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[2]/button[1]')))
        driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[2]/button[1]').click()
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]')))
        driver.execute_script("""
            function getElementByXpath(path) {
                return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            };
            getElementByXpath('/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]').innerHTML = '';
            getElementByXpath('/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]').innerHTML = '%s';
            getElementByXpath('/html/body/div[1]/div/div[2]/div[2]/div/div[3]/button[1]/div').click()
            
        """ % numero)
        return json('Se Conectando ao Número, Aguarde....', '')
    except Exception as e:
        print(e)
        driver.close()
        telegram()
        return json('Em Funcionamento!', '')

    
    


@app.route('/task', methods=['POST'])
def esperarCod():
    driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[4]/div/div[3]/div/input').send_keys(codigos)
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'input-field-input error')))
        time.sleep(30)
        task2(number=-1, tempostr='minutes')
        return json('O código estava incorreto. Tentado novamente...')
    except Exception as e :
        numeros.append(numero)
        

        return json('O driver se conectou ao Telegram com sucesso!')
    

@app.route('/scrape', methods=['POST'])
def scrape():
    global numero
    global tempo
    global link
    
    page = requests.get(random.choice(urls))
    soup = BeautifulSoup(page.text, 'html.parser')
    teste = soup.select('div.column')[1]
    tempo = teste.select('small')[1].text.split()[3]
    numero = teste.find('a').text.split('+')[1]
    link = teste.find('a').get('href')     
    if tempo != 'minute':             
        return json("Não há números novos...", '')
    
    

    return json('Novo número encontrado!!!', '')

                      
@app.route('/task2', methods=['POST'])
def scrape2():
    return task2(number=0, tempostr='minute')                       

        

def task2(number: int , tempostr: str):
    if tempo == tempostr:
        if (numero in numeros) == False:
            page = requests.get(link)
            soup = BeautifulSoup(page.text, 'html.parser')
            tbody = soup.select('table.messagesTable')[0].find('tbody').text.strip() 
            hr = soup.select('table.messagesTable')[0].find('tbody').contents
            valor_a_remover = '\n'
            hr = [x for x in hr if x != valor_a_remover]
            for i in range(10):
                sla = hr[i].text
                if 'TelegXXX' in sla:
                    padrao = r'\d{5}'
                    correspondencias = re.findall(padrao, sla)
                    for codigo in correspondencias:
                        codigos = codigo[number]
                        return json(json='Sms Encontrado!!!', code=int(codigo[0])) 
                    break
                else:
                    return json("Nenhum sms encontrado...", '')
                
     
    
def json(json, code):
    result = {'message': json , 'code': code}
    if 'code' in result and not result['code']:
        result['code'] = 'null'
        return jsonify(result)



if __name__ == '__main__':
   app.run(debug=True)
   
