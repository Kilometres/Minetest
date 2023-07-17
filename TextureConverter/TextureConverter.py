#!/usr/bin/env python
import shutil, csv, os, tempfile, sys, getopt, json
from math import floor
appname = "TextureConverter.py"

base_dir = None

dry_run = False
forceDelete = False
verbose = False

PXSIZE = 16

syntax_help = appname+""" -i <input dir> [-s size] [-d] [-v] [-h] 
Mandatory argument:
-i <input directory>
	Directory of Minecraft resource pack to convert

Optional arguments:
-s <texture size>
	(Size) Specify the size (in pixels) of the original textures (default: 16)
-d
	(Dry) Just pretend to convert 1:1 textures and just print output, but only crop and compose non-1:1 textures.
-v
	(Verbose) Print out all copying actions of 1:1 textures.
-f
	(Force) Removes the existing converted pack foldfolder.
-h
	(Help) Show this help and exit"""
try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:s:dvf")
except getopt.GetoptError:
	print(
"""ERROR! The options you gave me make no sense!

Here's the syntax reference:""")
	print(syntax_help)
	sys.exit(2)
for opt, arg in opts:
	if opt == "-h":
		print(
"""This is an unofficial MineClone2 Texture Converter.
This will convert textures from Minecraft resource packs (or default assets) to a Minetest texture pack.

Supported Minecraft version: 1.20 (Java Edition)

Syntax:""")
		print(syntax_help)
		sys.exit()
	elif opt == "-d":
		dry_run = True
	elif opt == "-v":
		verbose = True
	elif opt == "-f":
		forceDelete = True
	elif opt == "-i":
		base_dir = arg
		if arg.find(' ') != -1:
			print("Spaces not supported in file name, use underscores '_' instead.")
			sys.exit(2)
	elif opt == "-s":
		PXSIZE = int(arg)

if base_dir == None:
	print(
"""\x1b[1;31mERROR: No input path specified\x1b[0m

Try: """+appname+""" \x1b[0;36m-i <path to resource pack>\x1b[0m -p <texture size>

For the full help, use: """+appname+""" -h""")
	sys.exit(2);


tex_dir = os.path.normpath(base_dir + "/assets/minecraft/textures")

out_name = os.path.basename(base_dir) + '_Converted' #todo use path join
out_dir = os.path.normpath(base_dir + '/../' + out_name)

if os.path.isdir(out_dir):
	if forceDelete:
		shutil.rmtree(out_dir)
	else:
		print("\x1b[1;33mFolder already exists at output directory:\x1b[0m "+out_dir+"\nUse the \x1b[1;36m-f\x1b[0m flag to override.")
		sys.exit(2);
	

# FUNCTION DEFINITIONS
def colorize(colormap, source, colormap_pixel, texture_size, destination):
	os.system("magick convert "+colormap+" -crop 1x1+"+colormap_pixel+" -depth 8 -resize "+texture_size+"x"+texture_size+" "+tempfile1.name+".png")
	os.system("magick composite -compose Multiply "+tempfile1.name+".png "+source+" "+destination)

def colorize_alpha(colormap, source, colormap_pixel, texture_size, destination):
	colorize(colormap, source, colormap_pixel, texture_size, tempfile2.name+".png")
	os.system("magick composite -compose Dst_In "+source+" "+tempfile2.name+".png -alpha Set "+destination)

def convert_textures_csv():
	with open("Kilo_Conversion_Table_1.20.csv", newline="") as csvfile:
		reader = csv.reader(csvfile, delimiter=",", quotechar='"')

		first_row = True
		for row in reader:
			# Skip first row
			if first_row:
				first_row = False
				continue

			src_dir = row[0]
			src_filename = row[1]
			dst_filename = row[2]
			if row[3] != "":
				xs = row[3]
				ys = row[4]
				xl = row[5]
				yl = row[6]
			else:
				xs = None
			blacklisted = row[7]

			if blacklisted == "y":
				# Skip blacklisted files
				continue

			src_file = base_dir + src_dir + "/" + src_filename # source file
			src_file_exists = os.path.isfile(src_file)
			dst_file = out_dir + "/" + dst_filename # destination file

			if src_file_exists == False:
				print(f"\x1b[1;33mWARNING: Source file does not exist: {src_file}\x1b[0m")
				continue

			if xs != None:
				# Crop and copy images
				if not dry_run:
					os.system("magick convert \""+src_file+"\" -crop "+xl+"x"+yl+"+"+xs+"+"+ys+" \""+dst_file+"\"")
				if verbose:
					print(src_file + " → " + dst_file)
			else:
				# Copy image verbatim
				if not dry_run:
					shutil.copy2(src_file, dst_file)
				if verbose:
					print(src_file + " → " + dst_file)

