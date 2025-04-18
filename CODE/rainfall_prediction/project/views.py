from django.shortcuts import render
import requests
from django.conf import settings
from users.forms import UserRegistrationForm
from django.http import FileResponse
import os

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def logout(request):
    return render(request, 'index.html', {})

def UserLogin(request):
    return render(request, 'UserLogin.html', {})

def UserRegister(request):
    form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})

def AdminLogin(request):
    return render(request, 'AdminLogin.html', {})

def learn_more(request):
    filepath = os.path.join('static/pdf', 'rainfall.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

def ml(request):
    if request.method == 'POST':
        temp_high = int(request.POST.get('temp_high'))
        temp_avg = int(request.POST.get('temp_avg'))
        temp_low = int(request.POST.get('temp_low'))
        dew_point_high = int(request.POST.get('dew_point_high'))
        dew_point_avg = int(request.POST.get('dew_point_avg'))
        dew_point_low = int(request.POST.get('dew_point_low'))
        humidity_high = int(request.POST.get('humidity_high'))
        humidity_avg = int(request.POST.get('humidity_avg'))
        humidity_low = int(request.POST.get('humidity_low'))
        sea_level_pressure_avg_inches = float(request.POST.get('sea_level_pressure_avg_inches'))
        visibility_high = int(request.POST.get('visibility_high'))
        visibility_avg = int(request.POST.get('visibility_avg'))
        visibility_low = int(request.POST.get('visibility_low'))
        wind_high = int(request.POST.get('wind_high'))
        wind_avg = int(request.POST.get('wind_avg'))
        wind_gust = int(request.POST.get('wind_gust'))

        from .utility.ml import do_prediction
        result = do_prediction(
            temp_high=temp_high,
            temp_avg=temp_avg,
            temp_low=temp_low,
            dew_point_high=dew_point_high,
            dew_point_avg=dew_point_avg,
            dew_point_low=dew_point_low,
            humidity_high=humidity_high,
            humidity_avg=humidity_avg,
            humidity_low=humidity_low,
            sea_level_pressure_avg_inches=sea_level_pressure_avg_inches,
            visibility_high=visibility_high,
            visibility_avg=visibility_avg,
            visibility_low=visibility_low,
            wind_high=wind_high,
            wind_avg=wind_avg,
            wind_gust=wind_gust,
        )

        city = "Ongole"  # Assuming you want data for Ongole, or make this dynamic
        api_key = settings.OPENWEATHERMAP_API_KEY
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()

            live_temperature = weather_data['main']['temp']
            live_humidity = weather_data['main']['humidity']
            live_pressure = weather_data['main']['pressure']
            live_wind_speed = weather_data['wind']['speed']

            context = {
                'result': f"The precipitation in inches for the input is: {result}",
                'live_temperature': live_temperature,
                'live_humidity': live_humidity,
                'live_pressure': live_pressure,
                'live_wind_speed': live_wind_speed,
            }
        except requests.exceptions.RequestException as e:
            context = {
                'result': f"The precipitation in inches for the input is: {result}",
                'api_error': f"Error fetching weather data: {e}"
            }
        except KeyError as e:
            context = {
                'result': f"The precipitation in inches for the input is: {result}",
                'api_error': f"Error parsing weather data: {e}"
            }

        return render(request, 'users/ml.html', context)
    else:
        return render(request, 'users/ml.html')
