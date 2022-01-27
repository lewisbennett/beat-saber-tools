import hashlib
import json
import os
import requests
import sys
import time

def compute_beat_saber_hash(directory):

    global custom_levels_directory
    global info_dat_filename

    directory = custom_levels_directory + "\\" + directory + "\\"

    # Skip, if the 'info.dat' file doesn't exist.
    if not os.path.isfile(directory + info_dat_filename):
        return None

    info_dat_string = ""

    with open(directory + info_dat_filename) as info_dat_file:

        for line in info_dat_file.readlines():
            info_dat_string = info_dat_string + line

    info_dat = json.loads(info_dat_string)

    difficulty_filenames = []

    for beatmap_set in info_dat["_difficultyBeatmapSets"]:

        for difficulty in beatmap_set["_difficultyBeatmaps"]:

            difficulty_beatmap_filename = difficulty["_beatmapFilename"]

            difficulty_filenames.append(difficulty_beatmap_filename)

    # The level hash is the SHA1 of the contents of the 'info.dat' file, plus the contents of the
    # '[difficulty].dat' files in the order they appear in 'info.dat'.
    string_to_hash = info_dat_string

    for difficulty_filename in difficulty_filenames:

        if not os.path.isfile(directory + difficulty_filename):
            continue

        with open(directory + difficulty_filename, "r") as difficulty_file:

            for line in difficulty_file.readlines():
                string_to_hash = string_to_hash + line

    sha_1 = hashlib.sha1()
    sha_1.update(string_to_hash.encode())

    return sha_1.hexdigest()

def is_level_available(level_hash):

    response = None

    while (True):

        try:
            response = requests.request("GET", "https://beatsaver.com/api/maps/hash/" + level_hash)
            break

        except:
            time.sleep(5)

    return response.ok
    
def save_file(filename, data):

    with open(filename, 'w') as file:

        for line in data:

            file.write(line)
            file.write("\n")

def main():

    global custom_levels_directory
    global info_dat_filename

    info_dat_filename = "info.dat"

    # Get the custom levels directory from the arguments, if provided.
    # Otherwise, assume that either the string has been set manually,
    # or we're running in the custom levels directory.
    if len(sys.argv) == 2:
        custom_levels_directory = sys.argv[1]

    else:
        custom_levels_directory = ""

    custom_levels = []

    for subdirectory in os.listdir(custom_levels_directory):

        if os.path.isdir(custom_levels_directory + "\\" + subdirectory):
            custom_levels.append(subdirectory)

    if len(custom_levels) == 0:
        print ("No custom levels found.")
        return

    successes = []
    failures = []

    for custom_level in custom_levels:

        level_hash = compute_beat_saber_hash(custom_level)

        if level_hash == None:
            print ("Custom level does not contain '" + info_dat_filename + "' file: " + custom_level)
            continue

        if is_level_available(level_hash):
            successes.append(custom_level + " (" + level_hash + ")")

        else:
            print ("Custom level unavailable: " + custom_level + " (" + level_hash + ")")

            failures.append(custom_level + " (" + level_hash + ")")

    print ("\nFinished\n")

    if 'y' in input("Save successful queries (y/n)? "):
        save_file("successes.txt", successes)

    if 'y' in input("Save failed queries  (y/n)? "):
        save_file("failures.txt", failures)

if __name__ == "__main__":
    main()
