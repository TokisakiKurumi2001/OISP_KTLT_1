import re
import json


def remove_accents(input_str):
    S1 = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
    S0 = "AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy"

    """Đổi các ký tự từ Unicode sang dạng không dấu và in thường

    Arguments:
        input_str {str} -- string cần chuyển đổi

    Returns:
        str -- string nếu chuyển đổi thành công
        None - otherwise
    """

    if input_str is None:
        return 'none'

    s = ""
    for c in input_str:
        if c in S1:
            s += S0[S1.index(c)]
        else:
            s += c
    return s.lower()


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

    #realestate_type = dict_input['realestate_type']
    pattern = "dat\s+(nen|du\s+an)|nen\s+dat\s+((?!tho\s+cu).*)|phan\s+lo|dat_nen"
    # code goes here
    for item_read in dict_input:
        realestate_type = item_read['realestate_type']
        if (realestate_type == 1):
            dict_content = item_read['content']
            dict_content = remove_accents(dict_content)
            result = re.search(pattern, dict_content)

            if (result is not None):
                realestate_type = 10
                print(item_read['id'])

        item_read['realestate_type'] = realestate_type

############################
# Return
############################
    # return realestate_type


# For testing purposes
if __name__ == '__main__':
    with open('test.json') as json_file:
        data = json.load(json_file)
        phanbiet(data)
