# Windows69 Chat-Bot

Contributors:
Ari, Peter Tanning , Nicholas Davies and  Div 

Windows69 Chat-Bot is an authentic Windows 98 style chat experience. Engage in real-time chats with other users who share your great taste. Invite and customise your own AI chatbots with distinctive personalities. Ever wondered what Clippy thinks about the current economic state of the world? Now you can find out!

Windows69 Chat-Bot aims to recreate the feeling of the late 90s Windows experience. By blending state of the art modern AI chat technology with one of the most iconic vintage graphical interfaces, it aims to create a distinct, immersive, memorable experience for all.

# Windows69 Chat-Bot Demo 

[Demo.webm](https://github.com/CITS3403GroupProject/Windows69-Chatbot/assets/70004128/da4fde14-1f74-4733-a7ff-f946fbaa3ecb)


## Architecture

Windows69 Chat-Bot uses HTML, CSS, and JavaScript for the client-side interface. Server-side is handled using Flask, and integrates the ChatGPT API.

## Installation
##### [Steps Install](https://dbprassan12.github.io/CITS3403-Agile-Web-Development-Exam/)

Add the following to secret/secret.py

```python
SECRET_KEY = "Your Password"

OPENAI_API_KEY="Your OpenAI KEY"

GECKO_PATH="{gecko path }"
```

### On Windows

```bash
python -m venv .venv
source ./.venv/Scripts/activate
python -m pip install -r requirements.txt
```

Create a file `secret/secret.py` and put a secret key for SocketIO
### On Linux/MacOS

```bash
python -m venv .venv
source ./.venv/bin/activate
python -m pip install -r requirements.txt
```

### Run app with

```bash
python debug_run.py
```

## Credits

Thanks to Alex Meub for the icons [win98icons](https://win98icons.alexmeub.com/).

Thanks to Microsoft Windows Sounds for the souunds [ Microsoft Windows Sounds](https://www.youtube.com/@microsoftwindowssounds2487).

## Running tests

In the project root directory:

```bash
python test_run.py
```

Or you can include this in your VSCode `launch.json` file:

```json
{
  "name": "Python: Run Unit Test",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/test_run.py",
  "console": "integratedTerminal",
  "python": "${command:python.interpreterPath}"
}
```
