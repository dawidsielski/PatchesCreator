import cv2
import os
import random
import glob
import shutil

from tqdm import tqdm


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

    def process_image(self, path):
        cartoon_frame_number = os.path.basename(path).split('.')[0]

        cartoon = os.path.basename(os.path.dirname(path))

        img = cv2.imread(path)

        i = 0
        while i < self.patches:
            x, y = PatchesCreation.generate_new_position(self.patches_size, img.shape[0])
            patch = img[x: x + self.patches_size, y: y + self.patches_size]

            cv2.imwrite(os.path.join('patches', cartoon, '{}_{}_{}.png'.format(cartoon_frame_number, x, y)), patch)

            i += 1

    def process_directory(self, directory):
        try:
            shutil.rmtree('patches')
        except FileNotFoundError:
            pass

        ignore = shutil.ignore_patterns('*.png')
        src = os.path.join(os.getcwd(), directory)
        dst = os.path.join(os.getcwd(), 'patches')

        try:
            shutil.copytree(src, dst, ignore=ignore)
        except FileExistsError:
            pass

        images = glob.glob('{}/**/*.png'.format(directory), recursive=True)

        for img_path in tqdm(images):
            self.process_image(img_path)


if __name__ == '__main__':
    path = 'training_set'

    pc = PatchesCreation()
    pc.process_directory(path)
