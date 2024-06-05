from IPython.display import display
from random import randint
from functools import reduce
import math
import copy
import argparse
from PIL import Image


def generate_image_from_binary_matrix(matrix, pixel_size=10, background_color=(255, 255, 255), foreground_color=(0, 0, 0), dev=False):
    height = len(matrix)
    width = len(matrix[0])
    image_width = width * pixel_size
    image_height = height * pixel_size
    img = Image.new('RGB', (image_width, image_height), background_color)
    if not dev:
        for y in range(height):
            for x in range(width):
                if str(matrix[y][x]) >= str(1):
                    x1 = x * pixel_size
                    y1 = y * pixel_size
                    x2 = x1 + pixel_size
                    y2 = y1 + pixel_size
                    img.paste(foreground_color, (x1, y1, x2, y2))
    else:
        for y in range(height):
            for x in range(width):
                if str(matrix[y][x]) != str(0):
                    if str(matrix[y][x]) == str(2):
                        color = (0, 0, 255)
                    elif str(matrix[y][x]) == str(3):
                        color = (0, 255, 0)
                    elif str(matrix[y][x]) == str(4):
                        color = (255, 0, 0)
                    elif matrix[y][x] is None:
                        color = (128, 128, 128)
                    else:
                        color = (0, 0, 0)
                    x1 = x * pixel_size
                    y1 = y * pixel_size
                    x2 = x1 + pixel_size
                    y2 = y1 + pixel_size
                    img.paste(color, (x1, y1, x2, y2))

    return img

###############################################


# The following array contains 256 elements, each one containing the alpha
# element, and its associated integer value.
#   I.E: (10, 116) means that for alpha exponent 10, the associated integer is
#        116
ALPHA_EXP_TO_INTEGER = [
    (0, 1), (1, 2), (2, 4), (3, 8), (4, 16), (5,
                                              32), (6, 64), (7, 128), (8, 29), (9, 58),
    (10, 116), (11, 232), (12, 205), (13, 135), (14,
                                                 19), (15, 38), (16, 76), (17, 152), (18, 45), (19, 90),
    (20, 180), (21, 117), (22, 234), (23, 201), (24,
                                                 143), (25, 3), (26, 6), (27, 12), (28, 24), (29, 48),
    (30, 96), (31, 192), (32, 157), (33, 39), (34, 78), (35,
                                                         156), (36, 37), (37, 74), (38, 148), (39, 53),
    (40, 106), (41, 212), (42, 181), (43, 119), (44,
                                                 238), (45, 193), (46, 159), (47, 35), (48, 70), (49, 140),
    (50, 5), (51, 10), (52, 20), (53, 40), (54, 80), (55,
                                                      160), (56, 93), (57, 186), (58, 105), (59, 210),
    (60, 185), (61, 111), (62, 222), (63, 161), (64,
                                                 95), (65, 190), (66, 97), (67, 194), (68, 153), (69, 47),
    (70, 94), (71, 188), (72, 101), (73, 202), (74,
                                                137), (75, 15), (76, 30), (77, 60), (78, 120), (79, 240),
    (80, 253), (81, 231), (82, 211), (83, 187), (84, 107), (85,
                                                            214), (86, 177), (87, 127), (88, 254), (89, 225),
    (90, 223), (91, 163), (92, 91), (93, 182), (94, 113), (95,
                                                           226), (96, 217), (97, 175), (98, 67), (99, 134),
    (100, 17), (101, 34), (102, 68), (103, 136), (104, 13), (105,
                                                             26), (106, 52), (107, 104), (108, 208), (109, 189),
    (110, 103), (111, 206), (112, 129), (113, 31), (114, 62), (115,
                                                               124), (116, 248), (117, 237), (118, 199), (119, 147),
    (120, 59), (121, 118), (122, 236), (123, 197), (124,
                                                    151), (125, 51), (126, 102), (127, 204), (128, 133), (129, 23),
    (130, 46), (131, 92), (132, 184), (133, 109), (134,
                                                   218), (135, 169), (136, 79), (137, 158), (138, 33), (139, 66),
    (140, 132), (141, 21), (142, 42), (143, 84), (144, 168), (145,
                                                              77), (146, 154), (147, 41), (148, 82), (149, 164),
    (150, 85), (151, 170), (152, 73), (153, 146), (154, 57), (155,
                                                              114), (156, 228), (157, 213), (158, 183), (159, 115),
    (160, 230), (161, 209), (162, 191), (163, 99), (164, 198), (165,
                                                                145), (166, 63), (167, 126), (168, 252), (169, 229),
    (170, 215), (171, 179), (172, 123), (173, 246), (174,
                                                     241), (175, 255), (176, 227), (177, 219), (178, 171), (179, 75),
    (180, 150), (181, 49), (182, 98), (183, 196), (184, 149), (185,
                                                               55), (186, 110), (187, 220), (188, 165), (189, 87),
    (190, 174), (191, 65), (192, 130), (193, 25), (194,
                                                   50), (195, 100), (196, 200), (197, 141), (198, 7), (199, 14),
    (200, 28), (201, 56), (202, 112), (203, 224), (204, 221), (205,
                                                               167), (206, 83), (207, 166), (208, 81), (209, 162),
    (210, 89), (211, 178), (212, 121), (213, 242), (214,
                                                    249), (215, 239), (216, 195), (217, 155), (218, 43), (219, 86),
    (220, 172), (221, 69), (222, 138), (223, 9), (224, 18), (225,
                                                             36), (226, 72), (227, 144), (228, 61), (229, 122),
    (230, 244), (231, 245), (232, 247), (233, 243), (234,
                                                     251), (235, 235), (236, 203), (237, 139), (238, 11), (239, 22),
    (240, 44), (241, 88), (242, 176), (243, 125), (244, 250), (245,
                                                               233), (246, 207), (247, 131), (248, 27), (249, 54),
    (250, 108), (251, 216), (252, 173), (253, 71), (254, 142), (255, 1)
]


def alpha_to_int(alpha_value: int):
    return list(filter(lambda x: x[0] == alpha_value, ALPHA_EXP_TO_INTEGER))[0][1]


def int_to_alpha(int_value: int):
    return list(filter(lambda x: x[1] == int_value, ALPHA_EXP_TO_INTEGER))[0][0]


def simplify_polynomial(a):
    max_exponent = max(a, key=lambda x: x[1])[1]
    simplified_polynomial = []
    for i in range(max_exponent, -1, -1):
        terms_for_exponent_i = list(filter(lambda x: x[1] == i, a))
        if len(terms_for_exponent_i) == 1:
            simplified_polynomial.append(terms_for_exponent_i[0])
        else:
            xor_accumulator = 0
            for term in terms_for_exponent_i:
                # Given each term we have for a specific x exponent, take the alpha
                # exponent and find the corresponding integer using ALPHA_EXP_TO_INTEGER
                alpha_exponent = term[0]
                integer = list(
                    filter(lambda x: x[0] == term[0], ALPHA_EXP_TO_INTEGER))[0][1]
                xor_accumulator = xor_accumulator ^ integer
            # Now I have to use the xor_accumulator (integer) to get the alpha
            # exponent again.
            # new_alpha_exponent = xor_accumulator
            xor_accumulator = ((xor_accumulator % 256) + math.floor(
                xor_accumulator / 256)) if xor_accumulator > 255 else xor_accumulator
            new_alpha_exponent = list(
                filter(lambda x: x[1] == xor_accumulator, ALPHA_EXP_TO_INTEGER))[0][0]
            new_term = [new_alpha_exponent, i]
            simplified_polynomial.append(new_term)

    return simplified_polynomial


def multiply_polynomials(a, b):
    new_polynomial = []
    for t_a in a:
        for t_b in b:
            alpha_exponent = t_a[0] + t_b[0]
            alpha_exponent = ((alpha_exponent % 256) + math.floor(
                alpha_exponent / 256)) if alpha_exponent > 255 else alpha_exponent
            x_exponent = t_a[1] + t_b[1]
            x_exponent = ((x_exponent % 256) + math.floor(x_exponent / 256)
                          ) if x_exponent > 255 else x_exponent
            new_term = [alpha_exponent, x_exponent]
            # IMPORTANT: Here, I should check if any exponent is greater than 255
            new_polynomial.append(new_term)
    simplified_polynomial = simplify_polynomial(new_polynomial)
    return simplified_polynomial


