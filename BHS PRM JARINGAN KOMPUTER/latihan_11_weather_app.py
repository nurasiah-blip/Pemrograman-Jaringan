import requests # type: ignore
import sy # type: ignore

def get_weather(city_name, lat, lon):
    print(f"\n--- Mengambil Data Cuaca untuk {city_name} ---")

    # 1. Definisikan URL dan Parameter
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'timezone': 'auto' # Agar jam sesuai lokasi
    }

    try:
        # 2. Kirim Request GET
        # requests.get otomatis menyusun query string (?lat=...&lon=...)
        response = requests.get(base_url, params=params)

        # 3. Cek Status Code
        if response.status_code == 200:
            # 4. Parsing JSON
            data = response.json()

            # Ambil bagian yang penting saja
            current = data['current_weather']
            suhu = current['temperature']
            kecepatan_angin = current['windspeed']

            print(f"🌡️  Suhu Saat Ini: {suhu}°C")
            print(f"💨 Kecepatan Angin: {kecepatan_angin} km/h")
            print(f"🌍 Koordinat: {lat}, {lon}")

        else:
            print(f"[ERROR] Gagal mengambil data. Status: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("[ERROR] Tidak ada koneksi internet!")
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    # Koordinat Jakarta
    get_weather("Jakarta", -6.2088, 106.8456)

    # Koordinat Makassar
    get_weather("Makassar", -5.1477, 119.4327)