Sublime Text 3 slack.com integration plugin
=========================

A Sublime Text 3 plugin which integrates http://slack.com services.


### Installation
Search for "Slack" package in Sublime Package Control


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

### Configuration
Open "Settings - User" from Preferences -> Package Settings -> Slack

    {
        "team_tokens": {
            "Team 1": "team-1-token-goes-here",
            "Team 2": "team-2-token-goes-here",
        },
        "username": "SublimeTextBot"
    }

You can get the token from https://api.slack.com/#auth (make sure you are authenticated on slack.com with your account)

###Changelog
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


### Shortcuts
* ctrl+alt+u -> Send Selection (osx: control + option + u)
* ctrl+alt+n -> Send Custom Message (osx: control + option + n)


### Feedback
If you have any suggestions, please leave a reply here:
http://simionbaws.ro/sublime-text-3-slack-integration-plugin/

### Bug report / feature request
Please use github issues system: https://github.com/simion/sublime-slack-integration/issues

### Future development
This plugin will be updated as the slack.com service releases new features in their API.
If you want to contribute, feel free to fork and make a pull request.
Thanks


#### Screenshots
![](http://i.imgur.com/lyv6Yd6.png "Grab message from user input")

![](http://i.imgur.com/fu941bH.png "Receiver selection")

![](http://i.imgur.com/SXnHYZo.png "Direct message sending, skips channe/user/group selection")

![](http://i.imgur.com/SXnHYZo.png "Send message directly to user")

![](http://i.imgur.com/qaXE9EN.png "Send message directly to channel")

![](http://i.imgur.com/7n14c5H.png "Example of received message")
