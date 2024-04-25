## About

Simple reminder bot for telegram. 

## Features

- cron support
- timezone support
- setting up a task list from the `config.yaml`

## Commands

- `/list` getting list of tasks 

## Configuration

`.env`:
```
# Get from @BotFather
BOT_TOKEN=<Your API token from @BotFather>

# https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
CHAT_ID=<Your chat id>
```

`config.yaml`:
```
tasks:
  - name: "my first task"
    cron: "* * * * *"
    text: "task text"
```

## Up & Running

`make activte` - activating venv  
`make install` - installing poetry and dependencies  
`make run` - running bot  