from utils.TuEdaCommon import *


def replace_sub_arguments(match):
    #sub_arguments = match.group(1)
    #sub_arguments = re.sub(r'\((\d+),(\d+)\)', r'(\1:\2)', sub_arguments)
    #return sub_arguments
    x, y = match.group(1).split(',')
    mod_x = x.replace('(', '[')
    return f'({mod_x}:{y}]'

def replace_sub_comma_arguments(match):
    
    return match.group().replace(',', '::') 

#TODO:123

 #   ABS(x) => (x > 0 ? x : -x)


class SliceHandler:
    #index is tuple of length 2 as arg for __getitem__((2, 'B')) 
    def __getitem__(self, index):
        if isinstance(index, tuple) and len(index) == 2:
            idx, char = index
            if idx is None:
                if char == 'B3':
                    resStr = "[31:24]"
                    return resStr 
                elif char == 'B2':
                    resStr = "[23:16]"
                    return resStr
                elif char == 'B1':
                    resStr = "[15:8]"
                    return resStr
                elif char == 'B0':
                    resStr = "[7:0]"
                    return resStr
                elif char == 'CONCAT':
                    #TODO:
                    resStr = '::'
                    pass
            else:
                if char == 'B':
                    return self.get_b_slice(idx)
                if char == 'H':
                    return self.get_h_slice(idx) 
                elif char == 'W':
                        return self.get_w_slice(idx)
                elif char == 'D':
                        return self.get_d_slice(idx) 
                else:
                    raise ValueError("Invalid character")
        else:
            raise TypeError("Invalid index format")
            

    def _get_b_slice(self, idx):
        start = idx * 8 + 7
        end = idx * 8 
        return self.get_bits(start, end)
       
    def _get_h_slice(self, idx):
        start = idx*16 +15
        end = idx *8
        return self.get_bits(start, end)
    
    def _get_w_slice(self, idx):
        start = idx * 32 + 31
        end = idx * 32
        return self.get_bits(start, end)

    def _get_d_slice(self, idx):
        start = idx * 64 + 63
        end = idx * 64
        return self.get_bits(start, end)
     
    def _get_bits(self, start, end):
        resStr = "[" + str(int(start)) + ":" + str(int(end)) + " ]"
        return resStr

#def TuEdaBehavOnUnrolledSeBehav( mod_currBehavLst_unrolled_rv32, mod_currBehavLst_unrolled_rv64 ):
    #pass

def TuEdaBehavOnNonUnrolledSeBehav( mod_currBehavLst_unrolled_rv32, mod_currBehavLst_unrolled_rv64, mod_currBehavLst ):
    
    TuEdaBehavOnNonUnrolledSeBehavlvl1( mod_currBehavLst_unrolled_rv32 )
    TuEdaBehavOnNonUnrolledSeBehavlvl1( mod_currBehavLst_unrolled_rv64 )
    TuEdaBehavOnNonUnrolledSeBehavlvl1( mod_currBehavLst )
    

def TuEdaBehavOnNonUnrolledSeBehavlvl1( mod_currBehavLst_lvl1 ):

    signedExtpattern1 = r"SE(\d+)?\((.*?)\)"
    #signedExtXlenPattern1 = 
    #TODO: make multi-line instructions single line to access in dict as key value, needed ??
    
    #The list from concat function handler
    for currBehav in mod_currBehavLst_lvl1:
        for key, value in currBehav.items():
            
            #Multiple SE() op can be found in a single line of Behav
            matchSeOp = re.findall( signedExtpattern1, value )
            #matchSeOp = re.finditer( signedExtpattern1, value )
            
            #matchSeXlenOp = re.findall(signedExtXlenPattern1, value )
            seBehavFndFlg = False
            
            if matchSeOp:

                #split() doesn't raise err
                contents = value.split('=')
                
                seBehavFndFlg = True
                
                #for multiple SEs in a given line of inst
                se_indices = []

                #iterate over a given line of inst with 1 or more SE Operations
                for seOps in matchSeOp: 
                    
                    #startIdx = seOps.start()
                    #endIdx = seOps.end()                    
                    #se_indices.append( (startIdx, endIdx) )

                    seNum = seOps[0]  # "66"
                    seContentInParenthesis = seOps[1]  # "Rs1.W[0] s* Rs2.W[0]"
                    
                    #TODO: handle multiple SEs in single line
                    
                    currBehav[key] = str(contents[0]) + '= ' + 'signed<'+ str(seNum) +'>' + '('+ str(seContentInParenthesis) + ')'
                    
                    #if more than 1 SEs in a given line of instruction
                    if len(matchSeOp) > 1:
                        for tpl in se_indices:
                            #TODO: need to verify and/or handle multi-line SE() and replacing it in right loc if needed
                            pass
                        
    print("exiting")                
        

