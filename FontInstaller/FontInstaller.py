#!/usr/bin/env python
import os, sys, getopt, requests

def printHelp():
		print("""Minetest Font Installer: This tool installs minecraft fonts for minetest.
Place the tool in your minetest director and run `python FontInstaller.py -i`""")



try:
	opts, args = getopt.getopt(sys.argv[1:],"i")
except getopt.GetoptError:
    printHelp()
    sys.exit(2)

install = False
for opt, arg in opts:
    if opt == "-i":
        install = True

if not install:
    printHelp()
    sys.exit(2)

if not (os.path.isdir("fonts") and os.path.exists("bin/minetest.exe") and os.path.exists("minetest.conf")):
    print("\x1b[0;33mWARNING: You're missing either: 'fonts', 'bin/minetest.exe' or 'minetest.conf', are you sure you're in your minetest directory.\x1b[0m")
    sys.exit(2)



appendedLines = [
    "font_size_divisible_by = 10"
    "font_shadow = 1",
    "font_shadow_alpha = 127",
    "fallback_font_path = ../fonts/DroidSansFallbackFull.ttf",

    "font_size = 16",
    "font_path = ../fonts/MC-Fonts/Minecraft-Regular.otf",
    "font_path_bold = ../fonts/MC-Fonts/Minecraft-Bold.otf",
    "font_path_italic = ../fonts/MC-Fonts/Minecraft-Italic.otf",
    "font_path_bold_italic = ../fonts/MC-Fonts/Minecraft-BoldItalic.otf",

    "mono_font_size = 16",
    "mono_font_size_divisible_by = 6",
    "mono_font_path = ../fonts/MC-Fonts/Minecraft-Monospace.ttf",
    "mono_font_path_bold = ../fonts/MC-Fonts/Minecraft-Monospace.ttf",
    "mono_font_path_italic = ../fonts/MC-Fonts/Minecraft-Monospace.ttf",
    "mono_font_path_bold_italic = ../fonts/MC-Fonts/Minecraft-Monospace.ttf"
]

with open("minetest.conf", "r") as file:
    lines = file.readlines()
with open("minetest.conf", "w") as file:
    for line in lines:
        if line.find('font') == -1:
            file.write(line)
    
    for line in appendedLines:
        file.write(line+'\n')



def downloadFile(url, filepath):
    dir = os.path.dirname(filepath)
    if not os.path.exists(dir):
        os.mkdir(dir)
    if os.path.exists(filepath):
         os.remove(filepath)

    resp = requests.get(url)

    with open(filepath, "wb") as file:
        file.write(resp.content)

downloadFile('https://github.com/Kilometres/Minetest','README.md')
#Monospace
downloadFile('https://github.com/IdreesInc/Monocraft/releases/download/v3.0/Monocraft-no-ligatures.ttf', 'fonts/MC-Fonts/Minecraft-Monospace.ttf')
#Minecraft
downloadFile('https://get.fontspace.co/download/font/Bmg3/YzZmODk4Y2EzMzc3NGM2MDk4OWQxNDRhZDhlNTQ2ZjAub3Rm/MinecraftRegular-Bmg3.otf', 'fonts/MC-Fonts/Minecraft-Regular.otf')
downloadFile('https://get.fontspace.co/download/font/R8Mo/YjMxYzA1ZjZhNTcxNDFiZDk2NjRmMDVmMDNkYmFmYzIub3Rm/MinecraftItalic-R8Mo.otf', 'fonts/MC-Fonts/Minecraft-Bold.otf')
downloadFile('https://get.fontspace.co/download/font/nMK1/ZWIzOTlmODUzY2E0NGE1Njk2MDE2MjQ2ZDdmYTYwMWEub3Rm/MinecraftBold-nMK1.otf', 'fonts/MC-Fonts/Minecraft-Italic.otf')
downloadFile('https://get.fontspace.co/download/font/1y1e/ZTE2NjE0ZDY2YjEyNDM2M2FiOTQ4MGQ1ZDBiMzlkYTkub3Rm/MinecraftBoldItalic-1y1e.otf', 'fonts/MC-Fonts/Minecraft-BoldItalic.otf')