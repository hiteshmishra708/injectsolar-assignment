# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import ClearedLogs, UnClearedLogs
from .forms import toDoForm
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import csv

def index(request):
    cleared_logs = ClearedLogs.objects.order_by('id')
    un_cleared_logs = UnClearedLogs.objects.order_by('id')
    form = toDoForm()
    context = {'cleared_logs': cleared_logs, 'un_cleared_logs': un_cleared_logs, 'form': form}
    return render(request,'core/index.html',context)

def get_next_page_data(driver, count):
    data = []
    try:
        xpath = '/html/body/app-root/app-inject-solar/div/div[2]/div[2]/div/app-errore-log/div/div/div[2]/div/div/div/ngb-pagination/ul/li[' + str(count) + ']'
        driver.find_element_by_xpath(xpath).click()
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html)
        table = soup.find("table", {"class":"table table-striped table-bordered"})

        rows = table.findAll('tr')
        data = [[td.findNext(text=True) for td in tr.findAll("td") or tr.findAll("th")] for tr in rows]
        data.pop(0)
    except:
        pass
    return data

def refresh(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(chrome_options=options)

    driver.get('http://www.injectsolar.com/portal/#/')
    user = driver.find_element_by_id('login_id')
    user.send_keys('triose')
    password = driver.find_element_by_id('password')
    password.send_keys('triose123')
    btn = driver.find_element_by_xpath('/html/body/app-root/app-login/div/div/form/div/div[4]/button')
    btn.click() 
    time.sleep(10)
    log_btn = driver.find_element_by_xpath('/html/body/app-root/app-inject-solar/div/div[2]/div[1]/app-header/div[1]/nav/nav/div/ul/li[6]/a/span/i')
    el=driver.find_elements_by_xpath('/html/body/app-root/app-inject-solar/div/div[2]/div[1]/app-header/div[1]/nav/nav/div/ul/li[6]/a')[0]
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(el, 5, 5)
    action.click()
    action.perform()

    clear_alarm = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-inject-solar/div/div[2]/div[2]/div/app-errore-log/div/div/nav/div/a[2]')))
    time.sleep(10)
    clear_alarm.click()
    time.sleep(10)

    driver.find_element_by_id('mat-input-3').send_keys('1/1/2020')
    driver.find_element_by_id('mat-input-4').send_keys('2/29/2020')
    driver.find_element_by_xpath('/html/body/app-root/app-inject-solar/div/div[2]/div[2]/div/app-errore-log/div/div/div[2]/div/div/form/div/div[3]/button[1]').click()
    time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html)
    table = soup.find("table", {"class":"table table-striped table-bordered"})

    rows = table.findAll('tr')

    data = [[td.findNext(text=True) for td in tr.findAll("td") or tr.findAll("th")] for tr in rows]
    data.pop(0)
    count = 4
    while True:
        n_data = get_next_page_data(driver, count)
        if len(n_data) > 0:
            data = data + n_data
            count = count + 1
        else:
            break
    print(data)
    ClearedLogs.objects.all().delete()
    UnClearedLogs.objects.all().delete()
    for i in data:
        log = ClearedLogs.objects.create()
        log.device = i[0]
        log.inverter_name = i[1]
        log.alarm = i[2]
        log.occurance_time = i[3]
        log.clearance_time = i[4]
        log.message = i[5]
        log.save()
    # file = open('data.csv', 'w+', newline ='')
    # # writing the data into the file 
    # with file:     
    #     write = csv.writer(file) 
    #     write.writerows(data)
    driver.close()

    return redirect('index')