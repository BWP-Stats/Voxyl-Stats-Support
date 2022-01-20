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
- Replace all necessary information in cogs (Will be a config.json soon)
  - Add the token in the quotation marks in main.py
  - Replace supportcategory variable with your support category ID in on_component.py
  - Replace verifyrole variable with your verified role
  - Replace the logchannel variable in events.py with your log channel
- Run main.py (python3 main.py)
- Enjoy!

## Commands:

- /purge - Purge a specific amount of messages.  
- /verifymessage - Send a verification message to a channel.  
- /createpanel - Creates a Support Panel.  
- /create_embed - Create a custom embed.  
- /links - Sends all links associated with Voxyl Stats.  

## Required Libraries:

- [discord.py](https://pypi.org/project/discord.py/)
- [discord interactions](https://pypi.org/project/discord-py-slash-command/)
- [datetime](https://pypi.org/project/DateTime/)  
- [asyncio](https://pypi.org/project/asyncio/)
- [better-profanity](https://pypi.org/project/better-profanity/)