def get_generator_polynomial(code_words: int):
    if code_words < 7:
        raise Exception("Codewords cannot be less than 7.")

    base_polynomial = [[0, 1], [0, 0]]
    current_polynomial = copy.deepcopy(base_polynomial)
    for i in range(code_words - 1):
        multiplier = base_polynomial
        multiplier[1][0] = i + 1
        current_polynomial = multiply_polynomials(a=current_polynomial,
                                                  b=multiplier)
    return current_polynomial

###############################################

# Error correction levels:
# L	Recovers 7% of data
# M	Recovers 15% of data
# Q	Recovers 25% of data
# H	Recovers 30% of data


# The following variable represents the error correction reference table.
# Each key represents the QR version and the error correction level. For each
# key, there is an array with the follwing values:
#   [
#     total_number_of_datacodewords,
#     error_correction_codewords_per_block,
#     number_of_blocks_in_group_1,
#     number_of_codewords_per_block_in_group_1,
#     number_of_blocks_in_group_2,
#     number_of_codewords_per_block_in_group_2,
#   ]
ERROR_CORRECTION_CODE_WORDS = {
    "1-L": [19, 7, 1, 19], "1-M": [16, 10, 1, 16], "1-Q": [13, 13, 1, 13], "1-H": [9, 17, 1, 9],
    "2-L": [34, 10, 1, 34], "2-M": [28, 16, 1, 28], "2-Q": [22, 22, 1, 22], "2-H": [16, 28, 1, 16],
    "3-L": [55, 15, 1, 55], "3-M": [44, 26, 1, 44], "3-Q": [34, 18, 2, 17], "3-H": [26, 22, 2, 13],
    "4-L": [80, 20, 1, 80], "4-M": [64, 18, 2, 32], "4-Q": [48, 26, 2, 24], "4-H": [36, 16, 4, 9],
    "5-L": [108, 26, 1, 108], "5-M": [86, 24, 2, 43], "5-Q": [62, 18, 2, 15, 2, 16], "5-H": [46, 22, 2, 11, 2, 12],
    "6-L": [136, 18, 2, 68], "6-M": [108, 16, 4, 27], "6-Q": [76, 24, 4, 19], "6-H": [60, 28, 4, 15],
    "7-L": [156, 20, 2, 78], "7-M": [124, 18, 4, 31], "7-Q": [88, 18, 2, 14, 4, 15], "7-H": [66, 26, 4, 13, 1, 14],
    "8-L": [194, 24, 2, 97], "8-M": [154, 22, 2, 38, 2, 39], "8-Q": [110, 22, 4, 18, 2, 19], "8-H": [86, 26, 4, 14, 2, 15],
    "9-L": [232, 30, 2, 116], "9-M": [182, 22, 3, 36, 2, 37], "9-Q": [132, 20, 4, 16, 4, 17], "9-H": [100, 24, 4, 12, 4, 13],
    "10-L": [274, 18, 2, 68, 2, 69], "10-M": [216, 26, 4, 43, 1, 44], "10-Q": [154, 24, 6, 19, 2, 20], "10-H": [122, 28, 6, 15, 2, 16],
    "11-L": [324, 20, 4, 81], "11-M": [254, 30, 1, 50, 4, 51], "11-Q": [180, 28, 4, 22, 4, 23], "11-H": [140, 24, 3, 12, 8, 13],
    "12-L": [370, 24, 2, 92, 2, 93], "12-M": [290, 22, 6, 36, 2, 37], "12-Q": [206, 26, 4, 20, 6, 21], "12-H": [158, 28, 7, 14, 4, 15],
    "13-L": [428, 26, 4, 107], "13-M": [334, 22, 8, 37, 1, 38], "13-Q": [244, 24, 8, 20, 4, 21], "13-H": [180, 22, 12, 11, 4, 12],
    "14-L": [461, 30, 3, 115, 1, 116], "14-M": [365, 24, 4, 40, 5, 41], "14-Q": [261, 20, 11, 16, 5, 17], "14-H": [197, 24, 11, 12, 5, 13],
    "15-L": [523, 22, 5, 87, 1, 88], "15-M": [415, 24, 5, 41, 5, 42], "15-Q": [295, 30, 5, 24, 7, 25], "15-H": [223, 24, 11, 12, 7, 13],
    "16-L": [589, 24, 5, 98, 1, 99], "16-M": [453, 28, 7, 45, 3, 46], "16-Q": [325, 24, 15, 19, 2, 20], "16-H": [253, 30, 3, 15, 13, 16],
    "17-L": [647, 28, 1, 107, 5, 108], "17-M": [507, 28, 10, 46, 1, 47], "17-Q": [367, 28, 1, 22, 15, 23], "17-H": [283, 28, 2, 14, 17, 15],
    "18-L": [721, 30, 5, 120, 1, 121], "18-M": [563, 26, 9, 43, 4, 44], "18-Q": [397, 28, 17, 22, 1, 23], "18-H": [313, 28, 2, 14, 19, 15],
    "19-L": [795, 28, 3, 113, 4, 114], "19-M": [627, 26, 3, 44, 11, 45], "19-Q": [445, 26, 17, 21, 4, 22], "19-H": [341, 26, 9, 13, 16, 14],
    "20-L": [861, 28, 3, 107, 5, 108], "20-M": [669, 26, 3, 41, 13, 42], "20-Q": [485, 30, 15, 24, 5, 25], "20-H": [385, 28, 15, 15, 10, 16],
    "21-L": [932, 28, 4, 116, 4, 117], "21-M": [714, 26, 17, 42], "21-Q": [512, 28, 17, 22, 6, 23], "21-H": [406, 30, 19, 16, 6, 17],
    "22-L": [1006, 28, 2, 111, 7, 112], "22-M": [782, 28, 17, 46], "22-Q": [568, 30, 7, 24, 16, 25], "22-H": [442, 24, 34, 13],
    "23-L": [1094, 30, 4, 121, 5, 122], "23-M": [860, 28, 4, 47, 14, 48], "23-Q": [614, 30, 11, 24, 14, 25], "23-H": [464, 30, 16, 15, 14, 16],
    "24-L": [1174, 30, 6, 117, 4, 118], "24-M": [914, 28, 6, 45, 14, 46], "24-Q": [664, 30, 11, 24, 16, 25], "24-H": [514, 30, 30, 16, 2, 17],
    "25-L": [1276, 26, 8, 106, 4, 107], "25-M": [1000, 28, 8, 47, 13, 48], "25-Q": [718, 30, 7, 24, 22, 25], "25-H": [538, 30, 22, 15, 13, 16],
    "26-L": [1370, 28, 10, 114, 2, 115], "26-M": [1062, 28, 19, 46, 4, 47], "26-Q": [754, 28, 28, 22, 6, 23], "26-H": [596, 30, 33, 16, 4, 17],
    "27-L": [1468, 30, 8, 122, 4, 123], "27-M": [1128, 28, 22, 45, 3, 46], "27-Q": [808, 30, 8, 23, 26, 24], "27-H": [628, 30, 12, 15, 28, 16],
    "28-L": [1531, 30, 3, 117, 10, 118], "28-M": [1193, 28, 3, 45, 23, 46], "28-Q": [871, 30, 4, 24, 31, 25], "28-H": [661, 30, 11, 15, 31, 16],
    "29-L": [1631, 30, 7, 116, 7, 117], "29-M": [1267, 28, 21, 45, 7, 46], "29-Q": [911, 30, 1, 23, 37, 24], "29-H": [701, 30, 19, 15, 26, 16],
    "30-L": [1735, 30, 5, 115, 10, 116], "30-M": [1373, 28, 19, 47, 10, 48], "30-Q": [985, 30, 15, 24, 25, 25], "30-H": [745, 30, 23, 15, 25, 16],
    "31-L": [1843, 30, 13, 115, 3, 116], "31-M": [1455, 28, 2, 46, 29, 47], "31-Q": [1033, 30, 42, 24, 1, 25], "31-H": [793, 30, 23, 15, 28, 16],
    "32-L": [1955, 30, 17, 115], "32-M": [1541, 28, 10, 46, 23, 47], "32-Q": [1115, 30, 10, 24, 35, 25], "32-H": [845, 30, 19, 15, 35, 16],
    "33-L": [2071, 30, 17, 115, 1, 116], "33-M": [1631, 28, 14, 46, 21, 47], "33-Q": [1171, 30, 29, 24, 19, 25], "33-H": [901, 30, 11, 15, 46, 16],
    "34-L": [2191, 30, 13, 115, 6, 116], "34-M": [1725, 28, 14, 46, 23, 47], "34-Q": [1231, 30, 44, 24, 7, 25], "34-H": [961, 30, 59, 16, 1, 17],
    "35-L": [2306, 30, 12, 121, 7, 122], "35-M": [1812, 28, 12, 47, 26, 48], "35-Q": [1286, 30, 39, 24, 14, 25], "35-H": [986, 30, 22, 15, 41, 16],
    "36-L": [2434, 30, 6, 121, 14, 122], "36-M": [1914, 28, 6, 47, 34, 48], "36-Q": [1354, 30, 46, 24, 10, 25], "36-H": [1054, 30, 2, 15, 64, 16],
    "37-L": [2566, 30, 17, 122, 4, 123], "37-M": [1992, 28, 29, 46, 14, 47], "37-Q": [1426, 30, 49, 24, 10, 25], "37-H": [1096, 30, 24, 15, 46, 16],
    "38-L": [2702, 30, 4, 122, 18, 123], "38-M": [2102, 28, 13, 46, 32, 47], "38-Q": [1502, 30, 48, 24, 14, 25], "38-H": [1142, 30, 42, 15, 32, 16],
    "39-L": [2812, 30, 20, 117, 4, 118], "39-M": [2216, 28, 40, 47, 7, 48], "39-Q": [1582, 30, 43, 24, 22, 25], "39-H": [1222, 30, 10, 15, 67, 16],
    "40-L": [2956, 30, 19, 118, 6, 119], "40-M": [2334, 28, 18, 47, 31, 48], "40-Q": [1666, 30, 34, 24, 34, 25], "40-H": [1276, 30, 20, 15, 61, 16]
}


