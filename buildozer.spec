[app]
title = Touch Grass Simulator
package.name = touchgrasssim
package.domain = org.zhvan
source.dir = .
source.include_exts = py,png,jpg,ttf,wav,mp3,json
source.include_dirs = Backgrounds, Cutscenes, Other
version = 1.0

requirements = python3, pygame

orientation = landscape
fullscreen = 1

android.api = 33
android.minapi = 21
android.sdk_build_tools_version = 33.0.0
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

p4a.bootstrap = sdl2

android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.archs = arm64-v8a, armeabi-v7a

android.entrypoint = main.py

[buildozer]
log_level = 1
warn_on_root = 1
