from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import re
from kivy.clock import Clock
from kivy.lang import Builder
Builder.load_file('til_operator/operator.kv')


class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = []
        self.qty = []
        self.total = 0.00

    def calc(self, instance):
        print(self.ids['qrlabel'].text)

    def logout(self):
        self.parent.parent.current = 'scrn_si'

    def change_screen(self, instance):
        if instance.text == "Cart":
            self.ids.scrn_mngr.current = "scrn_cart"
        elif instance.text == "QRCode":
            self.ids.scrn_mngr.current = "scrn_code"
        else:
            pass

    def process_barcode(self):
        self.ids.memberStatus.text = self.ids.text_in.text
        self.ids.text_in.text = ""
        Clock.schedule_once(
            lambda *args: setattr(self.ids.text_in, 'focus', True))

    def update_purchases(self):
        pcode = self.ids.code_inp.text
        products_container = self.ids.Products
        if pcode == '1234' or pcode == '2345':
            details = BoxLayout(size_hint_y=None, height=30,
                                pos_hint={'top': 1})
            products_container.add_widget(details)

            code = Label(text=pcode, size_hint_x=.2,
                         color=(1, 1, 1, 1), bold=True)
            name = Label(text="Product One", size_hint_x=.3,
                         color=(1, 1, 1, 1), bold=True)
            qty = Label(text='9', size_hint_x=.1,
                        color=(1, 1, 1, 1), bold=True)
            disc = Label(text='0.00', size_hint_x=.1,
                         color=(1, 1, 1, 1), bold=True)
            price = Label(text='0.00', size_hint_x=.1,
                          color=(1, 1, 1, 1), bold=True)
            total = Label(text="0.00", size_hint_x=.2,
                          color=(1, 1, 1, 1), bold=True)

            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(disc)
            details.add_widget(price)
            details.add_widget(total)

            # update preview
            pname = "Product 1234"
            if pcode == '2345':
                pname = "Product 2345"
            pprice = 1.00
            pqty = str(1)
            self.total += pprice
            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t0.00' + str(self.total)
            self.ids.cur_product.text = pname
            self.ids.cur_price.text = str(pprice)
            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find('`')
            if _prev > 0:
                prev_text = prev_text[:_prev]

            ptarget = -1
            for i, c in enumerate(self.cart):
                if c == pcode:
                    ptarget = i
            if ptarget >= 0:
                pqty = self.qty[ptarget]+1
                self.qty[ptarget] = pqty
                expr = '%s\t\tx\d\t' % (pname)
                rexpr = pname + '\t\tx'+str(pqty)+'\t'
                nu_text = re.sub(expr, rexpr, prev_text)
                preview.text = nu_text + purchase_total
            else:
                self.cart.append(pcode)
                self.qty.append(1)
                nu_preview = '\n'.join(
                    [prev_text, pname + '\t\tx'+pqty+'\t\t' + str(pprice), purchase_total])
                preview.text = nu_preview


class OperatorApp(App):
    def build(self):
        return OperatorWindow()


if __name__ == "__main__":
    oa = OperatorApp()
    oa.run()
