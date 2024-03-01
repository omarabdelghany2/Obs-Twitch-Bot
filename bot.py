
from twitchio.ext import commands
import toml
from bs4 import BeautifulSoup
import obsws_python as obs
import keyboard

data = toml.load("./config.toml")

TMI_TOKEN = data["tmi"]["token"]
TMI_CLIENT_ID = data["tmi"]["client_id"]
TMI_BOT_NICK = data["tmi"]["bot_nick"]
TMI_BOT_PREFIX = data["tmi"]["bot_prefix"]
TMI_CHANNEL = data["tmi"]["channel"]

GLOBAL_COMMANDS = data["commands"]["global"]
SUB_COMMANDS = data["commands"]["subscribers"]
PAID_COMMANDS = data["commands"]["paid"]




       




class Bot(commands.Bot):
    def __init__(self, rewrite_html, refresh_browser):
        super().__init__(token= TMI_TOKEN, prefix= TMI_BOT_PREFIX, initial_channels= [TMI_CHANNEL])
        self.ArrayOfPeopleNames = [""]
        self.current_value=0
        self.rewrite_html = rewrite_html
        self.refresh_browser = refresh_browser
        keyboard.hook(self.on_key_event)
        self.pause=True

    def on_key_event(self,event):
        if event.event_type == keyboard.KEY_DOWN:
            if(event.name.lower() =='s'): #start
                    self.pause=False
                    print("S")
            elif(event.name.lower() =='r'): #reset
                    self.current_value=0
                    print("r")
            elif(event.name.lower() =='p'): #pause
                    self.pause=True
                    print("p")         


        

    def add_number(self, number):
        self.current_value = max(0, min(100, self.current_value + number))

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        
    def get_info(self):
        if 1 <= self.current_value <= 20:
            return ["segment 1", self.current_value]
        elif 21 <= self.current_value <= 40:
            return ["segment 2", self.current_value]
        elif 41 <= self.current_value <= 60:
            return ["segment 3", self.current_value]
        elif 61 <= self.current_value <= 80:
            return ["segment 4", self.current_value]
        elif 81 <= self.current_value <= 100:
            return ["segment 5", self.current_value]
        else:
            return ["segment 0", self.current_value]

    def send_info(self):
        content = self.get_info()
        self.rewrite_html(content)
        self.refresh_browser("Browser")
    
    @commands.command()
    async def test(self, ctx: commands.Context):
        await ctx.send("test passed")

    async def close(self):
        await super().close()  # Terminate the bot

    async def event_message(self,ctx):
        if(self.pause==False):    

            if ctx.content in GLOBAL_COMMANDS:
                if not ctx.author.name.lower() in self.ArrayOfPeopleNames:
                    self.add_number(GLOBAL_COMMANDS[ctx.content]["rate"])
                    self.ArrayOfPeopleNames.append(ctx.author.name.lower())
                    self.send_info()
                else:
                    print("User already voted")
            elif ctx.content in SUB_COMMANDS:
                if not ctx.author.name.lower() in self.ArrayOfPeopleNames:
                    self.add_number(SUB_COMMANDS[ctx.content]["rate"])
                    self.ArrayOfPeopleNames.append(ctx.author.name.lower())
                    self.send_info()
                else:
                    print("User already voted")
            elif ctx.content in PAID_COMMANDS:
                self.add_number(PAID_COMMANDS[ctx.content]["rate"])
                self.ArrayOfPeopleNames.append(ctx.author.name.lower())
                self.send_info()
            else:
                print("Command not found")



class Widget:

    def __init__(self):
        self.file = open("preview/index.html", "r+")
        self.soup = BeautifulSoup(self.file, "html.parser")

    def rewrite(self, content):
        # Modify the content of the <div> element
        old_value = self.soup.find("div", {"id": "oldvalue"})
        new_value = self.soup.find("div", {"id": "newvalue"})

        old_value.string = str(new_value.string)
        new_value.string = str(content[1])

        self.file.seek(0)
        self.file.write(str(self.soup))
        self.file.truncate()

    
    def close(self):
        self.file.close()



class Obs:
    
    def __init__(self, host, port, password):
        self.cl = obs.ReqClient(host=host, port=port, password=password, timeout=3)
    
    def refresh_html(self,source_name):
        self.cl.press_input_properties_button(source_name,"refreshnocache")

