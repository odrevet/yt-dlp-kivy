from functools import partial


from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class FormatSelectPopup(Popup):
    meta = {}
    selected_format_id = []

    def __init__(self, meta, **kwargs):
        super(FormatSelectPopup, self).__init__(**kwargs)
        self.selected_format_id.clear()

        if not meta or "formats" not in meta:
            print("Error: No formats found in metadata")
            grid = self.ids.layout
            grid.add_widget(Label(text="No formats found"))
            return
        else:
            formats_sorted = sorted(meta["formats"], key=lambda k: k["format"])
            for format in formats_sorted:
                grid = self.ids.layout
                grid.add_widget(Label(text=format["format"] + " " + format["ext"]))
                checkbox = CheckBox(active=False, size_hint_x=None, width=100)
                callback = partial(self.on_checkbox_active, format["format_id"])
                checkbox.bind(active=callback)
                grid.add_widget(checkbox)

    def on_checkbox_active(self, format_id, instance, value):
        if value:
            self.selected_format_id.append(format_id)
        else:
            self.selected_format_id.remove(format_id)
