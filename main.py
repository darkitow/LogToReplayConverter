import json
import re    
import collections    

Pattern = collections.namedtuple('Pattern', ['LogInput', 'ReplayOutput'])
Pokemon = collections.namedtuple('Pokemon', ['Health', 'PokemonName', 'PokemonType'])

def PatternReplacement(match):
    return f'(?P<{match.group(1)}>.+?)'

class LogToReplayCoverter:
    def __init__(self):
        self.GameInfo = dict()
        self.Lang = list()
        for el in json.load(open("lang.json")):
            self.Lang.append(Pattern(
                re.sub(r'\{(\w+)\}', PatternReplacement, el["Log"]),
                None
            ))
    
    def ParseLine(self, line:str):
        for pat in self.Lang:
            match = re.match(pat.LogInput, line)
            if match is not None:
                for k, v in match.groupdict().items(): # dict com todas as informações
                    self.GameInfo[k] = v
                print(self.GameInfo)
                return
        print("Couldn't find ")
                    

LTR = LogToReplayCoverter()
LTR.ParseLine("Start of Turdsadan 5a")