import xml.etree.ElementTree as et
from xml.etree import ElementTree as etree
from pyparsing import *
from pprint import pprint
import pyparsing as pp
from codecs import open
import string
import re
import tkinter as tk
from tkinter import filedialog
import os
import shutil



application_window = tk.Tk()
my_filetypes = [('all files', '.*'), ('text files', '.txt')]
count=-1
sowmith=0
acc_count=0
op_count=-1
cwd=os.getcwd()
# print(cwd)
# exit()
cwd=cwd.replace('\\','/')+'/' + 'output'
if not os.path.exists(cwd):
    os.makedirs(cwd)
cwd=os.getcwd()
cwd=cwd.replace('\\','/')+'/'+'others'
if not os.path.exists(cwd):
    os.makedirs(cwd)
answer=''
from surbi_func import *

# print(cwd)
# exit()

answer = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=my_filetypes)
print(answer)
# filehandler = open("VFS_ALL_BCFACC_O_810_4010.mxl"ll,"r",'utf-8')
dest_list=answer.split("/")
temp=dest_list[len(dest_list)-1]
dest_list[len(dest_list)-1]='others'
dest_list.append(temp)
dst='/'.join(dest_list)
cwd=os.getcwd()
cwd=cwd.replace('\\','/')+'/'+'others'
dst=cwd+"/"+temp
print(dst)
shutil.copy(answer,dst)
print(dst)

filehandler = open(dst,"r",'utf-8')
print(filehandler)
raw_data = et.parse(filehandler)
data_root = raw_data.getroot()
filehandler.close()
fo=open("others/writefile.txt",'w')
op_file=open("others/op_writefile.txt",'w')
input_format=''
output_format=''
inp_format_tag=data_root[3][0].tag
out_format_tag=data_root[4][0].tag

from surbi_remove_notes import *
empty_notes(data_root,etree,raw_data,dst)


# filehandler_ddf = open("VFS_ALL_BCFACC_O_810_4010.ddf","r")
# ddf_file=answer.replace('mxl','ddf')
# filehandler_ddf = open(ddf_file,"r")
# raw_data_ddf = et.parse(filehandler_ddf)
# data_root_ddf = raw_data_ddf.getroot()
# filehandler_ddf.close()


initialize_variable_set(data_root,fo)

if inp_format_tag.split('}')[1]=='EDISyntax':
    print("&&&&&&&&&&&&&&&&&")
    input_format='EDI'
    edi_initialize_dict(data_root,fo)
    # allcases = data_root_ddf.findall(".//EDIELEM")

elif inp_format_tag.split('}')[1]=='PosSyntax':
    input_format='IDOC'
    input_format='IDOC'
    print("DW")
    # exit()
    edi_initialize_dict(data_root,fo)
    # allcases = data_root_ddf.findall(".//POSFIELD")
elif inp_format_tag.split('}')[1]=='XMLSyntax':
    input_format='XML'
    print("**********")
    xml_initialize_dict(data_root,fo)
    # allcases = data_root_ddf.findall(".//XMLPCDATA")

# exit()


all_set=set()
# for item in allcases:
#     it=item.get('NAME')
#     if it in dict_ind_field:
#         name_field=''.join(dict_ind_field[it])
#         # if not (name_field.split('_')[0]=='TEMP'):
#         #     field_set.add(name_field)
#     type=item.get('TYPE')
#     if type=='numeric':
#         type='integer'
#     dict_type[name_field]=type.lower()


nf = open('others/newfile.txt','w')
of = open('others/writefile.txt','r')
remove_comments(nf,of)

jf = open('others/javafile.txt','w')
line_list = [line.rstrip('\n') for line in open('others/newfile.txt')]
block_code=handle_java(line_list,arr_java_inp,0)
jf.write(block_code)
jf.close()

# print("printing arr_java")
# print(arr_java_inp)

with open('others/javafile.txt','r') as f_read:
    data=f_read.read().replace('\n',' ')

result=start.parseString(data)
print("PARSE")
print(result)
make_dictionary(result,dict_token,0)
print("PARSE")
print(result)
fo.close()
# exit()

for k,v in dict_token.items():
    print(k)
    print(v)


if out_format_tag.split('}')[1] == 'EDISyntax':
    print("&&&&&&&&&&&&&&&&&")
    output_format = 'EDI'
    edi_initialize_output_dict(data_root, op_file)
elif out_format_tag.split('}')[1] == 'PosSyntax':
    output_format = 'IDOC'
    edi_initialize_output_dict(data_root, op_file)
elif out_format_tag.split('}')[1] == 'XMLSyntax':
    output_format = 'XML'
    xml_initialize_output_dict(data_root, op_file)



op_nf = open('others/op_newfile.txt','w')
op_of = open('others/op_writefile.txt','r')
remove_comments(op_nf,op_of)

op_jf = open('others/op_javafile.txt','w')
line_list_op = [line.rstrip('\n') for line in open('others/op_newfile.txt')]
block_code_op=handle_java(line_list_op,arr_java_inp,0)
op_jf.write(block_code_op)
op_jf.close()

with open('others/op_javafile.txt','r') as op_f_read:
    op_data=op_f_read.read().replace('\n',' ')


op_result=start.parseString(op_data)
print("OP_PARSE")
print(op_result)
# print(dict_op_field)
make_dictionary(op_result,dict_op_token,1)
op_file.close()

print(dict_op_token)
print("HOLA!")

initialize_const_map(data_root)




if output_format=='EDI':
    print("Is it here")
    edi_make_notes(data_root)
elif output_format=='IDOC':
    edi_make_notes(data_root)
elif output_format=='XML':
    xml_make_notes(data_root)



# for k,v in dict_notes.items():
#     print(k)
#     print(v)
print(link_notes_set)
print(standard_notes_set)
print(extended_notes_set)

if output_format=='EDI':
    edi_populate_notes(data_root,input_format,output_format)
elif output_format=='IDOC':
    edi_populate_notes(data_root,input_format,output_format)
elif output_format=='XML':
    print("did it enter...did it???????")
    xml_populate_notes(data_root,input_format,output_format)


# for k,v in dict_notes.items():
#     print(k)
#     print(v)


write_func(data_root,etree,raw_data,answer)

# print(variable_set)
# print(field_set)
#
#
for k, v in dict_notes.items():
    print(k)
    print(v)


print(link_notes_set)
print(standard_notes_set)
print(extended_notes_set)



# for k,v in dict_token.items():
#     print(k)
#     print(v)

lf = open('others/logfile.txt','w')
make_log(lf)
lf.close()
