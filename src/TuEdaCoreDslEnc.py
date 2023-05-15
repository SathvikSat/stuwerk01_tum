from utils.TuEdaCommon import *


"""
This is a multi-line comment that explains what the function does.

Parameters:
- arg1: text_file_part

Returns:
- text_format[0]:


def edaSelInstFrmt(text_file_part):
    
    pattern = '(?s)(?<=\*Format:\*\n\n).*?(?=\|===\n\n\*Syn)'
    
    text_format = re.findall(pattern, text_file_part)
    
    if (len(text_format)==0):
        text_format.append("None")
    else:
        pass
    return text_format[0]
"""

"""
This is a multi-line comment that explains what the function does.

Parameters:
- arg1: text_file_part

Returns:
- text_format[0]:

def edaSelInstEnc(instruction_format):
    pattern = '(?<= \+\n)(?:)\d+(?= |)|(?<= \|)(?:)\d+(?= |)'
    instruction_encoding_list_local = re.findall(pattern, instruction_format)

    looping_for_badding = len(instruction_encoding_list_local)
    number_of_encodng_var = 4

    while((number_of_encodng_var - looping_for_badding) > 0):
        instruction_encoding_list_local.append('')
        looping_for_badding = looping_for_badding + 1
    return instruction_encoding_list_local

"""
#END

