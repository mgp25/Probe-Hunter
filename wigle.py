import requests, json

class Wigle:

    AUTH            = ''
    ENDPOINT_SEARCH = 'https://api.wigle.net/api/v2/network/search'

    def wigle_location(ssid, wigle_flag):
        headers = {
            'accept': 'application/json',
            'authorization': Wigle.AUTH
            }
        payload = {
            'onlymine': False,
            'first': 0,
            'freenet': False,
            'paynet': False,
            'ssid': ssid
        }
        if Wigle.AUTH == '':
            return 1
        try:
            r = requests.get(Wigle.ENDPOINT_SEARCH, headers=headers, params=payload)
        except:
            return 1
        res = json.loads(r.text)
        if 'message' in res:
            if res['message'] == 'too many queries today':
                return 1
        if not wigle_flag:
            if len(res['results']) > 4:
                return 2
            else:
                try:
                    return res['results'][-1]
                except:
                    return None
        else:
            return None
