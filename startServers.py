import multiprocessing
from flask import Flask
import queryServer
import pyQBWC
import qwcSimulator
import time

# this is the script to start everything up. It starts two servers
# in two separate processes.
# by uncommenting the last three lines it can also start a third client process that simulates the Quickbooks web connector for testing.

def  QuickBooksFacing(requestQueue,responseQueue):
    pyQBWC.app.config['requestQueue'] = requestQueue
    pyQBWC.app.config['responseQueue'] = responseQueue    
    pyQBWC.app.run(port=8000,debug=False)
    
def WebFacing(requestQueue,responseQueue):
    queryServer.app.config['requestQueue'] = requestQueue
    queryServer.app.config['responseQueue'] = responseQueue
    queryServer.app.run(host='127.0.0.1',port=5001,debug=False)
    # having debug=True is throwing a lot of warnings

def qwc():
    qwcSimulator.runSimulator()
        
if __name__ == '__main__':
    jobs = []
    requestQueue = multiprocessing.Queue()
    responseQueue = multiprocessing.Queue()
    talktoquickbooks  = multiprocessing.Process(target=QuickBooksFacing, args=(requestQueue,responseQueue))
    jobs.append(talktoquickbooks)
    webserver = multiprocessing.Process(target=WebFacing, args=(requestQueue,responseQueue))
    jobs.append(webserver)
    #simulator = multiprocessing.Process(target=qwc)
    #jobs.append(simulator)
    talktoquickbooks.start()
    webserver.start()
    time.sleep(1)
    #simulator.start()
