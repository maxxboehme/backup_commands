#!/usr/bin/env python
# from __future__ import print_function
import sys
import os
import random
import time
import shutil
import logging
import glob
import optparse
import platform

_moduleLogger = logging.getLogger(__name__)

BARS = 50
MAX = 1000
LOCATION = ".\\temp"

def _file_count(folder):
   total = 0
   for root, dirs, files in os.walk(folder):
      total += len(files)
   return total

def _file_copy(source, destination, forceCopy=False):
   copyCount = 0
   totalNumberOfFiles = _file_count(source)
   fileCount = 0
   for root, dirs, files in os.walk(source):
      for file in files:
         fileCount += 1
         if not os.path.exists(destination+root.strip(".")):
            os.makedirs(destination+root.strip("."))
         if forceCopy or not os.path.exists(destination+root.strip(".")+"\\"+file):
            shutil.copy(root+"\\"+file, destination+root.strip(".")+"\\"+file)
            copyCount += 1
         else:
            if os.stat(root+"\\"+file).st_mtime > os.stat(destination+root.strip(".")+"\\"+file).st_mtime:
               shutil.copy(root+"\\"+file, destination+root.strip(".")+"\\"+file)
               copyCount += 1
         _print_loading_bar3(fileCount, totalNumberOfFiles, 50)
   return copyCount

def _delete_files(source):
   copyCount = 0
   totalNumberOfFiles = _file_count(source)
   fileCount = 0
   for root, dirs, files in os.walk(source):
      for file in files:
         fileCount += 1
         os.remove(root+"\\"+file)
         _print_loading_bar3(fileCount, totalNumberOfFiles, 50)
   shutil.rmtree(source)
   return copyCount

def _gen_files(destination, numberOfDirs, numberOfFiles, maxHeight):
   _gen_files_rec(destination, numberOfDirs, numberOfFiles, 0, maxHeight)
      
def _gen_files_rec(path, numberOfDirs, numberOfFiles, height, maxHeight):
   if height == maxHeight:
      return
   else:
      for i in xrange(0, numberOfDirs):
         newPath = path+"\\dev"+str(i)+"_"+str(height)
         os.makedirs(newPath)
         _gen_files_rec(newPath, numberOfDirs, numberOfFiles, height+1, maxHeight)
      for i in xrange(0, numberOfFiles):
         open(path+"\\TestFile"+str(i)+".txt", "w+")

def _print_loading_bar(x, maxLimit, numberBars):
   percentag = (x*100) / maxLimit
   #print "percentage: " + str(percentag)
   colums = 100.0 / numberBars
   #print "colums: " + str(colums)
   bars = int(percentag / colums)
   #print "bars: " + str(bars)
   arrow = ">" if (bars != numberBars) else ""
   print "[" + ("=" * bars) + arrow + (" " * (numberBars - bars - 1))+"]"
   if x < maxLimit:
      sys.stdout.write("\033[F") # Cursor up one line

def _print_loading_bar2(x, maxLimit, numberBars):
   percentag = (x * 100) / maxLimit
   #print "percentage: " + str(percentag)
   colums = 100.0 / numberBars
   #print "colums: " + str(colums)
   bars = int(percentag / colums)
   #print "bars: " + str(bars)
   arrow = ">" if (bars != numberBars) else ""
   end = '\n' if x >= maxLimit else '\r'
   #print("[" + ("=" * bars) + arrow + (" " * (numberBars - bars - 1))+"]"+"\t"+str(x)+"/"+str(maxLimit)+" Files Copied", end=end)
   sys.stdout.flush()
   
def _print_loading_bar3(x, maxLimit, numberBars):
   percentag = (x * 100) / maxLimit
   #print "percentage: " + str(percentag)
   colums = 100.0 / numberBars
   #print "colums: " + str(colums)
   bars = int(percentag / colums)
   #print "bars: " + str(bars)
   arrow = ">" if (bars != numberBars) else ""
   end = '\n' if x >= maxLimit else '\r'
   print "[" + ("=" * bars) + arrow + (" " * (numberBars - bars - 1)) + "]" + "\t" + str(x)+"/" + str(maxLimit) + " Files Copied" + end,
   sys.stdout.flush()
   
'''
backup list keys
'''
def _print_keys(keyFiles, destination):
   print "\nRemote Destination: " + destination + "\n"
   gap = 6
   maxLengthKey = len("Keys")
   maxLengthSource = len("Source")

   for key, source in keyFiles.iteritems():
      if maxLengthKey < len(key):
         maxLengthKey = len(key)
      if maxLengthSource < len(source):
         maxLengthSource = len(source)
   #maxLengthKey += gap
   maxLengthSource += gap
   
   col = ""
   for i in xrange(len("Keys"), maxLengthKey):
      col += " "
   col += "Keys"
   for i in xrange(len("Source"), maxLengthSource):
      col += " "
   col += "Source"
   print col
   l = len(col)
   col = ""
   for i in xrange(len("Keys"), maxLengthKey):
      col += " "
   for i in xrange(0, len("Keys")):
      col += "-"
   for i in xrange(len("Source"), maxLengthSource):
      col += " "
   for i in xrange(0, len("Source")):
      col += "-"
   print col
   
   for key, source in keyFiles.iteritems():
      col = ""
      for i in xrange(len(key), maxLengthKey):
         col += " "
      col += key
      for i in xrange(len(source), maxLengthSource):
         col += " "
      col += source
      print col

