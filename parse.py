import os

def get_deepest_folders(folder_path):
    deepest_folders = []
    
    for root, dirs, files in os.walk(folder_path):
        if not dirs:
            deepest_folder = os.path.basename(root)
            if deepest_folder != 'CA':
                outer_folder = os.path.basename(os.path.dirname(root))
                if outer_folder == "casters":
                    deepest_folders.append(deepest_folder + " 31 c XXXX")
                if outer_folder == "solos":
                    deepest_folders.append(deepest_folder + " 5 c 0000")
                if outer_folder == "units":
                    deepest_folders.append(deepest_folder + " 7/11 2 0000")
                if outer_folder == "lessers" or outer_folder == "heavies" or outer_folder == "lights" or outer_folder == "gargatuans":
                    deepest_folders.append(deepest_folder + " 15 U XXXX")
                if outer_folder == "engines":
                    deepest_folders.append(deepest_folder + " 15 2 0000")
            else:
                outer_folder = os.path.basename(os.path.dirname(root))
                deepest_folders.append(outer_folder + " 7/11 2 0000")
                deepest_folders.append(outer_folder + "_CA 5 0000")
    
    return deepest_folders

# Example usage
folder_path = 'assets/skorne'
deepest_folders = get_deepest_folders(folder_path)

themes = ["Disciples of Agony", "Masters of War", "The Exalted", "Winds of Death"]

# Write deepest_folders to a new file
with open('skorne_config.txt', 'w') as file:
    file.write("themes\n\n")
    for theme in themes:
        file.write(theme + '\n')
    file.write("\nmodels\n\n")
    for folder in deepest_folders:
        file.write(folder + '\n')

# Print the contents of the deepest_folders list
for folder in deepest_folders:
    print(folder)