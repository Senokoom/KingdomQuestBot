
class Player:
    def __init__(self, tgid, data=None):
        self.tgid = tgid

        default_data = {
            "count": 0,
            "gold": 0,
            "soldier": 0,
            "peasant": 0,
            "loyality_soldier": 50,
            "loyality_peasant": 50
        }

        self.data = data if data else default_data.copy()

    def to_tuple(self):
        return (
            self.data["count"],
            self.data["gold"],
            self.data["soldier"],
            self.data["peasant"],
            self.data["loyality_soldier"],
            self.data["loyality_peasant"]
        )

    def tostirng(self):
        return (
            f"👑 Ход: {self.data['count']}\n"
            f"💰 Золото: {self.data['gold']}\n"
            f"⚔ Солдаты: {self.data['soldier']} (лояльность: {self.data['loyality_soldier']})\n"
            f"👨‍🌾 Крестьяне: {self.data['peasant']} (лояльность: {self.data['loyality_peasant']})"
        )
