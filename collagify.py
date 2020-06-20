#!/usr/bin/env python3

from collections import defaultdict
from PIL import Image
import argparse
import math
import random
import sample_convex_combinations
import sys
import time


MIN_NUM_CELLS = 5
NUM_CELLS_PER_SOURCE = 2.2
CELLS_MARGIN = -50
WEIGHTING_MINDIST = 1e-3
# Should be between -inf and 0.  "closer to -inf" makes the cells "sharper".
# Positive values make everything weird.
WEIGHTING_ALPHA = -1.9
RGB_GAMMA = 1.8
PRINT_DOTS = 80
CHOOSE_UNIFORM = False


def sample_position(size):
    w, h = size
    pos = (CELLS_MARGIN + random.random() * (w - 2 * CELLS_MARGIN),
           CELLS_MARGIN + random.random() * (h - 2 * CELLS_MARGIN))
    return pos


def sample_combination(num_imgs):
    if CHOOSE_UNIFORM:
        return sample_convex_combinations.sample(num_imgs)
    else:
        result = [0] * num_imgs
        result[random.randrange(num_imgs)] = 1
        return result

# `x` and `y` can and will be floats!
def compute_indicator_weights(x, y, indicator_positions):
    weights = []
    for i_x, i_y in indicator_positions:
        dx, dy = i_x - x, i_y - y
        i_dist = max(math.sqrt(dx * dx + dy * dy), WEIGHTING_MINDIST)
        i_weight = i_dist ** WEIGHTING_ALPHA
        weights.append(i_weight)
    return weights


def compute_weighted_sum(weights, vectors):
    assert len(weights) == len(vectors)
    assert len(set(len(v) for v in vectors)) == 1
    vector_result = [0] * len(vectors[0])
    for weight, vector in zip(weights, vectors):
        for i, component in enumerate(vector):
            vector_result[i] += component * weight / sum(weights)
    return vector_result


def apply_gamma(rgbish):
    return tuple((c / 255) ** RGB_GAMMA for c in rgbish)


def remove_gamma(rgbish):
    return tuple(max(0, min(int(255 * c ** (1 / RGB_GAMMA)), 255)) for c in rgbish)


def run_with_images(imgs):
    assert len(set((img.mode, img.size) for img in imgs)) == 1
    num_cells = max(MIN_NUM_CELLS, math.ceil(NUM_CELLS_PER_SOURCE * len(imgs)))
    indicator_positions = [sample_position(imgs[0].size) for _ in range(num_cells)]
    indicator_combinations = [sample_combination(len(imgs)) for _ in range(num_cells)]

    data = []
    dots_printed = 0
    for y in range(imgs[0].height):
        while y / imgs[0].height >= dots_printed / PRINT_DOTS:
            print('.', end='')
            sys.stdout.flush()
            dots_printed += 1
        for x in range(imgs[0].width):
            nx, ny = x + 0.0, y + 0.0  # TODO: Add noise here
            indicator_weights = compute_indicator_weights(nx, ny, indicator_positions)
            weighted_vector = compute_weighted_sum(indicator_weights, indicator_combinations)
            assert len(weighted_vector) == len(imgs)
            assert 0.99 <= sum(weighted_vector) <= 1.01

            img_cols = [apply_gamma(img.getpixel((nx, ny))) for img in imgs]
            result_col = remove_gamma(compute_weighted_sum(weighted_vector, img_cols))
            data.append(result_col)
    print()
    result = Image.new(imgs[0].mode, imgs[0].size)
    result.putdata(data)
    return result


def run_with_files(sources, output):
    assert len(sources) >= 2
    assert 'all files in "sources" exist'
    imgs = [(Image.open(src), src) for src in sources]
    classes = defaultdict(list)
    for img, src in imgs:
        w, h = img.size
        classes[(w, h, img.mode)].append(src)
    if len(classes) != 1:
        print('Incompatible sizes:', file=sys.stderr)
        for (w, h), srcs in classes:
            print('{}x{} found in {}.'.format(w, h, ', '.join(srcs)), file=sys.stderr)
        return False
    just_imgs = [img for img, _ in imgs]
    result = run_with_images(just_imgs)
    result.save(output)
    return True


def make_parser(progname):
    parser = argparse.ArgumentParser(
        prog=progname, description='Makes a voronoi-y collage of the given images.')
    parser.add_argument(
        '-o', '--output', default=time.strftime('output_%s.png'), help='''
            Where the output shall be written.''')
    parser.add_argument(
        'sources', nargs='+', help='''
            Input files.  Supply at least 2.  Must of of identical size.''')
    return parser


def run(args):
    options = make_parser(args[0]).parse_args(args[1:])
    if len(options.sources) < 2:
        print('Must supply at least 2 source images.', file=sys.stderr)
        exit(1)
    if not run_with_files(options.sources, options.output):
        exit(2)


if __name__ == '__main__':
    run(sys.argv)
