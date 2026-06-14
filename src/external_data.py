import requests

def get_current_utc_time():

    try:

        response = requests.get(
            "https://worldtimeapi.org/api/timezone/Etc/UTC",
            timeout=5
        )

        data = response.json()

        return data.get(
            "datetime",
            "Unavailable"
        )

    except Exception:

        return "Unavailable"