def get_ec_codewords_by_level_version(qr_version: str,
                                      error_correction_level: str):
    ec_codewords_definition = ERROR_CORRECTION_CODE_WORDS[f"{qr_version}-{error_correction_level}"]
    total_number_of_datacodewords = ec_codewords_definition[0]
    error_correction_codewords_per_block = ec_codewords_definition[1]
    number_of_blocks_in_group_1 = ec_codewords_definition[2]
    number_of_codewords_per_block_in_group_1 = ec_codewords_definition[3]
    number_of_blocks_in_group_2 = ec_codewords_definition[4] if len(
        ec_codewords_definition) >= 5 else None
    number_of_codewords_per_block_in_group_2 = ec_codewords_definition[5] if len(
        ec_codewords_definition) >= 5 else None

    return ec_codewords_definition, total_number_of_datacodewords, error_correction_codewords_per_block, number_of_blocks_in_group_1, number_of_codewords_per_block_in_group_1, number_of_blocks_in_group_2, number_of_codewords_per_block_in_group_2


def generate_message_polynomial(
        data_bytes: list):
    # Split the data in 1 byte chunks
    # data_bytes = [data[i:i + 8] for i in range(0, len(data), 8)]
    message_polynomial = [[int(data_bytes[i], 2), len(
        data_bytes) - 1 - i] for i in range(len(data_bytes))]
    return message_polynomial


def get_ec_codewords(
        data: list,
        qr_version: str,
        error_correction_level: str,
        debug=False):

    ec_codewords_definition, \
        total_number_of_datacodewords, \
        error_correction_codewords_per_block, \
        number_of_blocks_in_group_1, \
        number_of_codewords_per_block_in_group_1, \
        number_of_blocks_in_group_2, \
        number_of_codewords_per_block_in_group_2 = get_ec_codewords_by_level_version(
            qr_version, error_correction_level)

    if debug:
        print("-------------------------------------------------------------------")
        print("GET_EC_CODEWORDS")
        print("\tDATA:", data)
        print("\tLENGTH OF DATA", len(data))

    # Get the message polynomial and the generator polynomial. Those two will be
    # divided.
    generator_polynomial = get_generator_polynomial(
        error_correction_codewords_per_block)
    message_polynomial = generate_message_polynomial(data)
    if debug:
        print("\tGENERATOR POLYNOMIAL:", generator_polynomial)

    # To make sure that the exponent of the lead term doesn't become too small
    #  during the division, multiply the message polynomial by x^n where n is the
    # number of error correction codewords that are needed.
    message_polynomial = [
        [x[0], x[1] + error_correction_codewords_per_block] for x in message_polynomial]

    # The lead term of the generator polynomial should also have the same
    # exponent, so we have to multiply the generator polynomial by n, where n
    # is the difference between the exponent of the message polynomial and the
    # generator polynomial.
    n = message_polynomial[0][1] - generator_polynomial[0][1]
    generator_polynomial = [[x[0], x[1] + n] for x in generator_polynomial]

    # IMPORTANT
    # MESSAGE POLYNOMIAL is in integer notation
    # GENERATOR POLYNOMIAL is in alpha notation (each zero element is multiplied
    # by alpha)

    # Now it is possible to perform the repeated division steps. The number of
    # steps in the division must equal the number of terms in the message
    # polynomial.
    current_polynomial = copy.deepcopy(message_polynomial)
    # for i in range(total_number_of_datacodewords):
    for i in range(len(data)):
        if debug:
            print("\tITERATION", i)
            print(f"\tSTEP {i + 1}a")

        if current_polynomial[0][0] == 0:
            current_polynomial = current_polynomial[1:]
            continue

        new_polinomial = []
        new_generator_polynomial = [[x[0], x[1]-i]
                                    for x in generator_polynomial]
        lead_term_current_polynomial = current_polynomial[0][0]
        lead_term_current_polynomial_alpha = int_to_alpha(
            lead_term_current_polynomial)
        if debug:
            print("\t\tCURRENT POLYNOMIAL", current_polynomial)
            print("\t\tLEAD TERM CURRENT POLYNOMIAL:",
                  lead_term_current_polynomial)
            print("\t\tLEAD TERM CURRENT POLYNOMIAL ALPHA:",
                  lead_term_current_polynomial_alpha)

        # Multiply generator polynomial by lead_term_current_polynomial_alpha
        new_generator_polynomial = [
            [(x[0] + lead_term_current_polynomial_alpha) % 255, x[1]] for x in new_generator_polynomial]
        if debug:
            print("\t\tGENERATOR POLYNOMIAL MULTIPLIED",
                  new_generator_polynomial)

        # Convert the new_generator_polynomial to integer notation
        new_generator_polynomial = [
            [alpha_to_int(x[0]), x[1]] for x in new_generator_polynomial]
        if debug:
            print("\t\tGENERATOR POLYNOMIAL MULTIPLIED INTEGER",
                  new_generator_polynomial)
            print(f"\tSTEP {i + 1}b")

        # XOR the new generator polynomial (auxiliary) with the current polynomial
        aux_polynomial = []

        # For generating the new polinomial, starting from the next exponent using
        # max exponent(first element of the message_polynomial) - 1
        for j in range(message_polynomial[0][1], -1, -1):
            a_term = list(filter(lambda x: x[1] == j, current_polynomial))
            a_term = None if len(a_term) == 0 else a_term[0]

            b_term = list(
                filter(lambda x: x[1] == j, new_generator_polynomial))
            b_term = None if len(b_term) == 0 else b_term[0]

            if a_term is not None and b_term is not None:
                aux_term = [(a_term[0] ^ b_term[0]), j]
            elif a_term is not None:
                aux_term = [(a_term[0]), j]
            elif b_term is not None:
                aux_term = [(b_term[0]), j]
            else:
                aux_term = None

            # if aux_term[0] != 0:
            #  aux_polynomial.append(aux_term)
            if aux_term is not None:
                aux_polynomial.append(aux_term)

        current_polynomial = aux_polynomial[1:]
        if debug:
            print("\t\tCURRENT POLYNOMIAL", current_polynomial)

    ec_codewords = [bin(x[0]).replace("0b", "").zfill(8)
                    for x in current_polynomial]
    if len(ec_codewords) < error_correction_codewords_per_block:
        ec_codewords = ec_codewords + \
            ["00000000"] * \
            (error_correction_codewords_per_block - len(ec_codewords))

    if debug:
        print("-------------------------------------------------------------------")
    return ec_codewords

###############################################

# Numeric mode / Alphanumeric mode / Byte mode (ASCII) / Kanji mode /
# Extended channel interpretation (ECI) / Structured append (data across
# multiple QR) / FNC1


