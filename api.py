import json
import subprocess
import sublime

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
        sublime.error_message(response['error'])
        if args.get('loader', None):
            args['loader'].done = True
        return False

    return response
