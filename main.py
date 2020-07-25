import os
import sys
import threading
from functools import partial
from os.path import expanduser, join

import kivy
import youtube_dl
from kivy.app import App
from kivy.factory import Factory
from kivy.properties import DictProperty, NumericProperty, StringProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

from about import AboutPopup
from downloaderThread import DownloaderThread
from logger import YdlLogger
from settings_json import settings_json
from status import STATUS_DONE, STATUS_ERROR, STATUS_IN_PROGRESS

if platform == 'android':
    from android.storage import primary_external_storage_path
    from android.permissions import check_permission, request_permissions, Permission


class RV(RecycleView):
    pass


class ActionBarMain(ActionBar):
    pass


class LogPopup(Popup):
    log = StringProperty()
    index = NumericProperty()

    def __init__(self, log, index, **kwargs):
        super(LogPopup, self).__init__(**kwargs)
        self.log = log
        self.index = index


class FormatSelectPopup(Popup):
    meta = {}
    selected_format_id = []

    def __init__(self, meta, **kwargs):
        super(FormatSelectPopup, self).__init__(**kwargs)
        self.selected_format_id.clear()
        formats_sorted = sorted(meta['formats'], key=lambda k: k['format'])
        for format in formats_sorted:
            grid = self.ids.layout
            grid.add_widget(Label(text=format['format'] + ' ' + format['ext']))
            checkbox = CheckBox(active=False, size_hint_x=None, width=100)
            callback = partial(self.on_checkbox_active, format['format_id'])
            checkbox.bind(active=callback)
            grid.add_widget(checkbox)

    def on_checkbox_active(self, format_id, instance, value):
        if value:
            self.selected_format_id.append(format_id)
        else:
            self.selected_format_id.remove(format_id)


class InfoDisplayPopup(Popup):
    meta = {}

    def __init__(self, meta, **kwargs):
        super(InfoDisplayPopup, self).__init__(**kwargs)
        self.meta = meta

        self.add_to_view(Label(text='[b]'+meta['title']+'[/b]', markup=True))

        if meta['description']:
            self.add_to_view(Label(text=meta['description']))

        if meta['thumbnails']:
            url = meta['thumbnails'][0]['url']
            thumbnail = AsyncImage(source=url)
            self.add_to_view(thumbnail)

    def add_to_view(self, widget):
        self.ids.view.add_widget(widget)


class DownloadStatusBar(BoxLayout):
    url = StringProperty('')
    status = NumericProperty(STATUS_IN_PROGRESS)
    log = StringProperty('')
    index = NumericProperty()
    status_icon = StringProperty('img/loader.png')
    title = StringProperty('')
    percent = NumericProperty(0)
    ETA = StringProperty('')
    speed = StringProperty('')
    file_size = StringProperty('')
    popup = None

    def on_release_show_log_button(self):
        self.popup = LogPopup(self.log, self.index)
        self.popup.open()

    def on_status(self, instance, value):
        if (value == STATUS_IN_PROGRESS):
            self.status_icon = 'img/loader.png'
        elif (value == STATUS_DONE):
            self.status_icon = 'img/correct.png'
        elif (value == STATUS_ERROR):
            self.status_icon = 'img/cancel.png'

    def on_log(self, instance, value):
        if(self.popup is not None and instance.index == self.popup.index):
            self.popup.log = value


