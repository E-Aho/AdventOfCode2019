from math import inf

def get_input():
    with open('8/input.txt', 'r') as input_file:
        return (input_file.read())

input = get_input()
len_x = 25
len_y = 6
layer_size = len_x * len_y

layers = [input[i:i+layer_size] for i in range(0,len(input),layer_size)]

result = 0
min_0s = inf

for layer in layers:
    count0 = layer.count('0')
    if count0 < min_0s:
        min_0s = count0

print('2s*1s = ', result)

def get_pixel(pixels):
    for pixel in pixels:
        if pixel == '0':
            return '0'
        elif pixel =='1':
            return '1'
        elif pixel =='2':
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

image = []

for y in range(len_y):
    row = []
    for x in range(len_x):
        i = (len_x * y) + x
        pixels = [layer[i] for layer in layers]
        row.append(get_pixel(pixels))
    image.append(row)

print(to_image(image))