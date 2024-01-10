import os
from datetime import datetime, timezone

# I copied code from here https://www.programiz.com/python-programming/datetime/current-datetime
# TODO it would be nice to support an argument which specifies the timezone instead of hardcoding UTC
def getDateTime():  
  # datetime object containing current date and time
  now = datetime.now(timezone.utc)
  # dd/mm/YY H:M:S
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  dt_string += " UTC"
  return dt_string

# This is similar to the code above except that slashes have been replaced with dashes to make it safe for filenames
def getDateTimeFormatedForFilename():
  # datetime object containing current date and time
  now = datetime.now(timezone.utc)
  dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
  dt_string += "_UTC"
  return dt_string

# Converts from seconds to hours, minutes, seconds - this is a wrapper for existing libraries 
def get_time_hh_mm_ss(seconds):
    from datetime import timedelta
    td = timedelta(seconds=seconds)
    return td

# Note: This assumes that there are only images and .txt and .log files in the directory
# A better implementation would be to have an argument that accepts a list of file extentions to count
def countNumberOfImagesInFolder(folder):
  count = 0
  # Iterate directory
  for f in os.listdir(folder):
      # check if current path is a file and also not a .txt file
      if (os.path.isfile(os.path.join(folder, f)) and not f.lower().endswith(".txt") and not f.lower().endswith(".log")):
          count += 1
  return count

#In Linux, if you use echo to write to a file echoing parentheses or & causes problems so we are using backslash to escape these characters before trying to echo them to a file
def reformatToSafeString(inputString):
  return inputString.replace("(", "\(").replace(")", "\)").replace("&", "\&")

def getTorF(booleanValue):
  if  booleanValue:
    return "True"
  else:
    return "False"
  
# Mount Google Drive from inside Google Colab
def connectToGoogleDrive():    
   from google.colab import drive
   if not os.path.exists('/content/drive'):
        print("Connecting to Google Drive.")
        drive.mount('/content/drive')

def checkFileExists(path, name):
   if not os.path.exists(path):
      return False
   if not os.path.isfile(os.path.join(path, name)):
      return False
   return True

# Its probably not effiencent to open and close the file everytime a line is written. I'll refactor if I see any proformance problems
def writeLineToFile(filePath, fileName, lineText):
   filePathName = os.path.join(filePath, fileName) 
   if(not checkFileExists(filePath, fileName)):
      # "w" will create a new file and open it 
      fileToUpdate = open(filePathName, "w")
   else: 
      # "a" will open an existing file for appending
      fileToUpdate = open(filePathName, "a")
   contentToWrite = lineText + "\n"
   fileToUpdate.write(contentToWrite)
   fileToUpdate.close()

def readFile(filePath, fileName):
   filePathName = os.path.join(filePath, fileName) 
   if(not checkFileExists(filePath, fileName)):
      print(f"Error. No file {filePathName} exists")
      return
   fileToRead = open(filePathName, 'r')
   data = fileToRead.read()
   fileToRead.close()
   return data

def writeLineBreakToFile(filePath, fileName):
  writeLineToFile(filePath, fileName, "==============================")
 
def writeHeaderToFile(filePath, fileName, headerString):
  writeLineToFile(filePath, fileName, "")
  writeLineBreakToFile(filePath, fileName)
  writeLineToFile(filePath, fileName, headerString)
  writeLineBreakToFile(filePath, fileName)
  writeLineToFile(filePath, fileName, "")

# This function is highly specific to AI Lora training
def writeLogHeaderToFile(filePath, fileName, projectName):
  writeLineBreakToFile(filePath, fileName)
  logLineOne = "Log file for Automated Lora Maker project: " + projectName
  writeLineToFile(filePath, fileName,  logLineOne)
  logDateTimeLine = "Date of creation: " + getDateTime()
  writeLineToFile(filePath, fileName, logDateTimeLine)
  writeLineBreakToFile(filePath, fileName)

