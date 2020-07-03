import json
import re
import numpy as np
from utils import remove_accents

def xacdinh(dict_input: dict) -> float:
    """Phân biệt cái gì đó ahihi, mọi người sửa lại dòng này cho đúng nhé.

    Arguments:
        inp_str {dict} -- dict chứa 3 thông tin sau:
            id              : id của bài đăng
            content         : content của bài đăng
            realestate_type : loại bất động sản
            floor           : số tầng
    Returns:
        float - gía trị của biến area_cal

    Như trong doc thì có 3 loại diện tích:
    """

    area_cal = 0
    ## code goes here
    arealist = []
    #pattern for keywords:
    pattern1 = re.compile(r"\b(dien tich cong nhan|dt cong nhan|cong nhan|dtcn|cn|so do|dien tich so)\s*:?")
    pattern2 = re.compile(r"\b(dien tich|dien tich dat|dt|dt dat|dtd)(?!(\s*(san|xd|xay dung)))")
    pattern3 = re.compile(r"\b(dien tich xay dung|dtxd|dien tich san)\s*:?")
    patternList = [pattern1, pattern2, pattern3]
    # pattern for area:
    re0 = re.compile(r'\d*[.,]?\d+')
    re1 = re.compile(r'(\d*[.,]?\d+\s*\(?m\s*2\(?|\d*[.,]?\d+\s*m\s*vuong\b)')
    re2 = re.compile(r"\d*[.,]?\d+\s*m?\s*[xX*]\s*\d*[.,]?\d+\s*[m,.[({]+")
    re3 = re.compile(r"(ngang\s*[:\d.,m ]*dai[:\d., ]*|dai\s*[:\d.,m ]*ngang[:\d., ]*|[\d., ]*m\s*ngang\s*[:\d.,m ]*dai|[\d., ]*m\s*dai\s*[:\w., ]*ngang)")
    re4 = re.compile(r"(\d*[.,]?\d+\s*(?=ha)|\d*[.,]?\d+\s*(?=hec-?\s*ta))")
    relist = [re1, re2, re3, re4]
    #pattern for searching end point:
    end = re.compile(r'(\n|\s\s\s\s+|\.\s*[a-z])')
    #preprocess the string:
    content = remove_accents(dict_input['content'])
    content = re.sub('[x*]?\s*\d*[.,]?\d+\s?tang','',content)
    content = re.sub('so\s*\d+','',content)
    #some special regex:
        # sr1 for case: dientich: .....m2 san
    sr1 = re.compile(r"m2?\s*(san|xay dung|xd)")
        #sr2 for case: d x d m2
    sr2 = re.compile(r'\d*[.,]?\d+\s*m?\s*[xX*]\s*\d*[.,]?\d+\s*m\s*2')
    if sr2.search(content):
        index = sr2.search(content).end()
        content1 = content[:(index-1)]
        content = content1 + content[(index+1):]
    sr3 = re.compile(r"\d*[.,]?\d+\s*-\s*\d*[.,]?\d+\s*m2")
    flag = 0
    san = 0
    #Start searching!
    #i = 1->3 is for case DTCN, DT and DT san, i =4 when none of the keywords matches:
    for i in range (0, 4):
        if i < 3:
            f = [m.end(0) for m in re.finditer(patternList[i],content)]
        else:
            f = [0]
        for k in f:
            if end.search(content,k):
                e = end.search(content,k).start()
            else:
                e = k + 30
            for r in relist:
                flag = 0
                if i==1 and sr1.search(content,k,e):
                    san = 1
                if i ==3 :
                    match = r.findall(content)
                else:
                    match = r.findall(content,k,e)
                if sr3.search(content,k,e):
                    s3 = content[k:e]
                    s3 = re.sub("m2","",s3)
                    match = re0.findall(s3,k,e)
                if match:
                    flag = 1
                for l in match:
                    area_cal = 1
                    l = re.sub(',','.',l)
                    l = re.sub('m\s*2','',l)
                    numlist = re0.findall(l)
                    for p in numlist:
                        area_cal*=float(p)
                    #cases 'dien tich san' found and special cases:
                    if i ==2 or san==1:
                        fl = dict_input['floor']
                        area_cal/=fl
                        san = 0
                    #cases the unit is hec-ta or ha:
                    if relist.index(r) == 3:
                        area_cal*=10000
                    #for cases when . is used to divide the large number
                    if area_cal < 10 and area_cal*1000 == int(area_cal*1000):
                        area_cal*=1000
                    if i==0 and area_cal > 1:
                        return float(area_cal)
                    #append the area calculated to the list
                    arealist.append(area_cal)
                #if one area type found, skip the loop and search for the next keyword
                if flag==1:
                    break

        #if the area(s) corresponding to one type of keyword has been found, return the value
        if f and arealist:
            #we discard the outliner
            if len(arealist) > 2:
                sorted(arealist)
                Q1, Q3 = np.percentile(arealist, [25, 75])
                iqr = Q3 - Q1
                lower_bound = Q1 - 1.5 * iqr
                upper_bound = Q3 + 1.5 * iqr
                arealist[:] = [x for x in arealist if (upper_bound >= x >= lower_bound)]
            return float(min(arealist))

    #When nothing is found, return -1
    print("UNDETERMINE!")
    return -1

    ############################
    ## Return
    ############################
    return area_cal

