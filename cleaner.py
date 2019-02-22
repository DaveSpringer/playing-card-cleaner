import subprocess

# TODO: Migrate this to be a command line arg.
remote_image_path = "/media/nas_share/Games/Netrunner/*"
image_path = "/home/devspringer/images"

if subprocess.call(["ls", image_path]) is not 0:
    print("Creating the " + image_path + " path.")
    subprocess.call(["mkdir", image_path])

    print("Copying from " + remote_image_path + " to " + image_path)
    # Copy from the remote into a local build directory
    if subprocess.call(["cp", "-r", remote_image_path, image_path]) is not 0:
        print("Failed to copy from " + remote_image_path + " to " + image_path)
        subprocess.call(['rm', '-rf', image_path])
        exit(1)

# First, let's start by renaming all files and removing any ' ' characters

i = 1
while i < 2:
# Start with directories
    print("Finding candidate directories to rename.")
    find_dir = subprocess.Popen(["find", image_path, "-type", "d", "-maxdepth", str(i), "-mindepth", str(i)], stdout=subprocess.PIPE)
    directories = find_dir.communicate()[0]
    print("Found: " + directories)

    # Tokenize the directories
    directory_list = directories.split('\n')
    print(directory_list)

    # Iterate over the directories and remove whitespace
    for directory in directory_list:
        if ' ' in directory:
            if subprocess.call(["mv", directory, directory.replace(" ", "_")]) is not 0:
                print("Failed to remove whitespace from directory: " + directory)
                exit(2)
    i += 1

# Let's do the same thing for all file types.
print("Finding candidate files to rename.")
find_file = subprocess.Popen(["find", image_path, "-type", "f", "-mindepth", "1"], stdout=subprocess.PIPE)
files = find_file.communicate()[0]
print("Found: " + files)

# Tokenize the files
files_list = files.split('\n')
print(files_list)

# Iterate over the files and remove whitespace
for file in files_list:
    if ' ' in file:
        if subprocess.call(["mv", file, file.replace(" ", "_")]) is not 0:
            print("Failed to remove whitespace from directory: " + directory)
            exit(2)

# Now we are ready to start running magick on all of the images.

# First, find all of the images again.
print("Finding images to mogrify.")
find_file = subprocess.Popen(["find", image_path, "-type", "f", "-mindepth", "1"], stdout=subprocess.PIPE)
files = find_file.communicate()[0]
images_list = files.split('\n')
print(images_list)

failed_list = []

for image in images_list:
    if '_' in image:
        if subprocess.call(['mogrify', '-mattecolor', 'black', '-frame', '100X80', image]) is not 0:
            print("Failed to mogrify: " + image)
            failed_list.append(image)

if len(failed_list) > 0:
    print("The following images failed to be mogrified:" + failed_list)
    exit(3)

exit(0)
