Sublime Text 3 slack.com integration plugin
=========================

A Sublime Text 3 plugin which integrates http://slack.com services.

### Features
* Send messages to users/channels/groups
* Can sends selected code
* Sends custom message from user input
* When sending messages from input, @user, #channel or .group at the beggining of the message skips channel/user/group selection dialog
* New message from input will have autofilled the @user #channel or .group (for quick chatting, if you want to reply directly from sublime and continue working)
* Multiple tokens(teams) supported

###Changelog
* 1.3.2: http://simionbaws.ro/plugins/sublime-slack-1-3-2/
* 1.3.1: http://simionbaws.ro/plugins/sublime-slack-1-3/

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

### Installation
Search for "Slack" package in Sublime Package Control


### Feedback
If you have any suggestions, please leave a reply here:
http://simionbaws.ro/sublime-text-3-slack-integration-plugin/

### Future development
This plugin will be updated as the slack.com service releases new features in their API.
If you want to contribute, feel free to fork and make a pull request.
Thanks
