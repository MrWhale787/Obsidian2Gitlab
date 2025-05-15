##directory contents lister 
#finds all files in directories and subdirectories and creates dictionary
#with file name as key and path as directory

import os
import shutil
import re
import argparse

def fileList(dir,lst):
    fileLst = lst.copy()
    items = os.listdir(dir) #create list of all items in directory
    for entry in items: 
        path = os.path.join(dir,entry)
        if os.path.isdir(path): #if entry in directory list is a directory, run recursively
            fileLst.update(fileList(path,fileLst))
        else: #add file to dictionary
            path = path.split("/")        
            path.pop(0)
            path = "/".join(path)
            entry = entry.lower()
            if entry.replace(".md","") in list(fileLst.keys()):
                #print(entry)
                entry = path.replace(".md","")
                fileLst.update({entry.replace(".md","") : path})
            else:
                fileLst.update({entry.replace(".md","") : path})
    return fileLst



def findAndReplace(filelst,dir):
    k=0
    for i in filelst:
        k+=1
        #print(f'now processing file {k}')
        if ".md" in filelst[i]:
            file = open(f'{dir}/{filelst[i]}',"r")
            content = file.read()
            links = re.findall(r"\[\[.*?\]\]",content)
            notes  = re.findall(r"\[\!.*?\]",content)
            for note in notes:
                content = content.replace(note,"")
            
            #iterate over all links in file
            for link in links:
                if ".png" in link: #skip images
                    continue
                string = link.replace("[","")  
                string = string.replace("||","|") #handling an obscure case of double pipe (this shouldnt exist)
                string = string.replace("]","")
                if "|" in string: # handing for normal cases [[ file | alias ]]
                    
                    string = string.split("|")
                    alias = string[1]
                else: #handing for cases which do not match pattern [[file | alias ]] 

                    string = [string]
                    alias = string[0]
                if "#" in string[0]: #handling for cases that reference specific part of file
                    part = string[0].split("#")
                    part.pop(1)
                    string[0] = part[0]
                    alias = string[0]
                try:    #try except for files that tyler forgot to give me smh
                    fileName = str(string[0])
                    fileName = fileName.lower()
                    path = filelst[fileName]
                except Exception as e:
                    #print(f'an error occured file\n {e} \n not found')
                    content = content.replace(link,fileName) 
                    continue
                
                newString = f'[{alias}](/{path})'
                
                
                content = content.replace(link,newString) 
            file.close()
            file = open(f'{dir}/{filelst[i]}',"w")
            file.write(content)
            file.close()
    
def copyDir(src,dst):
    shutil.copytree(src,dst)
    return "success"


def main():
    if args.mode == "c":
        dir = args.file
        if type(args.destination) == type(dir):
            dst = args.destination
        else:
            dst = "newNote"
        if os.path.isdir(dir):
            try:
                print(copyDir(dir,dst))    
            except:
                print(f'file {dst} already exists')      
        else:
            print("invalid directory")
    elif args.mode == "cw":
        dir = args.file
        if type(args.destination) == type(dir):
            dst = args.destination
        else:
            dst = "newNote"
        if os.path.isdir(dir):
            try:
                print(copyDir(dir,dst))
                files = fileList(dst,{})
                findAndReplace(files,dst)
                print("done")
            except Exception as e:
                print(f'an error occurred \n{e}')
        else:
            print("invalid directory")
    elif args.mode =="wo":
        try:
            dir = args.file
            files = fileList(dir,{})
            findAndReplace(files,dir)
            print("success")
        except Exception as e:
                print(f'an error occurred \n{e}')
    else:
        print("invalid option")
            
    
#run the thing
parser = argparse.ArgumentParser(
                    prog='obsidian2gitlab',
                    description='the things tyler wants it to (with some small limitations)',
                    epilog='by running this program you sell your soul to the GOATs')
parser.add_argument('-f','--file', help='the source file')
parser.add_argument('-d','--destination', help='the destination file name, default newNote')
parser.add_argument('-m','--mode',help='running mode c:copy only, cw:copy and write, wo: write only. (c,cw,wo)')
args = parser.parse_args()


main()
