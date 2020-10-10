from kivy.uix.modalview import ModalView


class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.background_color = (108/255, 90/255, 90/255, .76)
        self.size = (270, 50)


def cb(self):
    pass
