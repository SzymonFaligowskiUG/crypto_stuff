import asyncio
import time
import matplotlib.pyplot as plt


from main import analyze, try_decrypt_main

alphabet = "abcdefghijklmnopqrstuvwxyz".upper()

def encrypt(text, key):
    encrypted = ""
    for i, letter in enumerate(text):
        shift = (alphabet.index(letter) + alphabet.index(key[i])) % len(alphabet)
        encrypted += alphabet[shift]
    return encrypted

async def test1():
    dataset = {
        3: {
            "text_one_encrypted" : encrypt("LEO", "MAX"),
            "text_two_encrypted" : encrypt("TOM", "MAX"),
            "key" : "MAX"
        },
        4: {
            "text_one_encrypted" : encrypt("NEWS", "FOUR"),
            "text_two_encrypted" : encrypt("CONE", "FOUR"),
            "key" : "FOUR"
        },
        5: {
            "text_one_encrypted" : encrypt("ADULT", "FRUIT"),
            "text_two_encrypted" : encrypt("DRAMA", "FRUIT"),
            "key" : "CRAFT"
        },
        6: {
            "text_one_encrypted" : encrypt("DIRECT", "BORDER"),
            "text_two_encrypted" : encrypt("EFFECT", "BORDER"),
            "key" : "BORDER"
        }
    }
    times = []
    lengths = []
    for l, data in dataset.items():
        text_one = data["text_one_encrypted"]
        text_two = data["text_two_encrypted"]
        start = time.time()
        a =  await analyze(text_one,text_two)
        b =  await try_decrypt_main(text_one, text_two, a)
        end = time.time()
        times.append(end - start)
        lengths.append(l)
        print(f"Possible keys: {b}")
    fig, ax = plt.subplots()
    ax.stem(lengths, times)
    ax.set( xticks=[x for x in range(3, 7)])
    plt.show()

async def test2():
    dataset = {
        1: {
            "text_one_encrypted" : encrypt("LEO", "MAX"),
            "text_two_encrypted" : encrypt("TOM", "MAX"),
            "key" : "MAX"
        },
        2: {
            "text_one_encrypted" : encrypt("LEO", "KWA"),
            "text_two_encrypted" : encrypt("TOM", "KWA"),
            "key" : "KWA"
        },
    }
    times = []
    for _, data in dataset.items():
        text_one = data["text_one_encrypted"]
        text_two = data["text_two_encrypted"]
        start = time.time()
        a =  await analyze(text_one,text_two)
        b =  await try_decrypt_main(text_one, text_two, a)
        end = time.time()
        times.append(end - start)
        print(f"Possible keys: {b}")
        print(f"CASE know world: {times[0]}")
        print(f"CASE unknown world: {times[1]}")

async def test3():
    dataset = {
        1: {
            "text_one_encrypted" : encrypt("LEO", "MAX"),
            "text_two_encrypted" : encrypt("TOM", "MAX"),
            "key" : "MAX"
        },
    }
    times = []
    for _, data in dataset.items():
        text_one = data["text_one_encrypted"]
        text_two = data["text_two_encrypted"]
        a =  await analyze(text_one,text_two)
        b =  await try_decrypt_main(text_one, text_two, a)
        print(f"Possible keys: {b}")
        print(f"Effectiveness: {100/len(b)}")


async def main():
    await test1()
    await test2()

asyncio.run(main())