def convert_map():
	map_background_file = tex_dir + "/map/map_background.png"
	if os.path.isfile(map_background_file):
		os.system("convert \"" + map_background_file + "\" -interpolate Integer -filter point -resize \"140x140\" \"" + out_dir + "/mcl_maps_map_background.png\"")

def convert_armor():
	armor_files = [
		[ tex_dir + "/models/armor/leather_layer_1.png", tex_dir + "/models/armor/leather_layer_2.png", out_dir, "mcl_armor_helmet_leather.png", "mcl_armor_chestplate_leather.png", "mcl_armor_leggings_leather.png", "mcl_armor_boots_leather.png" ],
		[ tex_dir + "/models/armor/chainmail_layer_1.png", tex_dir + "/models/armor/chainmail_layer_2.png", out_dir, "mcl_armor_helmet_chain.png", "mcl_armor_chestplate_chain.png", "mcl_armor_leggings_chain.png", "mcl_armor_boots_chain.png" ],
		[ tex_dir + "/models/armor/gold_layer_1.png", tex_dir + "/models/armor/gold_layer_2.png", out_dir, "mcl_armor_helmet_gold.png", "mcl_armor_chestplate_gold.png", "mcl_armor_leggings_gold.png", "mcl_armor_boots_gold.png" ],
		[ tex_dir + "/models/armor/iron_layer_1.png", tex_dir + "/models/armor/iron_layer_2.png", out_dir, "mcl_armor_helmet_iron.png", "mcl_armor_chestplate_iron.png", "mcl_armor_leggings_iron.png", "mcl_armor_boots_iron.png" ],
		[ tex_dir + "/models/armor/diamond_layer_1.png", tex_dir + "/models/armor/diamond_layer_2.png", out_dir, "mcl_armor_helmet_diamond.png", "mcl_armor_chestplate_diamond.png", "mcl_armor_leggings_diamond.png", "mcl_armor_boots_diamond.png" ],
        [ tex_dir + "/models/armor/netherite_layer_1.png", tex_dir + "/models/armor/netherite_layer_2.png", out_dir, "mcl_armor_helmet_netherite.png", "mcl_armor_chestplate_netherite.png", "mcl_armor_leggings_netherite.png", "mcl_armor_boots_netherite.png" ]
	]
	for a in armor_files:
		APXSIZE = 16	# for some reason MineClone2 requires this
		layer_1 = a[0]
		layer_2 = a[1]
		adir = a[2]
		if os.path.isfile(layer_1):
			helmet = "\""+adir + "/" + a[3]+"\""
			chestplate = "\""+adir + "/" + a[4]+"\""
			boots = "\""+adir + "/" + a[6]+"\""
			os.system("magick convert -size "+str(APXSIZE * 4)+"x"+str(APXSIZE * 2)+" xc:none ( "+layer_1+" -scale "+str(APXSIZE * 4)+"x"+str(APXSIZE * 2)+" -geometry +"+str(APXSIZE * 2)+"+0 -crop "+str(APXSIZE * 2)+"x"+str(APXSIZE)+"+0+0 ) -composite -channel A -fx \"(a > 0.0) ? 1.0 : 0.0\" "+helmet)
			os.system("magick convert -size "+str(APXSIZE * 4)+"x"+str(APXSIZE * 2)+" xc:none ( "+layer_1+" -scale "+str(APXSIZE * 4)+"x"+str(APXSIZE * 2)+" -geometry +"+str(APXSIZE)+"+"+str(APXSIZE)+" -crop "+str(APXSIZE * 2.5)+"x"+str(APXSIZE)+"+"+str(APXSIZE)+"+"+str(APXSIZE)+" ) -composite -channel A -fx \"(a > 0.0) ? 1.0 : 0.0\" "+chestplate)
			os.system("magick convert -size "+str(APXSIZE * 4)+"x"+str(APXSIZE * 2)+" xc:none ( "+layer_1+" -scale "+str(APXSIZE * 4)+"x"+str(APXSIZE * 2)+" -geometry +0+"+str(APXSIZE)+" -crop "+str(APXSIZE)+"x"+str(APXSIZE)+"+0+"+str(APXSIZE)+" ) -composite -channel A -fx \"(a > 0.0) ? 1.0 : 0.0\" "+boots)
		if os.path.isfile(layer_2):
			leggings = adir + "/" + a[5]
			os.system("magick convert -size "+str(APXSIZE * 4)+"x"+str(APXSIZE * 2)+" xc:none ( "+layer_2+" -scale "+str(APXSIZE * 4)+"x"+str(APXSIZE * 2)+" -geometry +0+"+str(APXSIZE)+" -crop "+str(APXSIZE * 2.5)+"x"+str(APXSIZE)+"+0+"+str(APXSIZE)+" ) -composite -channel A -fx \"(a > 0.0) ? 1.0 : 0.0\" "+leggings)

