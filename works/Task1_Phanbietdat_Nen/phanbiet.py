import re
from utils import remove_accents


def phanbiet(dict_input: dict) -> int:
    """Phân biệt đất nền (10).

    Arguments:
        inp_str {dict} -- dict chứa 3 thông tin sau:
            id              : id của bài đăng
            content         : content của bài đăng
            realestate_type : loại bất động sản
    Returns:
        int - realestate_type mới của bài đăng
    """

    realestate_type = dict_input['realestate_type']
    # code goes here
    if (realestate_type == 1):
        dict_content = dict_input['content']
        dict_content = remove_accents(dict_content)

        pattern1 = "dat\s+nen\s|dat\s+nen\s+tho\s+cu|dat\s+du\s+an|dat\s+xay\s+dung|khu\s+du\s+an|nen\s+dat|phan\s+lo|dat_nen"
        result1 = re.search(pattern1, dict_content)

        """Test xem có chứa từ khoá của đất thổ cư và nông nghiệp không
            
        pattern2 = "len\s+tho\s+cu|len\s+100%\s+tho\s+cu|dat\s+tho\s+cu|dat\s+tc|dat\s+o\s+tai\s+(do\s+thi|nong\s+thon)|dat\s+trong\s+cay|dat\s+nong\s+nghiep|dat\s+lam\s+nghiep"
        result2 = re.search(pattern2, dict_content)
        if (result1 is not None):
            print("{0} {1}".format(dict_input['id'], result2 is not None))
		"""

        if (result1 is not None):
            realestate_type = 10

############################
# Return
############################
    return realestate_type
