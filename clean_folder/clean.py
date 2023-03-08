import sys
import os
import shutil
import re

file_types = {
    "images": [".jpeg", ".jpg", ".png", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".gz", ".tar"]}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def translate(name):
    return name.translate(TRANS)

def normalize(name, is_dir = False):
    extension = ""
    if not is_dir:
        full_name = os.path.splitext(name)
        name = full_name[0]
        extension += full_name[1]
    name = translate(name)
    name = re.sub(r"[ ()\-,.]", "_", name)
    if not is_dir:
        name += extension
    return name

def clean(root, relative_path="", ignore=[]):
    dir_path = os.path.join(root, relative_path)
    for entry in os.listdir(dir_path):
        if entry in ignore:
            continue
        relative_entry_path = os.path.join(relative_path, entry)
        entry_path = os.path.join(dir_path, entry)
        if os.path.isdir(entry_path):
            clean(root, relative_path=relative_entry_path)
    if os.listdir(dir_path):
        dir_name = os.path.basename(dir_path)
        dir_parent = os.path.dirname(dir_path)
        dir_name = normalize(dir_name)
        os.rename(dir_path, os.path.join(dir_parent, dir_name))
    else:
        os.rmdir(dir_path)

def move_audio(root, files):
    destination = os.path.join(root, "audio")
    if not os.path.exists(destination):
        os.makedirs(destination)
    names_encountered = {}
    for file in files:
        file_path = os.path.join(root, file)
        new_file_name = os.path.basename(file)
        new_file_name = normalize(new_file_name)
        if new_file_name in names_encountered:
            names_encountered[new_file_name] += 1
            base_name, extension = os.path.splitext(new_file_name)
            new_file_name = base_name + '_' + str(names_encountered[new_file_name]) + extension
        else:
            names_encountered[new_file_name] = 1
        new_file_path = os.path.join(destination, new_file_name)
        os.rename(file_path, new_file_path)
def move_video(root, files):
    destination = os.path.join(root, "video")
    if not os.path.exists(destination):
        os.makedirs(destination)
    names_encountered = {}
    for file in files:
        file_path = os.path.join(root, file)
        new_file_name = os.path.basename(file)
        new_file_name = normalize(new_file_name)
        if new_file_name in names_encountered:
            names_encountered[new_file_name] += 1
            base_name, extension = os.path.splitext(new_file_name)
            new_file_name = base_name + '_' + str(names_encountered[new_file_name]) + extension
        else:
            names_encountered[new_file_name] = 1
        new_file_path = os.path.join(destination, new_file_name)
        os.rename(file_path, new_file_path)
def move_images(root, files):
    destination = os.path.join(root, "images")
    if not os.path.exists(destination):
        os.makedirs(destination)
    names_encountered = {}
    for file in files:
        file_path = os.path.join(root, file)
        new_file_name = os.path.basename(file)
        new_file_name = normalize(new_file_name)
        if new_file_name in names_encountered:
            names_encountered[new_file_name] += 1
            base_name, extension = os.path.splitext(new_file_name)
            new_file_name = base_name + '_' + str(names_encountered[new_file_name]) + extension
        else:
            names_encountered[new_file_name] = 1
        new_file_path = os.path.join(destination, new_file_name)
        os.rename(file_path, new_file_path)
def move_documents(root, files):
    destination = os.path.join(root, "documents")
    if not os.path.exists(destination):
        os.makedirs(destination)
    names_encountered = {}
    for file in files:
        file_path = os.path.join(root, file)
        new_file_name = os.path.basename(file)
        new_file_name = normalize(new_file_name)
        if new_file_name in names_encountered:
            names_encountered[new_file_name] += 1
            base_name, extension = os.path.splitext(new_file_name)
            new_file_name = base_name + '_' + str(names_encountered[new_file_name]) + extension
        else:
            names_encountered[new_file_name] = 1
        new_file_path = os.path.join(destination, new_file_name)
        os.rename(file_path, new_file_path)
def move_archives(root, files):
    destination = os.path.join(root, "archives")
    if not os.path.exists(destination):
        os.makedirs(destination)
    names_encountered = {}
    for archive in files:
        archive_path = os.path.join(root, archive)
        new_archive_name = os.path.splitext(os.path.basename(archive))[0]
        new_archive_name = normalize(new_archive_name)
        if new_archive_name in names_encountered:
            names_encountered[new_archive_name] += 1
            base_name, extension = os.path.splitext(new_archive_name)
            new_archive_name = base_name + '_' + str(names_encountered[new_archive_name]) + extension
        else:
            names_encountered[new_archive_name] = 1
        new_archive_path = os.path.join(destination, new_archive_name)
        shutil.unpack_archive(archive_path, new_archive_path)
        os.remove(archive_path)
#"add functions, responsible for work with every file type" - task.

moving_functions = {
    "images": move_images,
    "video": move_video,
    "documents": move_documents,
    "audio": move_audio,
    "archives": move_archives
}

def move_files(root, catalogue):
    for type in file_types:
        if catalogue[type]:
            moving_functions[type](root, catalogue[type])

def log(sort_result):
    #sort_result - dict, that holds information about sorted files,
    #met extensions and unknown extensions
    #outputs this information into console
    message = "Soring is complete. Found files are:"
    for type in file_types:
        if sort_result[type]:
            message += f"\n{type}:"
            for file in sort_result[type]:
                message += f"\n\t{file}"
    if sort_result["found_extensions"]:
        message += "\nSorted files had extensions: " + ' '.join(sort_result["found_extensions"])
    if sort_result["unknown_extensions"]:
        message += "\nAlso were found files with unknown extensions: " \
                    + ' '.join(sort_result["unknown_extensions"])
    print(message)

def catalogue(root, relative_path = "", search_data = {}, ignore = []):
    #walks through the folder sorts files and records data about them
    #returns dictionary, with the recorded data

    if not search_data:
    #initializing the search data
        for type in file_types:
            search_data[type] = []
        #a key for every file type
        search_data["found_extensions"] = set()
        search_data["unknown_extensions"] = set()
        #a key for found known extensions and unknown extensions

    dir_path = os.path.join(root, relative_path)
    for entry in os.listdir(dir_path):
        if entry in ignore:
            continue
        relative_entry_path = os.path.join(relative_path, entry)
        entry_path = os.path.join(dir_path, entry)
        if os.path.isdir(entry_path):
            search_data = catalogue(root, relative_path=relative_entry_path, search_data=search_data)
        else:
            extension = os.path.splitext(entry_path)[1]

            is_type_recognized = False
            for type in file_types:
                if extension in file_types[type]:
                    search_data[type].append(relative_entry_path)
                    search_data["found_extensions"].add(extension)
                    is_type_recognized = True
                    break
            if not is_type_recognized:
                search_data["unknown_extensions"].add(extension)
    
    return search_data

def sort(path):
    #prepare(path) obsolete
    files = catalogue(path, ignore = file_types.keys())
    move_files(path, files)
    clean(path, ignore = file_types.keys())
    log(files)

def main():
    if len(sys.argv) < 2:
        print("Error. Path to the folder is required")
        return
    path = sys.argv[1]
    if not os.path.exists(path):
        print("Error. Specified path is not valid")
        return
    sort(path)

if __name__ == '__main__':
    main()