from utils.TuEdaCommon import *

def read_file():
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Construct the relative path to the file
    relative_path = os.path.join(current_dir, '/home/ash-ketchum/Downloads/code_generation-main/input/P-ext-proposal.txt')
    print( relative_path )
    with open( relative_path,'r') as file:
        text = file.read()
    #print(text)
    return text

def devide_text_file(text_file):
    pattern = '(?s)(?<=<<<).*?(?=<<<)'
    devided_text_file = re.findall(pattern, text_file)
    #print(devided_text_file)
    return devided_text_file

def apply_selection(devided_text_file, inst_encodeLst, inst_argsDisass ):
    lstofDict_ = []
    lstofEncoding = []
    lstofArgsDisass = []
    for part in devided_text_file:        
        #name
        instruction_name = select_instruction_names(part)
        if (instruction_name != "None"):
            instruction_name_list.append(instruction_name)
            #syntax    
            instruction_syntax = select_instruction_syntax(part)
            if (instruction_syntax == "None"):
                instruction_syntax_list.append("None")
            else:
                instruction_syntax_list.append(instruction_syntax)
            #number of operants
            number_of_operants.append(instruction_syntax.count(','))
            #description
            instruction_description = select_instruction_description(part)
            if (instruction_description == "None"):
                instruction_description_list.append("None")
            else:
                instruction_description_list.append(instruction_description)
            #operation
            instruction_operation = select_instruction_operation(part)
            if (instruction_operation == "None"):
                instruction_operation_list.append("None")
            else:
                instruction_operation_list.append(instruction_operation)
            #formate
            instruction_format = edaSelInstFrmt(part)
            if (instruction_format == "None"):
                instruction_format_list.append("None")

            else:
                instruction_format_list.append(instruction_format)
                instruction_encoding_list_local = []

                #Encoding
                #for every iter get a new encoding/encoding lst of dicts
                inst = part
                TuEdaEncodeRiscToCoreDsl(inst, lstofEncoding )
                #lstofDict_.append(lstofEncoding)
                #print("To Check if its done")
                #print(lstofEncoding[-1])
                #print("Len is ", len(lstofEncoding))
            
                #print("test")
                # Encoding Ends # 
            '''
            instruction_encoding_list_local = edaSelInstEnc(instruction_format)
            instruction_encoding_first_list.append(instruction_encoding_list_local[0])
            instruction_encoding_second_list.append(instruction_encoding_list_local[1])
            instruction_encoding_third_list.append(instruction_encoding_list_local[2])
            instruction_encoding_fourth_list.append(instruction_encoding_list_local[3])
            instruction_encoding_list_local.clear()
            '''
        else:
            pass

    #continue encoding after all encoding contents are extracted    
    for myDict in lstofEncoding:
        encoding = ""
        args_disass = ""
        for i, (k,v) in enumerate(myDict.items()):
            cleaned_k = k.strip()
            if i >= 1:
                encoding += '::'
                #args_disass += ','
            if '+' in k:
                encoding +=  str( int(v)+1 ) + '\'b'
                encoding += cleaned_k.split("+")[1] 
            elif 'R' in cleaned_k:
                encoding += cleaned_k.lower()
                encoding += "["+ str(int(v)) + ":0]"
                args_disass += "{name(" + cleaned_k.lower() + ")},"
            elif 'imm' in cleaned_k:
                #TODO immediate operand
                encoding += cleaned_k.lower()
                encoding += "["+ str(int(v)) + ":0]"
                
                #ASK: Is this needed for imm as well?
                args_disass += "{name(" + cleaned_k.lower() + ")},"
                #pass
            elif all(char in '01' for char in cleaned_k ):
                encoding += str( int(v)+1 ) + '\'b'
                encoding += cleaned_k
        inst_encodeLst.append(encoding)
        lstofArgsDisass.append(args_disass)

    inst_argsDisass = [s[:-1] if s.endswith(',') else s for s in lstofArgsDisass] 
    
    print("Done1") 
def apply_commenting():
    comment_text(instruction_format_list)
    comment_text(instruction_operation_list)
    comment_text(instruction_description_list)

def comment_text(text_list):
    for i in range (len(text_list)):
        text_list[i] = "//" + text_list[i]
        text_list[i] = text_list[i].replace("\n","\n//")
    return text_list

def select_instruction_syntax(text_file):
        pattern = '(?<=\*Syntax:\*\n\n ).*(?=)'
        instruction_syntax = re.findall(pattern, text_file)

        if (len(instruction_syntax)==0):
            instruction_syntax.append("None")
        else:
            pass
        return instruction_syntax[0]