class encoding_modes():
    NUMERIC = "NUMERIC_MODE"
    ALPHANUMERIC = "ALPHANUMERIC_MODE"
    BYTE = "BYTE_MODE"
    KANJI = "KANJI_MODE"

    def get_binary_mode_indicator(encoding_mode):
        if encoding_mode == "NUMERIC_MODE":
            return "0001"
        elif encoding_mode == "ALPHANUMERIC_MODE":
            return "0010"
        if encoding_mode == "BYTE_MODE":
            return "0100"
        if encoding_mode == "KANJI_MODE":
            return "1000"


ALPHANUMERIC_DICTIONARY = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

# The next dictionary contains a string of comma-separated values. Each value,
# in its zero-based position of the string, represents the maximum number of
# characters that can be accomodated per encoding mode, error correction
# level and QR code version. I.E:
#   The string in ENCODING_DATA_SIZES["NUMERIC_MODE"]["L"] = "41,77,127..."
#   means that for numeric mode and error correction level "L", in version 1
#   41 chars can be accomodated, in version 2 77 characters, version 3 127
#   characters, and so on.
ENCODING_DATA_SIZES = {
    "NUMERIC_MODE": {
        "L": "41,77,127,187,255,322,370,461,552,652,772,883,1022,1101,1250,1408,1548,1725,1903,2061,2232,2409,2620,2812,3057,3283,3517,3669,3909,4158,4417,4686,4965,5253,5529,5836,6153,6479,6743,7089",
        "M": "34,63,101,149,202,255,293,365,432,513,604,691,796,871,991,1082,1212,1346,1500,1600,1708,1872,2059,2188,2395,2544,2701,2857,3035,3289,3486,3693,3909,4134,4343,4588,4775,5039,5313,5596",
        "Q": "27,48,77,111,144,178,207,259,312,364,427,489,580,621,703,775,876,948,1063,1159,1224,1358,1468,1588,1718,1804,1933,2085,2181,2358,2473,2670,2805,2949,3081,3244,3417,3599,3791,3993",
        "H": "17,34,58,82,106,139,154,202,235,288,331,374,427,468,530,602,674,746,813,919,969,1056,1108,1228,1286,1425,1501,1581,1677,1782,1897,2022,2157,2301,2361,2524,2625,2735,2927,3057"
    },
    "ALPHANUMERIC_MODE": {
        "L": "25,47,77,114,154,195,224,279,335,395,468,535,619,667,758,854,938,1046,1153,1249,1352,1460,1588,1704,1853,1990,2132,2223,2369,2520,2677,2840,3009,3183,3351,3537,3729,3927,4087,4296",
        "M": "20,38,61,90,122,154,178,221,262,311,366,419,483,528,600,656,734,816,909,970,1035,1134,1248,1326,1451,1542,1637,1732,1839,1994,2113,2238,2369,2506,2632,2780,2894,3054,3220,3391",
        "Q": "16,29,47,67,87,108,125,157,189,221,259,296,352,376,426,470,531,574,644,702,742,823,890,963,1041,1094,1172,1263,1322,1429,1499,1618,1700,1787,1867,1966,2071,2181,2298,2420",
        "H": "10,20,35,50,64,84,93,122,143,174,200,227,259,283,321,365,408,452,493,557,587,640,672,744,779,864,910,958,1016,1080,1150,1226,1307,1394,1431,1530,1591,1658,1774,1852"
    },
    "BYTE_MODE": {
        "L": "17,32,53,78,106,134,154,192,230,271,321,367,425,458,520,586,644,718,792,858,929,1003,1091,1171,1273,1367,1465,1528,1628,1732,1840,1952,2068,2188,2303,2431,2563,2699,2809,2953",
        "M": "14,26,42,62,84,106,122,152,180,213,251,287,331,362,412,450,504,560,624,666,711,779,857,911,997,1059,1125,1190,1264,1370,1452,1538,1628,1722,1809,1911,1989,2099,2213,2331",
        "Q": "11,20,32,46,60,74,86,108,130,151,177,203,241,258,292,322,364,394,442,482,509,565,611,661,715,751,805,868,908,982,1030,1112,1168,1228,1283,1351,1423,1499,1579,1663",
        "H": "7,14,24,34,44,58,64,84,98,119,137,155,177,194,220,250,280,310,338,382,403,439,461,511,535,593,625,658,698,742,790,842,898,958,983,1051,1093,1139,1219,1273"
    },
    "KANJI_MODE": {
        "L": "10,20,32,48,65,82,95,118,141,167,198,226,262,282,320,361,397,442,488,528,572,618,672,721,784,842,902,940,1002,1066,1132,1201,1273,1347,1417,1496,1577,1661,1729,1817",
        "M": "8,16,26,38,52,65,75,93,111,131,155,177,204,223,254,277,310,345,384,410,438,480,528,561,614,652,692,732,778,843,894,947,1002,1060,1113,1176,1224,1292,1362,1435",
        "Q": "7,12,20,28,37,45,53,66,80,93,109,125,149,159,180,198,224,243,272,297,314,348,376,407,440,462,496,534,559,604,634,684,719,756,790,832,876,923,972,1024",
        "H": "4,8,15,21,27,36,39,52,60,74,85,96,109,120,136,154,173,191,208,235,248,270,284,315,330,365,385,405,430,457,486,518,553,590,605,647,673,701,750,784"
    }
}


def determine_code_words(
        qr_version: str,
        error_correction_level: str):
    key = str(qr_version) + '-' + str(error_correction_level)
    return ERROR_CORRECTION_CODE_WORDS[key][0]


def check_alphanunmeric(data: str):
    """
    The following function returns if all chars in the data are present in the
    alphanumeric mode dictionary.

    :data: The data to validate.
    :return: Returns False when a character is not present in the dictionary,
    else returns True
    """
    for c in data:
        if c not in ALPHANUMERIC_DICTIONARY:
            return False
    return True

def check_numeric(data: str):
    is_numeric = False

    if data.isnumeric():
        is_integer = float(data).is_integer()
        is_zero = int(data) == 0 # Zero is not rendered OK if encoded as numeric, so return false so it gets encoded as something else.

        is_numeric = is_integer and not is_zero

    return is_numeric

def best_encode_mode(data: str):
    """
    The following function returns the best encoding mode based on the data.

    :data: The data to define the best encoding mode.
    :return: The best encoding mode.
    """
    if check_numeric(data): 
        return encoding_modes.NUMERIC
    elif check_alphanunmeric(data):
        return encoding_modes.ALPHANUMERIC
    else:
        return encoding_modes.BYTE


def determine_smallest_qr_version(
        encoding_mode: str,
        error_correction_level: str,
        data: str):
    """
    The following function returns the smallest QR version that can accomodate
    the number of characters in the data.

    :data: The data to be encoded.
    :return: A string with the number that represents the QR version, starting
    from '1'.
    """
    sizes = ENCODING_DATA_SIZES[encoding_mode][error_correction_level]
    i = 0
    for size in sizes.split(","):
        i += 1
        if len(data) <= int(size):
            return i

    raise Exception("Data is too large to be fit in any of the QR versions. Please shorten the data.")

def get_char_count_indicator(
        encoding_mode: str,
        version: str,
        data: str):
    data_length = len(data)
    char_count_bit_lengths = {
        "9": {
            encoding_modes.NUMERIC: 10,
            encoding_modes.ALPHANUMERIC: 9,
            encoding_modes.BYTE: 8,
            encoding_modes.KANJI: 8,
        },
        "26": {
            encoding_modes.NUMERIC: 12,
            encoding_modes.ALPHANUMERIC: 11,
            encoding_modes.BYTE: 16,
            encoding_modes.KANJI: 10,
        },
        "40": {
            encoding_modes.NUMERIC: 14,
            encoding_modes.ALPHANUMERIC: 13,
            encoding_modes.BYTE: 16,
            encoding_modes.KANJI: 12,
        }
    }
    if int(version) <= 9:
        return bin(data_length).replace("0b", "").zfill(char_count_bit_lengths["9"][encoding_mode])
    elif int(version) <= 26:
        return bin(data_length).replace("0b", "").zfill(char_count_bit_lengths["26"][encoding_mode])
    elif int(version) <= 40:
        return bin(data_length).replace("0b", "").zfill(char_count_bit_lengths["40"][encoding_mode])


