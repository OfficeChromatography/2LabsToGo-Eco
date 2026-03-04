#!/usr/bin/env python3
#distort-fisheye.py

import cv2
import os
import typer
import numpy as np

from pathlib import Path
from typing import Optional

app = typer.Typer()


@app.command()
def straighten(file_format: Optional[str] = 'jpg',
               source_folder: Optional[Path] = typer.Option(Path('.'),
                                                            help="Source folder that contains the images"),
               output_folder: Optional[Path] = typer.Option(Path('./corrected/'),
                                                            help="Destination folder for the the images processed")):
    if not output_folder.is_dir():
        try:
            os.mkdir(output_folder)
        except OSError:
            print("Creation of the directory %s failed" % output_folder)

    for img_path in source_folder.glob(f"*.{file_format}"):
        FixDistortionImage(path=img_path, output_path=output_folder)


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


class FixDistortionImage:

    def __init__(self, path, output_path):
        self.path_photo = path
        self.output_path = output_path
        self.img = cv2.imread(str(self.path_photo))
        self.img = cv2.resize(self.img, dsize=(2028, 1520), interpolation=cv2.INTER_CUBIC)

        self.correction_mtx = np.array(
            [[1967.921637060819, 0.0, 980.07213571975], [0.0, 1964.823317953312, 741.073015742526], [0.0, 0.0, 1.0]])

        self.correction_dist = np.array([[-0.4778321949564693, 0.2886513041769561, 0.0016895448886501186,
                                          0.0047619737564622905, -0.12895314122999252]])

        self.rotation_angle = 180

        # Undistort the image
        self.undistort()

    def undistort(self):
        # Using the fixed values mtx and dist, it straighten the image
        # and also cut the black borders
        h, w = self.img.shape[:2]
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(self.correction_mtx,
                                                            self.correction_dist,
                                                            (w, h),
                                                            1,
                                                            (w, h))
        # undistort
        dst = cv2.undistort(self.img,
                            self.correction_mtx,
                            self.correction_dist,
                            None,
                            new_camera_mtx)
        # crop the image
        #x, y, w, h = roi
        #print (x)
        #print (y)
        #print (w)
        #print (h)
        
        x=420
        y=220
        w=1080
        h=1080
        
        #dst = dst[y:y + h, x:x + w]

        self.path_photo = f'{self.output_path}/{self.path_photo.stem}_corrected{self.path_photo.suffix}'

        new_image = rotate_image(dst, self.rotation_angle)
        # print(self.path_photo)
        cv2.imwrite(self.path_photo, new_image)


if __name__ == "__main__":
    app()
