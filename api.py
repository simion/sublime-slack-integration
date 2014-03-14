import json
import subprocess

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode, urlopen


def api_call(url, args={}):
    try:
        response = urlopen(url=url + "?{0}".format(urlencode(args))).read().decode('utf8')
    except:
        URL = url + "?" + urlencode(args)
        print('calling:', URL)
        proc = subprocess.Popen(
            ['curl', '-s', URL],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = proc.communicate()

        response = out.decode('utf8')

    response = json.loads(response)
    if not response['ok']:
        print(response['error'])
        return False

    return response