def encode(
        error_correction_level: str,
        data: str,
        qr_version=None):
    encoding_mode = best_encode_mode(data)
    # 1 - Get encoding mode indicator
    encoding_mode_indicator = encoding_modes.get_binary_mode_indicator(
        encoding_mode)

    # 2 - Get smallest QR version required
    #qr_version = qr_version if qr_version is not None else determine_smallest_qr_version(encoding_mode,
    #                                                                                     error_correction_level,
    #                                                                                     data)

    # 3 - Get character count indicator
    char_count_indicator = get_char_count_indicator(
        encoding_mode, qr_version, data)

    # 4 - Encode the data
    encoded_data = None
    if encoding_mode == encoding_modes.NUMERIC:
        encoded_data = encode_numeric(error_correction_level, data)
    elif encoding_mode == encoding_modes.ALPHANUMERIC:
        encoded_data = encode_alphanumeric(error_correction_level, data)
    elif encoding_mode == encoding_modes.BYTE:
        encoded_data = encode_byte(error_correction_level, data)
    else:
        raise Exception("Mode not available.")

    # 5 - Concatenate encoding_mode_indicator + char_count_indicator + encoed_data
    # This is required by the definition of the QR standard.
    encoded_data = encoding_mode_indicator + \
        char_count_indicator + "".join(encoded_data)

    # 6 - Calculate the terminator. The terminator is a string of four '0' at most.
    # For calculating the terminator, first we need to know how many data words
    # are required based on the QR version and the error correction level.
    data_bits_required = determine_code_words(
        qr_version, error_correction_level) * 8
    encoded_data_length = len(encoded_data)
    terminator = ('0000' if ((data_bits_required - encoded_data_length)
                  >= 4) else '0' * (data_bits_required - encoded_data_length))
    encoded_data = encoded_data + terminator

    # 7 - The encoded_data so far must have a length that is multiple of 8. If it
    # is not, we need to add more zeroes until the requirement is met.
    padding_zeroes = ("0" * (8 - (len(encoded_data) % 8))
                      ) if (len(encoded_data) % 8 != 0) else ""
    encoded_data = encoded_data + padding_zeroes

    # 8 - To reach the number of bits required, complete the encoded message with
    # the following sequence of bytes: 11101100 00010001
    bytes_sequence = ["11101100", "00010001"]
    i = 0
    while len(encoded_data) < data_bits_required:
        encoded_data = encoded_data + bytes_sequence[i % 2]
        i += 1

    return encoded_data


def encode_byte(
        error_correction_level: str,
        data: str):
    data_encoded = [bin(ord(i)).replace("0b", "").zfill(8) for i in data]
    return data_encoded


def encode_alphanumeric(
        error_correction_level: str,
        data: str):
    n = 2  # In numeric mode, the number is splitted in groups of three chars.
    data_groups = [data[i:i + n] for i in range(0, len(data), n)]
    data_encoded = []
    for group in data_groups:
        if len(group) > 1:
            group_value = ALPHANUMERIC_DICTIONARY.index(
                group[0]) * 45 + ALPHANUMERIC_DICTIONARY.index(group[1])
            group_value = bin(group_value).replace("0b", "").zfill(11)
        else:
            group_value = ALPHANUMERIC_DICTIONARY.index(group[0])
            group_value = bin(group_value).replace("0b", "").zfill(6)
        data_encoded.append(group_value)

    return data_encoded


def encode_numeric(
        error_correction_level: str,
        data: str):
    n = 3  # In numeric mode, the number is splitted in groups of three chars.
    data = str(int(data)) # Transform to int and then again to str to remove left zeroes.
    data_groups = [str(int(data[i:i + n])) for i in range(0, len(data), n)] 
    
    def convert_group(group):
        if len(group) == 1:
            number = (bin(int(group))).replace("0b", "").zfill(4)
        elif len(group) == 2:
            number = (bin(int(group))).replace("0b", "").zfill(7)
        else:
            number = (bin(int(group))).replace("0b", "").zfill(10)
        return number
    
    data_groups = [convert_group(i) for i in data_groups]
    return data_groups

###############################################


ALIGNMENT_PATTERN_LOCATIONS_PER_VERSION = {
    "1": [], "2": [6, 18], "3": [6, 22], "4": [6, 26], "5": [6, 30], "6": [6, 34], "7": [6, 22, 38], "8": [6, 24, 42], "9": [6, 26, 46],
    "10": [6, 28, 50], "11": [6, 30, 54], "12": [6, 32, 58], "13": [6, 34, 62], "14": [6, 26, 46, 66], "15": [6, 26, 48, 70], "16": [6, 26, 50, 74], "17": [6, 30, 54, 78], "18": [6, 30, 56, 82], "19": [6, 30, 58, 86],
    "20": [6, 34, 62, 90], "21": [6, 28, 50, 72, 94], "22": [6, 26, 50, 74, 98], "23": [6, 30, 54, 78, 102], "24": [6, 28, 54, 80, 106], "25": [6, 32, 58, 84, 110], "26": [6, 30, 58, 86, 114], "27": [6, 34, 62, 90, 118], "28": [6, 26, 50, 74, 98, 122], "29": [6, 30, 54, 78, 102, 126],
    "30": [6, 26, 52, 78, 104, 130], "31": [6, 30, 56, 82, 108, 134], "32": [6, 34, 60, 86, 112, 138], "33": [6, 30, 58, 86, 114, 142], "34": [6, 34, 62, 90, 118, 146], "35": [6, 30, 54, 78, 102, 126, 150], "36": [6, 24, 50, 76, 102, 128, 154], "37": [6, 28, 54, 80, 106, 132, 158], "38": [6, 32, 58, 84, 110, 136, 162], "39": [6, 26, 54, 82, 110, 138, 166],
    "40": [6, 30, 58, 86, 114, 142, 170]
}


def get_base_matrix(qr_version):
    matrix_size = (((qr_version - 1) * 4) + 21)
    base_matrix = [[None for i in range(matrix_size)]
                   for j in range(matrix_size)]
    return base_matrix


def add_finder_patterns(matrix):
    finder_pattern = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
    matrix_size = len(matrix)
    for i in range(7):
        for j in range(7):
            matrix[0 + i][0 + j] = finder_pattern[i][j]
            matrix[matrix_size - 7 + i][0 + j] = finder_pattern[i][j]
            matrix[0 + i][matrix_size - 7 + j] = finder_pattern[i][j]

    return matrix


def add_separators(matrix):
    matrix_size = len(matrix)
    for i in range(8):
        # UPPER LEFT SEPARATOR
        matrix[i][7] = 0
        matrix[7][i] = 0
        # UPPER RIGHT SEPARATOR
        matrix[i][matrix_size - 8] = 0
        matrix[7][matrix_size - 8 + i] = 0
        # BOTTOM LEFT SEPARATOR
        matrix[matrix_size - 8][i] = 0
        matrix[matrix_size - 8 + i][7] = 0

    return matrix


def add_alignment_patterns(matrix, qr_version):
    matrix_size = len(matrix)
    alignment_pattern_base_indexes = ALIGNMENT_PATTERN_LOCATIONS_PER_VERSION[str(
        qr_version)]
    alignment_pattern_locations = []
    for x in alignment_pattern_base_indexes:
        for y in alignment_pattern_base_indexes:
            alignment_pattern_locations.append((x, y))

    base_alignment_pattern = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]

    for location in alignment_pattern_locations:
        # Check if there is something in the matrix before placing the alignment
        # pattern.
        start_location_index_x = location[0] - 2
        start_location_index_y = location[1] - 2
        has_content = False
        for i in range(5):
            if has_content:
                break
            for j in range(5):
                if matrix[start_location_index_x + i][start_location_index_y + j] is not None:
                    has_content = True

        if not has_content:
            for i in range(5):
                for j in range(5):
                    matrix[start_location_index_x + i][start_location_index_y +
                                                       j] = base_alignment_pattern[i][j]

    return matrix


def add_timing_patterns(matrix):
    matrix_size = len(matrix)
    for i in range(matrix_size):
        if matrix[6][i] is None:
            matrix[6][i] = 1 if i % 2 == 0 else 0
        if matrix[i][6] is None:
            matrix[i][6] = 1 if i % 2 == 0 else 0
    return matrix


def add_dark_module(matrix, qr_version):
    dark_module_coordinates = (((4 * qr_version) + 9), 8)
    matrix[dark_module_coordinates[0]][dark_module_coordinates[1]] = 1

    return matrix


