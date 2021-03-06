#!/usr/bin/env python
"""
logo thread for the pymol master plugin
uses pycurl to connect to a remote server
and requests sequence logo

author: Nick Fiacco, 6/2015, using structure of search_thread.py from Tim Tregubov
"""


import threading
import json
import pycurl
import base64
from StringIO import StringIO
from constants import *
import traceback

class LogoThread(threading.Thread):
    """
    logo thread allows the ui to remain responsive while this sends off the logo request and waits
    """

    def __init__(self, rmsd, search_id, flag, url, cmd, logo_filepath = None, extension = "gif"):
        """
        This is the constructor for our SearchThread.  Each time we perform
        a structural search, a new thread will be created.
        """
        threading.Thread.__init__(self)

        self.databuffer = StringIO()

        self.rmsd_cutoff    = rmsd
        self.query          = search_id.strip()
        self.flag           = flag
        self.cmd = cmd
        self.logo_filepath = logo_filepath  # defalut value is None, will be set based on query name
        self.extension = extension

        self.seqs = []
        self.url = url  # Currently selected host
        self.conn = None
        self.error = None

        self.concurrency_management = {'begun': False,  # True once the thread begins consuming
                                       'ended': False,  # True once the thread finishes consuming
                                       'lock': threading.Lock()}  # This guards the 'begun' and 'end' variables

    def on_receive(self, streamdata):
        """
        callback for processing data
        """
        try:
            jsondata = json.loads(streamdata)
            if 'error' in jsondata:
                raise Exception(jsondata['error'])
            else:
                self.databuffer.write(streamdata.strip())
                # append to databuffer cause sometimes packets for results span multiple calls
        except ValueError:
            self.databuffer.write(streamdata.strip())
            # for valueerror we just append cause this could be multiple packets
        except Exception as e:
            # stop on error
            self.error = 'error processing response: ' + e.message
            return -1  # will trigger a close

    def run(self):
        """
        This method will send the search request to the server
        """
        try:

            # set begun atomically
            self.concurrency_management['lock'].acquire()
            try:
                self.concurrency_management['begun'] = True
            finally:
                self.concurrency_management['lock'].release()

            # setup pycurl connection to server
            self.conn = pycurl.Curl()
            self.conn.setopt(pycurl.URL, self.url)
            self.conn.setopt(pycurl.FOLLOWLOCATION, 1)
            self.conn.setopt(pycurl.MAXREDIRS, 5)
            self.conn.setopt(pycurl.POST, 1)
            self.conn.setopt(pycurl.CONNECTTIMEOUT, 1200)
            self.conn.setopt(pycurl.TIMEOUT, 1200)
            self.conn.setopt(pycurl.NOSIGNAL, 1)

            # create JSON object with required info
            data = [
                ('query', self.query),
                ('flag', str(self.flag)),
                ('rmsdCut', "999"),
                ('ext', self.extension)
            ]
            self.conn.setopt(pycurl.HTTPPOST, data)

            # this runs the callback every time we get new data
            self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
            self.conn.perform()

            if not self.error:
                # now we parse our databuffer
                # once we're done check the stringbuffer for the complete json matches
                try:
                    jsondata = json.loads(self.databuffer.getvalue())
                    if 'results' in jsondata:

                        if 'logo' in jsondata:
                            unencoded = base64.standard_b64decode(jsondata['logo'])

                            if self.logo_filepath == None:
                                if self.flag == 1:
                                    logo_filepath = LOGO_CACHE + str(self.query)+'s.gif'
                                elif self.flag == 2:
                                    logo_filepath = LOGO_CACHE + str(self.query)+'f.gif'
                            else:
                                logo_filepath = self.logo_filepath

                            # write to the specified filepath
                            print "trying to write %s..." % logo_filepath
                            logo_file = open(logo_filepath, 'wb')
                            logo_file.write(unencoded)
                            logo_file.close()

                except Exception as e:
                    print('error processing response: ' + str(e.message) + "\nrawdata: " + str(self.databuffer.getvalue()))
                    print(traceback.format_exc())

        except Exception as e:
            # check for self.error as that would contain certain types of errors that weren't exceptions
            if self.error:
                print("Trouble posting request1: " + self.error)
            else:
                print("Trouble posting request2: " + e.message)
                print(traceback.format_exc())

        finally:
            # once done set ended atomically
            self.concurrency_management['lock'].acquire()
            try:
                self.concurrency_management['ended'] = True
            finally:
                self.concurrency_management['lock'].release()

    def stop(self, message=''):
        """
        abort abort!
        """
        self.concurrency_management['lock'].acquire()
        try:
            if not self.concurrency_management['ended']:
                if self.concurrency_management['begun']:
                    try:
                        self.conn.close()
                    except Exception as e:
                        print("ran into trouble closing the connection: " + e.message)
                self.concurrency_management['ended'] = True
        finally:
            self.concurrency_management['lock'].release()
            if message != '':
                print message


    # def cacheData(self):
