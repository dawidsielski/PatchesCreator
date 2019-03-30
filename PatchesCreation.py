import cv2
import os
import random
import glob

from tqdm import tqdm

PATCHES_SIZE = 32
NUMBER_OF_PATCHES = 60


class PatchesCreation(object):

    def __init__(self, patches_size=32, patches=60):
        self.patches_size = patches_size
        self.patches = patches

    @staticmethod
    def check_entropy():
        pass

    @staticmethod
    def generate_new_position(patches_size, upper_bound_img_size):
        upper_bound, lower_bound = patches_size, upper_bound_img_size - patches_size
        x, y = random.randint(upper_bound, lower_bound), random.randint(upper_bound, lower_bound)
        return x, y

    @staticmethod
    def process_image(path, patches_size=PATCHES_SIZE):
        cartoon_number = os.path.basename(path).split('.')[0]

        if not os.path.isdir('patches'):
            os.mkdir('patches')

        cartoon = os.path.basename(os.path.dirname(path))
        new_dir = os.path.join('patches', cartoon)
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)

        img = cv2.imread(path)

        i = 0
        while i < NUMBER_OF_PATCHES:
            x, y = PatchesCreation.generate_new_position(patches_size, img.shape[0])
            patch = img[x: x + patches_size, y: y + patches_size]

            cv2.imwrite(os.path.join(new_dir, '{}_{}_{}.png'.format(cartoon_number, x, y)), patch)

            i += 1

    @staticmethod
    def process_directory():
        images = glob.glob('training_set/**/*.png', recursive=True)

        for path in tqdm(images):
            PatchesCreation.process_image(path)


if __name__ == '__main__':
    pc = PatchesCreation()
    pc.process_directory()
