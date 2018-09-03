import pickle
import re

#fileDec = open(r"hello.txt","r")
fileDec = open(r"declaration.txt","r")                  #open file
LowerDoc = fileDec.read().lower()
loadedlist = re.sub('[^ a-zA-Z0-9]',' ',LowerDoc) #change the special characters for ' '<-this means a space
word = loadedlist.split()                               #split by spaces
fileDec.close()
word.sort()                                            #sort alphabetically order
#for x in range(len(word)):
#    print(word[x])

file = open("declarationKey.txt","w")
#print (word)
#arr = {i:word.count(i) for i in word}
#file.write("%s\n" % arr)


#file.close

i = 0
num = 1                                                 #print the word and the number of times repeated
for i in range(0, len(word)-1):
    if word[i] != word[i+1]:
        word2 = {word[i], num}
        file.write("%s\n"% word2)
        num=1
    else:
        num+=1

word2 = {word[-1],num}
file.write("%s\n"% word2)

file.close()

#file.close()
#word = re.sub(r'\b(\w+)',r'\1',word)
#file = open("declarationKey.txt","w")                  #write in a file called declarationKey
#for x in range(len(word)):
#    file.write("%s\n" % word[x])
#file.close()