def convert_rails():
	rails = [
		# (Straigt src, curved src, t-junction dest, crossing dest)
		("rail.png", "rail_corner.png", "default_rail_t_junction.png", "default_rail_crossing.png"),
		("powered_rail.png", "rail_corner.png", "carts_rail_t_junction_pwr.png", "carts_rail_crossing_pwr.png"),
		("powered_rail_on.png", "rail_corner.png", "mcl_minecarts_rail_golden_t_junction_powered.png", "mcl_minecarts_rail_golden_crossing_powered.png"),
		("detector_rail.png", "rail_corner.png", "mcl_minecarts_rail_detector_t_junction.png", "mcl_minecarts_rail_detector_crossing.png"),
		("detector_rail_on.png", "rail_corner.png", "mcl_minecarts_rail_detector_t_junction_powered.png", "mcl_minecarts_rail_detector_crossing_powered.png"),
		("activator_rail.png", "rail_corner.png", "mcl_minecarts_rail_activator_t_junction.png", "mcl_minecarts_rail_activator_crossing.png"),
		("activator_rail_on.png", "rail_corner.png", "mcl_minecarts_rail_activator_d_t_junction.png", "mcl_minecarts_rail_activator_powered_crossing.png"),
	]
	for r in rails:
		os.system("magick composite -compose dst-over "+tex_dir+"/block/"+r[0]+" "+tex_dir+"/block/"+r[1]+" "+out_dir+"/"+r[2])
		os.system("magick convert "+tex_dir+"/block/"+r[0]+" -rotate 90 "+tempfile1.name+".png")
		os.system("magick composite -compose dst-over "+tempfile1.name+".png "+tex_dir+"/block/"+r[0]+" "+out_dir+"/"+r[3])

def convert_banner_overlays():
	overlays = [
		"base",
		"border",
		"bricks",
		"circle",
		"creeper",
		"cross",
		"curly_border",
		"diagonal_left",
		"diagonal_right",
		"diagonal_up_left",
		"diagonal_up_right",
		"flower",
		"gradient",
		"gradient_up",
		"half_horizontal_bottom",
		"half_horizontal",
		"half_vertical",
		"half_vertical_right",
		"rhombus",
		"mojang",
		"skull",
		"small_stripes",
		"straight_cross",
		"stripe_bottom",
		"stripe_center",
		"stripe_downleft",
		"stripe_downright",
		"stripe_left",
		"stripe_middle",
		"stripe_right",
		"stripe_top",
		"square_bottom_left",
		"square_bottom_right",
		"square_top_left",
		"square_top_right",
		"triangle_bottom",
		"triangles_bottom",
		"triangle_top",
		"triangles_top",
	]
	for o in overlays:
		orig = tex_dir + "/entity/banner/" + o + ".png"
		if os.path.isfile(orig):
			if o == "mojang":
				o = "thing"
			dest = out_dir+"/"+"mcl_banners_"+o+".png"
			os.system("magick convert "+orig+" -transparent-color white -background black -alpha remove -alpha copy -channel RGB -white-threshold 0 "+dest)

