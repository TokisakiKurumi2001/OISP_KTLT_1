from utils import remove_accents
import re

def phanbiet(dict_input: dict) -> int:

    """Phân biệt các post cho thuê phòng trọ hoặc phòng trong căn hộ cho thuê.
    BĐS có mục đích cho thuê hoặc sang nhượng.
    """

    realestate_type = dict_input['realestate_type']
    content = dict_input['content']

    if (realestate_type == 8):
        new_content = remove_accents(content)
       
       # Nếu chứa các từ "day nha/phong tro" hoặc "dang cho thue" thì trả về -1
        regex_not_type8 = "day (nha |phong )?tro|dang cho thue"
        not_type8= re.search(regex_not_type8, new_content)

        # Keywords of type 8: phong tro, phong cho thue, phong trong can ho cho thue, cho thue phong

        regex_type8 = "phong tro|phong (trong can ho )?(cho thue)|cho thue phong"
        result_type8 = re.search(regex_type8, new_content)

    if (not_type8 is not None):
        realestate_type = -1
    elif (result_type8 is not None):
        realestate_type = 8

    return realestate_type

