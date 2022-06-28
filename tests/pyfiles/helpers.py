from image_similarity import StructuralSimilarity
from text_similarity import TextSimilarly


def main():
    first = r"C:\Users\user\Downloads\qa_automation 2\qa_automation\pyfiles\testimage1.jpg"
    second = r"C:\Users\user\Downloads\qa_automation 2\qa_automation\pyfiles\testimage2.jpg"

    ic = StructuralSimilarity(first, second)

    print("image similarity: ", ic.score)

    ic.show_images(image=True, base_image=True,
                   diff=True, mask=False, output=True)
    ic.save_images()

    first = "It is not warm. It is winter. It is bad weather. Absolutely no time for a BBQ"
    second = "It is warm. It is summer. It is exceptional weather. So it is time for a BBQ"
    ct = TextSimilarly(first, second)

    print("distance and score: ", ct.damerau_levenshtein())

    print(ct.get_printable_comparation(
        sidebyside=True, compact=False, width=70))
    ct.write_comparation("output.txt")


if __name__ == '__main__':
    main()
