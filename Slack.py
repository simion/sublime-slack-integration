import sublime
import sublime_plugin
import threading
from os.path import isfile

from .api import api_call
from .loader import Loader

# methods
API_CHANNELS = 'channels.list'
API_USERS = 'users.list'
API_GROUPS = 'groups.list'
API_POST_MESSAGE = 'chat.postMessage'
API_UPLOAD_FILES = 'files.upload'
API_OPEN_IM_SESSION = 'im.open'
API_CLOSE_IM_SESSION = 'im.close'


class BaseSend(sublime_plugin.TextCommand):
    """ Base class which shows a channels list and sends messages """

    def __init__(self, view):
        super(BaseSend, self).__init__(view)
        # here we will store all messages
        self.messages = []
        self.last_receiver = None

        # this channels list is only populated once, per sublime session
        # you need to restart sublime to re-take channels from API
        self.receivers = []

        # load plugin settings
        self.settings = sublime.load_settings("Slack.sublime-settings")

    def _api_call(self, *args, **kwargs):
        if args[0] == API_POST_MESSAGE:
            kwargs['icon'] = self.settings.get('avatar_url')
        return api_call(*args, **kwargs)

    def run(self, view):
        # load settings each time a command is ran
        self.settings = sublime.load_settings("Slack.sublime-settings")
        # reset older messages stored in memory
        self.messages = []
        # check if token is set
        if not self.settings.get('team_tokens'):
            sublime.error_message('SLACK Error: Please set your API "team_tokens" in Preferences -> Package Settings -> Slack -> Settings - User')
            raise Exception('Team Token missing')

    def on_select_receiver(self, index):
        """ Triggered after a received is selected from the quick_panel """
        # start in a new thread, otherwise quick_panel is stuck
        threading.Thread(
            target=self.send_messages,
            args=(index, )).start()

    def send_messages(self, index):
        if index is -1:
            return

        receiver = self.receivers[index]
        token = receiver.get('token')

        username = self.settings.get('username')

        info = ''

        subtext = self.settings.get('username_subtext')
        if subtext and subtext is not None:
            info = "({0})".format(subtext)
        elif self.settings.get('show_plaform_and_name'):
            info = sublime.platform()
            try:
                import getpass
                info = "{0}, {1}".format(getpass.getuser(), info)
            except:
                # cannot get current OS user
                pass
            info = "({0})".format(info)

        loading = Loader('Sending message ...')

        channel = receiver.get('id')
        channel_needs_closing = False

        if receiver.get('type') == 'user':
            session_open_response = self._api_call(API_OPEN_IM_SESSION, {
                'token': token,
                'user': channel
            })
            # print(session_open_response)
            if not session_open_response.get('ok'):
                loading.done = True
                sublime.status_message('SLACK: Unexpected error!')
                return

            if not session_open_response.get('already_open'):
                channel_needs_closing = True

            im_channel = session_open_response.get('channel')
            if im_channel and im_channel.get('id'):
                channel = im_channel.get('id')

        for message in self.messages:
            args = {
                'token': token,
                'channel': channel,
                'text': message,
                'username': "{0} {1}".format(username, info)
            }
            response = self._api_call(API_POST_MESSAGE, args)
            loading.done = True
            if response['ok']:
                sublime.status_message('SLACK: Message sent successfully!')
                # set recipient for next autocomplete
                self.next_input_val = self.get_receiver_display(receiver)
            else:
                sublime.status_message('SLACK: Unexpected error!')

        if channel_needs_closing:
            self._api_call(API_CLOSE_IM_SESSION, {
                'token': token,
                'channel': channel
            })
        loading.done = True

    def init_message_send(self):
        # check is channels are cached in memory
        receivers = []
        if not self.receivers:
            # get the channels and users for each team
            loading = Loader('Loading channels/users/groups')
            for team, token in self.settings.get('team_tokens').items():
                channels_response = self._api_call(API_CHANNELS, {
                    'token': token,
                    'exclude_archived': 1
                }, loading=loading)
                for channel in channels_response['channels']:
                    # bind the token and team to the channel
                    channel['token'] = token
                    channel['team'] = team
                    channel['type'] = 'channel'
                    self.receivers.append(channel)

                groups_response = self._api_call(API_GROUPS, {
                    'token': token,
                    'exclude_archived': 1
                }, loading=loading)
                for group in groups_response['groups']:
                    # bind the token and team to the group
                    group['token'] = token
                    group['team'] = team
                    group['type'] = 'group'
                    self.receivers.append(group)

                users_response = self._api_call(API_USERS, {
                    'token': token
                }, loading=loading)
                for user in users_response['members']:
                    if not user['deleted']:
                        # bind the token and team to the user
                        user['token'] = token
                        user['team'] = team
                        user['type'] = 'user'
                        self.receivers.append(user)
            # loading done, remove status message
            loading.done = True

        # check if the message begins with #channel or @user, and if receiver exists
        if self._must_send_directly():
            return self.send_messages(self.forced_receiver_index)

        # create receivers dropdown
        for receiver in self.receivers:
            if receiver['type'] is 'channel':
                item = "# {0}".format(receiver['name'])
            elif receiver['type'] is 'group':
                item = "● {0}".format(receiver['name'])
            else:  # is user
                item = "@ {0}".format(receiver['name'])
            if len(self.settings.get('team_tokens')) > 1:
                item += "({0})".format(receiver['team'])
            receivers.append(item)

        # display a popup and let the user pick a channel
        self.view.window().show_quick_panel(
            receivers,
            self.on_select_receiver)

    def get_receiver_display(self, receiver):
        pre = ''
        if receiver['type'] == 'user':
            pre = '@'
        elif receiver['type'] == 'channel':
            pre = '#'
        elif receiver['type'] == 'group':
            pre = '.'
        else:
            return ''

        return "{0}{1} ".format(pre, receiver['name'])

    def _must_send_directly(self):
        """ Checks if the message from input box begins with @user #channel .group  """
        if len(self.messages) > 1 or not self.messages:
            return False
        msg = self.messages[0]
        # check if user
        if msg.startswith('@'):
            user = msg[1:msg.find(' ')]
            # check if the user exists in recipients list
            for index, receiver in enumerate(self.receivers):
                if receiver['type'] is 'user' and receiver['name'] == user:
                    self.messages[0] = self.messages[0].replace('@'+user, '', 1)
                    self.forced_receiver_index = index
                    return True

        # check if channel
        if msg.startswith('#'):
            channel = msg[1:msg.find(' ')]
            # check if the user exists in recipients list
            for index, receiver in enumerate(self.receivers):
                if receiver['type'] is 'channel' and receiver['name'] == channel:
                    self.messages[0] = self.messages[0].replace('#'+channel, '', 1)
                    self.forced_receiver_index = index
                    return True

        # check if group
        if msg.startswith('.'):
            group = msg[1:msg.find(' ')]
            # check if the user exists in recipients list
            for index, receiver in enumerate(self.receivers):
                if receiver['type'] is 'group' and receiver['name'] == group:
                    self.messages[0] = self.messages[0].replace('.'+group, '', 1)
                    self.forced_receiver_index = index
                    return True

        return False


