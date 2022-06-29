import os
import sys


class NoTestTypeError(Exception):
    pass


_test_names = {
    "test_docx_text": ("test_docx.py", "test_docx_text"),
    "test_docx_format": ("test_docx.py", "test_docx_format"),
    "test_jpg": ("test_images.py", "test_jpg"),
    "test_png": ("test_images.py", "test_png"),
    "test_pdf_text": ("test_pdf.py", "test_pdf_text"),
    "test_pdf_format": ("test_pdf.py", "test_pdf_format"),
    "test_pptx_text": ("test_pptx.py", "test_pptx_text"),
    "test_xlsx_text": ("test_xlsx.py", "test_xlsx_text"),
    "test_xlsx_format": ("test_xlsx.py", "test_xlsx_format"),
}


if __name__ == "__main__":
    import pytest
    test_name = None
    args = []
    for i, arg in enumerate(sys.argv):
        if arg == "--test":
            test_name = sys.argv[i + 1]
        elif not arg == test_name:
            args.append(arg)
    
    HERE = os.path.dirname(__file__)
    if not test_name:
        run_from = HERE
    else:
        test_file, test = _test_names[test_name]
        run_from = os.path.join(HERE, 'tests', test_file) + "::" + test
    errcode = pytest.main([run_from] + args[1:])
    sys.exit(errcode)