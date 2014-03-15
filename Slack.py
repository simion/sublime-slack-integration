import sublime
import sublime_plugin
import threading

from .api import api_call


API_CHANNELS = 'https://slack.com/api/channels.list'
API_POST_MESSAGE = 'https://slack.com/api/chat.postMessage'


class BaseSend(sublime_plugin.TextCommand):
    """ Base class which shows a channels list and sends messages """

    def __init__(self, view):
        super(BaseSend, self).__init__(view)

        # here we will store all messages
        self.messages = []

        # this channels list is only populated once, per sublime session
        # you need to restart sublime to re-take channels from API
        self.channels = []

        # load plugin settings
        self.settings = sublime.load_settings("Slack.sublime-settings")

    def run(self, view):
        # reset older messages stored in memory
        self.messages = []
        # check if token is set
        if not self.settings.get('team_tokens'):
            sublime.status_message('SLACK: Error! Please set your API "token" in Preferences -> Package Settings -> Slack -> Settings - User')
            raise Exception('Team Token missing')

    def on_select_channel(self, index):
        if index is -1:
            return sublime.status_message('SLACK: sending cancelled')

        channel = self.channels[index]
        sublime.status_message("Sending selection to: " + channel.get('name'))

        username = self.settings.get('username')
        info = sublime.platform()
        try:
            import getpass
            info = "{0}, {1}".format(getpass.getuser(), info)
        except:
            # cannot get current OS user
            pass

        for message in self.messages:
            args = {
                'token': channel.get('token'),
                'channel': channel.get('id'),
                'text': message,
                'username': "{0} ({1})".format(username, info)
            }
            response = api_call(API_POST_MESSAGE, args)
            if response['ok']:
                sublime.status_message('SLACK: Message sent successfully!')
            else:
                sublime.status_message('SLACK: Unexpected error!')

    def init_message_send(self):
        # check is channels are cached in memory
        if not self.channels:
            # get the channels for each team
            for team, token in self.settings.get('team_tokens').items():
                response = api_call(API_CHANNELS, {
                    'token': token
                })
                for channel in response['channels']:
                    if not channel['is_archived']:
                        # bind the token and team to the channel
                        channel['token'] = token
                        channel['team'] = team
                        self.channels.append(channel)
        # build a list with team/channel names, to use for menus
        channels = []
        print(self.channels)
        for channel in self.channels:
            channels.append("#{1} ({0})".format(
                channel['team'],
                channel['name']))

        # display a popup and let the user pick a channel
        self.view.window().show_quick_panel(
            channels,
            self.on_select_channel)


class SendSelectionCommand(BaseSend):
    """ Send the selected text to slack. Multiple selections supported """
    def run(self, view):
        super(SendSelectionCommand, self).run(view)
        # get all selected regions
        for region in self.view.sel():
            text = self.view.substr(region)

            if not text:
                sublime.status_message("SLACK: Error! No text selected")
                return
            self.messages.append(text)

        threading.Thread(target=self.init_message_send).start()


class SendMessageCommand(BaseSend):
    """ Send a message from user input """

    def run(self, view):
        super(SendMessageCommand, self).run(view)
        self.view.window().show_input_panel(
            "Enter a message", '', self.on_done, None, None)

    def on_done(self, message):
        if not message:
            return sublime.status_message('ERROR: Please enter a message')
        self.messages = [message]
        threading.Thread(target=self.init_message_send).start()


class SendFileCommand(BaseSend):
    """ Under development """
    def on_select_channel(self, index):
        if index is -1:
            return sublime.status_message('SLACK: sending cancelled')

    def run(self, view):
        print(self.view.file_name())
