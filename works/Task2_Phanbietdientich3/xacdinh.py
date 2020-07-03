# -*- coding: UTF-8 -*-
import re
import numpy
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
    removed_accent_str = remove_accents(dict_input["content"])
    copy_removed_accent_str = removed_accent_str
    copy_removed_accent_str = re.sub(r"\d*\s?tang","",removed_accent_str)
    removed_accent_str = re.sub("m2","",removed_accent_str)
    removed_accent_str = re.sub(r"(\d*\s?tang)","",removed_accent_str)
    
    # #print(removed_accent_str)

    #Patterns
    dtcn_patterns = re.compile(r'\b(dtcn|dien tich cong nhan|dt cong nhan|cong nhan|cn|dien tich so|so do|cong nhan)\:?', re.IGNORECASE)
    dt_patterns = re.compile(r'\b(dien tich|dt|dien tich dat|dt dat)\s?\:?')
    dt_patterns_2 = re.compile(r'\d+[.,]?\d*\s?(m2|m)?\s?[xX*]\s?\d+[.,]?\d*', re.IGNORECASE)
    dtxd_patterns = re.compile(r'\b(dien tich xay dung|dien tich san|dt san|dt xay dung|dtxd|dtsd)\:?', re.IGNORECASE)
    dtxd_patterns_2 = re.compile(r'\d+[.,]?\d*\s?(m2|m)?\s?[xX*]\s?\d+[.,]?\d*', re.IGNORECASE)
    hectare_patterns = re.compile(r'ha', re.IGNORECASE)
    dt_area_patterns = re.compile(r'\s?\d+[.,]?\d*\s?[^a-z0-9*.()\-,]?')
    m2_patterns = re.compile(r'\d+[.,]?\d*\s?(m2|m)')
    m2_patterns_2 = re.compile(r'\d+[.,]?\d*\s?m2')
    m2_area_patterns = re.compile(r'\d+[.,]?\d*')
    ngang_dai_patterns = re.compile(r'ngang\s?\d+[.,]?\d*[m]?\s?[*x,]?\s?dai\s?\d+[.,]?\d*')
    dtxd_area_patterns = re.compile(r'\d+[.,]?\d*')
    dtcn_area_patterns = re.compile(r'\d+[.,]?\d*')
    # Check for dien tich cong nhan
    if dtcn_patterns.search(removed_accent_str):
        #print('dtcn!!!')
        dtcn_index = dtcn_patterns.search(removed_accent_str).span()

        # #print(str(removed_accent_str[dtcn_index[0]:]) + " ")
        
        dtcn_string = removed_accent_str[dtcn_index[0] : dtcn_index[1] + 20]

        # #print(dtcn_area_patterns.search(dtcn_string))
        if (dtcn_area_patterns.search(dtcn_string)):
            dtcn_area_index = dtcn_area_patterns.search(dtcn_string).span()

            dtcn_area = dtcn_string[dtcn_area_index[0] : dtcn_area_index[1]]
            dtcn_area = re.sub(',', '.', dtcn_area)
            area_cal = float(dtcn_area)
        
        if dt_patterns_2.search(dtcn_string):
            dt_area_index = dt_patterns_2.search(dtcn_string).span()
            dims = dt_area_patterns.findall(dtcn_string[dt_area_index[0]:dt_area_index[1]+3])
            #print(dtcn_string[dt_area_index[0]:dt_area_index[1]+3])
            # #print(dims)
            area = 1
            for dim in dims:
                dim = re.sub(',', '.', dim)
                #print(dim)
                area *= float(dim)
                
            area_cal = area
            
        #print(area_cal)

    # Check for dien tich/ dien tich dat/ dien tich xay dung
    if area_cal == 0 and dt_patterns.search(removed_accent_str):
        #print('dt/ dt dat!!!!\n')
        # #print(dt_patterns.search(removed_accent_str))
        dt_index = dt_patterns.search(removed_accent_str).span()
        
        dt_string = removed_accent_str[dt_index[0]:]
        # #print(dt_string)

        #############OLD METHOD
        # if dt_area_patterns.search(dt_string):
            # dt_area_index = dt_area_patterns.search(dt_string).span()

            # dt_area = dt_string[dt_area_index[0] : dt_area_index[1]]
            
            # #print(dt_area)
            # #print("*")
            # dt_area = re.sub(',', '.', dt_area)

            # # #print(dt_area)
            # area_cal = float(dt_area)
            
            # if hectare_patterns.search(dt_string[dt_area_index[0] : dt_area_index[1]+3]):
            #     area_cal *= 100
               
        ##############ARRAY METHOD
        
    
        if m2_patterns_2.search(copy_removed_accent_str):
            area = 1
            #print(copy_removed_accent_str)
            areas = m2_patterns_2.finditer(copy_removed_accent_str)
            area_array = []
            i = 0
            for area in areas:
                index = area.span()
                area_array.append(copy_removed_accent_str[index[0]: index[1]]) 
                area_array[i] = re.sub('m2','',area_array[i])
                area_array[i] = re.sub('m','',area_array[i])
                area_array[i] = re.sub(',','.',area_array[i])
                area_array[i] = float(area_array[i])
                #print(area_array[i])                    
                i += 1
            
            #print("******")
            area_cal = min(area_array)
            #print(area_cal)    
            #print('*******')
            
        
        if dt_patterns_2.search(dt_string):
            dt_area_index = dt_patterns_2.search(dt_string).span()
            dims = dt_area_patterns.findall(dt_string[dt_area_index[0]:dt_area_index[1]+3])
            #print(dt_string[dt_area_index[0]:dt_area_index[1]+3])
            # #print(dims)
            area = 1
            for dim in dims:
                dim = re.sub(',', '.', dim)
                #print(dim)
                area *= float(dim)
                
            area_cal = area
            #print(area_cal)
        if area_cal == 0:
            ##Check for dien tich xay dung
            if dtxd_patterns.search(removed_accent_str):
                #print('dt xay dung!!!')
                dtxd_index = dtxd_patterns.search(removed_accent_str).span()
                dtxd_string = removed_accent_str[dtxd_index[0]:]
                #print(dtxd_string)
                
                dtxd_area_index = dtxd_patterns_2.search(dtxd_string).span()
                dims = dtxd_area_patterns.findall(dtxd_string[dtxd_area_index[0]:dtxd_area_index[1]])
                #print(dtxd_string[dtxd_area_index[0]:dtxd_area_index[1]])
                #print(dims)
                area = 1
                for dim in dims:
                    dim = re.sub(',', '.', dim)
                    #print(dim)
                    area *= float(dim)
                #print(area_cal)
            
    ##Last resort
    if (area_cal == 0):
        #print('Last resort!')
        #print(copy_removed_accent_str)
        if m2_patterns.search(copy_removed_accent_str):
            m2_index = m2_patterns.search(copy_removed_accent_str).span()
            m2_string = copy_removed_accent_str[m2_index[0] : m2_index[1]]
            #print(m2_string)
            #print('*')
            # #print(copy_removed_accent_str)
            
            m2_area_patterns_index = m2_area_patterns.search(m2_string).span()
            m2_area = m2_string[m2_area_patterns_index[0]:m2_area_patterns_index[1]]
            m2_area = re.sub(',', '.', m2_area)
            area_cal = float(m2_area)
            #print(area_cal)
        
        if dt_patterns_2.search(removed_accent_str):
            dt_area_index = dt_patterns_2.search(removed_accent_str).span()
            dims = dt_area_patterns.findall(removed_accent_str[dt_area_index[0]:dt_area_index[1]+3])
            #print(removed_accent_str[dt_area_index[0]:dt_area_index[1]+3])
            # #print(dims)
            area = 1
            for dim in dims:
                dim = re.sub(',', '.', dim)
                #print(dim)
                area *= float(dim)
                
            area_cal = area
            
        elif ngang_dai_patterns.search(removed_accent_str):
            #print('Ngang dai')
            dt_area_index = ngang_dai_patterns.search(removed_accent_str).span()
            dims = dt_area_patterns.findall(removed_accent_str[dt_area_index[0]:dt_area_index[1]+3])
            #print(removed_accent_str[dt_area_index[0]:dt_area_index[1]+3])
            # #print(dims)
            area = 1
            for dim in dims:
                dim = re.sub(',', '.', dim)
                #print(dim)
                area *= float(dim)
                
            area_cal = area
            
        #print(area_cal)
    ############################
    ## Return
    ############################
    return area_cal

