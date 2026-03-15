# Stream Pet

This project is a stream pet/chat bot that will sit in your stream chat and respond to various commands and/or chat messages, as defined by the user.  First goal is to support twitch streams only, altough support for other platforms will be considered once the bot is stable on twitch.

The bot will be intended to be run on the command line.  GUI is hard.  The intention is to have it always running on something like a raspberry pi or other local server, altough nothing should prevent it from being run as needed instead.

## The Plan

The bot will be written in python: it's easy to write and will run just about anywhere.  Releases should be created using (pyinstaller)[https://pypi.org/project/pyinstaller/].

### Features

- Connect to the Twitch API
- Extensive logging to local file
- React to commands in chat
- React to raids
- User interaction
    - Store users that show up in chat
    - Keep track of stream IDs
    - Track which users were in each stream
    - Custom welcome messages for a user's first message in chat each stream (eg. auto shoutouts)
    - Allow setting pronouns, possible interaction with the Alejo extention
    - Allow setting nicknames?  Could end up being a moderation nightmare but would be nice to have
- React to follows
- React to subscriptions
- React to channel point rewards
- Add a GUI

### Program flow

```mermaid
flowchart TD
    A([START]) -->
    B{Does settings file exist?}
    B -- Yes --> D
    B -- No --> C[Create default settings file] --> D
    D[Load settings]
    D --> E{Are client id and secret set?}
    E -- Yes --> F[Obtain access token]
    E -- No --> G([LOG ERROR AND EXIT])
    F --> H{Have valid token?}
    H -- Yes --> I[Start loop]
    H -- No --> J([LOG ERROR AND EXIT])
