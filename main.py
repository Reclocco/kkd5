import math
import sys


def check(r, g, b, switch):
    b_sectors = [int(math.pow(2, 8 - b) / 2 + i * math.pow(2, 8 - b)) for i in range(int(math.pow(2, b)))]
    g_sectors = [int(math.pow(2, 8 - g) / 2 + i * math.pow(2, 8 - g)) for i in range(int(math.pow(2, g)))]
    r_sectors = [int(math.pow(2, 8 - r) / 2 + i * math.pow(2, 8 - r)) for i in range(int(math.pow(2, r)))]

    f = open(sys.argv[1], "rb")
    f.read(12)
    x = f.read(2)
    y = f.read(2)
    f.read(2)

    x = int.from_bytes(x, byteorder='little')
    y = int.from_bytes(y, byteorder='little')

    quadra_all = 0
    quadra_b = 0
    quadra_g = 0
    quadra_r = 0
    sum_b = 0
    sum_g = 0
    sum_r = 0
    sum_all = 0

    for i in range(x * y):
        b_byte = int.from_bytes(f.read(1), byteorder='little')
        g_byte = int.from_bytes(f.read(1), byteorder='little')
        r_byte = int.from_bytes(f.read(1), byteorder='little')

        quantum_b = belong(b_sectors, b_byte)
        quantum_g = belong(g_sectors, g_byte)
        quantum_r = belong(r_sectors, r_byte)

        quadra_b += math.pow((b_byte - quantum_b), 2)
        quadra_g += math.pow((g_byte - quantum_g), 2)
        quadra_r += math.pow((r_byte - quantum_r), 2)
        quadra_all += math.pow((b_byte - quantum_b), 2) + math.pow((g_byte - quantum_g), 2) + math.pow(
            (r_byte - quantum_r), 2)

        sum_b += quantum_b ** 2
        sum_g += quantum_g ** 2
        sum_r += quantum_r ** 2
        sum_all += quantum_b ** 2 + quantum_g ** 2 + quantum_r ** 2

    mse = [quadra_b / (x * y), quadra_g / (x * y), quadra_r / (x * y)]
    if switch == 1:
        return max(mse)
    elif switch == 0:
        snr = []
        try:
            snr.append(sum_b / (x * y) / (quadra_b / (x * y)))
        except ZeroDivisionError:
            snr.append(float("inf"))

        try:
            snr.append(sum_g / (x * y) / (quadra_g / (x * y)))
        except ZeroDivisionError:
            snr.append(float("inf"))

        try:
            snr.append(sum_r / (x * y) / (quadra_r / (x * y)))
        except ZeroDivisionError:
            snr.append(float("inf"))

        return min(snr)


def read_tga(r, g, b):
    b_sectors = [int(math.pow(2, 8 - b) / 2 + i * math.pow(2, 8 - b)) for i in range(int(math.pow(2, b)))]
    g_sectors = [int(math.pow(2, 8 - g) / 2 + i * math.pow(2, 8 - g)) for i in range(int(math.pow(2, g)))]
    r_sectors = [int(math.pow(2, 8 - r) / 2 + i * math.pow(2, 8 - r)) for i in range(int(math.pow(2, r)))]

    f = open(sys.argv[1], "rb")
    out = open(sys.argv[2], "wb")
    out.write(f.read(12))

    x = f.read(2)
    out.write(x)

    y = f.read(2)
    out.write(y)

    out.write(f.read(2))

    x = int.from_bytes(x, byteorder='little')
    y = int.from_bytes(y, byteorder='little')

    quadra_all = 0
    quadra_b = 0
    quadra_g = 0
    quadra_r = 0
    sum_b = 0
    sum_g = 0
    sum_r = 0
    sum_all = 0

    for i in range(x * y):
        b_byte = int.from_bytes(f.read(1), byteorder='little')
        g_byte = int.from_bytes(f.read(1), byteorder='little')
        r_byte = int.from_bytes(f.read(1), byteorder='little')

        quantum_b = belong(b_sectors, b_byte)
        quantum_g = belong(g_sectors, g_byte)
        quantum_r = belong(r_sectors, r_byte)

        quadra_b += math.pow((b_byte - quantum_b), 2)
        quadra_g += math.pow((g_byte - quantum_g), 2)
        quadra_r += math.pow((r_byte - quantum_r), 2)
        quadra_all += math.pow((b_byte - quantum_b), 2) + math.pow((g_byte - quantum_g), 2) + math.pow(
            (r_byte - quantum_r), 2)

        sum_b += quantum_b ** 2
        sum_g += quantum_g ** 2
        sum_r += quantum_r ** 2
        sum_all += quantum_b ** 2 + quantum_g ** 2 + quantum_r ** 2

        out.write(quantum_b.to_bytes(1, 'little'))
        out.write(quantum_g.to_bytes(1, 'little'))
        out.write(quantum_r.to_bytes(1, 'little'))

    out.write(f.read(26))

    print("mse: ", quadra_all / (x * y * 3))
    print("mse B: ", quadra_b / (x * y))
    print("mse G: ", quadra_g / (x * y))
    print("mse R: ", quadra_r / (x * y))

    try:
        print("SNR: ", sum_all / (x * y * 3) / (quadra_all / (x * y * 3)),
              10 * math.log(sum_all / (x * y * 3) / (quadra_all / (x * y * 3)), 10))
    except ZeroDivisionError:
        print("SNR inf")

    try:
        print("SNR B: ", sum_b / (x * y) / (quadra_b / (x * y)),
              10 * math.log(sum_b / (x * y) / (quadra_b / (x * y)), 10))
    except ZeroDivisionError:
        print("SNR B inf")

    try:
        print("SNR G: ", sum_g / (x * y) / (quadra_g / (x * y)),
              10 * math.log(sum_g / (x * y) / (quadra_g / (x * y)), 10))
    except ZeroDivisionError:
        print("SNR G inf")

    try:
        print("SNR R: ", sum_r / (x * y) / (quadra_r / (x * y)),
              10 * math.log(sum_r / (x * y) / (quadra_r / (x * y)), 10))
    except ZeroDivisionError:
        print("SNR R inf")


def belong(sectors, x):
    inc = sectors[0] * 2
    s_size = inc

    if inc == 0:
        inc = 1
        s_size = 0

    i = 0
    while x > s_size:
        s_size += inc
        i += 1

    return sectors[math.floor(i)]


def omniverse(x):
    possibilities = []

    for i in range(x):
        for j in range(x - i):
            k = x - i - j
            possibilities.append([i, j, k])

    return possibilities


def main():
    possibilities = omniverse(int(sys.argv[3]))
    results = []
    switch = -1

    if sys.argv[4] == "SNR":
        switch = 0
    elif sys.argv[4] == "MSE":
        switch = 1

    for possibility in possibilities:
        results.append(check(possibility[0], possibility[1], possibility[2], switch))

    best = [0, 0, 0]
    if switch == 0:
        best = possibilities[results.index(max(results))]
    elif switch == 1:
        try:
            best = possibilities[results.index(min(results))]
        except ValueError:
            best = [0, 0, 0]

    print("Best case (rbg): ", best)
    read_tga(best[0], best[1], best[2])


main()
