from bs4 import BeautifulSoup as bs
import requests


def addZero(val):
    res = str(val)
    if len(res) == 1:
        res = '0' + str(val)
    return res

def IsLeap(year):
    if year % 4 != 0 or (year % 100 == 0 and year % 400 != 0):
        return False
    else:
        return True

def prevDate(date):
    #Вычитаем 1 день
    date[2] = addZero( int(date[2])-1 )
    #Наступил пред. месяц
    if date[2] == '00':
        date[1] = addZero( int(date[1])-1 )
        #В этом месяце 31 день
        if date[1] in more_days:
            date[2] = '31'
        #В этом месяце 30 дней
        elif date[1] in less_days:
            date[2] = '30'
        #Это февраль ._.
        else:
            #Високосный год
            if IsLeap( int(date[0]) ) == True:
                date[2] = '29'
            #Невисокосный год
            else:
                date[2] = '28'
    #Наступил пред. год
    if date[1] == '00':
        date[1] = '12'
        date[0] = str( int(date[0])-1 )
        date[2] = '31'

    #И, наконец, мы возвращаем измененную дату
    return date


def makelink(date):
    Url = 'https://www.anekdot.ru/release/anekdot/day/{}-{}-{}/'.format( date[0], date[1], date[2] )
    return Url


#Сам парсер
def parselink(url):
    URL = url
    HEADERS = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    response = requests.get(URL, headers = HEADERS)
    soup = bs(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'text')

    for i in items:
        print(i.text + '\n')


#Запуск парсера
def parse(quantity = 1):
    if quantity > 0:
        for i in range(quantity):
            link = makelink( prevDate(date) )
            print('\n'*7 + link + '\n'*7)
            parselink(link)
    else:
        while True:
            link = makelink( prevDate(date) )
            print('\n'*7 + link + '\n'*7)
            parselink(link)



#Получаем дату
year = addZero(input('Год: '))
month = addZero(input('Месяц: '))
day = addZero(input('День: '))

#Формируем дату как список
date = [year, month, day]

#31 или 30 дней в месяце
more_days = ['01', '03', '05', '07', '08', '10', '12']
less_days = ['04', '06', '09', '11']


#Кол-во страниц
quant = int(input('Количество страниц (0 для бесконечности): '))
parse(quant)