def writeLogForTagging(filePath, fileName, trigger, gelbooruSearchQuery, removedTags, topTags, taggingTime):
  writeHeaderToFile(filePath, fileName, "Tagging Logs")
  logTriggerLine = "Trigger(s): " + str(trigger)
  writeLineToFile(filePath, fileName, logTriggerLine)
  logGelbooruSearchQueryLine = "Gelbooru search query: " + str(gelbooruSearchQuery)
  writeLineToFile(filePath, fileName, logGelbooruSearchQueryLine)
  logAbsorbedTagsLine = "Tags absorbed into Trigger: " + str(removedTags)
  writeLineToFile(filePath, fileName,  logAbsorbedTagsLine)
  logTop50TagsLine = "Top 50 tags: " + str(topTags)
  writeLineToFile(filePath, fileName, logTop50TagsLine)
  logTagTimerLine = "Tagging Process took: " + str(get_time_hh_mm_ss(taggingTime))
  writeLineToFile(filePath, fileName, logTagTimerLine)

def calculateItemsPerSecond(items, seconds):
  return int(items) / int(seconds)

def writeLogForLoraTrainingSettings(filePath, fileName, dataSetFolder, modelName, flipAug, numRepeats, perferredUnits, howManyUnits, trainingBatchSize, dimToUse, trainingTime, totalTime):
    writeHeaderToFile(filePath, fileName, "Lora Training Data")
    logLoraTrainingLogTemp = "Trained on: " + str(countNumberOfImagesInFolder(dataSetFolder)) + " images"
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Training Model: " + modelName
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "flip_aug: " + getTorF(flipAug)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Num of Repeats: " + str(numRepeats)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Unit is Epochs or Steps: " + str(perferredUnits)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Number of Epochs or Steps: " + str(howManyUnits)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Training Batch Size: " + str(trainingBatchSize)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Network Dim: " + dimToUse
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTimerLine = "Lora Creation Process took: " + str(get_time_hh_mm_ss(trainingTime))
    writeLineToFile(filePath, fileName, logLoraTimerLine)
    logLoraTimerLine = "Total Process took: " + str(get_time_hh_mm_ss(totalTime))
    writeLineToFile(filePath, fileName, logLoraTimerLine)


# Adding a new v2 interface for the Training Settings log in such a way that it wont existing implementations 
def writeLogForLoraTrainingSettings_v2(filePath, fileName, dataSetFolder, modelName, flipAug, numRepeats, perferredUnits, howManyUnits, trainingBatchSize, dimToUse, totalSteps, resolution, trainingTime, totalTime):
    writeHeaderToFile(filePath, fileName, "Lora Training Data")
    logLoraTrainingLogTemp = "Trained on: " + str(countNumberOfImagesInFolder(dataSetFolder)) + " images"
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Training Model: " + modelName
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "flip_aug: " + getTorF(flipAug)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Num of Repeats: " + str(numRepeats)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Unit is Epochs or Steps: " + str(perferredUnits)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Number of Epochs or Steps: " + str(howManyUnits)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Training Batch Size: " + str(trainingBatchSize)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Total Steps: " + str(totalSteps)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Resolution: " + str(resolution)
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTrainingLogTemp = "Network Dim: " + dimToUse
    writeLineToFile(filePath, fileName, logLoraTrainingLogTemp)
    logLoraTimerLine = "Lora Creation Process took: " + str(get_time_hh_mm_ss(trainingTime))
    writeLineToFile(filePath, fileName, logLoraTimerLine)
    logLoraTimerLine = "Total Process took: " + str(get_time_hh_mm_ss(totalTime))
    writeLineToFile(filePath, fileName, logLoraTimerLine)

def writeLogForFlipAugs(filePath, fileName, isImageDownloadSkipped, isTaggingSkipped, isTrainingSkipped):
  writeHeaderToFile(filePath, fileName, "Skip Flags")
  logTemp = "skip_image_downloading: " + getTorF(isImageDownloadSkipped)
  writeLineToFile(filePath, fileName, logTemp)
  logTemp = "skip_tagging: " + getTorF(isTaggingSkipped)
  writeLineToFile(filePath, fileName, logTemp)
  logTemp = "skip_training: " + getTorF(isTrainingSkipped)
  writeLineToFile(filePath, fileName, logTemp)

# Copypasta from https://www.w3schools.com/python/python_file_remove.asp 
def deleteFile(filePath, fileName):
    fileToDelete = os.path.join(filePath, fileName)
    if os.path.exists(fileToDelete):
        os.remove(fileToDelete)
    else:
        print(f"The file {fileToDelete} does not exist")
