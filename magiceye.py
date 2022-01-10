# -*- coding: utf-8 -*-

from PIL import Image
import argparse, os


def create_magiceye(depth_image, pattern_image, shift_amplitude):
    """Creates a magiceye from depth map and pattern
    """
    depth_width, depth_height = depth_image.size
    depth_pixels = depth_image.load()
    pattern_width, pattern_height = pattern_image.size
    pattern_pixels = pattern_image.load()

    output_image = Image.new('RGB', (depth_width, depth_height))
    output_pixels = output_image.load()
    for r in range(depth_height):
        for c in range(depth_width):
            if c < pattern_width:
                # no values are shifted in the first pattern
                output_pixels[c, r] = pattern_pixels[c, r % pattern_height]
            else:
                shift = int(depth_pixels[c, r] * shift_amplitude * pattern_width / 255)
                output_pixels[c, r] = output_pixels[c - pattern_width + shift, r]
    return output_image


def load_image(filename, new_width=None):
    image = Image.open(filename)
    if new_width:
        # resize image
        width, height = image.size
        new_height = int(new_width * height / width)
        image = image.resize((new_width, new_height))
    return image


def get_basename(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('depth', help='File with the depth map')
    parser.add_argument('pattern', help='File with the background pattern')
    parser.add_argument('--shift', type=float, default=0.25, help='How much to shift the depth map')
    parser.add_argument('--output-size', type=int, default=1000, help='Size of output image')
    parser.add_argument('--pattern-size', type=int, default=200, help='Size of pattern image')
    parser.add_argument('--show', action='store_true', help='Whether to display image')
    parser.add_argument('--output', help='The output file')
    args = parser.parse_args()

    depth_image = load_image(args.depth, args.output_size).convert('I')
    pattern_image = load_image(args.pattern, args.pattern_size)
    output = create_magiceye(depth_image, pattern_image, args.shift)
    output_file = args.output if args.output else 'magiceye_{}_{}.jpg'.format(get_basename(args.depth), get_basename(args.pattern))
    output.save(output_file)
    if args.show:
        output.show()
    
    
if __name__ == '__main__':
    main()
