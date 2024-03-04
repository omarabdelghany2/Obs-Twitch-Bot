from bot import Bot, Obs, Widget
import toml

data = toml.load("./config.toml")

obs_settings = data["settings"]


if __name__ == "__main__":
    widget = Widget()
    obs = Obs(obs_settings["host"], obs_settings["port"], obs_settings["password"])
    bot = Bot(widget.rewrite, obs.refresh_html)
    bot.run()

