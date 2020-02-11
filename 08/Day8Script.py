from math import inf


def get_input():
    with open('08/input.txt', 'r') as input_file:
        return input_file.read()


def get_layers(inp):
    return [image_input[i:i + layer_size] for i in range(0, len(inp), layer_size)]


def part_1():
    result = 0
    min_0s = inf

    for layer in layers:
        count0 = layer.count('0')
        if count0 < min_0s:
            min_0s = count0

    return result


def get_pixel(pixels):
    for pixel in pixels:
        if pixel == '0':
            return ' '
        elif pixel == '1':
            return '*'
        elif pixel == '2':
            continue
        else:
            print('ERROR')
            break


def to_image(image):
    img_str = ''
    for y in range(len_y):
        for x in range(len_x):
            img_str += image[y][x]
        img_str += '\n'
    return img_str


def get_image():
    image = []
    for y in range(len_y):
        row = []
        for x in range(len_x):
            i = (len_x * y) + x
            pixels = [layer[i] for layer in layers]
            row.append(get_pixel(pixels))
        image.append(row)
    return to_image(image)


if __name__ == '__main__':
    image_input = get_input()
    len_x = 25
    len_y = 6
    layer_size = len_x * len_y
    layers = get_layers(image_input)

    print('2s*1s = ', part_1())
    print("resulting image: \n" + get_image())
