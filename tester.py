# #! /usr/bin/python3
# Created by Sugesh Chandran
#
# Copyright (c) 2020 Signi5sys Ltd
#
import os
import subprocess
import optparse


rpcFileName = "RPC.txt"
outFile = "out.txt"
# Function to check if a binary is exists in the system.
def isProgramExists(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def checkTesterBinaries():
    # check if dos2Unix exists
    if not isProgramExists("dos2unix"):
        print("Cannot find dos2unix in executable path.")
        return False
    # check if evans exists in the path:
    if not isProgramExists("evans"):
        print("Cannot find evans(https://github.com/ktr0731/evans.git) in executable path")
        return False
    return True

def getProgramArgs():
    parser = optparse.OptionParser()
    # add host/server to connect to
    parser.add_option('-H', '--host',
            action="store", dest="host",
            help="GRPC server address to connect", default="127.0.0.1")
    # add listen port of server
    parser.add_option('-p', '--port',
        action="store", dest="port",
        help="GRPC server port to connect", default="5678")
    # add proto file to use for testing.
    parser.add_option('-t', '--proto',
            action="store", dest="protoFile",
            help="GRPC proto file to use for testing", default="/tmp/test.proto")
    # json input message directory
    parser.add_option('-d', '--dir',
            action="store", dest="pDir",
            help="test input+output directory", default="/tmp")    
    options, _ = parser.parse_args()
    return options

def rpcName(path):
    rpcFile = os.path.join(path, rpcFileName)
    if not os.path.isfile(rpcFile):
        print ("\n Cannot find rpc file " + rpcFile + " in " + path)
        return ""
    # read the file content
    fp = open(rpcFile, "r")
    rpc = fp.read()
    fp.close()
    return rpc

def writeResult(fp, inputFile, result, error):
    fp.write("\n\n**********************************************************************")
    fp.write("\n file : " + inputFile)
    fp.write("\n Result : " + result)
    fp.write("\n Error : " + error)

def runTest(host, port, protoFile, rpc, inputFile, outFp):
    cmd = "evans --host " + host + " --port " + port + " --proto " + protoFile +\
         " cli call --file " +\
          inputFile + " --enrich " + rpc
    print("\n Executing : " + cmd)
    process = subprocess.Popen(cmd.split(), universal_newlines=True, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    writeResult(outFp, inputFile, str(output), str(error))

def createOutFile(path):
    outF = os.path.join(path, outFile)
    fp = open(outF, "a+")
    return fp

def toUnixFile(filePath):
    cmd = "dos2unix " +  filePath
    process = subprocess.Popen(cmd.split(), universal_newlines=True, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate() 

def runTests(options):
    fp = createOutFile(options.pDir)
    rpc = rpcName(options.pDir)
    if rpc == "":
        print("Failed to get the valid rpc, exiting the tests")
        return

    for filename in os.listdir(options.pDir):
        if filename.endswith(".json"):
            fileFullPath = os.path.join(options.pDir, filename)
            # update the file to use unix format
            toUnixFile(fileFullPath)
            runTest(options.host, options.port, options.protoFile, rpc, 
            fileFullPath, fp)

    fp.close()

def main():
    if not checkTesterBinaries():
        return
    options = getProgramArgs()
    # start the test from the directory
    runTests(options)

main()