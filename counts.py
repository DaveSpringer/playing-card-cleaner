import sys

print("Number of arguments: " + str(len(sys.argv) - 1))

index = 1
total_cards = 0
runner_count = 0
corp_count = 0
corp_output_list = []
runner_output_list = []
while index < len(sys.argv):
    print("Examining " + sys.argv[index])
    card_count = 0
    set_corp = 0
    set_runner = 0
    card_lines = [line.rstrip('\n') for line in open(sys.argv[index])]
    for line in card_lines:
        card_split = line.split('\t')
        card_count += int(card_split[2])
        if card_split[0] == 'Corp':
            corp_count += int(card_split[2])
            set_corp += int(card_split[2])
            corp_output_list.append(card_split)
        else:
            runner_count += int(card_split[2])
            set_runner += int(card_split[2])
            runner_output_list.append(card_split)
    total_cards += card_count
    print(sys.argv[index] + " has " + str(card_count) + " cards: " + str(set_corp) + " Corp / " + str(set_runner) + " runner")
    index += 1
print("Total cards to print: " + str(total_cards))
print("Corp cards: " + str(corp_count))
print("Runner cards: " + str(runner_count))

corp_output_list.sort(key=lambda tup: tup[1])
runner_output_list.sort(key=lambda tup: tup[1])

output_list = []
output_list.extend(corp_output_list)
output_list.extend(runner_output_list)

i = 1
merged = 0
while i < len(output_list) - merged:
    if output_list[i][1] == output_list[i - 1][1]:
        line = output_list.pop(i)
        output_list[i - 1][2] = str(int(output_list[i - 1][2]) + int(line[2]))
    i += 1

with open('card_list_finalized.txt', 'w') as f:
    for line in output_list:
        f.write("%s\n" % '\t'.join(line))