class DownloaderLayout(BoxLayout):
    popup = None  # info display popup

    def on_press_button_info(self):
        app = App.get_running_app()
        try:
            if not bool(app.meta):
                with youtube_dl.YoutubeDL(app.ydl_opts) as ydl:
                    app.meta = ydl.extract_info(app.url, download=False)

            self.popup = InfoDisplayPopup(app.meta)
            self.popup.open()
        except Exception as inst:
            print('Exception: ' + str(inst))

    def on_format_select_popup_dismiss(self, url, ydl_opts, meta, instance):
        if instance.selected_format_id:
            self.start_download(
                url, {**ydl_opts, **{'format': ','.join(instance.selected_format_id)}}, meta)

    def on_press_button_download(self):
        app = App.get_running_app()
        try:
            if not bool(app.meta):
                with youtube_dl.YoutubeDL(app.ydl_opts) as ydl:
                    app.meta = ydl.extract_info(app.url, download=False)
        except Exception as e:
            print('Error while trying to extract info: ' + str(e))
            return

        format_method = app.config.get('general', 'method')
        if format_method == 'Ask':
            self.popup = FormatSelectPopup(app.meta)
            callback = partial(self.on_format_select_popup_dismiss,
                               app.url, app.ydl_opts, app.meta)
            self.popup.bind(on_dismiss=callback)
            self.popup.open()

        else:
            self.start_download(app.url, app.ydl_opts, app.meta)

    def start_download(self, url, ydl_opts, meta):
        index = len(self.ids.rv.data)

        # Add UI status bar for this download
        self.ids.rv.data.append({'url': url,
                                 'index': index,
                                 'log': '',
                                 'title': meta['title'],
                                 'status': STATUS_IN_PROGRESS})

        # Create a logger
        ydl_opts['logger'] = YdlLogger(self.ids.rv, index)

        # Run youtube-dl in a thread so the UI do not freeze
        t = DownloaderThread(url, ydl_opts, self.ids.rv.data[-1])
        t.start()


class RootLayout(Label):
    pass


class StatusIcon(Label):
    status = NumericProperty(1)


class DownloaderApp(App):
    meta = DictProperty()
    ydl_opts = DictProperty()
    url = StringProperty()
    filetmpl = '%(title)s_%(format)s.%(ext)s'

    def get_output_dir(self):
        if platform == 'android':
            return os.getenv('EXTERNAL_STORAGE')
        return expanduser("~")

    def build_config(self, config):
        config.setdefaults('general', {
            'method': 'Preset',
            'custom': 'best',
            'preset': 'best',
            'quiet': False,
            'nowarning': False,
            'ignoreerrors': False,
            'call_home': False,
            'nocheckcertificate': False,
            'prefer_insecure': platform == 'android',
            'outtmpl': join(self.get_output_dir(), self.filetmpl),
            'savedir': self.get_output_dir()
        })

    def build_settings(self, settings):
        settings.add_json_panel('general', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        if(key == 'savedir'):
            self.ydl_opts['outtmpl'] = join(value, self.filetmpl)
        elif(key == 'preset' or (key == 'method' and value == 'Preset')):
            self.ydl_opts['format'] = self.config.get(
                'general', 'preset')
        elif(key == 'custom' or (key == 'method' and value == 'Custom')):
            self.ydl_opts['format'] = self.config.get(
                'general', 'custom')
        elif key == 'method' and value == 'Ask':
            self.ydl_opts.pop('format', None)
        else:
            self.ydl_opts[key] = value

    def build(self):
        if platform == 'android' and not check_permission('android.permission.WRITE_EXTERNAL_STORAGE'):
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

        self.ydl_opts['quiet'] = self.config.get('general', 'quiet')
        self.ydl_opts['nowarning'] = self.config.get('general', 'nowarning')
        self.ydl_opts['ignoreerrors'] = self.config.get(
            'general', 'ignoreerrors')
        self.ydl_opts['call_home'] = self.config.get('general', 'call_home')
        self.ydl_opts['nocheckcertificate'] = self.config.get(
            'general', 'nocheckcertificate')
        self.ydl_opts['prefer_insecure'] = self.config.get(
            'general', 'prefer_insecure')
        self.ydl_opts['outtmpl'] = join(
            self.config.get('general', 'savedir'), self.filetmpl)

        if self.config.get('general', 'method') == 'Preset':
            self.ydl_opts['format'] = self.config.get(
                'general', 'preset')
        elif self.config.get('general', 'method') == 'Custom':
            self.ydl_opts['format'] = self.config.get(
                'general', 'custom')

        self.use_kivy_settings = False
        return RootLayout()


if __name__ == '__main__':
    DownloaderApp().run()
