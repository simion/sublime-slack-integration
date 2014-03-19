Sublime Text 3 slack.com integration plugin
=========================

A Sublime Text 3 plugin which integrates http://slack.com services.


### Installation
Search for "Slack" package in Sublime Package Control

### Configuration
Open "Settings - User" from Preferences -> Package Settings -> Slack

    {
        "team_tokens": {
            "Team 1": "team-1-token-goes-here",
            "Team 2": "team-2-token-goes-here",
        },
        "username": "ST",
        "show_plaform_and_name": true
    }

You can get the token from https://api.slack.com/#auth (make sure you are authenticated on slack.com with your account)

### Features
* Send messages to
    * users
    * channels
    * private groups
* Can send message:
    * from selected code
    * from user input
* @user, #channel or .group supported (at beggining of message)
* Autofill last @user, #channel or .group used
* Multiple teams(tokens) support
* Upload files
    * current open file
    * contextual (right click) in sidebar
    * enter file path manually


###Changelog
* 1.4.0: http://simionbaws.ro/plugins/sublime-slack-1-4-0/
* 1.3.3: http://simionbaws.ro/plugins/sublime-slack-1-3-3/
* 1.3.2: http://simionbaws.ro/plugins/sublime-slack-1-3-2/
* 1.3.1: http://simionbaws.ro/plugins/sublime-slack-1-3/


### Usage
* Select a text and Right click (or ctrl+shift+p) -> Slack: Send selection
* Sending a custom message:
 - press Ctrl+Alt+n (or control + command + n)
 - enter the message
 - choose a channel/group/user from the dropdown
If the message begins with @username #channel or .group the message is sent directly to the specified receiver.
When using new message input box, it will have the last receiver name autocompletet automatically
* Send a file: right click, or using quick panel

### Shortcuts
* ctrl+alt+u -> Send Selection (osx: control + option + u)
* ctrl+alt+n -> Send Custom Message (osx: control + option + n)
* ctrl+alt+j -> Send Current File (osx: control + option + k)


### Feedback
If you have any suggestions, please leave a reply here:
http://simionbaws.ro/sublime-text-3-slack-integration-plugin/

### Bug report / feature request
Please use github issues system: https://github.com/simion/sublime-slack-integration/issues

### Development
This plugin is constantly being upgraded as the slack.com API team releases new features or fixes existing bugs.
If you want to contribute, feel free to fork and make a pull request. The code must pe PEP8 compliant to be accepted (or at least close to that)

### Support
I like beer.
So if you'd like to support the continuous development of this plugin, you could buy me a beer: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=NNPZNQULPETD4



#### Screenshots
![](http://i.imgur.com/lyv6Yd6.png "Grab message from user input")

![](http://i.imgur.com/fu941bH.png "Receiver selection")

![](http://i.imgur.com/SXnHYZo.png "Direct message sending, skips channe/user/group selection")

![](http://i.imgur.com/SXnHYZo.png "Send message directly to user")

![](http://i.imgur.com/qaXE9EN.png "Send message directly to channel")

![](http://i.imgur.com/7n14c5H.png "Example of receved message")

![](http://i.imgur.com/Gf6UvSn.png "Sidebar right click")

![](http://i.imgur.com/GTfi88U.png "Quick menu")