"""
    To further handling of behaviours on unrolled loops only

    Parameters:
    mod_currBehavLst_unrolled (list) to store the function return value 
    lstOfBehaviorDict32 (list)  
    lstOfBehaviorDict64 (list)  
    

    Returns:
    mod_currBehavLst_unrolled (list): updated mod_currBehavLst_unrolled
"""
#TODO: same logic for lstOfBehaviorDict64
#TODO: addition of signed and unsiged related as discussed
def TuEdaBehavOnUnrolledLoops( mod_currBehavLst_unrolled_rv32, mod_currBehavLst_unrolled_rv64, lstOfBehaviorDict32, lstOfBehaviorDict64 ):


    #concat handling for unrolled loops RV32
    TuEdaBehavOnUnrolledLoopslvl2( mod_currBehavLst_unrolled_rv32, lstOfBehaviorDict32 )
    
    #concat handling for unrolled loops RV64
    TuEdaBehavOnUnrolledLoopslvl2(mod_currBehavLst_unrolled_rv64, lstOfBehaviorDict64 )



"""
    To further handling of behaviours on unrolled loops only

    Parameters:
    mod_currBehavLst_unrolled (list) to store the function return value 
    lstOfBehaviorDict32 (list)  
    lstOfBehaviorDict64 (list)  
    

    Returns:
    mod_currBehavLst_unrolled (list): updated mod_currBehavLst_unrolled
"""
def TuEdaBehavOnUnrolledLoopslvl2( mod_currBehavLst_unrolled_rv32oder64, lstOfBehaviorDict ):

    Concatpattern1 = r'\bCONCAT\s*\('
    concatPattern = r'\bCONCAT\s*\(\s*(.*?)\s*\)'
    atlstOneConcat = False

    for currBehavLst in lstOfBehaviorDict:
        matchConcatFlg = False

        #checking with first member of the unrolled set i, where i= 1....n
        for dict_ in currBehavLst:

            #For every new member of the unrolled list/set
            mod_res_concat_dict = {}
            
            #to check for concat() in first member out of "unrolled list/set" 
            FirstIter = True
            
            matchConcatFlg = False
            lstOfKeyToRmv = []
            clean_k = []
            clean_v = []
            concatLstFlg = False
            
            if atlstOneConcat or FirstIter:
                FirstIter = False
                for key, value in dict_.items():
                    matchConcat = re.search( Concatpattern1, value ) 
                    if matchConcat:
                        atlstOneConcat = True
                        matchConcatFlg = True
                        dictItemSplit = value.split(';')
                        cleanDictItemSplit = [s.strip() for s in dictItemSplit if s != '' and  s != "" and s != ' ']
                        iter = 0

                        #if more than 1 concat() is available in the given line of code/behaviour
                        for concats in cleanDictItemSplit:
                            matches = re.search( concatPattern, concats )
                            if matches:
                                iter = iter + 1
                                arguments = matches.group(1)
                                
                                commaCnt = concats.count(',')
                                if commaCnt > 1:
                                    res = re.sub(r'\((.*?)\)', replace_sub_arguments, concats)
                                else: res = concats
                                res_concat = re.sub(r',',replace_sub_comma_arguments, res )
                                
                                keyToRem = "CONCAT"

                                # Find the starting index of the keyword
                                start_index = res_concat.find(keyToRem)

                                # Find the ending index of the associated closing parenthesis
                                end_index = res_concat.find(')', start_index)

                                # Remove the keyword and associated parentheses, len('CONCAT(') == 7
                                mod_res_concat = res_concat[:start_index] + res_concat[(start_index+7): end_index] + res_concat[end_index + 1:]

                                k, v = mod_res_concat.split('=')
                                k_mod =  k.replace(" ", "")

                                if  k_mod in clean_k:
                                    k_mod = str(k_mod) + "_" + str(iter)
                        
                                clean_k.append(k_mod)
                        
                                clean_v.append(v)

            #Modified behaviour for ith member in the unrolled list 
            if matchConcatFlg:
                matchConcatFlg = False
                mod_res_concat_dict = dict(zip(clean_k, clean_v))

                mod_currBehav = {}
                for key_, value_ in dict_.items():
                    modified_value = value_
                    for k_, v_ in mod_res_concat_dict.items():
                        if k_ in modified_value:
                            modified_value = modified_value.replace(value_, v_)
                            mod_currBehav[k_] = modified_value             
                        else:
                            mod_currBehav[key_] = modified_value             

                mod_currBehavLst_unrolled_rv32oder64.append(mod_currBehav)  
            
            else: #TODO: handle this properly
                mod_currBehav = {}
                for key, value in dict_.items():
                    mod_currBehav[key] = value
                mod_currBehavLst_unrolled_rv32oder64.append(mod_currBehav)     
    
    print("exiting, unrolled")              