def reserve_format_information_area(matrix):
    matrix_size = len(matrix)
    for i in range(9):
        # UPPER LEFT SEPARATOR
        if matrix[i][8] is None:
            matrix[i][8] = 1
        if matrix[8][i] is None:
            matrix[8][i] = 1
        # UPPER RIGHT SEPARATOR
        if i > 0 and matrix[8][matrix_size - 9 + i] is None:
            matrix[8][matrix_size - 9 + i] = 1
        # BOTTOM LEFT SEPARATOR
        # matrix[matrix_size - 9][i] = 4
        if i > 0 and matrix[matrix_size - 9 + i][8] is None:
            matrix[matrix_size - 9 + i][8] = 1

    return matrix


def reserve_version_information_area(matrix, qr_version):
    matrix_size = len(matrix)
    if qr_version >= 7:
        for i in range(6):
            for j in range(3):
                matrix[matrix_size - 11 + j][i] = 4
                matrix[i][matrix_size - 11 + j] = 4

    return matrix


printed = False


def mask_data(mask_number, row, column, data, dev=False):
    # 0
    if mask_number == 0 and ((row + column) % 2 == 0):
        if dev:
            return 3
        else:
            return "1" if data == "0" else "0"
    # 1
    if mask_number == 1 and ((row) % 2 == 0):
        if dev:
            return 3
        else:
            return "1" if data == "0" else "0"
    # 2
    if mask_number == 2 and ((column) % 3 == 0):
        if dev:
            return 3
        else:
            return "1" if data == "0" else "0"
    # 3
    if mask_number == 3 and ((row + column) % 3 == 0):
        if dev:
            return 3
        else:
            return "1" if data == "0" else "0"
    # 4
    if mask_number == 4 and ((math.floor(row / 2) + math.floor(column / 3)) % 2 == 0):
        if dev:
            return 3
        else:
            return "1" if data == "0" else "0"
    # 5
    if mask_number == 5 and (((row * column) % 2) + ((row * column) % 3) == 0):
        if dev:
            return 3
        else:
            return "1" if data == "0" else "0"
    # 6
    if mask_number == 6 and (((row*column) % 2)+((row*column) % 3)) % 2 == 0:
        if dev:
            return 3
        else:
            return "1" if data == "0" else "0"
    # 7
    if mask_number == 7 and (((row+column) % 2)+((row*column) % 3)) % 2 == 0:
        if dev:
            return 3
        else:
            return "1" if data == "0" else "0"

    return data


def add_data(matrix, data, mask_number, dev=False):
    new_matrix = copy.deepcopy(matrix)
    data_index = 0
    column_count = 0
    for i in range(int(len(new_matrix) - 1), 6, -2):
        if column_count % 2 == 0:
            for j in range(len(new_matrix)-1, -1, -1):
                if new_matrix[j][i] is None:
                    new_matrix[j][i] = mask_data(mask_number, j, i, data[data_index % len(
                        data)], dev)  # data[data_index % len(data)]
                    data_index += 1

                if new_matrix[j][i-1] is None:
                    new_matrix[j][i-1] = mask_data(mask_number,
                                                   j, i-1, data[data_index % len(data)], dev)
                    data_index += 1
        else:
            for j in range(len(new_matrix)):
                if new_matrix[j][i] is None:
                    new_matrix[j][i] = mask_data(
                        mask_number, j, i, data[data_index % len(data)], dev)
                    data_index += 1

                if new_matrix[j][i-1] is None:
                    new_matrix[j][i-1] = mask_data(mask_number,
                                                   j, i-1, data[data_index % len(data)], dev)
                    data_index += 1

        column_count += 1

    for i in range(5, -1, -2):
        if column_count % 2 == 0:
            for j in range(len(new_matrix)-1, -1, -1):
                if new_matrix[j][i] is None:
                    new_matrix[j][i] = mask_data(
                        mask_number, j, i, data[data_index % len(data)], dev)
                    data_index += 1

                if new_matrix[j][i-1] is None:
                    new_matrix[j][i-1] = mask_data(mask_number,
                                                   j, i-1, data[data_index % len(data)], dev)
                    data_index += 1
        else:
            for j in range(len(new_matrix)):
                if new_matrix[j][i] is None:
                    new_matrix[j][i] = mask_data(
                        mask_number, j, i, data[data_index % len(data)], dev)
                    data_index += 1

                if new_matrix[j][i-1] is None:
                    new_matrix[j][i-1] = mask_data(mask_number,
                                                   j, i-1, data[data_index % len(data)], dev)
                    data_index += 1

        column_count += 1

    return new_matrix


def calculate_mask_score(matrix):
    # matrix_size = (((qr_version - 1) * 4) + 21)
    matrix_size = len(matrix)
    final_score = 0

    # VALIDATION 1
    # For the first evaluation condition, check each row one-by-one. If there are
    # five consecutive modules of the same color, add 3 to the penalty. If there
    # are more modules of the same color after the first five, add 1 for each
    # additional module of the same color. Afterward, check each column one-by-one
    # , checking for the same condition. Add the horizontal and vertical total to
    # obtain penalty score #1.
    sum_x = 0
    sum_y = 0
    for i in range(matrix_size):
        count_consecutive_x = 0
        count_consecutive_y = 0
        last_value_x = None
        last_value_y = None
        for j in range(matrix_size):
            ##### VALIDATE ROW #####
            if matrix[i][j] == last_value_x:
                count_consecutive_x += 1
            else:
                if count_consecutive_x >= 6:
                    sum_x += 3
                if count_consecutive_x > 6 and (count_consecutive_x % 2 == 0):
                    sum_x += int((count_consecutive_x - 6) / 2)
                count_consecutive_x = 0
            last_value_x = matrix[i][j]
            ##### VALIDATE COL #####
            if matrix[j][i] == last_value_y:
                count_consecutive_y += 1
            else:
                if count_consecutive_y >= 6:
                    sum_y += 3
                if count_consecutive_y > 6 and (count_consecutive_y % 2 == 0):
                    sum_y += int((count_consecutive_y - 6) / 2)
                count_consecutive_y = 0
            last_value_y = matrix[j][i]

        if count_consecutive_x >= 6:
            sum_x += 3
        if count_consecutive_x > 6 and (count_consecutive_x % 2 == 0):
            sum_x += int((count_consecutive_x - 6) / 2)

        if count_consecutive_y >= 6:
            sum_y += 3
        if count_consecutive_y > 6 and (count_consecutive_y % 2 == 0):
            sum_y += int((count_consecutive_y - 6) / 2)

    final_score += sum_x + sum_y

    # VALIDATION 2
    # For second evaluation condition, look for areas of the same color that are
    # at least 2x2 modules or larger. The QR code specification says that for a
    # solid-color block of size m × n, the penalty score is 3 × (m - 1) × (n - 1).
    # However, the QR code specification does not specify how to calculate the
    # penalty when there are multiple ways of dividing up the solid-color blocks.
    # Therefore, rather than looking for solid-color blocks larger than 2x2,
    # simply add 3 to the penalty score for every 2x2 block of the same color in
    # the QR code, making sure to count overlapping 2x2 blocks. For example, a
    # 3x2 block of the same color should be counted as two 2x2 blocks, one
    # overlapping the other.
    validation_2_count = 0
    for i in range(matrix_size - 1):
        for j in range(matrix_size - 1):
            if matrix[i][j] == matrix[i][j+1] == matrix[i+1][j] == matrix[i+1][j+1]:
                validation_2_count += 3

    final_score += validation_2_count

    # VALIDATION 3
    # The third penalty rule looks for patterns of
    # dark-light-dark-dark-dark-light-dark that have four light modules on either
    # side. In other words, it looks for any of the following two patterns:
    validation_3_count = 0
    for i in range(matrix_size - 10):
        for j in range(matrix_size - 10):
            if matrix[i][j] == "0" and \
                    matrix[i][j+1] == "1" and \
                    matrix[i][j+2] == "0" and \
                    matrix[i][j+3] == "0" and \
                    matrix[i][j+4] == "0" and \
                    matrix[i][j+5] == "1" and \
                    matrix[i][j+6] == "0" and \
                    matrix[i][j+7] == "1" and \
                    matrix[i][j+8] == "1" and \
                    matrix[i][j+9] == "1" and \
                    matrix[i][j+10] == "1":
                validation_3_count += 40
            elif matrix[i][j] == "1" and \
                    matrix[i][j+1] == "1" and \
                    matrix[i][j+2] == "1" and \
                    matrix[i][j+3] == "1" and \
                    matrix[i][j+4] == "0" and \
                    matrix[i][j+5] == "1" and \
                    matrix[i][j+6] == "0" and \
                    matrix[i][j+7] == "0" and \
                    matrix[i][j+8] == "0" and \
                    matrix[i][j+9] == "1" and \
                    matrix[i][j+10] == "0":
                validation_3_count += 40

            if matrix[j][i] == "0" and \
                    matrix[j+1][i] == "1" and \
                    matrix[j+2][i] == "0" and \
                    matrix[j+3][i] == "0" and \
                    matrix[j+4][i] == "0" and \
                    matrix[j+5][i] == "1" and \
                    matrix[j+6][i] == "0" and \
                    matrix[j+7][i] == "1" and \
                    matrix[j+8][i] == "1" and \
                    matrix[j+9][i] == "1" and \
                    matrix[j+10][i] == "1":
                validation_3_count += 40
            elif matrix[j][i] == "1" and \
                    matrix[j+1][i] == "1" and \
                    matrix[j+2][i] == "1" and \
                    matrix[j+3][i] == "1" and \
                    matrix[j+4][i] == "0" and \
                    matrix[j+5][i] == "1" and \
                    matrix[j+6][i] == "0" and \
                    matrix[j+7][i] == "0" and \
                    matrix[j+8][i] == "0" and \
                    matrix[j+9][i] == "1" and \
                    matrix[j+10][i] == "0":
                validation_3_count += 40

    final_score += validation_3_count
    # VALIDATION 4
    # The final evaluation condition is based on the ratio of light modules to
    # dark modules. To calculate this penalty rule, do the following steps:
    # 1- Count the total number of modules in the matrix.
    # 2- Count how many dark modules there are in the matrix.
    # 3- Calculate the percent of modules in the matrix that are dark:
    #    (darkmodules / totalmodules) * 100
    # 4- Determine the previous and next multiple of five of this percent. For
    #    example, for 43 percent, the previous multiple of five is 40,
    #    and the next multiple of five is 45.
    # 5- Subtract 50 from each of these multiples of five and take the absolute
    #    value of the result.
    #    For example, |40 - 50| = |-10| = 10 and |45 - 50| = |-5| = 5.
    # 6- Divide each of these by five. For example, 10/5 = 2 and 5/5 = 1.
    # 7- Finally, take the smallest of the two numbers and multiply it by 10.
    #    In this example, the lower number is 1, so the result is 10.
    #    This is penalty score #4.

    count_0 = 0
    count_1 = 0
    for i in range(matrix_size):
        for j in range(matrix_size):
            if matrix[i][j] == "0":
                count_0 += 1
            else:
                count_1 += 1

    dark_pct = int((count_0 / count_1) * 100)

    if dark_pct % 5 != 0:
        previous_multiple_five = int(dark_pct / 5) * 5
        next_multiple_five = previous_multiple_five
    else:
        previous_multiple_five = dark_pct
        next_multiple_five = dark_pct

    previous_multiple_five = abs(previous_multiple_five - 50)
    next_multiple_five = abs(next_multiple_five - 50)

    previous_multiple_five = int(previous_multiple_five / 5)
    next_multiple_five = int(next_multiple_five / 5)

    if previous_multiple_five < next_multiple_five:
        final_score += (previous_multiple_five * 10)
    else:
        final_score += (next_multiple_five * 10)

    return final_score


