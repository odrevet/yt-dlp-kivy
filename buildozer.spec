[app]

title = yt-dlp-kivy

# (str) Package name
package.name = youtube_dl_kivy

# (str) Package domain (needed for android/ios packaging)
package.domain = fr.odrevet

source.dir = src
source.include_exts = py,kv,png,json,ini
source.include_patterns = src/img/*.png,src/downloader.ini,src/settings/*.json

version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/_version.py

# (list) Application requirements
requirements = openssl,requests,yt-dlp,kivy

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

fullscreen = 0

icon.filename = img/app.png
presplash.filename = img/splash.png

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.arch = arm64-v8a

android.release_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
