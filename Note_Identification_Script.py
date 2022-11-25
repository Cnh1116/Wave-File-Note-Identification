#Parameters--------------------------------------------------------
from distutils.log import error
from tkinter.tix import NoteBook


referenceFrequency = 440 #Middle A
noteList = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B'] #Index 0 - 11
noteRelationship = 2**(1/12)
errorAllowed = 0.025 #2.5% Error Allowed
noteIndex = 9 #Middle A Starts at index 9
currentOctave = 4 #Starting in the 4th octave

#---------------------------------------------
maximumFreq = 617.54
#---------------------------------------------

def PercentError(maximumFreq, currentFreq):
    error = (abs((maximumFreq-currentFreq)/currentFreq))
    percentError = error * 100
    print("Percent difference between ", maximumFreq, " and ", currentFreq, " is ", error, " or ", percentError, "%")
    return error

#Max Frequency is Middle A
if (PercentError(maximumFreq, referenceFrequency) <= errorAllowed):
    print("Your note is Middle A: ", noteList[9])

#Max Frequency is Lower than Middle A
elif (maximumFreq < referenceFrequency):
    currentFreq = referenceFrequency

    while(PercentError(maximumFreq, currentFreq) > errorAllowed):
        currentFreq = currentFreq / noteRelationship
        print("Current Frequency = ", currentFreq)
        if(noteIndex == 0): #If we are on C, then jump to B, one octave lower
            noteIndex = 11
            currentOctave = currentOctave -1
        else:
            noteIndex -= 1

    print("Your note was: ", noteList[noteIndex], " in octave: ", currentOctave)

#Max Frequency is Higher than Middle A
elif (maximumFreq > referenceFrequency):
    currentFreq = referenceFrequency

    while(PercentError(maximumFreq, currentFreq) > errorAllowed):
        currentFreq = currentFreq * noteRelationship
        print("Current Frequency = ", currentFreq)
        if(noteIndex == 11): #If we are on B, then jump to C, one octave higher
            noteIndex = 0
            currentOctave += 1
        else:
            noteIndex += 1

    print("Your note was: ", noteList[noteIndex], " in octave: ", currentOctave)
    
    