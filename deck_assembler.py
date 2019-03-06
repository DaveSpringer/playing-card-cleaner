import subprocess
import configparser
import sys

# Read in the inventory items
config = configparser.ConfigParser()
config.read('deck_assembler.ini')

result_path = config['card-paths']['ResultPath']
catalog_path = config['card-paths']['CatalogPath']
card_input_file = config['card-list']['InputFile']
find_path = config['configs']['findPath']

if len(sys.argv) is 2:
    card_input_file = sys.argv[1]

print("Finding cards in " + catalog_path + " and assembling them to " + result_path)

if subprocess.call(['ls', result_path]) is not 0:
    print('Creating the ' + result_path + ' for final images')
    subprocess.call(['mkdir', result_path])

if subprocess.call(['ls', result_path + "/Corp"]) is not 0:
    print('Creating the ' + result_path + '/Corp path for final images')
    subprocess.call(['mkdir', result_path + "/Corp"])

if subprocess.call(['ls', result_path + "/Runner"]) is not 0:
    print('Creating the ' + result_path + '/Runner path for final images')
    subprocess.call(['mkdir', result_path + "/Runner"])

card_lines = [line.rstrip('\n') for line in open(card_input_file)]
failed_copies = []
failed_names = []

find_process = subprocess.Popen([find_path, catalog_path, '-type', 'f'], stdout=subprocess.PIPE)
catalog_cards_bytes = find_process.communicate()[0].decode('utf-8')
catalog_cards = catalog_cards_bytes.splitlines()
print('Found these catalog cards: ' + str(catalog_cards))

for card_line in card_lines:
    card_name = card_line.split('\t')[1]
    print('Looking for card: ' + card_name)

    count = 0
    for card_path in catalog_cards:
        if card_name + '.jpg' in card_path:
            print('Copying from: ' + card_path)
            print('Copying to:   ' + result_path + "/" + card_line.split('\t')[0])
            count += 1
            pack_name_dirty = card_path.split("/")[-2]
            if pack_name_dirty[0].isdigit():
                pack_name = pack_name_dirty[5:].replace(' ', '_')
            else:
                pack_name = pack_name_dirty.replace(' ', '_')
            if subprocess.call(['cp', card_path, result_path + '/' + card_line.split('\t')[0] + '/' + card_name.replace(" ", "_") + '-' + str(count) + '_' + pack_name + ".jpg"]) is not 0:
                failed_copies.append(card_path)
                print("Failed to copy file: " + card_path + " for card name " + card_name)
    if count is 0:
        print("Failed to find card matching: " + str(card_name))
        failed_names.append(card_name)

print('Failed card names: ' + str(failed_names))


