import json
import subprocess

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode, urlopen


def api_call(url, args={}):
    URL = url + "?" + urlencode(args)
    print('calling:', URL)
    try:
        response = urlopen(url=URL).read().decode('utf8')
    except:
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