def convert_foliage():
	FOLIAGE = tex_dir+"/colormap/foliage.png"
	GRASS = tex_dir+"/colormap/grass.png"


	# Leaves
	colorize_alpha(FOLIAGE, tex_dir+"/block/oak_leaves.png", "116+143", str(PXSIZE), out_dir+"/default_leaves.png")
	colorize_alpha(FOLIAGE, tex_dir+"/block/dark_oak_leaves.png", "158+177", str(PXSIZE), out_dir+"/mcl_core_leaves_big_oak.png")
	colorize_alpha(FOLIAGE, tex_dir+"/block/acacia_leaves.png", "40+255", str(PXSIZE), out_dir+"/default_acacia_leaves.png")
	colorize_alpha(FOLIAGE, tex_dir+"/block/spruce_leaves.png", "226+230", str(PXSIZE), out_dir+"/mcl_core_leaves_spruce.png")
	colorize_alpha(FOLIAGE, tex_dir+"/block/birch_leaves.png", "141+186", str(PXSIZE), out_dir+"/mcl_core_leaves_birch.png")
	colorize_alpha(FOLIAGE, tex_dir+"/block/jungle_leaves.png", "16+39", str(PXSIZE), out_dir+"/default_jungleleaves.png")
	colorize_alpha(FOLIAGE, tex_dir+"/block/mangrove_leaves.png", "90+234", str(PXSIZE), out_dir+"/mcl_mangrove_leaves.png")

	# Waterlily
	#colorize_alpha(FOLIAGE, tex_dir+"/block/lily_pad.png", "16+39", str(PXSIZE), out_dir+"/flowers_waterlily.png") #todo mcl text no longer exists

	# Vines
	colorize_alpha(FOLIAGE, tex_dir+"/block/vine.png", "16+39", str(PXSIZE), out_dir+"/mcl_core_vine.png")

	# Tall grass, fern (inventory images)
	pcol = "50+173" # Plains grass color
	colorize_alpha(GRASS, tex_dir+"/block/grass.png", pcol, str(PXSIZE), out_dir+"/mcl_flowers_tallgrass_inv.png")
	colorize_alpha(GRASS, tex_dir+"/block/fern.png", pcol, str(PXSIZE), out_dir+"/mcl_flowers_fern_inv.png")
	colorize_alpha(GRASS, tex_dir+"/block/large_fern_top.png", pcol, str(PXSIZE), out_dir+"/mcl_flowers_double_plant_fern_inv.png")
	colorize_alpha(GRASS, tex_dir+"/block/large_fern_bottom.png", pcol, str(PXSIZE), out_dir+"/mcl_flowers_double_plant_grass_inv.png")


	os.system(f"magick convert -size 16x16 xc:transparent {out_dir}/mcl_dirt_grass_shadow.png")

