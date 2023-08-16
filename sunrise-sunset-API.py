import requests
from datetime import datetime
import pytz

# Gửi yêu cầu GET để lấy dữ liệu từ API Sunrise-Sunset.org
url = "https://api.sunrise-sunset.org/json"
parameters = {
    "lat": 21.0285,  # Vĩ độ của Hà Nội
    "lng": 105.8542,  # Kinh độ của Hà Nội
    "formatted": 0,  # Định dạng dữ liệu trả về
}
response = requests.get(url, params=parameters)
response.raise_for_status()
data = response.json()

# Lấy giá trị sunrise và sunset từ dữ liệu
sunrise_utc_string = data["results"]["sunrise"]
sunset_utc_string = data["results"]["sunset"]

# Chuyển đổi sang múi giờ Việt Nam
vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
sunrise_utc = datetime.fromisoformat(sunrise_utc_string)
sunset_utc = datetime.fromisoformat(sunset_utc_string)
sunrise_vn = sunrise_utc.astimezone(vn_tz)
sunset_vn = sunset_utc.astimezone(vn_tz)

print(sunrise_vn)
print(sunset_vn)

# Định dạng lại thời gian theo định dạng mong muốn
time_format = "%Y-%m-%d %H:%M:%S %p"
sunrise_vn_string = sunrise_vn.strftime(time_format)
sunset_vn_string = sunset_vn.strftime(time_format)

test = sunrise_vn_string.split(" ")[1].split(":")[0]
print(test)
# In ra kết quả
print("Giờ mặt trời mọc tại Hà Nội (Việt Nam):", sunrise_vn_string)
print("Giờ mặt trời lặn tại Hà Nội (Việt Nam):", sunset_vn_string)
