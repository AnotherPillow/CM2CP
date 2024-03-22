import json5, shutil, os, json
from preconditiontogsq import convert as preconditiontogsq

from .Logger import logger

curly_st = '{{'
curly_end = '}}'

class Converter:
    manifest: dict = {}
    incontent: dict = {}
    outcontent: dict = {
        "Format": "2.0",
        "Changes": []
    }
    
    def __init__(self):
        self.manifest = json5.load(open('input/manifest.json', encoding='utf8'))
        self.incontent = json5.load(open('input/content.json', encoding='utf8'))

        if os.path.exists('output'):
            shutil.rmtree('output')
        shutil.copytree('input', 'output')

    def convert(self):
        
        for track in self.incontent['Music']:
            # {
            # "Id": "title_night",
            # "File": "select.ogg",
            # "Loop": true,
            # "Ambient": false
            # }
            entry = {
                track['Id']: { # Ideally ID would be actually unique, but would require modifying of other parts.
                    'ID': track['Id'], 
                    'FilePaths': [
                        f'{curly_st}AbsoluteFilePath: {track["File"]}{curly_end}'
                    ],
                    'Category': 'Ambient' if track['Ambient'] == True else 'Default',
                    'Looped': track['Loop']
                }
            }
        

            change = {
                "Action": "EditData",
                "Target": "Data/AudioChanges",
                "Entries": entry
            }

            self.outcontent['Changes'].append(change)



        self.translateManifest()
        self.save()


    def translateManifest(self):
        self.manifest['UniqueID'] += '.CP'
        self.manifest['Author'] += ' ~ CM2CP'

        self.manifest['ContentPackFor']['UniqueID'] = 'Pathoschild.ContentPatcher'
        if 'Dependencies' in self.manifest:
            self.manifest['Dependencies'] = \
                [mod for mod in self.manifest['Dependencies'] if mod['UniqueID'] not in ['Platonymous.CustomMusic']]
        
    def save(self):
        
        with open('output/manifest.json', 'w') as f:
            json.dump(self.manifest, f, indent=4)
        
        with open('output/content.json', 'w') as f:
            json.dump(self.outcontent, f, indent=4)