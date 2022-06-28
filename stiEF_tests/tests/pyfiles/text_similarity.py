import difflib
import os
import re

import numpy as np
from rapidfuzz.string_metric import levenshtein


class TextSimilarly:
    __slots__ = ("base_text", "text", "__score",
                 "__distance", "__text_equalized", "__base_text_equalized")

    def __init__(self, text: str, base_text: str) -> None:
        self.text = text
        self.base_text = base_text

        self.__score: float = 0
        self.__distance: int = None
        self.__text_equalized: list[str] = None
        self.__base_text_equalized: list[str] = None
        self.damerau_levenshtein()

    def damerau_levenshtein(self) -> tuple[int, float]:
        """
        Compute the Damerau-Levenshtein distance between two strings.
        This distance is the number of additions, deletions, substitutions,
        and transpositions needed to transform the first string into the
        second string.
        """
        if not (self.__distance and self.__score):
            self.__distance = levenshtein(self.text, self.base_text)
            self.__score = 1 - self.__distance / \
                max(len(self.text), len(self.base_text))

        return (self.__distance, self.__score)

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
            output = f"{s1}\n{s2}"
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

        with open(output_path, 'w', encoding="utf-8") as f:
            f.write(output)
