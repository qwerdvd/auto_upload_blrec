import pathlib

import tomli
import json
from config_model import ConfigModel


class Config(ConfigModel):

    def load_cookies(self):
        self.data["user"] = {"cookies": {}}
        with open('cookies.json', encoding='utf-8') as stream:
            s = json.load(stream)
            for i in s["cookie_info"]["cookies"]:
                name = i["name"]
                self.data["user"]["cookies"][name] = i["value"]
            self.data["user"]["access_token"] = s["token_info"]["access_token"]

    def load(self, file):
        if file is None:
            if pathlib.Path('config.toml').exists():
                self.data['toml'] = True
                file = open('config.toml', "rb")
            else:
                raise FileNotFoundError('未找到配置文件，请先创建配置文件')
        with file as stream:
            if file.name.endswith('.toml'):
                self.data = tomli.load(stream)

        with file as stream:
            if file.name.endswith('.toml'):
                self.data = tomli.load(stream)
                self.data['toml'] = True

    def save(self):
        if self.data.get('toml'):
            import tomli_w
            with open('config.toml', 'rb') as stream:
                old_data = tomli.load(stream)
                old_data["lines"] = self.data["lines"]
                old_data["threads"] = self.data["threads"]
                old_data["streamers"] = self.data["streamers"]
            with open('config.toml', 'wb') as stream:
                tomli_w.dump(old_data, stream)


config = Config()
