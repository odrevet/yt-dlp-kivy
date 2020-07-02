class YdlLogger(object):
   rv = None

   def __init__(self, rv, index):
      self.rv = rv
      self.index = index

   def debug(self, msg):
      self.rv.data[self.index]['log'] += f"{msg}\n"
      self.rv.refresh_from_data()

   def warning(self, msg):
      self.rv.data[self.index]['log'] += f"[color=ffff00]{msg}[/color]\n"
      self.rv.refresh_from_data()

   def error(self, msg):
      self.rv.data[self.index]['log'] += f"[color=ff0000]{msg}[/color]\n"
      self.rv.refresh_from_data()

def ydl_progress_hook(d):
   if d['status'] == 'finished':
      print('Done downloading')