def select_instruction_names(text_file_part):
    pattern = '(?<=\*Syntax:\*\n\n )(\w+|\()'
    instruction_names = re.findall(pattern, text_file_part)

    if (len(instruction_names)==0):
        instruction_names.append("None")
    else:
        pass
    
    return instruction_names[0]


def select_instruction_description(text_file_part):
    pattern = '(?s)(?<=\*Description:\*)(.*?)(?=\*Operations:\*)'
    text_descriptions = re.findall(pattern, text_file_part)
    if (len(text_descriptions)==0):
        text_descriptions.append("None")
    else:
        pass

    return text_descriptions[0]

def select_instruction_operation(text_file_part):
    pattern = '(?s)(?<=\*Operations:\*).*?(?=\*Exceptions:)'
    text_operations = re.findall(pattern, text_file_part)

    if (len(text_operations)==0):
        text_operations.append("None")
    else:
        pass

    return text_operations[0]

def edaSelInstFrmt(text_file_part):
    pattern = '(?s)(?<=\*Format:\*\n\n).*?(?=\|===\n\n\*Syn)'
    text_format = re.findall(pattern, text_file_part)
    if ( len(text_format) == 0 ):
        text_format.append("None")
    else:
        pass

    return text_format[0]


#TODO: Need to modify this function
def edaSelInstEnc(instruction_format):
    pattern = '(?<= \+\n)(?:)\d+(?= |)|(?<= \|)(?:)\d+(?= |)'
    instruction_encoding_list_local = re.findall(pattern, instruction_format)

    looping_for_badding = len(instruction_encoding_list_local)
    number_of_encodng_var = 4

    while((number_of_encodng_var - looping_for_badding) > 0):
        instruction_encoding_list_local.append('')
        looping_for_badding = looping_for_badding + 1
    return instruction_encoding_list_local

def create_file():
    with open('generated/RVP_try_v1.core_desc', 'w') as file:
        file.write('import "RISCVBase.core_desc"\n')
        file.write('\n')
        file.write('InstructionSet RV32Zpn extends RV32I {\n')
        file.write('    architectural_state {\n')
        file.write('        unsigned<32> VXSAT_ADDR__ = 0x009;\n')
        file.write('        unsigned<32>& VXSAT_CSR__ = CSR[VXSAT_ADDR__];\n')
        file.write('    }\n')
   
        file.write('instructions {\n')
        for i in range (len(instruction_name_list)):
            file.write('//--------------\n')
            file.write('// ||' + instruction_name_list[i] + '||\n')
            file.write('//--------------\n')
            file.write('//Instruction description:-\n')
            file.write(instruction_description_list[i])
            file.write('Instruction operation:-\n')
            file.write(instruction_operation_list[i])
            file.write('Instruction syntax:-   ')
            file.write(instruction_syntax_list[i])
            file.write('\n//Instruction formate:-\n')
            file.write(instruction_format_list[i])
            file.write('\n')
            file.write('    ' + instruction_name_list[i])
            file.write(' {\n')
            

            if(number_of_operants[i]==1):
                file.write('        encoding: 0b' + instruction_encoding_first_list[i]+ ' :: rs1[4:0] :: 0b' + instruction_encoding_second_list[i]+ ' :: rd[4:0] :: 0b' + instruction_encoding_third_list[i]+ ';' + '\n') # TODO generate a encoding #TODO what is a better name for instruction_encoding_first sec third  
                file.write('        args_disass:"{name(rd)}, {name(rs1)}";' + '\n')
                file.write('        behavior: {' + '\n')
                file.write('            if(rd != 0) {' + '\n\n\n')
                #TODO generate a rs1 , 2 , ... based on encoding
            elif(number_of_operants[i]==2):
                file.write('        encoding: 0b' + instruction_encoding_first_list[i]+ ' :: rs2[4:0] :: rs1[4:0] :: 0b' + instruction_encoding_second_list[i]+ ' :: rd[4:0] :: 0b' + instruction_encoding_third_list[i]+ ';' + '\n') # TODO generate a encoding #TODO what is a better name for instruction_encoding_first sec third  
                file.write('        args_disass:"{name(rd)}, {name(rs2)}, {name(rs1)}";' + '\n')
                file.write('        behavior: {' + '\n')
                file.write('            if(rd != 0) {' + '\n\n\n')
                #TODO generate a rs1 , 2 , ... based on encoding
            elif(number_of_operants[i]==3):
                file.write('        encoding: 0b' + instruction_encoding_first_list[i]+ ':: rs3[4:0] :: rs2[4:0] :: rs1[4:0] :: 0b' + instruction_encoding_second_list[i]+ ' :: rd[4:0] :: 0b' + instruction_encoding_third_list[i]+ ';' + '\n') # TODO generate a encoding #TODO what is a better name for instruction_encoding_first sec third  
                file.write('        args_disass:"{name(rd)}, {name(rs3)}, {name(rs2)}, {name(rs1)}";' + '\n')
                file.write('        behavior: {' + '\n')
                file.write('            if(rd != 0) {' + '\n\n\n')
                #TODO generate a rs1 , 2 , ... based on encoding
            else:
                pass

            file.write('')
            file.write('                X[rd] = rd_val;' + '\n')
            file.write('            }' + '\n')
            file.write('        }' + '\n')
            file.write('    }\n')
            file.write('    }\n\n\n\n')