def add_format_information_string(error_correction_level, mask_pattern, matrix):
    FORMAT_INFORMATION_STRINGS = {
        "L0": "111011111000100",
        "L1": "111001011110011",
        "L2": "111110110101010",
        "L3": "111100010011101",
        "L4": "110011000101111",
        "L5": "110001100011000",
        "L6": "110110001000001",
        "L7": "110100101110110",
        "M0": "101010000010010",
        "M1": "101000100100101",
        "M2": "101111001111100",
        "M3": "101101101001011",
        "M4": "100010111111001",
        "M5": "100000011001110",
        "M6": "100111110010111",
        "M7": "100101010100000",
        "Q0": "011010101011111",
        "Q1": "011000001101000",
        "Q2": "011111100110001",
        "Q3": "011101000000110",
        "Q4": "010010010110100",
        "Q5": "010000110000011",
        "Q6": "010111011011010",
        "Q7": "010101111101101",
        "H0": "001011010001001",
        "H1": "001001110111110",
        "H2": "001110011100111",
        "H3": "001100111010000",
        "H4": "000011101100010",
        "H5": "000001001010101",
        "H6": "000110100001100",
        "H7": "000100000111011"
    }

    key = f"{error_correction_level}{mask_pattern}"
    format_information_string = FORMAT_INFORMATION_STRINGS[key]
    matrix_size = len(matrix)

    # TOP-LEFT format information
    matrix[8][0] = format_information_string[0]
    matrix[8][1] = format_information_string[1]
    matrix[8][2] = format_information_string[2]
    matrix[8][3] = format_information_string[3]
    matrix[8][4] = format_information_string[4]
    matrix[8][5] = format_information_string[5]
    matrix[8][7] = format_information_string[6]
    matrix[8][8] = format_information_string[7]
    matrix[7][8] = format_information_string[8]
    matrix[5][8] = format_information_string[9]
    matrix[4][8] = format_information_string[10]
    matrix[3][8] = format_information_string[11]
    matrix[2][8] = format_information_string[12]
    matrix[1][8] = format_information_string[13]
    matrix[0][8] = format_information_string[14]

    # BOTTOM LEFT + UPPER RIGHT format information
    matrix[matrix_size - 1][8] = format_information_string[0]
    matrix[matrix_size - 2][8] = format_information_string[1]
    matrix[matrix_size - 3][8] = format_information_string[2]
    matrix[matrix_size - 4][8] = format_information_string[3]
    matrix[matrix_size - 5][8] = format_information_string[4]
    matrix[matrix_size - 6][8] = format_information_string[5]
    matrix[matrix_size - 7][8] = format_information_string[6]
    matrix[8][matrix_size - 8] = format_information_string[7]
    matrix[8][matrix_size - 7] = format_information_string[8]
    matrix[8][matrix_size - 6] = format_information_string[9]
    matrix[8][matrix_size - 5] = format_information_string[10]
    matrix[8][matrix_size - 4] = format_information_string[11]
    matrix[8][matrix_size - 3] = format_information_string[12]
    matrix[8][matrix_size - 2] = format_information_string[13]
    matrix[8][matrix_size - 1] = format_information_string[14]

    return matrix


def add_version_information(qr_version, matrix):
    VERSION_INFORMATION_STRINGS = {
        "7": "000111110010010100",
        "8": "001000010110111100",
        "9": "001001101010011001",
        "10": "001010010011010011",
        "11": "001011101111110110",
        "12": "001100011101100010",
        "13": "001101100001000111",
        "14": "001110011000001101",
        "15": "001111100100101000",
        "16": "010000101101111000",
        "17": "010001010001011101",
        "18": "010010101000010111",
        "19": "010011010100110010",
        "20": "010100100110100110",
        "21": "010101011010000011",
        "22": "010110100011001001",
        "23": "010111011111101100",
        "24": "011000111011000100",
        "25": "011001000111100001",
        "26": "011010111110101011",
        "27": "011011000010001110",
        "28": "011100110000011010",
        "29": "011101001100111111",
        "30": "011110110101110101",
        "31": "011111001001010000",
        "32": "100000100111010101",
        "33": "100001011011110000",
        "34": "100010100010111010",
        "35": "100011011110011111",
        "36": "100100101100001011",
        "37": "100101010000101110",
        "38": "100110101001100100",
        "39": "100111010101000001",
        "40": "101000110001101001"
    }

    version_information_string = VERSION_INFORMATION_STRINGS[str(qr_version)]
    matrix_size = len(matrix)
    # BOTTOM LEFT
    matrix[matrix_size - 11][0] = version_information_string[17]
    matrix[matrix_size - 10][0] = version_information_string[16]
    matrix[matrix_size - 9][0] = version_information_string[15]
    matrix[matrix_size - 11][1] = version_information_string[14]
    matrix[matrix_size - 10][1] = version_information_string[13]
    matrix[matrix_size - 9][1] = version_information_string[12]
    matrix[matrix_size - 11][2] = version_information_string[11]
    matrix[matrix_size - 10][2] = version_information_string[10]
    matrix[matrix_size - 9][2] = version_information_string[9]
    matrix[matrix_size - 11][3] = version_information_string[8]
    matrix[matrix_size - 10][3] = version_information_string[7]
    matrix[matrix_size - 9][3] = version_information_string[6]
    matrix[matrix_size - 11][4] = version_information_string[5]
    matrix[matrix_size - 10][4] = version_information_string[4]
    matrix[matrix_size - 9][4] = version_information_string[3]
    matrix[matrix_size - 11][5] = version_information_string[2]
    matrix[matrix_size - 10][5] = version_information_string[1]
    matrix[matrix_size - 9][5] = version_information_string[0]

    # TOP RIGHT
    matrix[0][matrix_size - 11] = version_information_string[17]
    matrix[0][matrix_size - 10] = version_information_string[16]
    matrix[0][matrix_size - 9] = version_information_string[15]
    matrix[1][matrix_size - 11] = version_information_string[14]
    matrix[1][matrix_size - 10] = version_information_string[13]
    matrix[1][matrix_size - 9] = version_information_string[12]
    matrix[2][matrix_size - 11] = version_information_string[11]
    matrix[2][matrix_size - 10] = version_information_string[10]
    matrix[2][matrix_size - 9] = version_information_string[9]
    matrix[3][matrix_size - 11] = version_information_string[8]
    matrix[3][matrix_size - 10] = version_information_string[7]
    matrix[3][matrix_size - 9] = version_information_string[6]
    matrix[4][matrix_size - 11] = version_information_string[5]
    matrix[4][matrix_size - 10] = version_information_string[4]
    matrix[4][matrix_size - 9] = version_information_string[3]
    matrix[5][matrix_size - 11] = version_information_string[2]
    matrix[5][matrix_size - 10] = version_information_string[1]
    matrix[5][matrix_size - 9] = version_information_string[0]

    return matrix

