#! /usr/bin/env python3

import os, sys, time, re

while 1 :               #run always
    hasPipe = False                         #This two variable will be used to do the second part of the pipe

    userIN = input("").split("|")
    rightPipe = userIN

    if len(userIN) == 2:
        rightPipe = userIN[1].split()
        userIN = userIN[0].split()
        hasPipe = True
    else:
        userIN = userIN[0].split()


    if userIN[0] == 'exit':
        break

    else:                               #start the shell
        r, w = os.pipe()

        pid = os.getpid()               # get and remember pid

        os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

        rc2 = -1


        #for i in userIN:
        #    if i == "|":
        #         hasPipe =True


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
                if hasPipe:
                    # os.close(1)
                    args = [userIN[0], userIN[1]]
                    #  sys.stdout = open(userIN[1], "w")
                    #  fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                    # os.set_inheritable(fd, True)
                    os.close(r)
                    w = os.fdopen(w, 'w')
                    fd = sys.stdout.fileno()
                    w.write("hello")
                    w.close()
                    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
                        program = "%s/%s" % (dir, args[0])
                        try:
                            os.execve(program, args, os.environ)  # try to exec program
                        except FileNotFoundError:  # ...expected
                            pass
                else:
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

            # elif userIN[1] == "|":


            elif len(userIN) == 4:
                if userIN[2] == ">":  # if is only (ex) wc file.txt > H.txt
                    os.close(1)
                    sys.stdout = open(userIN[3], "w")
                    fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                    os.set_inheritable(fd, True)
                    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
                        program = "%s/%s" % (dir, args[0])
                        try:
                            os.execve(program, args, os.environ)  # try to exec program
                        except FileNotFoundError:  # ...expected
                            pass


                elif userIN[2] == "<":  # if is only (ex) wc H.txt < file.txt
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

                else:
                    os.close(1)
                    args = [userIN[0], userIN[3]]
                    #  sys.stdout = open(userIN[1], "w")
                    #  fd = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
                    # os.set_inheritable(fd, True)
                    os.close(r)
                    w = os.fdopen(w, 'w')
                    fd = sys.stdout.fileno()
                    w.write(fd)
                    w.close()
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
            if hasPipe:  # if it has a pipe then fork ###############################################################
                rc2 = os.fork()
                # print(" I enter to pipe")
                # print("wait")
                # Parentpipe = os.wait()
                # print("WAIT2")

            if rc2 == 0:  # second part of the pipe
                os.write(2, ("got error %d\n" % rc2).encode())
                os.write(2, ("help me please %d\n" % rc2).encode())
                os.close(w)
                r = os.fdopen(r)
                print(r.read())
                sys.exit(1)


           # ''''os.close(r)  # I'll pass my the output of one process to the input of another process with this       ``
            #w = os.fdopen(w, 'w')
            # w.write(userIN)
            #w.close()
            
            #os.close(w)
           # r = os.fdopen(r)
           # print(r.read())''''

            #os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
            # childPidCode).encode())