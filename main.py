import subprocess
import sys
import os
import glob
import shutil
import traceback

dir_wkitCLI = os.getcwd() + "\\wkitCLI\\WolvenKit.CLI.exe "
dir_input_packed = os.getcwd() + "\input_packed"
dir_output_packed = os.getcwd() + "\output_packed"
dir_output_unbundled = os.getcwd() + "\output_unbundled"
dir_structures = os.getcwd() + "\structures"
dir_tempfiles = os.getcwd() + "\\tempfiles"
cmd_pack = "pack -p "
cmd_unbundle = "unbundle -p "

loconame_panam_stand = "wa_panam_unarmed_locomotion_relaxed.anims"
loconame_genfem_crouch = "wa_gang_unarmed_locomotion_stealth.anims"


# def unbundler():
    


def unbundler():
    # We're only interested in files ending with .archive
    archives = glob.glob(dir_input_packed + "/*.archive")

    if not archives:
        print("Error: There were no archives detected in " + dir_input_packed)
        return

    try:
        for archive_path in archives:
            archive_name = os.path.basename(archive_path)
            unbundle_path = dir_wkitCLI + cmd_unbundle + '"' + archive_path + '"'

            try:
                p = subprocess.Popen(
                    ["powershell.exe", unbundle_path], stdout=sys.stdout)
                p.communicate()
            except:
                print("Error: WolvenKit failed to unbundle " + archive_name)

            # Copy to other directory
            try:
                src_path = archive_path[:-8]    # omit '.archive' from string
                dst_path = os.getcwd() + "\output_unbundled\\" + \
                    archive_name[:-8]

                # Copy to directory
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                # Delete from current directory
                shutil.rmtree(src_path)

            except:
                traceback.print_exc()
                print("Error during shutil file transfer operation")
    except:
        print("Error occured during unbundle.")
    print("Task completed.")


def packer():
    for folder in os.listdir(dir_tempfiles):
        folder_path = os.getcwd() + "\\" + "tempfiles\\" + folder
        wkitCommand = dir_wkitCLI + cmd_pack + '"' + folder_path + '"'

        print(wkitCommand)

        try:
            p = subprocess.Popen(["powershell.exe", wkitCommand], stdout=sys.stdout)
            p.communicate()
        except:
            print("Packing Error: WolvenKit failed to pack " + folder)


def npc_folder_builder(panam_folder):
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
    folders = []
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
        anim_copy(path_to_anim, panam_folder_stand + loc_path_stand, loconame_panam_stand)
        anim_copy(path_to_anim, panam_folder_crouch + loc_path_crouch, loconame_genfem_crouch)





# Main
print("Launching Cybertools by @wolv2077")

unbundler()
locomotion_convertor()
packer()
