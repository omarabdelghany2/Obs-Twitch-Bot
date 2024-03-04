
from twitchio.ext import commands
import toml
from bs4 import BeautifulSoup
import obsws_python as obs
from pynput import keyboard as pynput_keyboard

data = toml.load("./config.toml")

TMI_TOKEN = data["tmi"]["token"]
TMI_BOT_PREFIX = data["tmi"]["bot_prefix"]
TMI_CHANNEL = data["tmi"]["channel"]

GLOBAL_COMMANDS = data["commands"]["global"]
SUB_COMMANDS = data["commands"]["subscribers"]
PAID_COMMANDS = data["commands"]["paid"]

GOAL = data["settings"]["goal"]
SOURCE_NAME = data["settings"]["source_name"]

HOTKEYS = data["hotkeys"]


class Bot(commands.Bot):
    def __init__(self, rewrite_html, refresh_browser):
        super().__init__(token=TMI_TOKEN, prefix=TMI_BOT_PREFIX, initial_channels=[TMI_CHANNEL])
        self.ArrayOfPeopleNames = []
        self.current_value = GOAL / 2
        self.points = 0
        self.rewrite_html = rewrite_html
        self.refresh_browser = refresh_browser
        self.pause = True

        # Create a listener for keyboard events
        self.keyboard_listener = pynput_keyboard.Listener(on_press=self.on_key_event)
        self.keyboard_listener.start()

        self.send_info()  # reset

    def on_key_event(self, key):
        try:
            # Convert the key to lowercase to ensure case-insensitivity
            key_name = key.char.lower()
        except AttributeError:
            # Handle special keys
            key_name = str(key).lower()

        if key_name == HOTKEYS["start"]:
            if not self.pause:
                self.pause = True
                print("Script resumed")
        elif key_name == HOTKEYS["reset"]:
            self.current_value = GOAL / 2
            self.ArrayOfPeopleNames = []
            self.points = 0
            self.send_info()
            print("Script reset")
        elif key_name == HOTKEYS["pause"]:
            if self.pause:
                self.pause = False
                print("Script paused")

    def add_number(self, number):
        self.points = number
        self.current_value = max(0, min(GOAL, self.current_value + number))

    async def event_ready(self):
        print(f'Script Started | Logged in as | {self.nick}')

    def get_info(self):
        percentage = int((self.current_value / GOAL) * 100)

        if 1 <= percentage <= 20:
            return ["segment-1", percentage, self.points]
        elif 21 <= percentage <= 40:
            return ["segment-2", percentage, self.points]
        elif 41 <= percentage <= 60:
            return ["segment-3", percentage, self.points]
        elif 61 <= percentage <= 80:
            return ["segment-4", percentage, self.points]
        elif 81 <= percentage <= 100:
            return ["segment-5", percentage, self.points]
        else:
            return ["segment-1", percentage, self.points]

    def send_info(self):
        content = self.get_info()
        self.rewrite_html(content)
        self.refresh_browser(SOURCE_NAME)

    async def close(self):
        self.keyboard_listener.stop()
        await super().close()  # Terminate the bot

    async def event_message(self, ctx):
        first_part = ctx.content.split()[0]

        if self.pause:
            if first_part in GLOBAL_COMMANDS:
                if not ctx.author.name.lower() in self.ArrayOfPeopleNames:
                    self.add_number(GLOBAL_COMMANDS[first_part]["rate"])
                    self.ArrayOfPeopleNames.append(ctx.author.name.lower())
                    self.send_info()
                    await ctx.channel.send(f"{ctx.author.name} {GLOBAL_COMMANDS[first_part]['message']}")
            elif first_part in SUB_COMMANDS:
                if not ctx.author.name.lower() in self.ArrayOfPeopleNames:
                    if ctx.author.is_subscriber:
                        self.add_number(SUB_COMMANDS[first_part]["rate"])
                        self.ArrayOfPeopleNames.append(ctx.author.name.lower())
                        self.send_info()
                        await ctx.channel.send(f"{ctx.author.name} {SUB_COMMANDS[first_part]['message']}")
            elif ctx.content in PAID_COMMANDS:
                self.add_number(PAID_COMMANDS[ctx.content]["rate"])
                self.send_info()
                await ctx.channel.send(f"{ctx.author.name} {PAID_COMMANDS[ctx.content]['message']}")


class Widget:

    def __init__(self):
        self.file = open("preview/index.html", "r+")
        self.soup = BeautifulSoup(self.file, "html.parser")

    def rewrite(self, content):
        calculated_value = (content[1] / 100) * 180

        image = self.soup.find("img", {"id": "rotateImage"})
        background = self.soup.find("img", {"id": "background"})
        percentage = self.soup.find("div", {"id": "per"})

        positive = self.soup.find('div', class_='pos')
        negative = self.soup.find('div', class_='neg')

        if content[2] > 0:
            if 'hide' in positive['class']:
                positive['class'].remove('hide')
            if not 'hide' in negative['class']:
                negative['class'] = negative.get('class', []) + ['hide']

        elif content[2] < 0:
            if 'hide' in negative['class']:
                negative['class'].remove('hide')
            if not 'hide' in positive['class']:
                positive['class'] = positive.get('class', []) + ['hide']
        elif content[2] == 0:
            if not 'hide' in negative['class']:
                negative['class'] = negative.get('class', []) + ['hide']
            if not 'hide' in positive['class']:
                positive['class'] = positive.get('class', []) + ['hide']

        image['style'] = f'transform: rotate({calculated_value}deg);'
        background['src'] = f'../assets/{content[0]}.png'
        percentage.string = f"{content[1]}%"

        self.file.seek(0)
        self.file.write(str(self.soup))
        self.file.truncate()

    def close(self):
        self.file.close()


class Obs:

    def __init__(self, host, port, password):
        self.cl = obs.ReqClient(host=host, port=port, password=password, timeout=3)

    def refresh_html(self, source_name):
        self.cl.press_input_properties_button(source_name, "refreshnocache")