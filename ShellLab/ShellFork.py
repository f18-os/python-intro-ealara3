#! /usr/bin/env python3

import os, sys, time, re

userIN = input("").split()

pid = os.getpid()               # get and remember pid

os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                 #(os.getpid(), pid)).encode())
   # args = ["wc", "p3-exec.py"]
    args =[userIN[0], userIN[1]]

    #os.close(1)                 # redirect child's stdout
    #sys.stdout = open("Name.txt", "w")
    #fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
    #os.set_inheritable(fd, True)

    #os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
    if len(userIN) < 3:                             #if is only (ex) wc file.txt
      for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly

    elif len(userIN) == 3:                          #if is only (ex) wc < file.txt
        if userIN[1] == "<":
            args[1] = userIN[2]
            for dir in re.split(":", os.environ['PATH']):  # try each directory in path
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ)  # try to exec program
                except FileNotFoundError:  # ...expected
                    pass


    elif userIN[2] == ">":                          #if is only (ex) wc file.txt > H.txt
         os.close(1)
         sys.stdout = open(userIN[3], "w")
         fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
         os.set_inheritable(fd, True)
         for dir in re.split(":", os.environ['PATH']):  # try each directory in path
             program = "%s/%s" % (dir, args[0])
             try:
                os.execve(program, args, os.environ)  # try to exec program
             except FileNotFoundError:  # ...expected
                 pass

    elif userIN[2] == "<":                          #if is only (ex) wc H.txt < file.txt
        os.close(1)
        args = [userIN[0], userIN[3]]
        sys.stdout = open(userIN[1], "w")
        fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd, True)
        for dir in re.split(":", os.environ['PATH']):  # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass



    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)
    #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                # (pid, rc)).encode())
    childPidCode = os.wait()
    #os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                # childPidCode).encode())
