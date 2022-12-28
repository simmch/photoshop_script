import os
from datetime import datetime
from tempfile import mkdtemp
import glob
from time import sleep
from elements import element_list
from photoshop import Session

###################################################
#####                                         #####
##### Split up images per type, tier, and element #
#####                                         #####
###################################################

# Filename Example
# 5_fire_nameOfCharacter.png


#### Make sure Photoshop is already open with the template file loaded
#### Ask for Path to images
#### list_of_images stores the Filenames of each image in the path
directory_where_images_are = input("Enter Path to Images:\n")
list_of_images = [os.path.basename(x) for x in glob.glob(f"{directory_where_images_are}\*")]

def hide_all_layers(layers):
    for layer in layers:
        layer.visible = False

def set_stars(layers, card_tier):
    for layer in layers:
        stars = layer.name
        if int(stars) == card_tier:
            layer.visible = True

def set_element(layers, element):
    for layer in layers:
        template = layer.name
        if template == element.upper():
            layer.visible = True

def set_name(layers, name):
    for layer in layers:
        layer.textItem.contents = name.upper()
    

with Session() as ps:
    docRef = ps.active_document
    #### MAKE SURE the "IMAGE HERE" layer is selected
    #### This script will not work if the IMAGE HERE layer is not selected
    replace_contents = ps.app.stringIDToTypeID("placedLayerReplaceContents")
    desc = ps.ActionDescriptor
    idnull = ps.app.charIDToTypeID("null")

    for image in list_of_images:
        sliced_image_name_for_tier = image.split("_")[0]
        sliced_image_name_for_element = image.split("_")[1].upper()
        sliced_image_name_for_nameOfCharacter = image.split("_")[2].upper()
        character = sliced_image_name_for_nameOfCharacter.split(".")[0] # Remove the . from the file name to get just the name

        # Edit the Card Name
        text_layer = docRef.layerSets.getByName("NAME")
        set_name(text_layer.layers, character)

        layer_set = docRef.layerSets.getByName("STARS")
        desc.putPath(idnull, rf"{directory_where_images_are}\{image}")
        ps.app.executeAction(replace_contents, desc)

        
        # Turn all Stars off first
        hide_all_layers(layer_set.layers)
        
        # Add Stars
        set_stars(layer_set.layers, int(sliced_image_name_for_tier))

        # Set active layer as Templates
        layer_set = docRef.layerSets.getByName("TEMPLATES")
        
        # Turn off all Elements
        hide_all_layers(layer_set.layers)

        # Set Element
        set_element(layer_set.layers, sliced_image_name_for_element)

        psd_file = rf"{directory_where_images_are}\{image}.psd"
        doc = ps.active_document
        options = ps.PhotoshopSaveOptions()
        layers = doc.artLayers
        doc.saveAs(psd_file, options, True)
        # ps.alert("Task done!")
        ps.echo(doc.activeLayer)
        # sleep(3)