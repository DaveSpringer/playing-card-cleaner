import subprocess
import configparser

# Read in the inventory items
config = configparser.ConfigParser()
config.read('cleaner.ini')

result_path = config['card-paths']['ResultPath']
catalog_path = config['card-paths']['CatalogPath']
card_input_file = config['card-list']['InputFile']
find_path = config['configs']['findPath']

# TODO: Migrate this to be a command line arg.
result_path = result_path

print("Using the find_path of: " + find_path)

if subprocess.call(["ls", result_path]) is not 0:
    print("Creating the " + result_path + " path.")
    subprocess.call(["mkdir", result_path])
    subprocess.call(["mkdir", result_path + "/Runner"])
    subprocess.call(["mkdir", result_path + "/Corp"])


# Convert from the CatalogPath to the ResultPath
print("Converting images from " + catalog_path + " to " + result_path)

# First, let's start by renaming all files and removing any ' ' characters
i = 1
while i < 3:
# Start with directories
    print("Finding candidate directories to rename.")
    find_dir = subprocess.Popen([find_path, catalog_path, "-maxdepth", str(i), "-mindepth", str(i), "-type", "d"], stdout=subprocess.PIPE)
    directories = find_dir.communicate()[0].decode('utf-8')
    print("Found: " + directories)

    # Tokenize the directories
    directory_list = directories.split('\n')
    print(directory_list)

    # Iterate over the directories and remove whitespace
    for directory in directory_list:
        if ' ' in directory:
            if subprocess.call(["mv", directory, directory.replace(" ", "_")]) is not 0:
                print("Failed to remove whitespace from file: " + directory)
                exit(2)
    i += 1

# Let's do the same thing for all file types.
print("Finding candidate files to rename.")
find_file = subprocess.Popen([find_path, catalog_path, "-type", "f", "-mindepth", "1"], stdout=subprocess.PIPE)
files = find_file.communicate()[0].decode('utf-8')
print("Found: " + files)

# Tokenize the files
files_list = files.split('\n')
print(files_list)

# Iterate over the files and remove whitespace
for file_name in files_list:
    if '/' in file_name:
        clean_file = file_name.replace(" ", "_")
        new_file_name = '.'.join(clean_file.split('/')[-1].split(".")[:-1]) + '.png'
        print("New file name is: " + new_file_name)
        result_file = result_path + '/' + clean_file.split('/')[-2] + '/' + new_file_name
        print("New file is: " + result_file)
        if subprocess.call(['convert', file_name, result_file]) is not 0:
            print("Failed to convert file from " + file_name + " to " + result_file)
            exit(3)

# A quick pause to run a gimp command on all images in the Corp and Runner folders.
if subprocess.call(['gimp', '-i', '-b', '(batch-despeckle "' + result_path + '/Corp/*.png" 0.5)', '-b', '(gimp-quit 0)']) is not 0:
    print("Failed to despeckle the Corp cards.")
    exit(4)

if subprocess.call(['gimp', '-i', '-b', '(batch-despeckle "' + result_path + '/Runner/*.png" 0.5)', '-b', '(gimp-quit 0)']) is not 0:
    print("Failed to despeckle the Runner cards.")
    exit(4)

# Now we are ready to start running magick on all of the images.

# First, find all of the images again.
print("Finding images to mogrify.")
find_file = subprocess.Popen([find_path, result_path, "-type", "f", "-mindepth", "1"], stdout=subprocess.PIPE)
files = find_file.communicate()[0].decode('utf-8')
images_list = files.split('\n')
print(images_list)

failed_list = []

for image in images_list:
    if '_' in image:
        if subprocess.call(['mogrify', '-gravity', 'center', '-crop', '2.48:3.46', '+repage', image]) is not 0:
            print("Failed to mogrify: " + image)
            failed_list.append(image)
        else:
            #subprocess.call(['mogrify', '-gaussian-blur', '12x2', '+repage', '-sharpen', '12x2', '-sharpen', '12x2', image])
            # if subprocess.call(['mogrify', '-shave', '5x7', '+repage', '-resize', '744x1038!', '-unsharp', '0x0.75+0.75+0.008', image]) is not 0:
            if subprocess.call(['mogrify', '-shave', '5x7', '+repage', '-resize', '744x1038!', image]) is not 0:
                print("Failed to shave image: " + image)
                failed_list.append(image)
            else:
                if subprocess.call(['./bin/saturation', '1.75', image, image]) is not 0:
                    print("Failed to saturate image: " + image)
                    failed_list.append(image)
                else:
                    #subprocess.call(['mogrify', '-brightness-contrast', '10', image])
                    if subprocess.call(['./bin/imageborder', '-s', '36', '-p', '0', '-t', '0', '-e', 'mirror', image, image]) is not 0:
                        print("Failed to imageborder image: " + image)
                        failed_list.append(image)
                    else:
                        print("Cleaned and mogrified: " + image)

if len(failed_list) > 0:
    print("The following images failed to be mogrified:" + failed_list)
    exit(3)

exit(0)
