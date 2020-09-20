# Automated GRPC tester client using evans

A simple wrapper tester script to run different permutation combination of inputs to a rpc.

## How to run

The script has following command line options

```
    $ python3 tester.py --help
    Usage: tester.py [options]

    Options:
    -h, --help            show this help message and exit
    -H HOST, --host=HOST  GRPC server address to connect
    -p PORT, --port=PORT  GRPC server port to connect
    -t PROTOFILE, --proto=PROTOFILE
                            GRPC proto file to use for testing
    -d PDIR, --dir=PDIR   test input+output directory

```

* Start the GRPC server on a given host and port using the given proto file.

* start the tester to connect to specific server using the same proto file.

 Eg:

```
    $ python3 tester.py -p 5678 -t ./test/user.proto -d ./test

```
In this example the client will connect to a server that running locally on port 5678.

The specific directory(-t) contains all the test inputs in json files. Only one input message is stored in single json file. i.e total number of json files in the directory is equal to the total number of input sets that user wanted to test.

```
    $ ls ./test
    out.txt  RPC.txt  testInput2.json  testInput3.json  testInput.json  user.proto

```
The directory has also contain a file 'RPC.txt' which has the rpc name to be called.

```
    $ cat ./test/RPC.txt 
    UserAuthProto.UserAuthService.AddUser

```

After executing all the tests, the generated results are stored under same directory as './test/out.txt'