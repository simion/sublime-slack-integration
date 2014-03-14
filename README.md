Sublime Text 3 slack.com integration plugin
=========================

A Sublime Text 3 plugin which integrates http://slack.com services.

## Features
* Sends selection to slack
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
to be updated
