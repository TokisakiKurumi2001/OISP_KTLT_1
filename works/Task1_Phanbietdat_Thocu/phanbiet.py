# Next line will import regex module of python, if already import
# please comment the next line
import re
from utils import remove_accents

def phanbiet(dict_input: dict) -> int:
    """Distinguish "dat tho cu" from other "dat" based on provided keywords

    The keywords we are using are:
    - dat tho cu
    - dat tc
    - dat o tai do thi
    - dat o tai nong thon
    - mat tien
    - dat kiet

    Arguments:
    inp_str {dict} -- dict chứa 3 thông tin sau:
    id              : id của bài đăng
    content         : content của bài đăng
    realestate_type : loại bất động sản
    Returns:
    int - realestate_type mới của bài đăng
    """

    # Firstly, get needed information from input
    realestate_type = dict_input['realestate_type']
    content = dict_input['content']

    if (realestate_type == 1):
        # remove Vietnameses accent from content using built-in function
        # `remove_accents` in utils.py
        new_content = remove_accents(content)

        # find all the post that has such keyword by using regex rules
        regex_rule = "dat\s+tho\s+cu|dat\s+tc|dat\s+o\s+tai\s+(do\s+thi|nong\s+thon)|mat\s+tien|dat\s+kiet"
        result = re.search(regex_rule, new_content)

        if (result is not None):
            realestate_type = 1
        else:
            # Not dat tho cu
            realestate_type = -1
    else:
        # not the part we have to categorize
        realestate_type = -1


    ############################
    ## Return
    ############################
    return realestate_type