from bot import Bot, Obs, Widget



if __name__ == "__main__":
    widget = Widget()
    obs = Obs("localhost", 4444, "password")
    bot = Bot(widget.rewrite, obs.refresh_html)
    bot.run()

