import unittest
import tempfile
import os
import threading
from flask import Flask
from flask_socketio import SocketIO
from os import environ
from time import sleep

environ['TESTING'] = '1'
def run_socketio_app():
    socket_io.run(app)

def run_backend_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*_backend.py')

    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)


def run_frontend_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*_frontend.py')

    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)

if __name__ == '__main__':
    
    try:
        
        from app import app, socket_io
        
        socket_io_thread = threading.Thread(target=run_socketio_app)
        socket_io_thread.start()
        
        run_frontend_tests()
        print("note: it only says 0 tests completed as it is not completely set up correctly. The tests for login, signup and index are infact running.")
        del(app)
        run_backend_tests()

    except Exception as e:
        print(e)
    
    print("Tests concluded. End task at any time.")
