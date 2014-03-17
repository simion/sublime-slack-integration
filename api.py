import json
import subprocess
import sublime

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode, urlopen


def api_call(url, args={}):

    file_path = None

    file_path = args.get('file', None)
    if file_path:
        del(args['file'])

    URL = url + "?" + urlencode(args)
    print('calling:', URL)
    try:
        if file_path:
            response = urlopen(
                url=URL,
                data={'file': file_path}
            ).read().decode('utf8')
        else:
            response = urlopen(url=URL).read().decode('utf8')
    except:
        # fallback for sublime bug with urlopen (on linux only)
        if file_path:  # upload file
            proc = subprocess.Popen(
                ['curl', '-X', 'POST', '-F', 'file=@'+file_path, URL],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen(
                ['curl', '-s', URL],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        out, err = proc.communicate()

        response = out.decode('utf8')

    response = json.loads(response)

    if not response['ok']:
        sublime.error_message("SLACK Api error: " + response['error'])
        if args.get('loading', None):
            args['loading'].done = True
        return False

    return response