def TuEdaBehavOnNonUnrolledLoops( mod_currBehavLst, lstnonLoopBehaviorDict ):
    
    Concatpattern1 = r'\bCONCAT\s*\('
    concatPattern = r'\bCONCAT\s*\(\s*(.*?)\s*\)'

    #iterate behavior
    for currBehav in lstnonLoopBehaviorDict:
        
        #check for 'CONCAT'
        
        matchConcatFlg = False
        lstOfKeyToRmv = []
        clean_k = []
        clean_v = []
        mod_res_concat_dict = {}
        concatLstFlg = False

        for key, value in currBehav.items():
            matchConcat = re.search(Concatpattern1, value )
            if matchConcat:
                concatLstFlg = True
                matchConcatFlg = True
                dictItemSplit = value.split(';')
                cleanDictItemSplit = [s.strip() for s in dictItemSplit if s != '' and  s != "" and s != ' ']
                
                #iterate multiple CONCATs if any
                iter = 0
                #TODO: cascading of concat needs to be addressed
                for concats in  cleanDictItemSplit:
                    matches = re.search( concatPattern, concats )
                    if matches:
                        iter = iter + 1
                        #for match in matches:
                        arguments = matches.group(1)

                        commaCnt = concats.count(',')
                        if commaCnt > 1:
                            res = re.sub(r'\((.*?)\)', replace_sub_arguments, concats)
                        else: res = concats

                        res_concat = re.sub(r',',replace_sub_comma_arguments, res )
                        #Remove concat keyword and associated braces

                        #### Partial Ref. ChatGPT Begins #####
                        #TODO: key need not be removed always
                        keyToRem = "CONCAT"

                        # Find the starting index of the keyword
                        start_index = res_concat.find(keyToRem)

                        # Find the ending index of the associated closing parenthesis
                        end_index = res_concat.find(')', start_index)

                        # Remove the keyword and associated parentheses, len('CONCAT(') == 7
                        mod_res_concat = res_concat[:start_index] + res_concat[(start_index+7): end_index] + res_concat[end_index + 1:]

                        #print(mod_res_concat)  # Output: "t_L = Rd[4:1]::1'b0"
                        #### Partial Ref. ChatGPT Ends #####

                        k, v = mod_res_concat.split('=')
                        k_mod =  k.replace(" ", "")                    
                        
                        #To make the key unique
                        #TODO: key is modified here to make it unique need to verify if its handled properly
                        if  k_mod in clean_k:
                            k_mod = str(k_mod) + "_" + str(iter)
                        
                        clean_k.append(k_mod)
                        
                        clean_v.append(v)

                        #once concat operation is being perfomed remove the associated key,value from dict
                        #TODO: this doesn't apply for all
                        lstOfKeyToRmv.append(key)
            
            if matchConcatFlg:
                matchConcatFlg = False
                mod_res_concat_dict = dict(zip(clean_k, clean_v))

        for key in lstOfKeyToRmv:
            if key in currBehav:
                currBehav.pop(key)
    

            #update concatenated variable locations
        if concatLstFlg:
            
            concatLstFlg = False
            mod_currBehav = {}

            for key_, value_ in currBehav.items():
                modified_value = value_
                for k_, v_ in mod_res_concat_dict.items():
                    if k_ in modified_value:
                        modified_value = modified_value.replace(k_, v_)
                mod_currBehav[key_] = modified_value

            #Store the results of concat operation for all unrolled instructions    
            #TODO: need to seperate RV32 and RV64 in non-loop behaviours as well
            #TODO: certain concats lines are deleted as expected  but are not used in the behaviour fix this bug 
            mod_currBehavLst.append(mod_currBehav)
        
        #If no concat, store the behaviour as it is 
        else: #TODO: do this else case for unrolled function as well
            mod_currBehav = {}
            for key, value in currBehav.items():
                mod_currBehav[key] = value
            mod_currBehavLst.append(mod_currBehav) 

