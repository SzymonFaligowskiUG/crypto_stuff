import os
import asyncio
import enchant # This is library of many dictionaries from LibreOffice (super compacted)
import itertools
import numpy as np

most_frequent = ["E", "T", "A", "O", "I", "N"]
least_frequent = ["V", "K", "J", "X", "Q", "Z"]

alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
dezznuts = enchant.Dict("en_US")


def en_fq_score(text):
    counter = {}
    for letter in text:
        if not letter in alphabet:
            continue
        if letter in counter:
            counter[letter] +=1
        else:
            counter[letter] = 1
    flatWeights = []
    for letter in counter:
        flatWeights.append((letter, counter[letter]))
    sortedWeights = sorted(flatWeights, key=lambda x: x[1], reverse=True)

    score = 0

    # only most frequent
    if len(sortedWeights) <= len(most_frequent):
        for i in range(len(sortedWeights)):
            if sortedWeights[i][0] in most_frequent:
                score +=1
    else:
        for i in range(len(most_frequent)):
            if sortedWeights[i][0] in most_frequent:
                score +=1
        remaining_letters = len(sortedWeights) - len(most_frequent)
        if remaining_letters <= len(least_frequent):
            for i in range(len(sortedWeights) - remaining_letters, len(sortedWeights)):
                if sortedWeights[i][0] in least_frequent:
                    score += 1
        else:
            print(sortedWeights)
            print(len(sortedWeights) - len(least_frequent))
            for i in range(len(sortedWeights) - len(least_frequent)+1 , len(sortedWeights)):
                if sortedWeights[i][0] in least_frequent:
                    score += 1
    return score

async def all_case_task_sum(super_duper_all, sub_cipher):
    super_duper_all[sub_cipher] = {}
    for i, A_letter in enumerate(alphabet):
        decrypted = ""
        for letter in sub_cipher:
            shit = (alphabet.index(letter) - i) % len(alphabet)
            decrypted += alphabet[shit]
        super_duper_all[sub_cipher][decrypted] = (A_letter, en_fq_score(decrypted))

def try_decrypt(cipher, key):
    decrypted = ""
    for i, letter in enumerate(cipher):
        shift = (alphabet.index(letter) - alphabet.index(key[i])) % len(alphabet)
        decrypted += alphabet[shift]
    return decrypted

async def test_decryption_task(text1, text2, possibleKeys):
    results = []
    for perm in possibleKeys:
        dec1 = try_decrypt(text1, perm)
        dec2 =  try_decrypt(text2, perm)
        checkAll = dezznuts.check(dec2) and dezznuts.check(dec1)
        if checkAll:
            results.append((dec1, dec2, perm))
            print(f"Try: {dec1} and {dec2} Key: {perm}; check: {checkAll}")


async def main(): 
    text_one = input().upper()
    text_two = input().upper()

    if len(text_one) != len(text_two):
        os.exit(1)

    sub_ciphers = []

    for one, two in zip(text_one, text_two):
        sub_ciphers.append(one+two)


    super_duper_all = {}
    tasks =[]
    for sub_cipher in sub_ciphers:
        task = asyncio.create_task(all_case_task_sum(super_duper_all, sub_cipher))
        tasks.append(task)
    await asyncio.gather(*tasks)

    
    sub_dict = []
    for sub_cipher, possibilities in super_duper_all.items():
        find_max = 0
        for _, possibility in possibilities.items():
            if find_max < possibility[1]:
                find_max = possibility[1]
        letter = []
        for _, possibility in possibilities.items():
            if possibility[1] == find_max:
                letter.append(possibility[0])
            # back_word propagation !!
            if find_max > 1 and possibility[1] == find_max-1:
                letter.append(possibility[0])
        sub_dict.append(letter)
        print(f"Subi: {sub_cipher}, max: {str(find_max)}, letters {letter}")
    
    permutations = [ "".join(x) for x in itertools.product(*sub_dict)] # All keys possibilities

    testTasks = []
    for perm in np.array_split(permutations, len(permutations)/10):
        testTask = asyncio.create_task(test_decryption_task(text_one, text_two, perm))
        testTasks.append(testTask)
    results = await asyncio.gather(*testTasks)

async def analyze(text_one, text_two):
    if len(text_one) != len(text_two):
        os.exit(1)

    sub_ciphers = []

    for one, two in zip(text_one, text_two):
        sub_ciphers.append(one+two)


    super_duper_all = {}
    tasks =[]
    for sub_cipher in sub_ciphers:
        task = asyncio.create_task(all_case_task_sum(super_duper_all, sub_cipher))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(super_duper_all)

    
    sub_dict = []
    for sub_cipher, possibilities in super_duper_all.items():
        find_max = 0
        for _, possibility in possibilities.items():
            if find_max < possibility[1]:
                find_max = possibility[1]
        letter = []
        for _, possibility in possibilities.items():
            if possibility[1] == find_max:
                letter.append(possibility[0])
            # back_word propagation !!
            if find_max > 1 and possibility[1] == find_max-1:
                letter.append(possibility[0])
        sub_dict.append(letter)
        print(f"Subi: {sub_cipher}, max: {str(find_max)}, letters {letter}")
    
    permutations = [ "".join(x) for x in itertools.product(*sub_dict)] # All keys possibilities
    return permutations

async def try_decrypt_main(text_one, text_two, permutations):
    testTasks = []
    for perm in np.array_split(permutations, len(permutations)/10):
        testTask = asyncio.create_task(test_decryption_task(text_one, text_two, perm))
        testTasks.append(testTask)
    results = await asyncio.gather(*testTasks)
    return results