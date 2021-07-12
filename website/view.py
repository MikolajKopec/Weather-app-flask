from flask import render_template,request
from flask.blueprints import Blueprint
from flask.helpers import flash
import json, urllib.request

API_KEY = '####GET_API_CODE#####'
LANG = 'PL'


view = Blueprint('view',__name__)

@view.route('/',methods = ['POST','GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        city = request.form.get('city')
        city = city.capitalize()
        acc_city = city.replace('ł','l').replace('ó','o').replace('ą','a').replace('ś','s').replace('ż','z').replace('ź','z').replace('ń','n').replace('ę','e')
        try:
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + acc_city + '&appid='+API_KEY).read()
        except:
            flash("Podane miasto nie istnieje. Spróbuj ponownie.", category='error')
            return render_template('index.html')
        data_list = json.loads(source)
        if(LANG == 'PL'):
            cc = "Kraj"
            temp = "Temperatura"
            weather = "Pogoda"
        kelvin = int(data_list['main']['temp'])
        celcius = (kelvin-273.15)
        data ={
            cc:str(data_list['sys']['country']),
            temp:format(celcius,'.0f'),
            weather:str(data_list['weather'][0]['description']),
            'icon':str(data_list['weather'][0]['icon']),
            'card_style':str(data_list['weather'][0]['main'])
        }
        print(data)
        return render_template('index.html',data = data, city = city) 