# Now mod_currBehav contains the modified values
 
    #y = ABS(x)
    #  if x > 0: 
    #      y = x 
    #  else: 
    #      y = -x     
    #absPattern = r'\bABS\s*\('
    #absPattern1 = r'\bABS\s*\(\s*(.*?)\s*\)'
    #for currBehavWoConcat in mod_currBehavLst:
    #    
    #    #iterate thro behaviour at a time to check for ABS()
    #    for key, value in currBehavWoConcat.items():
    #        matchAbs = re.search(absPattern, value )
    #        if matchAbs:
    #            
    #            #if multiple ABS in a line of instruction
    #            dictItemSplit = value.split(';')
    #            cleanDictItemSplit = [s.strip() for s in dictItemSplit if s != '' and  s != "" and s != ' ']
    #            
    #            #iterate multiple ABSs if any
    #            iter = 0
    #            for absolutes in cleanDictItemSplit:
    #                matches = re.search(absPattern1, value)
    #                if matches:
    #                    iter = iter + 1
    #                    
    #                    #for match in matches:
    #                    arguments = matches.group(1)
    #                    pass




    print("Exiting non-unrolled")  

def read_file():
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Construct the relative path to the file
    relative_path = os.path.join(current_dir, '/home/ash-ketchum/Downloads/code_generation-main/input/P-ext-proposal1.txt')
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
    
    #for storing instruction encodings
    lstofDict_ = []
    lstofEncoding = []
    lstofArgsDisass = []

    #for storing unrolled loops 
    lstOfBehaviorDict32 = []
    lstOfBehaviorDict64 = []
    currBehavDict = {}
    lstnonLoopBehaviorDict = []

    #for handling certain non-unrolled cases
    behaviour = SliceHandler()
    #result = behaviour((5, 'B')) OR
    #result = behaviour[5, 'B']


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
                #if instruction_syntax == "MINW Rd, Rs1, Rs2":
                    #pass
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
                inst = part

                TuEdaBehaviourRiscVToCoreDsl( inst, lstOfBehaviorDict32, lstOfBehaviorDict64,\
                                            currBehavDict, behaviour, lstnonLoopBehaviorDict )
                
            #formate
            instruction_format = edaSelInstFrmt(part)
            if (instruction_format == "None"):
                instruction_format_list.append("None")

            else:
                instruction_format_list.append(instruction_format)
                instruction_encoding_list_local = []

                # Encoding Begins #
                #for every iter get a new encoding/encoding lst of dicts
                inst = part
                TuEdaEncodeRiscToCoreDsl(inst, lstofEncoding )
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

    #Store the result of concat() operations for all unrolled loops
    mod_currBehavLst_unrolled_rv32 = []
    mod_currBehavLst_unrolled_rv64 = [] 

    #continue further handling of behaviours on unrolled loops only, RV32 and RV64
    TuEdaBehavOnUnrolledLoops( mod_currBehavLst_unrolled_rv32, mod_currBehavLst_unrolled_rv64, lstOfBehaviorDict32, lstOfBehaviorDict64 )

    #store the result of concat() + 'SE' keywords handling
    #lstofSeBehavDictUnroll = []
    #TuEdaBehavOnUnrolledSeBehav( mod_currBehavLst_unrolled_rv32, mod_currBehavLst_unrolled_rv64 )

    #Store the result of concat() operations for all non-unrolled loops and other non-loop
    mod_currBehavLst = []
    TuEdaBehavOnNonUnrolledLoops( mod_currBehavLst, lstnonLoopBehaviorDict )
     
    TuEdaBehavOnNonUnrolledSeBehav( mod_currBehavLst_unrolled_rv32, mod_currBehavLst_unrolled_rv64, mod_currBehavLst )

    #TODO: continue abs(), ZE(), B[], H[] etc
    print("done1")

    #continue Encoding after all encoding contents are extracted    
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
                #args_disass += "{name(" + cleaned_k.lower() + ")},"
                #pass
            elif all(char in '01' for char in cleaned_k ):
                encoding += str( int(v)+1 ) + '\'b'
                encoding += cleaned_k
        inst_encodeLst.append(encoding)
        lstofArgsDisass.append(args_disass)

    inst_argsDisass = [s[:-1] if s.endswith(',') else s for s in lstofArgsDisass] 
    
    json_file_path1 = "encode.json"
    json_file_path2 = "diassemble.json"
    json_file_path3 = "mod_currBehavLst_unrolled.json"
    json_file_path4 = "mod_currBehavLst.json"

