from django.shortcuts import redirect, render
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import io
import pytz

APIKEY = "e3338b7f725119db74e8b5e8894544ad"
def getData(lat,lon):
    response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + str(lat) + "&lon=" + str(lon) + "&exclude=minutely&appid=" + APIKEY).json()
    data = {}
    data['current'] = {}
    ST = pytz.timezone(response['timezone'])
    data['current']['time'] = datetime.fromtimestamp(response['current']['dt'],tz=ST).strftime("%I:%M %p")
    data['current']['temp'] = round(response['current']['temp']-273.15,2)
    data['current']['icon'] = response['current']['weather'][0]['icon']
    data['current']['description'] = response['current']['weather'][0]['description']
    data['current']['pressure'] = response['current']['pressure']
    data['current']['humidity'] = response['current']['humidity']
    data['current']['sunrise'] = datetime.fromtimestamp(response['current']['sunrise']).strftime("%I:%M %p")
    data['current']['sunset'] = datetime.fromtimestamp(response['current']['sunset']).strftime("%I:%M %p")
    data['current']['clouds'] = response['current']['clouds']
    data['current']['wind_speed'] = response['current']['wind_speed']
    data['daily'] = []
    for i in range(6):
        day = {}
        day['weekday'] = datetime.fromtimestamp(response['daily'][i]['dt']).strftime("%A")
        day['max_temp'] = round(response['daily'][i]['temp']['max']-273.15,2)
        day['min_temp'] = round(response['daily'][i]['temp']['min']-273.15,2)
        day['icon'] = response['daily'][i]['weather'][0]['icon']
        day['description'] = response['daily'][i]['weather'][0]['description']
        day['pressure'] = response['daily'][i]['pressure']
        day['humidity'] = response['daily'][i]['humidity']
        day['sunrise'] = datetime.fromtimestamp(response['daily'][i]['sunrise']).strftime("%I:%M %p")
        day['sunset'] = datetime.fromtimestamp(response['daily'][i]['sunset']).strftime("%I:%M %p")
        day['clouds'] = response['daily'][i]['clouds']
        day['wind_speed'] = response['daily'][i]['wind_speed']
        data['daily'].append(day)
    x = []
    y = []
    data['hourly'] = []
    for i in range(24):
        hour = {}
        hour['time'] = datetime.fromtimestamp(response['hourly'][i]['dt'],tz=ST).strftime("%I:%M %p")
        x.append(datetime.fromtimestamp(response['hourly'][i]['dt'],tz=ST).strftime("%I:%M %p"))
        hour['temp'] = round(response['hourly'][i]['temp']-273.15,2)
        y.append(round(response['hourly'][i]['temp']-273.15,2))
        hour['icon'] = response['hourly'][i]['weather'][0]['icon']
        hour['description'] = response['hourly'][i]['weather'][0]['description']
        data['hourly'].append(hour)
    fig = plt.figure(facecolor='lightgray')
    fig.set_figwidth(12)
    ax = plt.axes()
    ax.set_facecolor("lightgray")
    ax.figure.autofmt_xdate()
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    plt.plot(x,y,color='black',marker='.')
    plt.xlabel("Time (next 24 hours)")
    plt.ylabel("Temperature (in celsius)")
    plt.title("")
    imgdata = io.StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data['graph'] = imgdata.getvalue()
    return data
def home(request):
    if request.method == 'POST':
        loc = request.POST['location']
        response = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + loc + '&limit=1&appid=' + APIKEY).json()
        lat = response[0]['lat']
        lng = response[0]['lon']
        return redirect('userlocation',lat,lng)
    else:
        return render(request,'index.html')
def userlocation(request,lat,lng):
    response = requests.get('http://api.openweathermap.org/geo/1.0/reverse?lat=' + lat + '&lon=' + lng + '&limit=1&appid=' + APIKEY).json()
    data = getData(lat,lng)
    data['address'] = response[0]['name'] + ', ' + response[0]['state'] + ', ' + response[0]['country']
    return render(request,'index.html', data)
def aboutus(request):
    return render(request,'aboutus.html')