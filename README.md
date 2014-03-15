Sublime Text 3 slack.com integration plugin
=========================

A Sublime Text 3 plugin which integrates http://slack.com services.

## Features
* Sends selected code to slack (multiple cursors == multiple messages)
* Sends custom message from user input to slack
* allows user to pick a channel to send

## Configuration
Open "Settings - User" from Preferences -> Package Settings -> Slack

    {
      "token": "your-token-goes-here",
      "username": "SublimeTextBot"
    }

You can get the token from https://api.slack.com/#auth (make sure you are authenticated on slack.com with your account)

## Usage
* Select a text and Right click (or ctrl+shift+p) -> Slack: Send selection
* Choose channel
* Sending a custom message: same process, but choose "Send message". An input box will be prompted.

## Shortcuts
* ctrl+alt+u -> Send Selection
* ctrl+alt+n -> Send Custom Message

## Installation
Search for "Slack" package in Sublime Package Control


## Feedback
If you have any suggestions, please leave a reply here:
http://simionbaws.ro/sublime-text-3-slack-integration-plugin/

## Future development
This plugin will be updated as the slack.com service releases new features in their API.
If you want to contribute, feel free to fork and make a pull request.
Thanks