def _write_dictionary_to_file(dictionary, destination):
   with open(destination, 'w') as outputFile:
      json.dump(dictionary, outputFile)
      
def _write_variables_to_file(outputPath, destination):
   with open(outputPath, 'w') as outputFile:
      pickle.dump(destination, outputFile)
      
def _load_variables_from_file(source):
   results = ()
   if os.path.exists(source):
      with open(source, 'r') as inputFile:
         results = pickle.load(inputFile)
   return results
      
def _load_dictionary_from_file(source):
   dictionary = {}
   if os.path.exists(source):
      with open(source, 'r') as inputFile:
         dictionary = json.load(inputFile)
   return dictionary
   '''
   for i in xrange(0, MAX+1):
      newline = True if i == MAX else False
      _print_loading_bar2(i, newline, MAX, BARS)
      time.sleep(.1)
   '''

def _parse_options(args):
   # Setup the required arguments for this script
   usage = r"""
usage: %prog [options]

Ex: 
> python %prog 
""".strip()
   parser = optparse.OptionParser(usage)
   parser.add_option(
     "--copy",
     action="store", dest="copy", default="",
     help=""
   )
   parser.add_option(
     "--list",
     action="store_true", dest="list", default=False,
     help=""
   )
   parser.add_option(
     "--gen",
     action="store_true", dest="gen", default=False,
     help=""
   )
   parser.add_option(
     "--add",
     action="store", dest="add", default="",
     help=""
   )
   parser.add_option(
     "--remove",
     action="store", dest="remove", default="",
     help=""
   )
   parser.add_option(
     "--force",
     action="store_true", dest="force", default=False,
     help=""
   )
   parser.add_option(
     "--all",
     action="store_true", dest="all", default=False,
     help=""
   )
   parser.add_option(
     "--delete",
     action="store", dest="delete", default=False,
     help=""
   )
   parser.add_option(
     "-s", "--source",
     action="store", dest="source", metavar="SOURCE", default="",
     help="NIMXL file to check for colliding ranges. Can include more then one source to test if ranges in any files collide with each other."
   )
   parser.add_option(
      "--destination",
      action="store", dest="destination", default="",
      help=""
   )
   debugGroup = optparse.OptionGroup(parser, "Debug")
   debugGroup.add_option(
      "--verbose",
      action="store", dest="verboseLevel", default='1',
      help="Verbose output level."
   )
   debugGroup.add_option(
      "--log-file", metavar="PATH",
      action="store", dest="logFile",
      help="Write the log to file (if specified)"
   )
   debugGroup.add_option(
      "--test",
      action="store_true", dest="test", default=False,
      help="Run doctests then quit."
   )
   parser.add_option_group(debugGroup)

   options, positional = parser.parse_args(args)
   if positional:
      parser.error("Unsupported positional arguments %r" % positional)

   loggingLevel = {
      0: logging.DEBUG,
      1: logging.INFO,
      2: logging.WARNING,
      3: logging.ERROR,
      4: logging.CRITICAL,
   }.get(int(options.verboseLevel), None)
   if loggingLevel is None:
      parser.error("Unsupported verbosity: %r" % options.verboseLevel)

   return options, loggingLevel


def _main(args):
   options, loggingLevel = _parse_options(args)

   logFormat = '(%(asctime)s) %(levelname)-5s %(name)s.%(funcName)s: %(message)s'
   logging.basicConfig(level=loggingLevel, format=logFormat)
   if options.logFile is not None:
      fileHandler = logging.FileHandler(options.logFile, "w")
      fileHandler.setFormatter(logging.Formatter(logFormat))
      root = logging.getLogger()
      root.addHandler(fileHandler)

   if options.test:
      import doctest
      print (doctest.testmod())
      return 0
    
   print "For this script to work make sure you have at lest Python 2.7 and that you are running with administrator or root privileges.\nContinue?[y/n]"
   answer = sys.stdin.readline().upper().strip()
   if answer != "Y" and answer != "YES":
      return 0
   userOS = platform.system()
   print "Installing for "+userOS
   winInstallPath = "C:\\Program Files\\BackupScript"
   if userOS == "Windows":
      if not os.path.exists(winInstallPath):
         os.makedirs(winInstallPath)
      shutil.copy(".\\installers\\windows\\backup.py", winInstallPath+"\\backup.py")
      shutil.copy(".\\installers\\windows\\backup.bat", winInstallPath+"\\backup.bat")
      os.environ["BACKUPSCRIPT"] = winInstallPath + "\\backup.bat"
      os.system(".\\installers\\windows\\backupinstaller.bat")
      #path = os.environ["PATH"]
      #if path[-1] != ";" os.envrion["PATH"] += ";"
      #os.environ["PATH"] += "%BACKUPSCRIPT%;"

if __name__ == "__main__":
   retCode = _main(sys.argv[1:])
   sys.exit(retCode)