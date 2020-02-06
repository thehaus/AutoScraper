supporteddbtypes=['text','sql','mongo']
dbtype=''

def initialize(databasetype):
    if databasetype in supporteddbtypes:
        global dbtype
        dbtype = databasetype
    else:
        #invalid initialization, default to text
        dbtype = 'text'

def writetodb(target,value):
    global dbtype
    if dbtype=='':
        #if module was not initialized, default to text
        initialize('text')
    if dbtype=='text':
        __writetotextdb(target,value)

def readfromdb(source):
    global dbtype
    if dbtype=='':
        #if module was not initialized, default to text
        initialize('text')
    if dbtype=='text':
        return __readfromtextdb(source)

def existsindb(target,value):
    global dbtype
    if dbtype=='':
        #if module was not initialized, default to text
        initialize('text')
    if dbtype=='text':
        return __existsintextdb(target,value)
    return False

def __writetotextdb(target,value):
    if not __existsintextdb(target,value):
        with open('textdata/'+target,'a+',encoding='utf-8') as filewriter:
            filewriter.write(value+'\n')

def __readfromtextdb(source):
    with open('textdata/'+source,'r') as filereader:
        return filereader.read().splitlines()

def __writetosqldb(target,value):
    #not implemented
    return False

def __readfromsqldb(source):
    #not implemented
    return False
    
def __writetomongodb(target,value):
    #not implemented
    return False

def __readfrommongodb(source):
    #not implemented
    return False

def __existsintextdb(target,value):
    try:
        if value in __readfromtextdb(target):
            return True
    except:
        return False
    return False