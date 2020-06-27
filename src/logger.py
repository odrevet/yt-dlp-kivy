class YdlLogger(object):
   log = ''

   def debug(self, msg):
      self.log += f"{msg}\n"

   def warning(self, msg):
      self.log += f"[color=ffff00]{msg}[/color]\n"

   def error(self, msg):
      self.log += f"[color=ff0000]{msg}[/color]\n"

def ydl_progress_hook(d):
   if d['status'] == 'finished':
      print('Done downloading')