# Voxyl-Stats-Support
The support bot Voxyl Stats [Discord Sever](https://discord.gg/fBnfWXSDpu)

<br/>

## Voxyl Stats Links:

- [Discord Bot Invite](https://discord.com/api/oauth2/authorize?client_id=926814210321707028&permissions=277025442816&scope=bot%20applications.commands)  
- [Support Server](https://discord.gg/fBnfWXSDpu)  
- [Buymeacoffee](https://www.buymeacoffee.com/voxlystats/)

## Setup:

- Install all [required libraries](#Required-Libraries)
- Download all files from the github
- Create a discord application and bot [here](https://discordapp.com/developers/applications)
- Add files to a server (If you are using one)
- Create a file called `config.json` and include the following info
```json
{
    "TOKEN": "",
    "logchannel": 1,
    "mutedrole": 1,
    "suggestionchannel": 1,
    "verifyrole": 1,
    "supportcategory": 1
}
```
- Run main.py (python3 main.py)
- Enjoy!


## Commands:

- /purge - Purge a specific amount of messages.  
- /verifymessage - Send a verification message to a channel.  
- /createpanel - Creates a Support Panel.  
- /create_embed - Create a custom embed.  
- /links - Sends all links associated with Voxyl Stats.  
- /lock - Lock a channel
- /unlock - Unlock a channel
- /slowmode - Add a slowmode to a channel
- /tag
    - Create - create a new tag
    - Remove - remove a tag
    - List - get a list of all current tags
    - Use - use one of the created tags

## Required Libraries:

- [discord.py](https://pypi.org/project/discord.py/)
- [discord interactions](https://pypi.org/project/discord-py-slash-command/)
- [datetime](https://pypi.org/project/DateTime/)  
- [asyncio](https://pypi.org/project/asyncio/)
- [better-profanity](https://pypi.org/project/better-profanity/)


