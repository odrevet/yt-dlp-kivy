[app]

title = youtube-dl Kivy

# (str) Package name
package.name = youtube_dl_kivy

# (str) Package domain (needed for android/ios packaging)
package.domain = fr.odrevet

# (str) Source code where the main.py live
source.dir = src

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# (list) Application requirements
# comma seperated e.g. requirements = sqlite3,kivy
requirements = enum34,openssl,requests,youtube-dl,kivy

# (str) Supported orientation (one of landscape, portrait or all)
orientation = all

fullscreen = 0

android.permissions = INTERNET


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
