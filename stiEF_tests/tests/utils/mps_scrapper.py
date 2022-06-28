from PIL import ImageGrab
import pytesseract
import pyautogui
import os
from re import match
import time

from pytesseract import Output
from pywinauto.application import Application
pytesseract.pytesseract.tesseract_cmd = (r"C:\Costum\Tesseract\tesseract.exe")


def get_screen_boxes() -> dict:
    r = window.rectangle()
    screen = ImageGrab.grab(bbox=(0, 0, r.right/4, r.bottom))
    data = pytesseract.image_to_data(screen, output_type=Output.DICT)

    transformed_data = {}
    n_boxes = len(data['level'])

    for i in range(n_boxes):
        if data["text"][i] != "":
            transformed_data.setdefault(
                data["text"][i], (data['left'][i], data['top'][i], data['width'][i], data['height'][i]))

    return transformed_data


def export_model(model):
    filtered_value = list(filter(lambda v: match(
        f'^{model}', v), transformed_data.keys()))[0]
    coords = transformed_data[filtered_value]
    model_click = (coords[0]+10, coords[1]+10)
    pyautogui.click(model_click, clicks=2)
    icon_path = r"C:\Costum\mps_qa_automantion\qa_automation\pyfiles\scenarioIcon.PNG"
    top_x = coords[0]-50
    top_y = coords[1]
    region = (top_x, top_y, top_x+300, top_y+300)
    print(region)
    for pos in pyautogui.locateAllOnScreen(icon_path, confidence=0.9):
        pyautogui.click(pos, clicks=2)
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'alt', 'e')
        close_btn_path = r"C:\Costum\mps_qa_automantion\qa_automation\pyfiles\closeModel.PNG"
        time.sleep(5)
        pyautogui.click(x=507, y=983)
        close_btn = pyautogui.locateCenterOnScreen(
            close_btn_path, region=(340, 73, 1187, 103))

        pyautogui.click(close_btn)
        print(pos)

    pyautogui.click(model_click, clicks=2)
    return model_click


app = Application().connect(title_re="audi-dsl-qa.*")
window = app.window(title_re="audi-dsl-qa.*")
window.set_focus()


transformed_data = get_screen_boxes()
# screen.show()
coords = transformed_data["stiEF_3"]
pyautogui.click(x=coords[0]+10, y=coords[1]+10)

files = os.listdir(
    r"C:\Users\user\MPSProjects\audi-dsl-qa\solutions\Defects_and_Feature_Requests\models")
stief_3_models = [f.replace("stiEF_3.", "") for f in files if "stiEF_3." in f]
stief_3_models_trimmed = [f[:f.find("_", 8)] for f in stief_3_models]

for model in stief_3_models_trimmed:
    try:
        last_click_pos = export_model(model)
    except:
        pyautogui.click(last_click_pos)
        for i in range(10):
            pyautogui.keyDown("down")
        export_model(model)
