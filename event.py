
class Event:
    def __init__(self, event_id, text, outcome, buttons, outtext, chance=1, pic=None):
        self.event_id = event_id
        self.text = text
        self.outcome = outcome
        self.buttons = buttons
        self.outtext = outtext

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            event_id=data["event_id"],
            text=data["text"],
            outcome=data["outcome"],
            buttons=data["buttons"],
            outtext=data["outtext"],
            chance=data.get("chance", 1),
            pic=data.get("pic")
        )