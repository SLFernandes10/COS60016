import json
import requests
import sqlite3

def main(city):
    # securely obtain API key
    file = open('services/key.txt', 'r')
    key = file.read()
    file.close()

    # check response
    response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat=0&lon=0&appid={key}')
    if response.status_code != 200:
        forecast = f"Error {response.status_code}, unable to connect to the weather database. Please try again later."
        return(forecast)
        exit()

    # dictionary of locations and coordinates (as tuples)
    locations = {
        'cumbria': ('54.4609', '-3.0886'),
        'corfe': ('50.6395', '-2.0566'),
        'cotswolds': ('51.8330', '-1.8433'),
        'cambridge': ('52.2053', '0.1218'),
        'bristol': ('51.4545', '-2.5879'),
        'oxford': ('51.7520', '-1.2577'),
        'norwich': ('52.6309', '1.2974'),
        'stonehenge': ('51.1789', '-1.8262'),
        'watergate': ('50.4429', '-5.0553'),
        'birmingham': ('52.4862', '-1.8904')
    }

    select_city = city

    # retrieve coordinates from dictionary and separate strings
    latlon = locations[select_city]
    lat, lon = latlon

    # API call and data formatting
    forecast = (requests.get
                (f'https://api.openweathermap.org/data/3.0/onecall?units=metric&lat={lat}&lon={lon}&appid={key}'))
    content = json.loads(forecast.text)['daily']

    #pull desired data from api call and place into lists for 5 day forecast
    days = {
        'day1': content[0],
        'day2': content[1],
        'day3': content[2],
        'day4': content[3],
        'day5': content[4]
    }

    def get_max_temp(day):
        temp = day['temp']
        max_temp = temp['max']
        return(max_temp)

    max_temp = []
    for x in days:
        max_temp.append(get_max_temp(days[x]))

    def get_min_temp(day):
        temp = day['temp']
        min_temp = temp['min']
        return(min_temp)

    min_temp = []
    for x in days:
        min_temp.append(get_min_temp(days[x]))

    def get_values(d, v):
        value = d[v]
        return(value)

    humidity = []
    for x in days:
        humidity.append(get_values(days[x], 'humidity'))

    uvi = []
    for x in days:
        uvi.append(get_values(days[x], 'uvi'))

    summary = []
    for x in days:
        summary.append(get_values(days[x], 'summary'))

    def add_to_db(max_temp, min_temp, humidity, uvi, summary):
        con = sqlite3.connect("weather.db")
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS data")
        cur.execute("CREATE TABLE data (max_temp TEXT, min_temp TEXT, humidity TEXT, uvi TEXT, summary TEXT)")
        entry = [max_temp, min_temp, humidity, uvi, summary]
        transposed_entry = list(zip(*entry))
        for row in transposed_entry:
            cur.execute("INSERT INTO data (max_temp, min_temp, humidity, uvi, summary) VALUES (?, ?, ?, ?, ?)", row)
        con.commit()
        #close db to conserve system resources
        con.close()
        return

    def pull_from_db():
        con = sqlite3.connect("weather.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM data")
        rows = cur.fetchall()
        con.close()
        forecast = {
            'today': rows[0],
            'tomorrow': rows[1],
            'in 2 days': rows[2],
            'in 3 days': rows[3],
            'in 4 days': rows[4]
        }
        return(forecast)

    add_to_db(max_temp, min_temp, humidity, uvi, summary)

    forecast = pull_from_db()
    return(forecast)