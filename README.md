# Discordbot

## Overview
A discord bot made in python to increase the quality of life of the users in the discord servers. It can automatically join the voice calls and use speech recognition to interact with users in voice calls for a hands free experience. The bot can join calls, listen and speak using Gemini AI. It also has some games, plays music and has tools that help with moderating. Special assigned users can also edit the code to add functionality straight from the chat.

## Features
### Voice Channel Integration
- Ability to Join and Leave voice channels with user commands or automatically join with users if signed up to.
- Users can control the bot through voice commands for an immersive hands free experience.
- Voice commands include playing youtube music, changing volume, changing volume when a user talks and more.

### Audio Playback
- Play, pause, stop and queue music from youtube video titles and links.
- Manage the playback with commands like skip, fast forward and repeat.

### AI-Powered Interactions
- Engage in conversations with Gemini AI using api's which save and clear history for better context.

### Moderation Tools
- Keep track of deleted or edited messages to ensure server transperency and moderation.

### User Friendly Commands
- Many helpful commands to make the user experience better with some fun guessing games.
- A helpful menu that allows users to see all the commands and capabilities of the chatbot.

### Server Code Editor Tools
- Allows people with editing permisson to be able to code and add functionality to the bot through discord chat easily using built in commands or commands of the system they are running the server on and be able to run those changes.
- Revert the changes back to a safe commit if the new version causes the program to crash and report the error.

## Getting Started
### Prerequisites
Before you begin, ensure that you have the following requirements:
- Python 3.8 or later edition
- A discord account and the valid permissions to add bots

### Installation
1. Clone the repository:
   `git clone https://github.com/ank266/discordbot.git`
2. Navigate to the project directory:
   `cd discordbot`
3. Install the required packages:
   `pip install -r requirements.txt`
4. Create a .env file and add your credentials:
```
BOT_TOKEN=your_token
GEMINI_API_KEY=your_api_key
MAIN_CHAT_ID=chat_id_for_the_who_sent_the_message_guessing_game
NORMAL_CHAT_ID=chat_id_to_exclude_the_chat_where_guessing_game_command_should_work
```
5. Create file settings.txt in the settings folder and add the following (leave the point after = sign empty if no user id but make sure to include all lines):
```
Volume = 1.0
Editors = user_id_of_editors_who_can_edit_code_from_chat
Voice Command Users = user_id_of_people_who_the_bot_listens_to_in_calls
Join Call with Users = user_id_of_people_to_join_the_call_with
Channel to send message to = channel_to_send_voice_call_message_to
Channel to send deletes and edits to = channel_to_send_deleted_and_edited_messages_to
```
6. Install ffmpeg from `https://www.ffmpeg.org/download.html` and change the location of the ffmpeg.exe executable file in voicechat_integration.py function play_audio_file(ctx).
### Running the Bot
To start the bot, run:
  `python run_script.py`
## Usage
- Run the commands $commands for a description all general commands, $ecommands for bot editing commands, $vcommands for the voice call speech commands for more insight on the commands.
- Or visit the general_commands/qol.py file and scroll to the commands functions for help with the commands.

- Example code `$askGem how are you` to so ask gemini 'how are you'.
- Example code `clearHistory` to clear the history of the chat with gemini.
## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
## Contribution Guidelines
If you have any suggestions or want to address any issues that you encounter, please open an issue to do so. If you have any changes so add than please take appropriate actions (fork the project and create a new branch, etc.) and open a pull request to do so.
## Contact
For any questions or feedback, please reach out via anuragkhare97@gmail.com or open an issue on Github.
