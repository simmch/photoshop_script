import os
from datetime import datetime
from tempfile import mkdtemp
import glob
from time import sleep

from photoshop import Session

###################################################
#####                                         #####
##### Split up images per type and transform  #####
#####                                         #####
##### 1. Setup BASE, DUNGEON, DESTINY, & BOSS #####                                    
#####    folders.                             #####
#####                                         #####
##### 2. Inside each folder from step 1,      #####
#####    create BASE, FOCUS, and RESOLVE      #####
#####    folders.                                           
#####
##### 3. Name images starting with tier_ and place
#####    them inside of each respective folder.
#####    Example: 2_goku_base_base.jpg
#####  
##### 4. The script will need to be ran for each
#####    specific Type and Transform of cards
#####
#####
###################################################


#### Make sure Photoshop is already open with the template loaded
#### Ask for Path to images
#### list_of_images stores the Filenames of each image in the path
directory_where_images_are = input("Enter Path to Images:\n")
list_of_images = [os.path.basename(x) for x in glob.glob(f"{directory_where_images_are}\*")]

with Session() as ps:
    #### MAKE SURE the "IMAGE HERE" layer is selected
    #### This script will not work if the IMAGE HERE layer is not selected
    replace_contents = ps.app.stringIDToTypeID("placedLayerReplaceContents")
    desc = ps.ActionDescriptor
    idnull = ps.app.charIDToTypeID("null")
    layer_set = ps.active_document.layerSets.getByName("stars")

    for image in list_of_images:
        desc.putPath(idnull, rf"{directory_where_images_are}\{image}")
        ps.app.executeAction(replace_contents, desc)
        sliced_image_name_for_tier = image.split("_")[0]
        
        # Turn all Stars off first
        for layer in layer_set.layers:
            layer.visible = False
        
        max = int(sliced_image_name_for_tier)
        min = 0
        counter = 6

        # Add Stars
        for layer in layer_set.layers:
            if min < max:
                layer.visible = True
                min = min + 1

        psd_file = rf"{directory_where_images_are}\{image}.psd"
        doc = ps.active_document
        options = ps.PhotoshopSaveOptions()
        layers = doc.artLayers
        doc.saveAs(psd_file, options, True)
        # ps.alert("Task done!")
        ps.echo(doc.activeLayer)
        # sleep(3)