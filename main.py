import subprocess
import sys
import os
import glob
import shutil
import traceback
import time

# Stats
total_conversions = 0
start_time = time.time()

# Important Variables
dir_wkitCLI = os.getcwd() + "\\wkitCLI\\WolvenKit.CLI.exe "   
# dir_wkitCLI = os.getcwd() + "\\cp77tools\\CP77Tools.exe "     # Backup - slower but most reliable
dir_input_packed = os.getcwd() + "\input_packed"
dir_output_packed = os.getcwd() + "\output_packed"
dir_output_unbundled = os.getcwd() + "\output_unbundled"
dir_structures = os.getcwd() + "\structures"
dir_tempfiles = os.getcwd() + "\\tempfiles"
cmd_pack = "pack -p "
cmd_unbundle = "unbundle -p "

loconame_panam_stand = "wa_panam_unarmed_locomotion_relaxed.anims"
loconame_genfem_crouch = "wa_gang_unarmed_locomotion_stealth.anims"


def unbundler():
    wkit_command = dir_wkitCLI + cmd_unbundle + '"' + \
        dir_input_packed + '" -o ' + '"' + dir_output_unbundled + '"'
    print(wkit_command)

    try:
        p = subprocess.Popen(
            ["powershell.exe", wkit_command], stdout=sys.stdout)
        p.communicate()
        print("Unbundle completed successfully.")
    except:
        print("Error during unbundle")
        return


def packer():
    for folder in os.listdir(dir_tempfiles):
        folder_path = os.getcwd() + "\\" + "tempfiles\\" + folder
        wkit_command = dir_wkitCLI + cmd_pack + '"' + folder_path + '"'

        try:
            p = subprocess.Popen(
                ["powershell.exe", wkit_command], stdout=sys.stdout)
            p.communicate()

        except:
            print("Packing Error: WolvenKit failed to pack " + folder)

    # Copy archives to output_packed
    archives = glob.glob(dir_tempfiles + "/*.archive")
    try:
        for archive_path in archives:
            shutil.copy(archive_path, dir_output_packed)
    except:
        print("Packing Error: Error during transfer of files")

    # Delete archives from tempfiles
    archives = glob.glob(dir_tempfiles + "/*.archive")
    try:
        for archive_path in archives:
            os.remove(archive_path)
    except:
        print("Packing Error: Error during deletion of tempfiles content")


def npc_folder_builder(panam_folder):
    # First check if the folder already exists. If it does, delete it so we can start fresh
    if os.path.isdir(panam_folder):
        print("Note: Folder already exists (perhaps from a previous session). Overwriting contents...")
        shutil.rmtree(panam_folder, ignore_errors=True)

    try:
        src_path = os.getcwd() + "\\structures\\npc_panam"
        shutil.copytree(src_path, panam_folder, dirs_exist_ok=True)
    except:
        print("Locomotion Extraction Error when building NPC folder")


def anim_copy(src_path, panam_folder, locomotion_type):
    # Copy anim to Panam folder and rename
    try:
        dst_path = panam_folder
        # dst_path = panam_folder + "\\base\\animations\\npc\\main_characters\\panam\\locomotion"
        shutil.copy(src_path, dst_path)
        os.rename(dst_path + "\\ui_female.anims",
                  dst_path + "\\" + locomotion_type)
        print("Successfully converted locomotion to Panam locomotion!")
    except:
        traceback.print_exc()
        print("Locomotion Extraction Error when copying animation file")


def locomotion_convertor():
    global total_conversions
    for folder in os.listdir(dir_output_unbundled):
        # Extract locomotion
        path_to_anim = dir_output_unbundled + "\\" + folder + \
            "\\base\\animations\\ui\\female\\ui_female.anims"

        # Build Panam folders
        panam_folder_stand = os.getcwd() + "\\tempfiles\\" + "0_namPOSE_S_" + folder
        panam_folder_crouch = os.getcwd() + "\\tempfiles\\" + "0_namPOSE_C_" + folder
        npc_folder_builder(panam_folder_stand)
        npc_folder_builder(panam_folder_crouch)

        # Copy anim to Panam folders and rename
        loc_path_stand = "\\base\\animations\\npc\\main_characters\\panam\\locomotion"
        loc_path_crouch = "\\base\\animations\\npc\\gameplay\\woman_average\\gang\\unarmed"
        anim_copy(path_to_anim, panam_folder_stand +
                  loc_path_stand, loconame_panam_stand)
        anim_copy(path_to_anim, panam_folder_crouch +
                  loc_path_crouch, loconame_genfem_crouch)
        total_conversions += 1


# Delete contents of output_unbundle and tempfiles. Optionally delete output_packed as well.
def reset(delete_output_packed=False):
    # Delete tempfile
    shutil.rmtree(dir_tempfiles, ignore_errors=True)
    # Make new blank tempfile folder
    if not os.path.isdir(dir_tempfiles):
        os.makedirs(dir_tempfiles)

    # Delete output_unbundled
    shutil.rmtree(dir_output_unbundled, ignore_errors=True)
    # Make new blank output_unbundled folder
    if not os.path.isdir(dir_output_unbundled):
        os.makedirs(dir_output_unbundled)

    # Delete contents of output_packed
    if delete_output_packed:
        shutil.rmtree(dir_output_packed, ignore_errors=True)
        # Make new blank output_unbundled folder
        if not os.path.isdir(dir_output_packed):
            os.makedirs(dir_output_packed)
    print("Cleanup complete")


# Main
print("\nLaunching Cybertools by @wolv2077")

reset(True)
unbundler()
locomotion_convertor()
packer()

# reset(True)

# Render statistics
time_taken = round(time.time() - start_time, 3)
print("\n\nA total of", total_conversions,
      "conversions were completed in", time_taken, "seconds.")
print("End of program execution. See output_packed for final archives.")
