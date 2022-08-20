import re
import requests
import os
from os import walk

def add_highlight(path):
    '''It only add notes that do not have type #Conecpt or #MOC, and have a status of ✅ or 🌲
        Tags are small case and have underscores between words
    '''
    with open(path) as f:
        lines = f.readlines()

        highlight = ''
        tags = []
        note = ''
        for line in lines:
            if re.match('^# (.+)', line):
                highlight = re.findall('# (.+)', line)
                #print(highlight)
                highlight = highlight[0]
            
            elif re.match('Tags:', line):
                # After the [[ match everything that is not ] 
                tags = re.findall('\[\[([^\]]*)',line)
                #print(tags)
            elif (re.match('Type: #Concept', line) or re.match('Status: #MOC', line)):
                return None, None
            


    with open(path) as f:
        text = f.read()


        try:
            body_start = re.search(r"#\s+(.*)\n", text).end()
        except:
            body_start = 0
        
        # In case ##References does not exist, take till the end of file
        try:
            body_end = re.search(r"##\s+References", text).start()
        except:
            body_end = None

        #The title should be simply the name of the file not the headline
        full_path = f.name 
        sections = full_path.split('/')
        filename = sections[-1]
        #to remove extension
        title = filename.split('.')[0]
        body = text[body_start:body_end]
        note = body
        highlight = title


    
    return note, highlight



