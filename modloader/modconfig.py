"""This file is free software under the GPLv3 license"""
import sys
import os
import shutil

import renpy

from modloader.modinfo import get_mods


def remove_mod(mod_name):
    """Remove a mod from the game and reload.

    Args:
        mod_name (str): The internal name of the mod to be removed
    """
    mod_class = get_mods()[mod_name]
    mod_folder = mod_class.__module__
    shutil.rmtree(os.path.join(renpy.config.gamedir, "mods", mod_folder))
    print "Sucessfully removed {}, reloading".format(mod_name)
    sys.stdout.flush()
    renpy.exports.reload_script()