def convert_grass_palettes():
	GRASS = tex_dir+"/colormap/grass.png"

	# Convert grass palette: https://minecraft.fandom.com/wiki/Tint
	grass_colors = [
		# [Coords or #Color, AdditionalTint], # Index - Minecraft biome name (MineClone2 biome names)
		["50+173"], # 0 - Plains (flat, Plains, Plains_beach, Plains_ocean, End)
		["0+255"], # 1 - Savanna (Savanna, Savanna_beach, Savanna_ocean)
		["255+255"], # 2 - Ice Spikes (IcePlainsSpikes, IcePlainsSpikes_ocean)
		["255+255"], # 3 - Snowy Taiga (ColdTaiga, ColdTaiga_beach, ColdTaiga_beach_water, ColdTaiga_ocean)
		["178+193"], # 4 - Giant Tree Taiga (MegaTaiga, MegaTaiga_ocean)
		["178+193"], # 5 - Giant Tree Taiga (MegaSpruceTaiga, MegaSpruceTaiga_ocean)
		["203+239"], # 6 - Montains (ExtremeHills, ExtremeHills_beach, ExtremeHills_ocean)
		["203+239"], # 7 - Montains (ExtremeHillsM, ExtremeHillsM_ocean)
		["203+239"], # 8 - Montains (ExtremeHills+, ExtremeHills+_snowtop, ExtremeHills+_ocean)
		["50+173"], # 9 - Beach (StoneBeach, StoneBeach_ocean)
		["255+255"], # 10 - Snowy Tundra (IcePlains, IcePlains_ocean)
		["50+173"], # 11 - Sunflower Plains (SunflowerPlains, SunflowerPlains_ocean)
		["191+203"], # 12 - Taiga (Taiga, Taiga_beach, Taiga_ocean)
		["76+112"], # 13 - Forest (Forest, Forest_beach, Forest_ocean)
		["76+112"], # 14 - Flower Forest (FlowerForest, FlowerForest_beach, FlowerForest_ocean)
		["101+163"], # 15 - Birch Forest (BirchForest, BirchForest_ocean)
		["101+163"], # 16 - Birch Forest Hills (BirchForestM, BirchForestM_ocean)
		["0+255"], # 17 - Desert and Nether (Desert, Desert_ocean, Nether)
		["76+112", "#28340A"], # 18 - Dark Forest (RoofedForest, RoofedForest_ocean)
		["#90814d"], # 19 - Mesa (Mesa, Mesa_sandlevel, Mesa_ocean, )
		["#90814d"], # 20 - Mesa (MesaBryce, MesaBryce_sandlevel, MesaBryce_ocean)
		["#90814d"], # 21 - Mesa (MesaPlateauF, MesaPlateauF_grasstop, MesaPlateauF_sandlevel, MesaPlateauF_ocean)
		["#90814d"], # 22 - Mesa (MesaPlateauFM, MesaPlateauFM_grasstop, MesaPlateauFM_sandlevel, MesaPlateauFM_ocean)
		["0+255"], # 23 - Shattered Savanna (or Savanna Plateau ?) (SavannaM, SavannaM_ocean)
		["12+36"], # 24 - Jungle (Jungle, Jungle_shore, Jungle_ocean)
		["12+36"], # 25 - Modified Jungle (JungleM, JungleM_shore, JungleM_ocean)
		["12+61"], # 26 - Jungle Edge (JungleEdge, JungleEdge_ocean)
		["12+61"], # 27 - Modified Jungle Edge (JungleEdgeM, JungleEdgeM_ocean)
		["#6A7039"], # 28 - Swamp (Swampland, Swampland_shore, Swampland_ocean)
		["25+25"], # 29 - Mushroom Fields and Mushroom Field Shore (MushroomIsland, MushroomIslandShore, MushroomIsland_ocean)
	]

	grass_palette_file = out_dir + "/mcl_core_palette_grass.png"
	os.system("magick convert -size 16x16 canvas:transparent " + grass_palette_file)

	for i, color in enumerate(grass_colors):
		if color[0][0] == "#":
			os.system("magick convert -size 1x1 xc:\"" + color[0] + "\" " + tempfile1.name + ".png")
		else:
			os.system("magick convert " + GRASS + " -crop 1x1+" + color[0] + " " + tempfile1.name + ".png")

		if len(color) > 1:
			os.system("magick convert " + tempfile1.name + ".png ( -size 1x1 xc:\"" + color[1] + "\" ) -compose blend -define compose:args=50,50 -composite " + tempfile1.name + ".png")

		os.system("magick convert " + grass_palette_file + " -set colorspace sRGB ( " + tempfile1.name + ".png -geometry +" + str(i % 16) + "+" + str(int(i / 16)) + " ) -composite " + grass_palette_file)


def translate_metadata():
	with open(base_dir+'/pack.mcmeta') as json_file:
		mcmeta = json.load(json_file)

	meta = f"""name = KILO_{'_'.join(out_name.split(' ')).upper()}
title = {' '.join(out_name.split('_'))}
description = {mcmeta['pack']['description']}"""
	meta_file = open(out_dir + "/texture_pack.conf", "w")
	meta_file.write(meta)
	meta_file.close()

	os.system("magick convert -size 300x200 canvas:transparent \""+out_dir + "/screenshot.png\"")
	os.system("magick composite \""+base_dir+"/pack.png\" \""+out_dir + "/screenshot.png\" -gravity center \""+out_dir + "/screenshot.png\"") #todo: account for res

def convert_signs():
	os.system("magick convert \""+tex_dir+"/item/oak_sign.png\" -set colorspace Gray   \""+out_dir+"/mcl_signs_default_sign_greyscale.png\"")
	os.system("magick convert \""+tex_dir+"/entity/signs/oak.png\" -set colorspace Gray   \""+out_dir+"/mcl_signs_sign_greyscale.png\"")

