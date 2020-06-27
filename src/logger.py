class YdlLogger(object):
   log = ''

   def debug(self, msg):
      self.log += msg + "\n"

   def warning(self, msg):
      self.log += msg + "\n"

   def error(self, msg):
      self.log += msg + "\n"

def ydl_progress_hook(d):
   if d['status'] == 'finished':
      print('Done downloading')