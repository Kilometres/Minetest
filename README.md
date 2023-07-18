<h1 align="center"> Minetest Tools & Mods </h1>
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Minetest_logo.svg/1200px-Minetest_logo.svg.png" alt="minetest logo" width="250"/>
 <br>
    A compilation of my <a href="https://github.com/minetest/minetest">minetest</a> and <a href="https://git.minetest.land/MineClone2/MineClone2">mineclone2</a> tools, guides and mods.
</p>

### Tools
 - [Texture Pack Converter](#t-minecraft-to-minetestmineclone2-texture-pack-converter)
 - Minecraft Font Installer for Minetest
### Guides
 - Make Mineclone2 look like Minecraft
<br><br>

## [T] Minecraft to Minetest/Mineclone2 Texture Pack Converter
This is an unofficial MineClone2 Texture Converter. This will convert textures from Minecraft resource packs (or default assets) to a Minetest texture pack.

Supported Minecraft version: `1.20 (Java Edition)`
### Requirements
- Python 3.x
- [Imagemagick](https://imagemagick.org/script/download.php#windows) (use of the `magick` command)
<br><br>

### Usage
Simply run `python TextureConverter.py -i <input dir>` and the converted texture pack will be produced in the same folder as the original pack.

`python TextureConverter.py -i <input dir> [-h] [-s size] [-d] [-v]  [-f]`

|Optional Parameter|Description|
|--|--|
|-h|Show this help and exit.|
|-s \<texture size>|Specify the size (in pixels) of the original textures (default: 16).|
|-d|Dry run, don't create the texture pack but check files exist and dependencies.|
|-v|Verbose, print out all copying actions of 1:1 textures.|
|-f|Forces the removal of the existing converted pack folder.|

### Known Issues
This is a work-in-progress tool, and therefore has some known issues:
- [Texture Related Issues](https://github.com/Kilometres/Minetest/projects?query=is%3Aopen) (being fixed)
- Does not yet support texture packs with sizes other than 16x16 (planned to change)
- Can cause errors with texture packs with spaces in their names, even names that appear escaped. (fixed when move to image library)
<br><br>

## [T] Minecraft Fonts for Minetest Auto-Installer

## [G] How to make Mineclone2 look like Minecraft