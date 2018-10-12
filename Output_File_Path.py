print("Which file do u want to run..??\nSource or Target")
ch=int(input('Enter\n1.SOURCE \n or\n2.TARGET\n'))

if ch == 1:
    p="C:\Python3.7\Oracle_Schema_Validation\SRC_Validation_File.txt"
elif ch == 2:
    p="C:\Python3.7\Oracle_Schema_Validation\TGT_Validation_File.txt"
else:
    exit