# Write the combined data to the JSON file
    with open(json_file_path1, "w") as json_file:
        json.dump(inst_encodeLst, json_file, indent=4)
    with open(json_file_path2, "w") as json_file:
        json.dump(inst_argsDisass, json_file, indent=4)
    with open(json_file_path3, "w") as json_file:
        json.dump(mod_currBehavLst_unrolled_rv32, json_file, indent=4)
    with open(json_file_path3, "w") as json_file:
        json.dump(mod_currBehavLst_unrolled_rv64, json_file, indent=4)
    with open(json_file_path4, "w") as json_file:
        json.dump(mod_currBehavLst, json_file, indent=4)

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


 
"""
    Used with TuEdaEncodeRiscToCoreDsl()
    Strip contents from the string before ith occurance of '|'
    Using '|' for count and strip reference 

    Parameters:
    myLst   (list): 
    count   (int) :

    Returns:
    myLst (list): updated myLst
    """
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



"""
    Used with TuEdaEncodeRiscToCoreDsl()
    dictionary updation with list of values, initially 'values' being set to None

    Parameters:
    lst      (list) : 
    dict_    (dict) :

    Returns:
    dict_ (dict): updated dict_
    """
def update_dict(lst, dict_):
    for k, v in zip(dict_.keys(), lst):
        if dict_[k] is None:
            dict_[k] = [v.strip()]
        else:
            dict_[k].append(v.strip()) 
    return dict_



def concatMatch():
    pass
def absMatch():
    pass
def seMatch():
    pass
def zeMatch():
    pass
def halfWordMatch():
    pass
def byteMatch():
    pass
def doubleWordMatch():
    pass
def wordMatch():
    pass
def saturateQnMatch():
    pass
def saturateUmMatch():
    pass
def xlenMatch():
    pass


"""
    To convert RSIC-V instruction behaviours into coreDSL format

    Parameters:
    inst                    (str) : 
    lstOfBehaviorDict32     (list): 
    lstOfBehaviorDict64     (list): 
    lstnonLoopBehaviorDict  (list):
    currBehavDict           (dict):
    behaviour               (__main__.SliceHandler):

    Returns:
    results stored back to lstOfBehaviorDict32/64/otherNonLoopCases (list)
    """