def convert_sign_font():
	ascii_file = tex_dir+"/font/ascii.png"

	ascii_chars = [
		       1    , 2    , "_hs", "_dl", "_pr", "_am", 3    , 4    , 5    , 6    , "_ps", 7    , "_mn", 8    , "_dv",
		"_0" , "_1" , "_2" , "_3" , "_4" , "_5" , "_6" , "_7" , "_8" , "_9" , 9    , 10   , "_lt", "_eq", "_gt", "_qu",
		11, "_a_", "_b_", "_c_", "_d_", "_e_", "_f_", "_g_", "_h_", 12   , "_j_", "_k_", "_l_", "_m_", "_n_", "_o_",
		"_p_", "_q_", "_r_", "_s_", "_t_", "_u_", "_v_", "_w_", "_x_", "_y_", "_z_", 13   , "_re", 14   , "_ca", "_un",
		15   , "_a" , "_b" , "_c" , "_d" , "_e" , 16 , "_g" , "_h" , 17   , "_j" , "_k" , 18   , "_m" , "_n" , "_o" ,
		"_p" , "_q" , "_r" , "_s" , 19 , "_u" , "_v" , "_w" , "_x" , "_y" , "_z" , 20   , 21   , 22   , 23
	]
	ascii_nonuniform_chars = [
		["_ex", 1], ["_qo", 3], ["_ap", 1], ["_bl", 3], ["_br", 3], ["_as", 3], ["_cm", 1], ["_dt", 1],
		["_co", 1], ["_sm", 1],
		["_at", 6], ["_i_", 3],
		["_sl", 3], ["_sr", 3],
		["_gr", 2], ["_f", 4], ["_i", 1], ["_l", 2],
		["_t", 3], ["_cl", 3], ["_vb", 1], ["_cr", 3], ["_tl", 6],
	]

	for i in range(len(ascii_chars)):
		char = ascii_chars[i]
		width = "5"
		filename = char
		if type(char) == int:
			width = str(ascii_nonuniform_chars[char-1][1])
			filename = ascii_nonuniform_chars[char-1][0]
		filename += ".png"
		sprite = i+1
		texturex = str( (sprite%16)*8 )
		texturey = str( floor(sprite/16)*8 + 16 )
		if int(width) < 5:
			os.system("magick convert -size 5x8 canvas:transparent \""+out_dir + "/"+filename+"\"")
			os.system("magick convert \""+ascii_file+"\" -crop "+width+"x8"+"+"+texturex+"+"+texturey+" \""+tempfile1.name+".png\"")
			os.system("magick composite \""+tempfile1.name+".png\" \""+out_dir + "/"+filename+"\" -gravity center \""+out_dir + "/"+filename+"\"")
		else:
			os.system("magick convert \""+ascii_file+"\" -crop "+width+"x8"+"+"+texturex+"+"+texturey+" \""+out_dir+"/"+filename+"\"")

def convert_hud():
	icons_file = tex_dir+"/gui/icons.png"

	hud_icons = [
		[
			["hbarmor_bgicon.png", 16, 9, 9, 9],
			["hbarmor_icon.png", 34, 9, 9, 9]
		],
		[
			["hudbars_bgicon_health.png", 16, 0, 9, 9],
			["hudbars_icon_health.png", 52, 0, 9, 9],
			["hbhunger_icon_health_poison.png", 88, 0, 9, 9]
		],
		[
			["hbhunger_bgicon.png", 16, 27, 9, 9],
			["hbhunger_icon.png", 52, 27, 9, 9],
			["mcl_hunger_icon_foodpoison.png", 88, 27, 9, 9]
		]
	]

	for icon_set in hud_icons:
		bg = icon_set[0]
		os.system(f"magick convert \"{icons_file}\" -crop {bg[3]}x{bg[4]}+{bg[1]}+{bg[2]} \"{out_dir}/{bg[0]}\"")

		for i in range (1, len(icon_set)):
			icon = icon_set[i]
			os.system(f"magick convert \"{icons_file}\" -crop {icon[3]}x{icon[4]}+{icon[1]}+{icon[2]} \"{out_dir}/{icon[0]}\"")
			os.system(f"magick composite -compose dst-over \"{out_dir}/{bg[0]}\" \"{out_dir}/{icon[0]}\" \"{out_dir}/{icon[0]}\"")
	
	os.system(f"magick convert \"{icons_file}\" -crop 182x5+0+64 -rotate 90 \"{out_dir}/mcl_experience_bar_background.png\"")
	os.system(f"magick convert \"{icons_file}\" -crop 182x5+0+69 -rotate 90 \"{out_dir}/mcl_experience_bar.png\"")

	os.system(f"magick convert \"{icons_file}\" -crop 16x16+0x0 -scale 300% \"{out_dir}/crosshair.png\"")