class SendSelectionCommand(BaseSend):
    """ Send the selected text to slack. Multiple selections supported """
    def run(self, view):
        super(SendSelectionCommand, self).run(view)
        # get all selected regions
        for region in self.view.sel():
            text = self.view.substr(region)

            if not text:
                sublime.error_message("SLACK Error: No text selected")
                return
            self.messages.append("```{0}```".format(text))

        threading.Thread(target=self.init_message_send).start()


class SendMessageCommand(BaseSend):
    """ Send a message from user input """

    def run(self, view):
        super(SendMessageCommand, self).run(view)

        ac = ''
        if hasattr(self, 'next_input_val'):
            ac = self.next_input_val
            del(self.next_input_val)

        self.view.window().show_input_panel(
            "Slack: Enter a message", ac, self.on_done, None, None)

    def on_done(self, message):
        if not message:
            return sublime.error_message('ERROR: Please enter a message')
        self.messages = [message]
        threading.Thread(target=self.init_message_send).start()


class UploadCurrentFileCommand(BaseSend):
    """ Uploads the current file (active tab)  """

    def run(self, view):
        super(UploadCurrentFileCommand, self).run(view)

        self.file = self.view.file_name()
        if not self.file:
            return sublime.error_message('SLACK: No file open')
        threading.Thread(target=self.init_message_send).start()

    def on_select_receiver(self, index):
        if index == -1:
            return
        if self.receivers[index]['type'] == 'user':
            return sublime.error_message('Slack: sending files to users is disabled for the moment.\nHowever, you can send files to channels/groups.')
        threading.Thread(target=self.upload_file, args=(index,)).start()

    def upload_file(self, receiver_index):
        receiver = self.receivers[receiver_index]
        loading = Loader('Uploading file ...', False)

        self._api_call(API_UPLOAD_FILES, {
            'token': receiver.get('token'),
            'channels': receiver.get('id'),
            'filename': self.friendly_filename()
        }, loading=loading, filename=self.file)
        loading.done = True
        sublime.status_message('File uploaded successfully!')
        self.file = None

    def friendly_filename(self):
        filename = self.file.split('/').pop()
        if self.settings.get('repeat_file_ext') and len(filename.split('.')) > 1:
            filename += '.' + filename.split('.').pop()
        return filename


class UploadSelectionAsFileCommand(UploadCurrentFileCommand):
    """ Uploads current selected text as file """

    def run(self, view):
        super(UploadCurrentFileCommand, self).run(view)

        self.file = self.view.file_name()

        # get all selected regions
        for region in self.view.sel():
            text = self.view.substr(region)

            if not text:
                sublime.error_message("SLACK Error: No text selected")
                return
            self.messages.append(text)

        threading.Thread(target=self.init_message_send).start()

    def friendly_filename(self):

        if self.file is None:

            self.file = 'Untitled'
            ext = self.get_extension_from_scope()

            if ext:
                self.file = '{}.{}'.format(self.file, ext)

        return super(UploadSelectionAsFileCommand, self).friendly_filename()

    def get_extension_from_scope(self):

        scope = self.view.scope_name(0)

        if 'html' in scope:
            return 'html'
        if 'python' in scope:
            return 'py'
        if 'sql' in scope:
            return 'sql'

        return ''

    def upload_file(self, receiver_index):

        receiver = self.receivers[receiver_index]
        loading = Loader('Uploading file ...', False)

        for content in self.messages:

            self._api_call(API_UPLOAD_FILES, {
                'token': receiver.get('token'),
                'channels': receiver.get('id'),
                'filename': self.friendly_filename(),
                'content': content
            }, loading=loading)

        loading.done = True
        sublime.status_message('Selection uploaded successfully!')
        self.file = None


class UploadFromPathCommand(UploadCurrentFileCommand):
    def run(self, view):
        self.settings = sublime.load_settings("Slack.sublime-settings")
        self.view.window().show_input_panel(
            'Slack: Enter file path:', '',
            self.on_done, False, False)

    def on_done(self, path):
        if not isfile(path):
            return sublime.error_message('SLACK Error: File not found!\n'+path)
        self.file = path
        threading.Thread(target=self.init_message_send).start()
