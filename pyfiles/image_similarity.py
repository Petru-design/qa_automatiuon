import os

import cv2
import numpy as np
from skimage.metrics import structural_similarity


class StructuralSimilarity:
    __slots__ = ("__base_image", "__image", "__score",
                 "__diff", "__contours", "__mask", "__output")

    def __init__(self, base_image: str, image: str) -> None:
        self.__base_image = cv2.imread(base_image)
        self.__image = cv2.imread(image)

        self.__diff: np.ndarray = None
        self.__score: float = None
        self.__contours: np.ndarray = None
        self.__mask: np.ndarray = None
        self.__output: np.ndarray = None
        self.__resize_images()
        self.__highlight_diferences_in_images()

    @property
    def base_image(self) -> np.ndarray:
        """ Get base image with contours around differences from input image """
        return self.__base_image

    @property
    def image(self) -> np.ndarray:
        """ Get input image with contours around differences from base image """
        return self.__image

    @property
    def diff(self) -> np.ndarray:
        """
        Get structural difference image
        """
        return self.__diff

    @property
    def score(self) -> float:
        """
        Get score of structural similarity
        """
        return self.__score

    @property
    def contours(self) -> np.ndarray:
        """
        Get contours of differences
        """
        if not self.__contours:
            # The diff image contains the actual image differences between the two images
            # and is represented as a floating point data type so we must convert the array
            # to 8-bit unsigned integers in the range [0,255] before we can use it with OpenCV
            _, diff = self.__structural_similarity
            diff = (diff * 255).astype("uint8")

            # Threshold the difference image, followed by finding contours to
            # obtain the regions that differ between the two images
            thresh = cv2.threshold(
                diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            contours = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.__contours = contours[0] if len(
                contours) == 2 else contours[1]
        return self.__contours

    @property
    def mask(self) -> np.ndarray:
        """
        Get mask image of differences
        """
        return self.__mask

    @property
    def output(self) -> np.ndarray:
        """
        Get output image (input+mask)
        """
        return self.__output

    def __resize_images(self) -> None:
        """
        Resize images to same dimensions
        """
        if self.__image.shape != self.__base_image.shape:
            self.__image = cv2.resize(
                self.__image, self.__base_image.shape[:2])

    @property
    def __structural_similarity(self) -> tuple[float, np.ndarray]:
        """Compute the structural similarity between two images"""
        # if score and diff already computed, return
        if not (self.__score and self.__diff):
            # Compute SSIM between two images
            first_gray = cv2.cvtColor(self.__base_image, cv2.COLOR_BGR2GRAY)
            second_gray = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)
            self.__score, self.__diff = structural_similarity(
                first_gray, second_gray, full=True)
        return (self.__score, self.__diff)

    def __highlight_diferences_in_images(self) -> None:
        """
        Highlight differences in the images
        """
        if not (self.__mask and self.__output):
            self.__mask = np.zeros(self.__image.shape, dtype="uint8")
            self.__output = self.__image.copy()
            contours = self.contours
            for c in contours:
                area = cv2.contourArea(c)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(self.__base_image, (x, y),
                                  (x + w, y + h), (36, 255, 12), 2)
                    cv2.rectangle(self.__image, (x, y),
                                  (x + w, y + h), (36, 255, 12), 2)
                    cv2.drawContours(self.__mask, [c], 0, (0, 255, 0), -1)
                    cv2.drawContours(self.__output, [c], 0, (0, 255, 0), -1)

    def show_images(self,
                    image: bool | None,
                    base_image: bool | None,
                    diff: bool | None,
                    mask: bool | None,
                    output: bool = True,
                    labels: bool = True,
                    timer: int = 0) -> None:
        """
        Show images

        image (optional): bool -> show original image
        base_image (optional): bool -> show base image
        diff (optional): bool -> show differences between images
        mask (optional): bool -> show mask of differences
        output (default=True): bool -> show output image (original+mask)
        labels (default=True): bool -> show labels on output
        timer (default=0 [inf]): int -> time in miliseconds to wait before closing preview
        """
        images = []
        if image:
            images.append(("Image", self.__image))
        if base_image:
            images.append(("Base Image", self.__base_image))
        if diff:
            images.append(("Diff", self.__diff))
        if mask:
            images.append(("Mask", self.__mask))
        if output:
            images.append(("Output", self.__output))
        for (name, image) in images:
            if labels:
                org = (int(image.shape[0]/2), 50)
                cv2.putText(img=image, text=name, org=org,
                            fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0), thickness=2)

            cv2.imshow("Image Similarity", image)
            cv2.waitKey(timer)

    def save_images(self,
                    output_dir: str | None = None,
                    image: bool = False,
                    base_image: bool = False,
                    diff: bool = False,
                    mask: bool = False,
                    output: bool = True,
                    labels: bool = True) -> None:
        """
        Save images

        Arguments:

        output_dir (optional): bool -> output directory
        image (optional): bool -> image name
        base_image (optional): bool -> base image name
        diff (optional): bool -> diff name
        mask (optional): bool -> mask name
        output (optional): bool -> output name
        labels (default=True): bool -> show labels on output
        """
        images = []
        if image:
            images.append(("Image", self.__image))
        if base_image:
            images.append(("Base Image", self.__base_image))
        if diff:
            images.append(("Diff", self.__diff))
        if mask:
            images.append(("Mask", self.__mask))
        if output:
            images.append(("Output", self.__output))
        for (name, image) in images:
            if labels:
                org = (int(image.shape[0]/2), 50)
                cv2.putText(img=image, text=name, org=org,
                            fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0), thickness=2)

            if output_dir:
                cv2.imwrite(os.path.join(output_dir, name), image)
            else:
                cv2.imwrite(f"{name}.png", image)
