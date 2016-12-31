# coding: utf-8
import csv
import time
import os
import itertools
import base64
import inflection
import csv, codecs, cStringIO
import glob
import math
import pycurl
from io import BytesIO
import pandas as pd
import requests
import shutil
from csv import DictWriter
from cStringIO import StringIO
import datetime
import collections

class DateUtils:
    @staticmethod
    def get_current_date_month_day_year():
        return datetime.datetime.now().strftime("%m/%d/%Y")

    @staticmethod
    def get_current_date_year_month_day():
        return datetime.datetime.now().strftime("%Y_%m_%d_")

class PickleUtils:
    @staticmethod
    def pickle_cells(cells, pickle_name ):
        pickle.dump( cells, open(picked_dir + pickle_name + "_pickled_cells.p", "wb" ) )

    @staticmethod
    def unpickle_cells(pickle_name):
        return pickle.load( open(picked_dir + pickle_name +"_pickled_cells.p", "rb" ) )


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class FileUtils:
    '''class for file/os util functions'''
    @staticmethod
    def getFileListForDir(filepath_str_to_search):
        '''gets file list in a directory based on some path string to search- ie: /home/adam/*.txt'''
        return glob.glob(filepath_str_to_search)

    @staticmethod
    def getAttachmentFullPath(output_dir, output_fn, download_url):
        '''downloads an attachment from whereever'''
        #equivelent to: curl -L "https://screendoor.dobt.co/attachments/s5wflD750Nxhai9MfNmxes4TR-0xoDyw/download" > whateverFilename.csv
        # As long as the file is opened in binary mode, can write response body to it without decoding.
        downloaded = False
        try:
            with open(output_dir + output_fn, 'wb') as f:
                c = pycurl.Curl()
                c.setopt(c.URL, download_url)
                # Follow redirect.
                c.setopt(c.FOLLOWLOCATION, True)
                c.setopt(c.WRITEDATA, f)
                c.perform()
                c.close()
                downloaded = True
        except Exception, e:
            print str(e)
        return downloaded

    @staticmethod
    def getFiles(output_dir, output_fn, download_url ):
        dowloaded = False
        r = requests.get(download_url, stream=True)
        with open(output_dir+output_fn, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            downloaded = True
        return downloaded

    @staticmethod
    def remove_files_on_regex(dir, regex):
        files_to_remove =  FileUtils.getFileListForDir(dir + regex )
        for the_file in files_to_remove:
            try:
                if os.path.isfile(the_file):
                    os.unlink(the_file)
                #this would remove subdirs
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    @staticmethod
    def write_wkbk_csv(fn, dictList, headerCols):
        wrote_wkbk = False
        with open(fn, 'w') as csvfile:
            try:
                fieldnames = headerCols
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for data in dictList:
                    try:
                        writer.writerow({ s:str(v).encode("ascii",  'ignore') for s, v in data.iteritems()  } )
                    except:
                        print "could not write row"
                wrote_wkbk = True
            except Exception, e:
                print str(e)
        return wrote_wkbk

class ListUtils:

    '''class for list util functions'''
    @staticmethod
    def flatten_list(listofLists):
        return [item for sublist in listofLists for item in sublist]


class EncodeObjects:

    @staticmethod
    def convertToString(data):
        '''converts unicode to string'''
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(EncodeObjects.convertToString, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(EncodeObjects.convertToString, data))
        else:
            return data

    @staticmethod
    def convertToUTF8(data):
        '''converts unicode to string'''
        if isinstance(data, basestring):
            return data.encode('utf-8')
        elif isinstance(data, collections.Mapping):
            return dict(map(EncodeObjects.convertToUTF8, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(EncodeObjects.convertToUTF8, data))
        else:
            return data


class ShtUtils:
    '''class for common wksht util functions'''
    @staticmethod
    def getWkbk(fn):
        wkbk = pd.ExcelFile(fn)
        return wkbk

    @staticmethod
    def get_sht_names(wkbk):
        shts =  wkbk.sheet_names
        return [ sht for sht in shts if sht != 'Dataset Summary']





if __name__ == "__main__":
    main()
