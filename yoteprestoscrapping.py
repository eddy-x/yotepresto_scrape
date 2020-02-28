import datetime
import requests
from bs4 import BeautifulSoup
import os

#Variables USERNAME and PASSWORD are ENV VARIABLES, please make sure you set them up before running the code

USERNAME = os.environ.get('GMAIL')
PASSWORD = os.environ.get('YTPPASS')

with requests.session() as s:
    #URL yotepresto uses to log in
    url = 'https://www.yotepresto.com/sign_in'
    #yotepresto list of prestamos
    prestar = 'https://www.yotepresto.com/user/requisitions_listings'
    # I was testing how to retrieve my current balance but was not able to find how, the dashboard variable can be used to find out how, SCRAPPING JS methods with python is unknown to me right now
    #dashboard = 'https://www.yotepresto.com/user/dashboard'
    #login_data contains user and password to log in in json format
    login_data = {'sessions[email]': USERNAME, 'sessions[password]': PASSWORD}
    # r = s.get(url)
    #s.post submits the information to log in
    s.post(url, data=login_data)
    #----
    response = s.get(prestar).text
    soup = BeautifulSoup(response, 'lxml')
    #IDs of current available prestamos 
    ids = soup.findAll('td', class_='id')
    #los rates de cada prestamo
    rates = soup.findAll('td', class_='rate')
    #amounts of prestamos
    amounts = soup.findAll('td', class_='amount')
    #terms of the current prestamos
    terms = soup.findAll('td', class_='term')
    #how much money is left to reach the goal of each available prestamo
    faltan = soup.findAll('td', class_='hidden-xs hidden-sm')

    #create 4 empty lists (im sure from this part and forward, the code can be upgraded to a newer and cleaner version)
    idslist = []
    rateslist = []
    amountslist = []
    termslist = []
    faltanlist = []

    #Method to get and append each available prestamo and use the zip built in function to show them in one line
    def yote(list1,list2,list3,list4,list5):
        for i in list1:
            if i.text.strip() == 'Faltan' or i.text.strip() == 'Restan':
                continue
            idslist.append(i.text.strip())
        for i in list2:
            if i.text.strip() == 'Faltan' or i.text.strip() == 'Restan':
                continue
            rateslist.append(i.text.strip())
        for i in list3:
            if i.text.strip() == 'Faltan' or i.text.strip() == 'Restan':
                continue
            amountslist.append(i.text.strip())
        for i in list4:
            if i.text.strip() == 'Faltan' or i.text.strip() == 'Restan':
                continue
            termslist.append(i.text.strip())
        for i in list5:
            if i.text.strip() == 'Faltan' or i.text.strip() == 'Restan':
                continue
            faltanlist.append(i.text.strip())

    # run method
    yote(ids,rates,amounts,terms,faltan)



    # i was trying to add headers but they didnt fit correctly so work in progress, i guess i should add a list with the headers
    # print('ID    ' + ' - ' + 'Interes' + ' - ' + 'Pide' + ' - ' + 'Plazo' + ' - ' + 'Restan')
    if idslist == [] and rateslist == [] and amountslist == [] and termslist == [] and faltanlist == []:
        print('no hay prestamos disponibles')    
    else:
        for i,j,z,a,b in zip(idslist, rateslist, amountslist, termslist, faltanlist):
            print(i + ' - ' + j + ' - ' + z + ' - ' + a + ' - ' + b)

    #adding time to know when was it last run
    dt = datetime.datetime.now()#.time()
    x = dt.strftime("%Y-%m-%d %H:%M:%S")
    print('------------------')
    print('ultimo update: ' + x)