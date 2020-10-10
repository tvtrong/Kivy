from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from utils.notify import Notify
from kivy.clock import Clock
from kivy.uix.label import Label
from pymongo import MongoClient
import hashlib
from kivy.core.window import Window


Builder.load_file('Login/signin.kv')


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.username_field.focus = True
        self.notify = Notify()

    def cb(self, dt):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def validate_user(self):
        client = MongoClient()
        db = client.silverpos
        users = db.users

        user = self.ids.username_field
        pwd = self.ids.pwd_field
        #info = self.ids.info

        uname = user.text
        passw = pwd.text

        #user.text = ''
        #pwd.text = ''

        if not uname and not passw:
            self.notify.add_widget(
                Label(text='[color=#FFFFFF][b]Username and Password are Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.cb, 1.1)
        elif not uname:
            self.notify.add_widget(
                Label(text='[color=#FFFFFF][b]Username is Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.cb, 1.1)
            # info.text = "[color=#FF0000]Username required ![/color]"
        elif passw == '':
            self.notify.add_widget(
                Label(text='[color=#FFFFFF][b]Password is Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.cb, 1.1)
            # info.text = "[color=#FF0000]Password required ![/color]"
        else:
            user = users.find_one(({'user_name': uname}))
            if user == None:
                self.notify.add_widget(
                    Label(text='[color=#FF0000][b]Invalid Username[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.cb, 1.1)
            # info.text = "[color=#FF0000]Invalid Username ![/color]"
            else:
                passw = hashlib.sha256(passw.encode()).hexdigest()
                if passw == user['password']:
                    des = user['designation']
                    self.notify.add_widget(
                        Label(text='[color=#00FF00][b]Success Login[/b][/color]', markup=True))
                    self.notify.open()
                    Clock.schedule_once(self.cb, 1.3)
                    self.parent.parent.parent.ids.scrn_op.children[0].ids.loggedin_user.text = uname
                    if des == 'Administrator':
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.current = 'scrn_op'
                else:
                    self.notify.add_widget(
                        Label(text='[color=#FF0000][b]Invalid Password[/b][/color]', markup=True))
                    self.notify.open()
                    Clock.schedule_once(self.cb, 1.1)


class SigninApp(App):

    def build(self):
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.primary_hue = 'A700'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_color = 'Red'
        return SigninWindow()


if __name__ == "__main__":
    Window.show_currsor = True
    Window.size = (500, 600)
    sa = SigninApp()
    sa.run()
