# Stream Pet

This project is a stream pet/chat bot that will sit in your stream chat and respond to various commands and/or chat messages, as defined by the user.  First goal is to support twitch streams only, altough support for other platforms will be considered once the bot is stable on twitch.

## The Plan

The bot will probably be written in python: it's easy to write and will run just about anywhere.  Releases should be compiled into a [zipapp](https://docs.python.org/3/library/zipapp.html).

### Features

- Connect to the Twitch API
- Respond to commands in chat
- User interaction
    - Store users that show up in chat
    - Keep track of stream IDs
    - Track which users were in each stream
    - Custom welcome messages for a user's first message in chat each stream (eg. auto shoutouts)
    - Allow setting pronouns, possible interaction with the Alejo extention
    - Allow setting nicknames?  Could end up being a moderation nightmare but would be nice to have
- Respond to channel point rewards