def  TuEdaBehaviourRiscVToCoreDsl( inst, lstOfBehaviorDict32, lstOfBehaviorDict64,
                                currBehavDict, behaviour, lstnonLoopBehaviorDict ):
    #extract all the content between Operations and Exceptions
    pattern = r"Operations:(.*?)Exceptions:"
    match = re.search(pattern, inst, re.DOTALL)
    
    # if certain operation exists 
    if match:

        #strip white spaces
        res = match.group(1).strip() 
        content = res.split("\n")

        if '' in content:
            start_index = content.index('') + 1
            end_index = 0

            #reset
            currBehavDict = {}    
            cleanContent = []
            
            for i in range(start_index, len(content)):
                if content[i] == '*': #or content[i] == '  ':
                    end_index = i - 1
                    break
            if end_index > start_index:  
                
                # for loop patterns
                #TODO: Just a note: forPattern1 not needed because of break!
                #forPattern1 = r'\s*for\s*\(\s*i\s*=\s*(\d+)\s*to\s*(\d+)\s*\)'

                forPattern2 = r'\s*for\s*(RV\d+)\s*[,:]*\s*x\s*=\s*(\d+)\s*\.\.\s*(\d+)\s*[,:]*'

                #clean content to be unrolled, RV32, RV64
                cleanContent = content[start_index:end_index]
                count = 0
                
                #for code in cleanContent:
                currBehavDict = {i: code for i, code in enumerate(cleanContent)}
                #lstOfBehaviorDict.append(currBehavDict)
                unrollLstofDict32 = []
                unrollLstofDict64 = []
                rv32_exists = False

                #unrollDict = {}
                #for loop pattern
                #for code in lstOfBehaviorDict[-1]:
                toRmvKey = []
                dummyCount = 0

                #both match1 and match2 pattern occured
                match1and2 = 0
                
                #default value set to zero
                #TODO: remove this 
                match1Flg = 0

                #to check unrolling was performed or not 
                unrolled = False

                #for myDict in currBehavDict:
                for index, (key, value) in enumerate(currBehavDict.items()):
                
                    rv32_exists = False
                    '''
                    match1 = re.search(forPattern1, value )
                    
                    if value == "}" and dummyCount == 0:
                        toRmvKey.append(key)
                        dummyCount = 1
                    #TODO: add remove key for "}"
                    
                    if match1:
                        unrolled = True
                        doNothing = False
                        match1Flg = 1
                        toRmvKey.append(key)
                        start = int(match1.group(1))
                        end = int(match1.group(2))
                        print("Range for 'i':", start, "to", end)
                        # pattern = r'[\[(]\s*i\s*[\])]' [i] & (i)
                        pattern = r'\[\s*i\s*\]' # just [i]
                        patternDoNothing = r'\(\s*i\s*\)'
                        if start > end:
                            tmp = start
                            start = end
                            end = tmp

                        #check if pattern do nothing was found
                        for key, value in currBehavDict.items():
                            matchDoNthng = re.search( patternDoNothing, value )
                            if matchDoNthng:
                                doNothing = True
                       
                        #eg: for i in 31 downto 0
                        for i in range( start, end+1 ):

                            if doNothing == True:
                                doNothing = False
                                #do nothing and break sice patternDoNthng Matched
                                break

                            #idx = count
                            unrollDict = {}
                            for key, value in currBehavDict.items():
                                match = re.search( pattern, value )
                                if match:
                                    #TODO: need to replace () or [] 
                                    replace = "["+ str(i) +"]"
                                    clnCntUnrolld = re.sub( pattern, replace, value )
                                    unrollDict[key] = clnCntUnrolld 
                                    print(clnCntUnrolld)
                                    print("\n")
                                    #idx = idx + 1
                                else:
                                    unrollDict[key] = value
                                    #print(cleanContent[idx+1])
                                    print("\n")
                                    #idx = idx + 1
                            unrollLstofDict.append(unrollDict)
                            print("\n")


                    '''
                        #pass #temp remove it
                    #for loop pattern 2
                    
                    match2 = re.search(forPattern2, value )                    
                    
                    #to seperate RV32 and RV64
                    #rv32_exists = match2.group(1) == 'RV32' if match2 else False

                    #to seperate RV32 and RV64
                    #rv64_exists = forPattern2.group(1) == 'RV64' if forPattern2 else False

                    if match2:
                        rv = match2.group(1)
                        if rv == 'RV32':
                            rv32_exists = True
                            rv64_exists = False

                        #if rv32_exists == True
                        unrolled = True
                        
                        toRmvKey.append(key)
                        rv = match2.group(1)
                        start_value = int(match2.group(2))
                        end_value = int(match2.group(3))
                        
                        #pattern = r'[\[(]\s*x\s*[\])]' [x] and (x)
                        pattern = r'\[\s*x\s*\]' # just [x]
                        
                        if start_value > end_value:
                            tmp = start_value
                            start_value = end_value
                            end_value = tmp

                        if match1Flg == 1:

                            '''
                            #reset match1Flg
                            match1Flg = 0
                            match1and2 = 1

                            modUnrollDictLst = []
                            #patternWhnMtch1 = r'[\[(]\s*x\s*[\])]'
                            patternWhnMtch1 = r'\[\s*x\s*\]'

                            for currUnrolledDict in unrollLstofDict:
                                unrollDict = {} # need to change inplace
                                unrollDictCpy = {}
                                 
                                
                                for i in range(start_value, end_value+1):
                                    k = 0
                                    modUnrollDict = {}
                                    for key, value in currUnrolledDict.items():
                                        match = re.search( patternWhnMtch1, value )
                                        if match:
                                            #TODO: cross check this 
                                            replace = "["+ str(i) +"]"
                                            
                                            #copy available value
                                            unrollDictCpy = currUnrolledDict[key]
                                            
                                            #replace new value
                                            unrollDict = re.sub( pattern, replace, value )
                                            #clnCntUnrolld = re.sub( pattern, replace, value )
                                            #unrollDict[key] = clnCntUnrolld

                                            #update to new value only in modUnrollDict
                                            currUnrolledDict[key] = unrollDict
                                            modUnrollDict[k] = currUnrolledDict[key]

                                            #retain back old value in ith loc in currUnrolledDict
                                            currUnrolledDict[key] = unrollDictCpy


                                            k += 1
                                        else:
                                            #TODO: Need to remove unwanted lines
                                            currUnrolledDict[key] = value
                                            modUnrollDict[k] = currUnrolledDict[key]
                                            k += 1
                                            #unrollDict[key] = value
                                    modUnrollDictLst.append(modUnrollDict)
                                
                                #as re-modifying the previously available unrolledLst
                                #unrollLstofDict.append(unrollDict)
                            '''
                        #if match1 didnt happen 
                        else:
                            
                            for i in range( start_value, (end_value + 1) ):
                                unrollDict = {}
                                for key, value in currBehavDict.items():
                                    match = re.search( pattern, value )
                                    if match:
                                        replace = "["+ str(i) +"]"
                                        clnCntUnrolld = re.sub( pattern, replace, value )
                                        unrollDict[key] = clnCntUnrolld
                                    else:
                                        unrollDict[key] = value
                                if rv32_exists == True:
                                    unrollLstofDict32.append(unrollDict)
                                else:
                                    unrollLstofDict64.append(unrollDict)
                    
                        #Handle non-loop behaviour cases  
                    else:
                        #if no RV32 or RV64 with forloop pattern2 was detected
                        if (index == len(currBehavDict) - 1):
                            lstnonLoopBehaviorDict.append( currBehavDict )
                            break
                        pass
                    #dont
                    '''and match1and2 != 1'''
                
                if (len(unrollLstofDict32) != 0  or match2 or len(unrollLstofDict64) != 0 ) :  
                    if (len(unrollLstofDict64) != 0):
                        lstOfBehaviorDict64.append(unrollLstofDict64)
                    if (len(unrollLstofDict32) != 0):
                      lstOfBehaviorDict32.append(unrollLstofDict32)

                
                #################################      DUMMY    #######################################################
                '''
                if unrolled == False:

                    #eg. parse "t_L = CONCAT(Rd(4,1),1'b0); t_H = CONCAT(Rd(4,1),1'b1);"
                    #This "concatPattern" is just used to split multiple concat in a given line/string
                    #not for exact matching of concat
                    concatPattern = r'CONCAT\s*\((.*?)\)'
                    
                    #TODO: need to handle forLoop1Pattern here
                    #currBehavDict use this
                    for key, value in currBehavDict.items():
                        concatMatches = re.findall( concatPattern, value, re.IGNORECASE )

                        if concatMatches:
                            #split the string at ';' if concat was found in the string
                            split_value_clean = []
                            split_value = value.split(";")
                            for s in split_value:
                                s = s.strip()
                                if s:
                                    split_value_clean.append(s) 
                            if len(split_value_clean) > 0:
                                pass   
                        #concatMatches = re.findall( concatPattern, value, re.IGNORECASE )
                        #if concatMatches:
                            #for concatMatch in concatMatches:
                                #concatArgs = [arg.strip() for arg in concatMatch.split(',')]
                               # pass 
                            #pass
                        #match different patterns and call equivalent functions 
                        #match from lowest one to highest one

                        pass
                    pass
                '''
                ###################################        DUMMY         ##############################################
            else:
                print("Index handling error in the behaviour extraction!!!!!!") 
                          
    
"""
    To convert RSIC-V instruction encodings into coreDSL encoding format

    Parameters:
    inst          (str) : 
    lstofEncoding (list):

    Returns:
    results stored back to lstofEncoding (list)
"""
def TuEdaEncodeRiscToCoreDsl(inst, lstofEncoding ):
     #extract all the content between Format and Syntax,
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
                        
                        #TODO: copy it to seperate list?
                        #splCase.append(lstofEncoding[-1])

                        
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
                    # TODO: SMDS32 check its appending
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


"""
    main function

    Parameters:
    Returns:
"""
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
    #apply_commenting()
    print("Calling create_file")
    #create_file()
    #create_file_table()

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

#EoF