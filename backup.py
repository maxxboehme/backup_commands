#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import random
import time
import shutil

BARS = 50
MAX = 1000
LOCATION = ".\temp"

def _file_count(folder):
   total = 0
   for root, dirs, files in os.walk(folder):
      total += len(files)
   return total
   
def _file_copy(source_folder, destination_folder):
   for root, dirs, files in os.walk(source_folder):
      for item in files:
         src_path = os.path.join(root, item)
         dst_path = os.path.join(destination_folder, src_path.replace(source_folder, ""))
         if os.path.exists(dst_path):
            if os.stat(src_path).st_mtime > os.stat(dst_path).st_mtime:
               shutil.copy2(src_path, dst_path)
         else:
            shutil.copy(src_path, dst_path)
      for item in dirs:
         src_path = os.path.join(root, item)
         dst_path = os.path.join(destination_folder, src_path.replace(source_folder, ""))
         if not os.path.exists(dst_path):
            os.mkdir(dst_path)
   
def _print_loading_bar(x, newline, maxLimit, numberBars):
   percentag = (x*100) / maxLimit
   #print "percentage: " + str(percentag)
   colums = 100.0 / numberBars
   #print "colums: " + str(colums)
   bars = int(percentag / colums)
   #print "bars: " + str(bars)
   arrow = ">" if (bars != numberBars) else ""
   print("[" + ("=" * bars) + arrow + (" " * (numberBars - bars - 1))+"]")
   if not newline:
      sys.stdout.write("\033[F") # Cursor up one line

def _print_loading_bar2(x, newline, maxLimit, numberBars):
   percentag = (x*100) / maxLimit
   #print "percentage: " + str(percentag)
   colums = 100.0 / numberBars
   #print "colums: " + str(colums)
   bars = int(percentag / colums)
   #print "bars: " + str(bars)
   arrow = ">" if (bars != numberBars) else ""
   end = '\n' if newline else '\r'
   print("[" + ("=" * bars) + arrow + (" " * (numberBars - bars - 1))+"]", end=end)
   sys.stdout.flush()

def _main(args):
   print(_file_count(".\\test"))
   #shutil.copytree(".\\test", ".\\testTemp")
   _file_copy(".\\test", ".\\testTemp")
   '''
   for i in xrange(0, MAX+1):
      newline = True if i == MAX else False
      _print_loading_bar2(i, newline, MAX, BARS)
      time.sleep(.1)
   '''

if __name__ == "__main__":
   retCode = _main(sys.argv[1:])
   sys.exit(retCode)