#strip contents from the string before ith occurance of '|'
#using '|' for count and strip reference  
def strip_str_contents( myLst, count ):
    for i, string_ in enumerate(myLst):
        parts = string_.split('|')
        if count <= len(parts):
            index = sum(len(part) + 1 for part in parts[:count])
            stripped_string = string_[index-1:]
            myLst[i] = stripped_string
            #myStripLst[i] = string_[:index-1]
    return myLst


def split_list(lst, count):
    new_lst = []
    split_count = 0
    for item in lst:
        split_items = item.split('|')
        new_lst.extend( split_items[1:count] )
        split_count += split_items.count('|')
        if split_count >= count:
            break
    return new_lst


#dict updation with list of values, initially 'values' being set to None
def update_dict(lst, dict_):
    for k, v in zip(dict_.keys(), lst):
        if dict_[k] is None:
            dict_[k] = [v.strip()]
        else:
            dict_[k].append(v.strip()) 
    return dict_

def TuEdaEncodeRiscToCoreDsl(inst, lstofEncoding ):
     #extract all the content between Format and Syntax
        pattern = r"Format:(.*?)Syntax:"

        match = re.search(pattern, inst, re.DOTALL)
        if match:

            #strip white spaces
            res = match.group(1).strip() 
            
            colptrn = 'cols="'

            #find the number of occurance of "cols=" pattern
            colCnt = len(re.findall(colptrn, res))
            
            #split the content at "cols=" pattern
            content = res.split("cols=")

            #for each cols get number of cols info
            #numColsPtrn = r'\[cols="(\d+)\*\^\.\^"\]'
            #numColMatches = re.findall( numColsPtrn, content)
            #if numColMatches:
                #numOfCols = [int(numColMatches)]

            #extract only the useful content with "|===" pattern into contentToParse lst
            contentToParse = list(filter(lambda x: '|===' in x, content))

            #extract number of cols info for each col
            numColInfo = []
            for string_ in contentToParse:
                use = re.search(r'\d+', string_)
                if use:
                    numCol = int(use.group())
                    numColInfo.append(numCol)

            #iterate thro all the useful content in contentToParse
            
            #for match in re.finditer(numColsPtrn, res):
             #   startIdx = match.start()
             #   endIdx = match.end()
                
            #numColMatch = re.findall( numColsPtrn, res )
            #if numColMatch:
                #numCols = int(numColMatch.group(1))
    
            #cleaning of the content
            singlLinRes = list( map( lambda x: x.replace('\n', ''), contentToParse ) )
            idx = 0
            for op in singlLinRes:
                idx += 1
                try:
                    #count for "l|" pattern
                    cntPipe = op.count('l|') 
                    if(0 == cntPipe ): #TODO: Handle this case eg. line 9432
                        print("pattern not found!\n", inst)
                        pattern = r'\|===(.*?)\|==='
                        matches = re.findall(pattern, op, re.DOTALL)
                        
                        #eg: caseCol = ['|*[.underline]#xy#* |*[.underline]#code[4:0]#*|10 |01100|20 |01101|30 |01110|31 |01111|32 |10111'] 
                        caseCol = [match.strip() for match in matches]
                        
                        #PipeCnt = [12, 6]
                        PipeCnt = [member.count('|') for member in caseCol ]

                        for info in caseCol:
                            count = 0
                            result = ''
                            i = 0
                            while count < (numColInfo[idx - 1] +1) and i < len(info):
                                if info[i] == '|':

                                    ''' 
                                    count has the number of unique cols+1 value
                                    eg. for |*[.underline]#xy#* |*[.underline]#zz#* |RV32 |RV64
                                    count is 5 
                                    '''
                                    count += 1
                                result += info[i]
                                i += 1

                        #result = '|*[.underline]#xy#* |*[.underline]#code[4:0]#*|'
                        result_split = result.split('|')
                        result_split = list(filter(None, result_split))

                        #eg. {'*[.underline]#xy#* ': None, '*[.underline]#code[4:0]#*': None}
                        res_dict = {}
                        keys_of_res_dict = []
                        for key in result_split:
                            res_dict[key] = None

                        '''
                        TODO: PACK/PACKU, RV32, 64, PK16, 32
                        what exactly will be the generalised encodoing format
                        encoding:
                            Is it: 

                                   funct7:            funct3:
                            PKBB16 0000--111  rs2 rs1     001 rd 
                            PKBT16 0001--111
                            PKTB16 0011--111
                            PKTT16 0010--111
                        '''
                        while ( caseCol != [''] ): 
                            #use this to strip off extracted values from string
                            caseCol = strip_str_contents( caseCol, count)
                        
                            #values of dict being list of and use it as encoding info for the previous column 
                            #now reuse caseCol to form values of the dict 
                        
                            #eg. resLst = ['BB ', '00 ', '         ', '&#10003;']
                            resLst = split_list( caseCol, count)

                            #update res_dict values with the info in resLst
                            #eg. res_dict = {'*[.underline]#xy#* ': ['BB'], '*[.underline]#zz#* ': ['00'], 'RV32 ': [''], 'RV64': ['&#10003;']}
                            res_dict = update_dict( resLst, res_dict )
                        
                        #print(res_dict)
                        #TODO: Use this result to prev list for encoding purpose
                        

                        #SUNPKD8**[.underline]#xy#** + *code[4:0]*
                        #SUNPKD810

                        #special case handling
                        splCase = []
                        
                        #eg. {'PK**[.underline]#xy#...#zz#* 111 ': '6', 'Rs2 ': '4', 'Rs1 ': '4', '001 ': '2', 'Rd': '4', 'OP-P +1110111': '6'}
                        splCase.append(lstofEncoding[-1])

                        
                        continue
                    
                    #if cntPipe exists
                    cntPipe = op.count('l|')
                    start = op.index('l|')
                    
                    op = op[start:]
                    lstIdx = op.rindex("|")
                    
                    op = op[:lstIdx+1]
                    op = op.replace("l|", "|")
                    
                    # singlLinRes = singlLinRes.split('|')
                    valLst =  op.split('|')[:cntPipe+1]
                    keyLst =  op.split('|')[cntPipe+1:]
                    valLst = list(filter(lambda x: x != '', valLst))
                    keyLst = list(filter(lambda x: x != '', keyLst))
                    valIdxPair = dict(zip(keyLst, valLst)) 
                    
                    valIdxDict = {}
                    for k, v in valIdxPair.items():
                        values = v.strip().split()
                        if len(values) == 2:
                            start, end = map(int, values) 
                            if end > start:
                                newVal = str(end - start)
                            else:
                                newVal = str(start - end)
                        else:
                            #handle this scenario completely
                            start = end = int(values[0])
                        valIdxDict[k] = newVal
                    lstofEncoding.append(valIdxDict)                    
                    
                except Exception as e:
                    #TODO: handle errors or exceptions
                    print(f"Error occured:{e}")
                    print(lstofEncoding[-1])
                    print("Len is ", len(lstofEncoding))
                    if len(lstofEncoding) == 284:
                        pdb.set_trace()
                    
                    
                    continue
                # if len(lstofEncoding) == 283:
                #     print(111)
                    #pdb.set_trace()
            return lstofEncoding