#######################################


def generate_qr(data: str, error_correction_level=None, qr_version=None, dev=False, file_name=None):
    if not error_correction_level:
        error_correction_level = "Q"
    encoding_mode = best_encode_mode(data)
    encoding_mode_indicator = encoding_modes.get_binary_mode_indicator(
        encoding_mode)
    if qr_version is None:
        qr_version = determine_smallest_qr_version(encoding_mode,
                                                   error_correction_level,
                                                   data)
    encoded_qr_info = encode(error_correction_level,
                             data,
                             qr_version=qr_version)

    encoded_qr_info_codewords = [encoded_qr_info[i:i + 8] for i in range(
        0, len(encoded_qr_info), 8)]  # Only for debugging, can be eliminated

    ec_codewords_definition, \
        total_number_of_datacodewords, \
        error_correction_codewords_per_block, \
        number_of_blocks_in_group_1, \
        number_of_codewords_per_block_in_group_1, \
        number_of_blocks_in_group_2, \
        number_of_codewords_per_block_in_group_2 = get_ec_codewords_by_level_version(
            qr_version, error_correction_level)
    number_of_groups = 1 if not number_of_blocks_in_group_2 else 2
    data_codewords = [encoded_qr_info[i:i + 8]
                      for i in range(0, len(encoded_qr_info), 8)]

    groups = []
    ec_groups = []
    start_index = 0
    for i in range(number_of_groups):
        group = []
        ec_group = []
        number_of_blocks = number_of_blocks_in_group_1 if i == 0 else number_of_blocks_in_group_2
        number_of_codewords = number_of_codewords_per_block_in_group_1 if i == 0 else number_of_codewords_per_block_in_group_2
        for j in range(number_of_blocks):
            end_index = start_index + number_of_codewords
            block = data_codewords[start_index: end_index]
            ec_block = get_ec_codewords(
                block,
                qr_version,
                error_correction_level,
            )
            start_index = end_index
            group.append(block)
            ec_group.append(ec_block)
        groups.append(group)
        ec_groups.append(ec_group)

    for i in range(len(ec_groups)):
        group = groups[i]
        ec_group = ec_groups[i]
        for j in range(len(group)):
            block = group[j]
            ec_block = ec_group[j]
    # INTERLEAVE THE DATA CODEWORDS
    iterlieaved_data_codewords = []
    blocks = groups[0] if number_of_groups == 1 else groups[0] + groups[1]
    max_block_length = max([len(x) for x in blocks])

    for i in range(max_block_length):
        for j in range(len(blocks)):
            if i < len(blocks[j]):
                iterlieaved_data_codewords.append(blocks[j][i])

    # INTERLEAVE THE EC CODEWORDS
    iterlieaved_ec_codewords = []
    ec_blocks = ec_groups[0] if number_of_groups == 1 else ec_groups[0] + ec_groups[1]
    max_ec_block_length = max([len(x) for x in ec_blocks])
    for i in range(max_ec_block_length):
        for j in range(len(ec_blocks)):
            if i < len(ec_blocks[j]):
                iterlieaved_ec_codewords.append(ec_blocks[j][i])

    # APPEND INTERLEAVED INFO AND ADD REMAINDERS IF NECCESARY
    binary_data = "".join(iterlieaved_data_codewords +
                          iterlieaved_ec_codewords)

    if qr_version in [2, 3, 4, 5, 6]:
        binary_data = binary_data + "0" * 7
    elif qr_version in [14, 15, 16, 17, 18, 19, 20, 28, 29, 30, 31, 32, 33, 34]:
        binary_data = binary_data + "0" * 3
    elif qr_version in [21, 22, 23, 24, 25, 26, 27]:
        binary_data = binary_data + "0" * 4

    ##########################

    #### MATRIX PLACEMENT ######
    matrix = get_base_matrix(qr_version)
    matrix = add_finder_patterns(matrix)
    matrix = add_separators(matrix)
    matrix = add_alignment_patterns(matrix, qr_version)
    matrix = add_timing_patterns(matrix)
    matrix = add_dark_module(matrix, qr_version)
    matrix = reserve_format_information_area(matrix)
    matrix = reserve_version_information_area(matrix, qr_version)

    best_matrix = None
    best_mask = None
    best_mask_score = None
    for x in range(8):  # Loop through all the possible masking options
        temp_matrix = add_data(matrix, binary_data, x, dev=False)
        temp_score = calculate_mask_score(temp_matrix)
        if best_mask_score is None:
            best_matrix = temp_matrix
            best_mask_score = temp_score
            best_mask = x
        elif temp_score < best_mask_score:
            best_matrix = temp_matrix
            best_mask_score = temp_score
            best_mask = x

    best_matrix = add_format_information_string(error_correction_level,
                                                best_mask,
                                                best_matrix)

    if qr_version >= 7:
        best_matrix = add_version_information(qr_version,
                                              best_matrix)

    image = generate_image_from_binary_matrix(best_matrix)
    # display(image)
    image.save(file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--data", type=str,
                        help="The data to add as information in the QR code.")
    parser.add_argument("--file_name", type=str,
                        help="The name of the file to save the QR code.")
    parser.add_argument("--error_correction_level", type=str, help="""The error correction level to use for generating the QR code. This argument must take any of the following values
  L:	Recovers 7% of data
  M:	Recovers 15% of data
  Q:	Recovers 25% of data
  H:	Recovers 30% of data
If no error correction level is specified, by default the script will use Q.""")
    parser.add_argument("--qr_version", type=int, help="The QR version to use. It must take a value from 1 to 40. If no version is specified, the script will use the most convenient. Keep in mind that if you use a version that cannot store all data, it will result in a QR code with partial information.")

    args = parser.parse_args()
    data = args.data
    file_name = args.file_name
    error_correction_level = args.error_correction_level
    qr_version = args.qr_version

    errors = []
    if data is None:
        errors.append("data - Missing the data to add to the QR code.")

    if file_name is None:
        errors.append(
            "file_name - Missing the name of the file to save the QR code.")

    if qr_version is not None and (qr_version < 1 or qr_version > 40):
        errors.append(
            "qr_version - The QR version must be a number between 1 and 40.")

    if error_correction_level is not None and error_correction_level not in ["L", "M", "Q", "H"]:
        errors.append(
            "error_correction_level - The error correction level must be 'L','M','Q' or 'H'.")

    if errors != []:
        errors_str = "\n\t" + "\n\t".join(errors)
        raise Exception(f"Missing or incorrect configurations: {errors_str}")
    else:
        generate_qr(data=data, error_correction_level=error_correction_level,
                    qr_version=qr_version, file_name=file_name)
