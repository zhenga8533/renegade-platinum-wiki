import re


class PokemonSet:
    def __init__(self, data: str):
        self.species = ""
        self.level = 0
        self.item = ""
        self.nature = ""
        self.ability = ""
        self.moves = []
        self.parse_data(data)

    def parse_data(self, data: str):
        strs = data.split("/")

        match = re.match(r"(.+?) \(Lv\. (\d+)\) @ (.+)", strs[0].strip())
        self.species = match.group(1)
        self.level = int(match.group(2))
        self.item = match.group(3)
        self.nature = strs[1].strip()
        self.ability = strs[2].strip()
        self.moves = strs[3].strip().split(", ")

    def to_string(self):
        if self.moves[-1].endswith("(!)"):
            self.moves[-1] = self.moves[-1][:-4]
            self.species += " (!)"

        s = f"<b>{self.species}</b> @ {self.item if self.item != "-" else "No Item"}\n"
        s += f"<b>Ability:</b> {self.ability if self.ability != "-" else "?"}\n"
        s += f"<b>Level:</b> {self.level}\n"
        s += f"<b>Moves:</b>\n"
        for i, move in enumerate(self.moves):
            s += f"{i + 1}. {move}\n"
        return s