def create_file_table():
    df = pd.DataFrame(list(zip(instruction_name_list, instruction_syntax_list,instruction_description_list, instruction_operation_list)),
               columns =['Name', 'syntax', 'description', 'operations'])
    writer = pd.ExcelWriter('generated/data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False)
    writer.close()

if __name__ == "__main__":

    instruction_name_list = [] 
    instruction_syntax_list = []
    instruction_description_list = []
    instruction_operation_list = []
    instruction_format_list = []

    instruction_encoding_list_length = []
    instruction_encoding_first_list = []
    instruction_encoding_second_list = []
    instruction_encoding_third_list = []
    instruction_encoding_fourth_list = []
    number_of_operants = []

    text_file = read_file()
    text_file_devided = devide_text_file(text_file)
    #lstofEncoding = []
    
    #iterate over all the instructions in the document
    #for inst in text_file_devided:
    #
    inst_encodeLst = []
    inst_argsDisass = []

    apply_selection(text_file_devided, inst_encodeLst, inst_argsDisass)
    apply_commenting()
    print("Calling create_file")
    create_file()
    create_file_table()

#TODO: special case encoding handling pending.
#TODO: assembly name() using regular expr re.sub() , 7b0`000 
#TODO: Printing into a file, imm operation handling
'''
for k, v in lstofEncoding[325].items():
    encoding += "::"
    if '+' in k:
      encoding += '0b'
      encoding += k.split("+")[1]
    #else if 'R' in k:
      #encoding += 
'''
'''
    apply_selection(text_file_devided, inst_encodeLst)
    apply_commenting()

    create_file()
    create_file_table()
    '''