# used chatgpt for this cuz i aint no fucking genius
import random

def Get_IDs():
    ranges = [
        ((1, 1_250_000), 4), # 3% 
        ((2_520_000, 7_960_000), 21), # 16%
        ((8_000_000, 9_930_000), 4), # 3%
        ((9_960_000, 17_000_000), 33), # 22%
        ((32_000_000, 35_250_000), 38) # 38% between 32M and 35.25M
    ]

    ids = [random.randint(start, end) for (start, end), count in ranges for _ in range(count)]
    return str(ids).replace(" ", "")[:-1][1:]