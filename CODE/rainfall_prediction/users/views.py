from django.conf import settings
from django.shortcuts import render
# from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import UserRegistrationModel
import pandas as pd
import requests


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have  successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Exists')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('password')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account has not been activated by Admin.')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHome.html', {})


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

        # print(temp_high, temp_low, temp_avg, dew_point_high, dew_point_low, dew_point_avg,
        #       humidity_low, humidity_avg, humidity_high, sea_level_pressure_avg_inches,
        #       visibility_avg, visibility_low, visibility_high, wind_avg, wind_high, wind_gust, sep='\n')
        #
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
        return render(request, 'users/ml.html', {'result': f"The precipitation in inches for the input is:{result}"})
        # return render(request, 'users/prediction.html')


    else:
        # return render(request, 'users/prediction.html')
        return render(request, 'users/ml.html')


def dataset(request):
    dataset_url = settings.DATASET_URL
    data = pd.read_csv(dataset_url)
    context = {
        'data': data.to_html(
            index=False,
            classes=['table table-striped table-bordered table-hover table-sm']
        ).replace('<tr style="text-align: right;">', '<tr>')
    }

    return render(request, 'users/view_data.html', context)


def ann(request):
    from .utility import artificial_neural_network as ann
    print('Lets print the results... ')
    regressor = ann.build_regressor()
    # Evaluate Loss (Mean Squared Error), Mean Absolute Error, Accuracy,
    regressor_results = regressor.evaluate(ann.X_test, ann.y_test)
    print("*************** Regressor Result ***************")

    loss = regressor_results[0]
    mae = regressor_results[1]
    accuracy = regressor_results[2]
    print('__LOSS__:', loss)
    print('__MAE__:', mae)
    print('__ACCURACY__:', accuracy)

    context = {
        'loss': loss,
        'mae': mae,
        'accuracy': accuracy
    }
    return render(request, 'users/ann.html', context)


def mlr(request):
    from .utility.ml import mae_mse_r2_score
    result = mae_mse_r2_score()

    context = {
        'mean_absolute_error': result[0],
        'mean_squared_error': result[1],
        'r2_score': result[2]
    }

    return render(request, 'users/mlr.html', context)


def get_weather(request):
    """
    Fetches live weather details from OpenWeatherMap API.

    Args:
        request: The Django request object.

    Returns:
        A rendered HTML template with weather data or an error message.
    """

    api_key = getattr(settings, "OPENWEATHERMAP_API_KEY", None) #Retrieve the API key from settings.py
    city = request.GET.get('city', 'London')  # Default city if none provided

    if not api_key:
        return render(request, 'users/weather.html', {'error': 'API key not configured.'})

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"  # Use metric units

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        weather_data = response.json()
        data = {
            'imageurl' : get_city_image(city),
            'city': weather_data['name'],
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],  # Add feels_like
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'icon': weather_data['weather'][0]['icon'],
            'icon_url': f"http://openweathermap.org/img/w/{weather_data['weather'][0]['icon']}.png",
        }
        print("=============================================================================================")
        print("=============================================================================================")
        print("=============================================================================================")
        print("=============================================================================================")
        print("hit:", data)
        return render(request, 'users/weather.html', data)

    except requests.exceptions.RequestException as e:
        return render(request, 'users/weather.html', {'error': f'Error fetching weather data CHECK YOUR CITY'})
    except (KeyError, ValueError, TypeError) as e: # Catch json parsing errors, and key errors
      return render(request, 'users/weather.html', {'error': f'Error processing weather data: {e}'})
    except Exception as e: #Catch any other error
      return render(request, 'users/weather.html', {'error': f'An unexpected error occured: {e}'})
  
  
  

def get_city_image(city_name):
    api_key = "knfdknb"
    """
    Retrieves an image URL of an iconic place in a given city.

    Args:
        city_name: The name of the city.
        api_key: Your Google Places API key.

    Returns:
        A URL to an image, or None if an error occurs.
    """
    try:
        # Geocoding to get city coordinates
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={api_key}"
        geocode_response = requests.get(geocode_url).json()

        if geocode_response["status"] == "OK":
            location = geocode_response["results"][0]["geometry"]["location"]
            lat, lng = location["lat"], location["lng"]

            # Places API to find iconic places
            places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=15000&type=tourist_attraction&key={api_key}" # can also use landmark, point_of_interest
            places_response = requests.get(places_url).json()

            if places_response["status"] == "OK" and places_response["results"]:
                place_id = places_response["results"][0]["place_id"] # Get first result
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=photos&key={api_key}"
                details_response = requests.get(details_url).json()

                if details_response["status"] == "OK" and "photos" in details_response["result"]:
                    photo_reference = details_response["result"]["photos"][0]["photo_reference"]
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_reference}&key={api_key}"
                    return photo_url
                else:
                    return None #No photos found.
            else:
                return None #No places found.
        else:
            return None #Geocoding failed.

    except Exception as e:
        print(f"An error occurred: {e}")
        return None