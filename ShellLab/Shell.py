#! /usr/bin/env python3

import os, sys, time, re

def ispath(word):
    return word[0] is '/'

def doPath(args):
    if len(args) > 1:
        if ispath(args[1]):
            os.chdir(args[1])
            os.getcwd()
    if ispath(args[0]):
        program = args[0]
        try:
            os.execve(program, args, os.environ)  # try to exec program
        except FileNotFoundError:  # ...expected
            pass  # ...fail quietly
    else:
        for dir in re.split(":", os.environ['PATH']):  # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly


def userChoice(userIN):
    pid = os.getpid()               # get and remember pid


    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

    #rc = os.fork()

    #if rc < 0:
    #os.write(2, ("fork failed, returning %d\n" % rc).encode())
    #sys.exit(1)

    #elif rc == 0:                   # child
    # os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
    #  (os.getpid(), pid)).encode())
    # args = ["wc", "p3-exec.py"]

    if ispath(userIN[0]):
        doPath(userIN)

    elif '|' in userIN:
        j=0
        for i in userIN:
            if i == "|":
                break
            j=j+1
        LeftPart = userIN[0: j]
        print(LeftPart)
        RightPart = userIN[(j+1):]
        print(RightPart)
        pippingHere(LeftPart, RightPart)


    elif '<' in userIN:
        if len(userIN) == 3:                                #screen cat < text.txt
            args = [userIN[0], userIN[2]]
            if ispath(userIN[2]):
                doPath(args)
            else:
                ScreenExec(args)                               ########try
            #doPath(args)
        else:
            args = [userIN[0],userIN[3]]
            OutUser =  userIN[1]
            fileExec(args,OutUser)

    elif '>' in userIN:
        if len(userIN) == 3:                                #ex ls > output.txt
            args = [userIN[0]]
            OutUser = userIN[2]
            fileExec(args, OutUser)
        args = [userIN[0], userIN[1]]
        OutUser = userIN[3]
        fileExec(args, OutUser)

    else:
        if ispath(userIN[0]):
            doPath(userIN)
        else:
            ScreenExec(userIN)                                     #########try
        #doPath(args)

            # os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        #sys.exit(1)                 # terminate with error

    #else:                           # parent (forked ok)
        #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                     #(pid, rc)).encode())
        #childPidCode = os.wait()
        #os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                   #childPidCode).encode())


def pippingHere(Left, Right):
    rc2 = os.fork()

    if rc2 < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc2 == 0:
        if '<' in Left:
            sys.exit(1)
        elif '>' in Left:
            sys.exit()
        #else:
            #print("Doing work")
        PipeLeft(Left)
           # print("finish work")
    else:
        #print("waiting")
        os.wait()
        PipeRight(Right)
        #print("continue")

def PipeLeft(Left):
    #print("I arrive")
    os.close(1)             #close the screen
    os.dup(w)
    for i in (r,w):
        os.close(i)


    fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
    os.set_inheritable(fd, True)

    os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
        program = "%s/%s" % (dir, Left[0])
        try:
            os.execve(program, Left, os.environ)  # try to exec program
        except FileNotFoundError:  # ...expected
            pass  # ...fail quietly




def PipeRight(Right):
    #print("HALLO!!!!!!!")
    os.close(0)             #close keyboard
    os.dup(r)
    for i in (r,w):
        os.close(i)


    fd = sys.stdin.fileno()  # os.open("p4-output.txt", os.O_CREAT)
    os.set_inheritable(fd, True)
    if '<' in Right:
        sys.exit(1)

    elif '>' in Right:
        os.close(1)
        sys.stdout = open(Right[2], "w")
        fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd, True)


    os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
        program = "%s/%s" % (dir, Right[0])
        try:
            os.execve(program, Right, os.environ)  # try to exec program
        except FileNotFoundError:  # ...expected
            pass  # ...fail quietly


def ScreenExec(args):                                                                      #print in screen (if there is reading the args will have the command and the file(the reading file)
    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)  # try to exec program
        except FileNotFoundError:  # ...expected
            pass  # ...fail quietly

def fileExec(args, OutUser):                                                                #get the command (ex ls, cat) and the file that is using (if there is any (ex cat text.txt)) and where will be output it which is variable OutUser
    os.close(1)  # redirect child's stdout                                                  #the command and the file that is reading are within args.
    #sys.stdout = open("p4-output.txt", "w")
    sys.stdout = open(OutUser, "w")
    fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
    os.set_inheritable(fd, True)
    os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)  # try to exec program
        except FileNotFoundError:  # ...expected
            pass  # ...fail quietly
########################################################################################### main
try:
   sys.ps1 = os.environ.get('PS1')
except AttributeError:
    sys.ps1 = '$ '

if sys.ps1 is None:
    sys.ps1 = '$'

while 1 :
   r, w = os.pipe()
   try:
       userIN = input(sys.ps1).split()
   except EOFError:
       sys.exit(1)
   #userIN = input("").split()
   if 'PS1' in os.environ:
       os.write(1, os.environ['PS1'].encode())

   if 'cd' in userIN:
       if len(userIN) == 1:
           continue
       elif '..' in userIN:
           place = os.getcwd().split('/')
           newplace = '/'.join(place[0:len(place)-2])
           os.chdir(newplace)


   if 'exit' in userIN:
       sys.exit(1)

   pdl = os.fork()
   if pdl < 0:
       os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
   elif pdl == 0:
       if len(userIN)>0:
           userChoice(userIN)

   else:
       for i in (r, w):
           os.close(i)
       os.wait




      # if len(userIN) == 2:
      #     Right = userIN[0]
     #      Left = userIN[1]
     #  else:
    #       newuserIn = userIN.split()
    #       userChoice(newuserIn)