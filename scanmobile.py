import sys
import subprocess
from firebase import firebase
import time
import urllib2, urllib, httplib
import json
import os
from functools import partial
from datetime import datetime
from pytz import timezone
from subprocess import check_output

interface = "wlan0"
firebase = firebase.FirebaseApplication('https://le615-d865e.firebaseio.com/', None)

def get_address(cell):
    return matching_line(cell,"Address: ")

rules={
       "Address":get_address
       }


def matching_line(lines, keyword):
    """Returns the first matching line in a list of lines. See match()"""
    for line in lines:
        matching=match(line,keyword)
        if matching!=None:
            return matching
    return None

def match(line,keyword):
    """If the first part of line (modulo blanks) matches keyword,
    returns the end of that line. Otherwise returns None"""
    line=line.lstrip()
    length=len(keyword)
    if line[:length] == keyword:
        return line[length:]
    else:
        return None

def parse_cell(cell):
    """Applies the rules to the bunch of text describing a cell and returns the
    corresponding dictionary"""
    parsed_cell={}
    for key in rules:
        rule=rules[key]
        parsed_cell.update({key:rule(cell)})
    return parsed_cell

def main():
    """Pretty prints the output of iwlist scan into a table"""

    cells=[[]]
    parsed_cells=[]

    proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()

    for line in out.split("\n"):
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())

    cells=cells[1:]


    for cell in cells:
        parsed_cells.append(parse_cell(cell))

    beam = {'Address' : 'B8:57:D8:A3:F3:B2'}
    bew =  {'Address' : 'BE:54:36:07:E7:8A'}
    tz = timezone('Asia/Bangkok')

    for sc in range(len(parsed_cells)) :
         print(parsed_cells[sc])
         if parsed_cells[sc] == beam and parsed_cells[sc] == bew :
           #connectwifi()
            data1 = 'Beam here !'
            data2 = 'Bew here !'
            now = datetime.now(tz)
            dt = now.strftime("%d/%m/%Y %H:%M:%S")
            firebase.post('/scanwifi',{'Timestamps':dt,'who':data1})
            firebase.post('/scanwifi',{'Timestamps':dt,'who':data2})
            break
         elif parsed_cells[sc] == beam:
           #connectwifi()
            data = 'Beam here !'   #insert own name room
            now = datetime.now(tz)
            dt = now.strftime("%d/%m/%Y %H:%M:%S")
            firebase.post('/scanwifi', {'Timestamps':dt,'who':data})
            break

         elif parsed_cells[sc] == bew:
            #connectwifi()
            data = 'Bew here !'   #insert own name room
            now = datetime.now(tz)
            dt = now.strftime("%d/%m/%Y %H:%M:%S")
            firebase.post('/scanwifi', {'Timestamps':dt,'who':data})
            break


while True :
        main()
        time.sleep(30)
