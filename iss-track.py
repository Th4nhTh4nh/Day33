import requests
from datetime import datetime
import pytz
import smtplib
import time

MY_EMAIL = "phamdatthanh213@gmail.com"
PASSWORD = "iaojfqjfdmylcdtn"
MY_LAT = 21.027763  # Your latitude
MY_LONG = 105.834160  # Your longitude


def iss_is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if (
        MY_LAT - 5 <= iss_latitude <= MY_LAT + 5
        and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
    ):
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Lay gia tri sunrise va sunset
    sunrise_utc_string = data["results"]["sunrise"]
    sunset_utc_string = data["results"]["sunset"]

    # Chuyen doi sang mui gio VN
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    sunrise_utc = datetime.fromisoformat(sunrise_utc_string)
    sunset_utc = datetime.fromisoformat(sunset_utc_string)
    sunrise_vn = sunrise_utc.astimezone(vn_tz)
    sunset_vn = sunset_utc.astimezone(vn_tz)

    # Dinh dang lai thoi gian
    time_format = "%Y-%m-%d %H:%M:%S"
    sunrise_vn_string = sunrise_vn.strftime(time_format)
    sunset_vn_string = sunset_vn.strftime(time_format)
    # Lay ra gio
    sunrise_hour = int(sunrise_vn_string.split(" ")[1].split(":")[0])
    sunset_hour = int(sunset_vn_string.split(" ")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset_hour or time_now <= sunrise_hour:
        return True


while True:
    time.sleep(60)
    if iss_is_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:LOOK UP\n\nThe ISS is above you in the sky!",
            )
