import math

def adpcm2pcm(pat):
    guess = 0
    delta = 127
    f = [57, 57, 57, 57, 77, 102, 128, 153]

    for adpcm in pat:
        if (adpcm < 8):
            guess = guess + ((adpcm & 7) * 2 + 1) * math.floor(delta / 8)
        else:
            guess = guess - ((adpcm & 7) * 2 + 1) * math.floor(delta / 8)

        # clamp
        guess = max(-0x8000, min(guess, 0x7fff))

        print(guess)

        delta = math.floor(delta * f[adpcm & 7] / 64)
        if (delta < 127):
            delta = 127
        elif (delta > 24576):
            delta = 24576

pat = [
    7,7,7,7,
    7,7,7,7,
    7,7,15,15,
    15,15,15,15,

    3,3,3,3,
    3,3,11,11,
    11,11,11,11,
    4,3,12,11,

    4,3,12,11,
    4,3,12,11,
    4,3,12,11,
    4,3,12,11,

    4,3,12,11,
    4,3,12,11,
    4,3,12,11,
    4,3,12,11,
]

adpcm2pcm(pat)
