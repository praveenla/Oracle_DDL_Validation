#-------------------------------------------------------------------------------
# Name          :       Oracle Schema Validation Tool
# Purpose       :       This tool is used to extract data from database and
#                       compares in 2 text files and generates report with
#                       differences in xls file.
# 
# Author        :       M32341
# Created       :       22/08/2018
# Version       :       0.1
#-------------------------------------------------------------------------------

import subprocess
import os
import datetime
import time
import shutil

#importing the path where we want to generate the description of the table
import Output_File_Path 

#Creating the query
first=("""SET DEFINE OFF;
SET ECHO OFF;
SET LINESIZE 32000;
SET PAGESIZE 40000;
SET LONG 50000;
SET TRIMSPOOL ON;
SET TRIMOUT ON;
SET WRAP OFF;
SET NEWPAGE 0;
SET SPACE 0;
SET FEEDBACK OFF;
SET HEADING OFF;
COLUMN OWNER FORMAT A32
COLUMN TABLE_NAME FORMAT A32
COLUMN COLUMN_NAME FORMAT A30
COLUMN DATA_TYPE FORMAT A20
SET DESCRIBE DEPTH 2 LINENUM ON INDENT ON
SPOOL """)
f=(""";
SELECT   ATC.OWNER
       || ATC.TABLE_NAME
       || ATC.COLUMN_NAME
       || '|'
       || ATC.OWNER
       || '|'
       || ATC.TABLE_NAME
       || '|'
       || ATC.COLUMN_NAME
       || '|'
       || ATC.DATA_TYPE
       || '|'
       || ATC.DATA_LENGTH
       || '|'
       || ATC.DATA_PRECISION
       || '|'
       || ATC.NULLABLE
       || '|'
       || ATC.COLUMN_ID
    FROM ALL_TAB_COLUMNS ATC
   WHERE ATC.TABLE_NAME IN(""")

#To read the list of Tables from Input_Table_List.txt file 
with open('Input_Table_List.txt','r') as file_input:
        filedata = file_input.readlines()
        filedata = [file_input.strip() for file_input in filedata]
        #print(type(filedata))
s=''
for ele in filedata:
    s+="'"+ele+"',\n"
second=s.strip(',\n')

#To read the list of Owners from Input_Owner_List.txt file
with open('Input_Owner_List.txt','r') as file_input2:
        content1 = file_input2.readlines()
        content1 = [file_input2.strip() for file_input2 in content1]
        #print(type(content1))
s1=''
for ele in content1:
    s1+="'"+ele+"',\n"
third=s1.strip(',\n')

#To create the intermediate file for SQL query
with open('Intermediate_Query.Sql', 'w') as file_out:
      file_out.write(first+Output_File_Path.p+f+second+r')'+'\n'+r'AND ATC.OWNER IN('+third+""")\nORDER BY ATC.OWNER,ATC.TABLE_NAME, ATC.COLUMN_ID;
SPOOL OFF; """)

#Connecting to SQL PLUS
def run_sqlplus(sqlplus_script):
    p = subprocess.Popen(['sqlplus','/nolog'],stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (stdout,stderr) = p.communicate(sqlplus_script.encode('utf-8'))
    stdout_lines = stdout.decode('utf-8').split("\n")
    return stdout_lines

#Running the SQL Scripts through SQL PLUS
#Connection_String.Sql file contains the connection sting details for required DB.
sqlplus_script=r"""
@Connection_String.Sql
@Intermediate_Query.Sql;
exit
"""

sqlplus_output = run_sqlplus(sqlplus_script)

line = 'REMARKS|OWNER|TABLE_NAME|COLUMN_NAME|DATA_TYPE|DATA_LENGTH|DATA_PRECISION|NULLABLE|COLUMN_ID'
if Output_File_Path.p == 'C:\Python3.7\Oracle_Schema_Validation\SRC_Validation_File.txt':
    with open('SRC_Validation_File.txt', 'r+') as f:
         file_data = f.read()
         f.seek(0, 0)
         f.write(line.rstrip('\r\n') + '\n' + file_data)
         input_file_name = 'SRC_Validation_File.txt'
         rename_input_file_name = 'C:\Python3.7\Oracle_Schema_Validation\Data\SRC_Validation_File_'+time.strftime("%Y-%m-%d-%H-%M")+'.txt'
         shutil.copy(input_file_name, rename_input_file_name)
elif Output_File_Path.p == 'C:\Python3.7\Oracle_Schema_Validation\TGT_Validation_File.txt':
    with open('TGT_Validation_File.txt', 'r+') as f:
         file_data = f.read()
         f.seek(0, 0)
         f.write(line.rstrip('\r\n') + '\n' + file_data)
         input_file_name = 'TGT_Validation_File.txt'
         rename_input_file_name = 'C:\Python3.7\Oracle_Schema_Validation\Data\TGT_Validation_File_'+time.strftime("%Y-%m-%d-%H-%M")+'.txt'
         shutil.copy(input_file_name, rename_input_file_name)
         
         subprocess.call("python Schema_Data_Validation.py")
else:
    exit
