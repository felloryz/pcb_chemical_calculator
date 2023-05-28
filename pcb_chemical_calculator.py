from PIL import Image
from prettytable import PrettyTable
import sys

Image.MAX_IMAGE_PIXELS = None

print('Enter path to the image:')
image_path = input()

with Image.open(image_path) as im:

    if im.format != 'BMP':
        print('Incorrect image format')
        sys.exit()

    image_dpi = im.info['dpi'][0];

    pcb_width = im.width / (image_dpi / 25.4)
    pcb_height = im.height / (image_dpi / 25.4)

    print(f'PCB dimensions are {round(pcb_width, 2)} x {round(pcb_height, 2)} mm? (y/n)')
    check_pcb_dimensions = input()
    if (check_pcb_dimensions == 'y'):
        pass
    elif (check_pcb_dimensions == 'n'):
        print('Enter PCB width in mm:')
        pcb_width = float(input())
        print('Enter PCB height in mm:')
        pcb_height = float(input())
    else:
        print('Incorrect command')
        sys.exit()
    pcb_area = pcb_width * pcb_height

    print('Image inverted? (y - traces are white, n - traces are black)')
    check_colors = input()
    if (check_colors == 'y'):
        is_inverted = True
    elif (check_colors == 'n'):
        is_inverted = False
    else:
         print('Incorrect command')
         sys.exit()

    print('Concentration of hydrogen peroxide solution (H2O2) is 37%? (y/n)')
    h2o2_check = input()
    if (h2o2_check == 'y'):
        h2o2_concentration = 37
    elif (h2o2_check == 'n'):
        print('Enter dhdrogen peroxide (H2O2) concentration in percent (%):')
        h2o2_concentration = int(input())
    else:
         print('Incorrect command')
         sys.exit()

    print('\nCalculating...\n')

    black = 0
    white = 0

    for pixel in im.getdata():
        if pixel == 0:
            black += 1
        else:
            white += 1
        
    if is_inverted:
        copper_area = (black / (black + white)) * pcb_area
    else:
        copper_area = (white / (black + white)) * pcb_area

    h2o2_solution = (3 * 100 / h2o2_concentration) / 10000 * copper_area
    h2o = (100 - (3 * 100 / h2o2_concentration)) / 10000 * copper_area
    c6h8o7 = 30 / 10000 * copper_area
    nacl = 5 / 10000 * copper_area

    # print(f'{h2o2_concentration}% hydrogen peroxide solution (H2O2): {round(h2o2_solution, 2)} g')
    # print(f'Water (H2O): {round(h2o, 2)} g')
    # print(f'Citric acid (C6H8O7): {round(c6h8o7, 2)} g')
    # print(f'Salt (NaCl): {round(nacl, 2)} g\n')

    table = PrettyTable(['Chemical', 'Formula', 'Weight, gr'])
    table.add_row([f'{h2o2_concentration}% hydrogen peroxide solution', 'H2O2', round(h2o2_solution, 2)])
    table.add_row(['Water', 'H2O', round(h2o, 2)])
    table.add_row(['Citric acid', 'C6H8O7', round(c6h8o7, 2)])
    table.add_row(['Salt', 'NaCl', round(nacl, 2)])
    print(table, end='\n\n')