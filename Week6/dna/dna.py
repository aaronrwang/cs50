import csv
from sys import argv


def main():

    # TODO: Check for command-line usage
    if len(argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        return 1

    # TODO: Read database file into a variable
    rows = []
    with open(argv[1]) as file:
        reader = csv.DictReader(file)
        strs = reader.fieldnames
        for row in reader:
            rows.append(row)

    # TODO: Read DNA sequence file into a variable
    sequence = open(argv[2], "r")
    sequence = sequence.read()

    # TODO: Find longest match of each STR in DNA sequence
    seql = len(sequence)
    seqans = rows[0].copy()
    seqans['name'] = 'No Match'
    for strand in strs[1:]:
        most = 0
        strl = len(strand)
        for i in range(0, seql-strl):
            if (strand == sequence[i:i+strl]):
                cursor = i
                count = 0
                while cursor < seql-strl and strand == sequence[cursor:cursor+strl]:
                    cursor += strl
                    count += 1
                most = max(count, most)
        seqans[strand] = most
    # TODO: Check database for matching profiles
    for c in rows:
        isAnswer = True
        for s in c:
            if s != 'name':
                if int(c.get(s)) != int(seqans.get(s)):
                    isAnswer = False
                    break
        if isAnswer == True:
            seqans['name'] = c['name']
    print(seqans['name'])


main()
