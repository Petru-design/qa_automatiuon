import difflib
import os
import re

import cv2
import numpy as np
from skimage.metrics import structural_similarity


class StructuralSimilarity:

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

        output_dir (optional): str -> output directory
        image (optional): str -> image name
        base_image (optional): str -> base image name
        diff (optional): str -> diff name
        mask (optional): str -> mask name
        output (optional): str -> output name
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


class TextSimilarly:

    def __init__(self, text: str, base_text: str) -> None:
        self.text = text
        self.base_text = base_text

        self.__score: float = 0
        self.__distance: int = None
        self.__text_equalized: list[str] = None
        self.__base_text_equalized: list[str] = None
        self.damerau_levenshtein()

    def damerau_levenshtein(self) -> float:
        """
        Compute the Damerau-Levenshtein distance between two strings.
        This distance is the number of additions, deletions, substitutions,
        and transpositions needed to transform the first string into the
        second string.
        """
        if not (self.__distance and self.__score):
            n1 = len(self.text)
            n2 = len(self.base_text)
            self.__distance = self.__levenshtein_distance_matrix(is_damerau=False)[
                n1, n2]
            self.__score = 1 - self.__distance / \
                max(len(self.text), len(self.base_text))

        return (self.__distance, self.__score)

    def __levenshtein_distance_matrix(self, is_damerau: bool = False) -> np.ndarray:
        """
        Compute the Levenshtein distance matrix between two strings.
        This distance is the number of additions, deletions, substitutions,
        and transpositions needed to transform the first string into the
        second string.
        """

        # Initialize the matrix
        matrix = np.zeros(
            (len(self.text) + 1, len(self.base_text) + 1), dtype="uint8")

        # Compute the Levenshtein distance matrix
        for i in range(1, len(self.text) + 1):
            for j in range(1, len(self.base_text) + 1):
                if self.text[i - 1] == self.base_text[j - 1]:
                    matrix[i][j] = matrix[i - 1][j - 1]
                else:
                    matrix[i][j] = min(
                        matrix[i - 1][j] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j - 1] + 1,
                    )
                if is_damerau:
                    if i > 1 and j > 1 and self.text[i - 1] == self.base_text[j - 2] and self.text[i - 2] == self.base_text[j - 1]:
                        matrix[i][j] = min(
                            matrix[i][j], matrix[i - 2][j - 2] + 1)

        return matrix

    @staticmethod
    def __tokenize(s: str) -> str:
        """ Tokenize a string """
        return re.split('\s+', s)

    @staticmethod
    def __untokenize(s: str) -> str:
        """ Untokenize a string """
        return ' '.join(s)

    def __equalize(self) -> tuple[str, str]:
        """Make strings equal in size by inserting _ characters in diffrerring positions"""
        if not (self.__text_equalized and self.__base_text_equalized):
            self.__text_equalized = self.__tokenize(self.text)
            self.__base_text_equalized = self.__tokenize(self.base_text)
            l1 = self.__tokenize(self.text)
            l2 = self.__tokenize(self.base_text)
            res1 = []
            res2 = []
            prev = difflib.Match(0, 0, 0)
            for match in difflib.SequenceMatcher(a=l1, b=l2).get_matching_blocks():
                if (prev.a + prev.size != match.a):
                    for i in range(prev.a + prev.size, match.a):
                        res2 += ['_' * len(l1[i])]
                    res1 += l1[prev.a + prev.size:match.a]
                if (prev.b + prev.size != match.b):
                    for i in range(prev.b + prev.size, match.b):
                        res1 += ['_' * len(l2[i])]
                    res2 += l2[prev.b + prev.size:match.b]
                res1 += l1[match.a:match.a+match.size]
                res2 += l2[match.b:match.b+match.size]
                prev = match

            self.__text_equalized = self.__untokenize(res1)
            self.__base_text_equalized = self.__untokenize(res2)

        return (self.__text_equalized, self.__base_text_equalized)

    @staticmethod
    def __split_into_lines(string: str, every: int = 40, window: int = 10) -> list[str]:
        """ Split a string into lines of a given length.
        Every specifies the number of characters in each line.
        """
        result = []
        from_str = string
        while len(from_str) > 0:
            cut_off = every
            if len(from_str) > every:
                while (from_str[cut_off - 1] != ' ') and (cut_off > (every-window)):
                    cut_off -= 1
            else:
                cut_off = len(from_str)
            part = from_str[:cut_off]
            result += [part]
            from_str = from_str[cut_off:]
        return result

    def get_printable_comparation(self,
                                  width: int = 40,
                                  margin: int = 10,
                                  sidebyside: bool = True,
                                  compact: bool = False) -> str:
        """ Show a comparison of two strings.
        The strings are split into lines of a given length.
        The comparison is shown side by side or vertically.

        Args:
            width: The width of the lines.
            margin: The margin considered for a word to be a part of the same line.
            sidebyside: If True, the comparison is shown side by side.
            compact: If True, the comparison is shown compact (without _). """
        s1, s2 = self.__equalize()
        output = ""
        if sidebyside:
            s1_tokens = self.__split_into_lines(s1, width, margin)
            s2_tokens = self.__split_into_lines(s2, width, margin)
            if compact:
                for i in range(0, len(s1_tokens)):
                    lft = re.sub(
                        ' +', ' ', s1_tokens[i].replace('_', '')).ljust(width)
                    rgt = re.sub(
                        ' +', ' ', s2_tokens[i].replace('_', '')).ljust(width)
                    output += f"{lft} | {rgt} | \n"
            else:
                for i in range(0, len(s1_tokens)):
                    lft = s1_tokens[i].ljust(width)
                    rgt = s2_tokens[i].ljust(width)
                    output += f"{lft} | {rgt} | \n"
        else:
            output = f"{lft}\n{rgt}"
        return output

    def write_comparation(self,
                          output_path: str,
                          width: int = 40,
                          margin: int = 10,
                          sidebyside: bool = True,
                          compact: bool = False) -> None:
        """ Show a comparison of two strings.
        The strings are split into lines of a given length.
        The comparison is shown side by side or vertically.

        Args:
            output_path: The path to the output file. If None, the output is printed to stdout.
            width: The width of the lines.
            margin: The margin considered for a word to be a part of the same line.
            sidebyside: If True, the comparison is shown side by side.
            compact: If True, the comparison is shown compact (without _). """

        output = self.get_printable_comparation(
            width, margin, sidebyside, compact)

        with open(output_path, 'w') as f:
            f.write(output)
