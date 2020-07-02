[app]

title = youtube-dl Kivy

# (str) Package name
package.name = youtube_dl_kivy

# (str) Package domain (needed for android/ios packaging)
package.domain = fr.odrevet.youtube_dl_kivy

source.dir = .
source.include_exts = py,kv,png
source.include_patterns = img/*.png

version = 0.1

# (list) Application requirements
# comma seperated e.g. requirements = sqlite3,kivy
requirements = openssl,requests,youtube-dl,kivy

# (str) Supported orientation (one of landscape, portrait or all)
orientation = all

fullscreen = 0

icon.filename = img/app.png
presplash.filename = img/splash.png

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