def patch_chests():
	chest_sections = [ #width, height, x1, y1
		[28, 14, 14, 0 ],
		[14, 5 , 0 , 14],
		[42, 5 , 14, 14],
		[28, 14, 14, 19],
		[14, 10, 0 , 33],
		[42, 10, 14, 33]
	]

	single_chests = [
		"mcl_chests_normal.png", "mcl_chests_trapped.png", "mcl_chests_ender.png", "mcl_chests_normal_present.png", "mcl_chests_trapped_present.png", "mcl_chests_ender_present.png"
	]

	for single_chest in single_chests:
		chest_path = out_dir+"/"+single_chest
		for sec in chest_sections:
			os.system(f"magick convert -crop {sec[0]}x{sec[1]}+{sec[2]}+{sec[3]} -rotate 180 {chest_path} {tempfile1.name}.png")
			os.system(f"magick composite {tempfile1.name}.png -geometry +{sec[2]}+{sec[3]} {chest_path} {chest_path}")

def progress_color(pos, curpos):
	if pos < curpos:
		return " ✔ \x1b[0;37m"
	elif pos == curpos:
		return " ⚙ \x1b[1;37m"
	else:
		return " - \x1b[2;37m"

def progress_list(position):
	print(f'''\x1b[10A\x1b[1;32mConverting Texture Pack:\x1b[0m
{progress_color(0, position)} 1:1 Textures\x1b[0m		{progress_color(8, position)} Sign Textures\x1b[0m
{progress_color(1, position)} Map Textures\x1b[0m		{progress_color(9, position)} Sign Font Textures\x1b[0m
{progress_color(2, position)} Armor Textures\x1b[0m		{progress_color(10, position)} Hud Textures\x1b[0m
{progress_color(3, position)} Banner Overlay Textures\x1b[0m	{progress_color(11, position)} Patch Chest Textures\x1b[0m
{progress_color(4, position)} Rail Textures\x1b[0m		
{progress_color(5, position)} Foliage Textures\x1b[0m		
{progress_color(6, position)} Palette Textures\x1b[0m		
{progress_color(7, position)} Translating Metadata\x1b[0m	
''')

def convert_textures():
	global tempfile1, tempfile2
	tempfile1 = tempfile.NamedTemporaryFile()
	tempfile2 = tempfile.NamedTemporaryFile()
	
	print("\n\n\n\n\n\n\n\n\n\n")
	progress_list(0)
	convert_textures_csv()
	progress_list(1)
	convert_map()
	progress_list(2)
	convert_armor()
	progress_list(3)
	convert_banner_overlays()
	progress_list(4)
	convert_rails()
	progress_list(5)
	convert_foliage()
	progress_list(6)
	convert_grass_palettes()
	progress_list(7)
	translate_metadata()
	progress_list(8)
	convert_signs()
	progress_list(9)
	convert_sign_font()
	progress_list(10)
	convert_hud()
	progress_list(11)
	patch_chests()
	progress_list(12)

	if dry_run:
		shutil.rmtree(out_dir)
	
	tempfile1.close()
	tempfile2.close()


# ENTRY POINT
os.mkdir(out_dir)

convert_textures()

print("\x1b[1;32mFinished Converting Texture Pack\x1b[0m")
print("\n\x1b[0;33mREMINDER: This is a work-in-progress tool and may misrepresent textures.\x1b[0m")
print(f"\x1b[0;33mREMINDER: If you see any \x1b[1;36mmissing or misrepresented textures\x1b[0;33m please open an issue on the github (\x1b[0;36mhttps://github.com/Kilometres/Minetest\x1b[0;33m)\x1b[0m")
if not dry_run:
	print(f"\nThe texture pack can be retrieved from: \x1b[1;36m{out_dir}/\x1b[0m\n")
