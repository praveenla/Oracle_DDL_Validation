#-------------------------------------------------------------------------------
# Name          :       Comparison of 2 text files
# Purpose       :       This module will compare the 2 text files and generete
#                       report with diffences in xls file.
# 
# Author        :       m21737
# Created       :       21/08/2018
#-------------------------------------------------------------------------------


def main():
    pass

if __name__ == '__main__':
    main()
from xlwt import Workbook, easyxf
from xlwt.Utils import rowcol_to_cell



def data_file_Vld1(src_file,tgt_file,mismtch_file,tgt_delimiter,src_delimiter,tgt_skip_header,src_skip_header,tgt_table_nm):
    col_num=0
    row = easyxf('pattern: pattern solid, fore_colour blue')
    col = easyxf('pattern: pattern solid, fore_colour green')
    cell = easyxf('pattern: pattern solid, fore_colour yellow')
    nosrc = easyxf('pattern: pattern solid, fore_colour orange')
    header = easyxf('pattern: pattern solid, fore_colour aqua')
    notgt = easyxf('pattern: pattern solid, fore_colour green')
    tab_nm=tgt_table_nm
    tgt_skip_header=tgt_skip_header
    src_skip_header=src_skip_header

    src_header_cnt=1
    tgt_header_cnt=1
    src_header=''
    tgt_header=''
    tgt_vs_src_mism_cnt=0
    tgt_vs_src_mtch_cnt=0
    tgt_mis_cnt=0
    src_mis_cnt=0
    book = Workbook()
    sheet = book.add_sheet(tab_nm)
    with open(src_file, 'r') as file1:
        with open(tgt_file, 'r') as file2:
            same = set(file1).difference(file2)
    same.discard('\n')
    src_rec={}
    tgt_rec={}

    print("Mismatch Count                  ::",same.__len__())

    if same.__len__() > 0:
        srcfile=open(src_file, 'r')
        src_header=srcfile.readlines()[0:src_header_cnt]
        srcfile=open(src_file, 'r')

        for line in srcfile:
            if src_skip_header=='Y':
                src_skip_header='N'
                src_header=line.split(src_delimiter)

                continue

            value=line
            key=line.split(src_delimiter)[0]

            if key not in src_rec:
                src_rec[key]=value
        tgtfile=open(tgt_file, 'r')
        mismatch_ind='N'
        row_num=2

        for  line in tgtfile:
            if tgt_skip_header=='Y':
                tgt_skip_header='N'
                tgt_header=line.split(tgt_delimiter)

                continue

            tgt_col=line.split(tgt_delimiter)
            tgt_pk=tgt_col[0]
            tgt_rec[tgt_pk]=""
            if tgt_pk in src_rec:
                src_col= src_rec[tgt_pk].split(src_delimiter)
                mismatch_pos=[]
                mismatch_ind="N"
                for i in range(0,len(tgt_col)):
                    if tgt_col[i]!=src_col[i]:
                        mismatch_ind="Y"
                        mismatch_pos.append(i)
                if  mismatch_ind=="Y":
                    tgt_vs_src_mism_cnt+=1
                    col_num=0
                    sheet.row(row_num).set_cell_text(col_num,'SOURCE ROW')
                    sheet.row(row_num+1).set_cell_text(col_num,'TARGET ROW')
                    for j in range(1,len(tgt_col)):
                        col_num+=1
                        if j in mismatch_pos:
                            sheet.row(row_num).set_cell_text(col_num,src_col[j],cell)
                            sheet.row(row_num+1).set_cell_text(col_num,tgt_col[j],cell)
                        else:
                            sheet.row(row_num).set_cell_text(col_num,src_col[j])
                            sheet.row(row_num+1).set_cell_text(col_num,tgt_col[j])
                    row_num+=2
                else:
                    tgt_vs_src_mtch_cnt+=1
            
            else:
         ###rows which are not present in source
                sheet.row(row_num).set_cell_text(0,'TARGET ROW NOT IN SOURCE',nosrc)
                tgt_mis_cnt+=1
                col_num=1
                for j in range(1,len(tgt_col)):
                    sheet.row(row_num).set_cell_text(col_num,src_col[j],nosrc)
                    col_num+=1
                row_num+=1
        src_missing = { k : src_rec[k] for k in set(src_rec) - set(tgt_rec) }

        for key, value in src_missing.items():
            src_mis_cnt+=1
            sheet.row(row_num).set_cell_text(0,'SOURCE ROW NOT IN TARGET',notgt)
            value_list=value.split(src_delimiter)
            for j in range(1,len(value_list)):
                sheet.row(row_num).set_cell_text(j,value_list[j],notgt)
                col_num+=1
            row_num+=1

        sheet.row(0).set_cell_text(0,"TARGET HEADER",header)
        for j in range(1,len(tgt_header)):
            sheet.row(0).set_cell_text(j,tgt_header[j],header)
        sheet.row(1).set_cell_text(0,"SOURCE HEADER",header)
        for j in range(1,len(src_header)):
            sheet.row(1).set_cell_text(j,src_header[j],header)
        if tgt_mis_cnt != 0 or src_mis_cnt != 0 or tgt_vs_src_mism_cnt != 0:
            book.save(mismtch_file)
    return([tgt_vs_src_mism_cnt,tgt_mis_cnt,src_mis_cnt,tgt_vs_src_mtch_cnt])

src_file_nm='C:\\Python3.7\\Oracle_Schema_Validation\\SRC_Validation_File.txt'
tgt_file_nm='C:\\Python3.7\\Oracle_Schema_Validation\\TGT_Validation_File.txt'
mismtch_file= 'C:\\Python3.7\\Oracle_Schema_Validation\\Validation_Report.xls'
tgt_delimiter='|'
src_delimiter="|"
tgt_table_nm='Validation_Report'
tgt_skip_header="Y"
src_skip_header="Y"

data_vld_res=data_file_Vld1(src_file_nm,tgt_file_nm,mismtch_file,tgt_delimiter,src_delimiter,tgt_skip_header,src_skip_header,tgt_table_nm)

print("Source vs Target Mismatch Count :: "+ str(data_vld_res[0]) + "\nRecords in Target not in Source :: "+str(data_vld_res[1]) +"\nRecords in Source not in Target :: "+str(data_vld_res[2])+"\nMatched Record Count            :: "+str(data_vld_res[3]))
