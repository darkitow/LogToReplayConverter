import json
import re    
import collections    

Pattern = collections.namedtuple('Pattern', ['LogInput', 'ReplayOutput'])
Pokemon = collections.namedtuple('Pokemon', ['Health', 'PokemonName', 'PokemonType'])

class LogToReplayCoverter:
    def __init__(self):
        self.GameInfo = dict()
        self.Lang = list()
        for el in json.load(open("lang.json")):
            self.Lang.append(Pattern(
                re.sub(
                    r'\{(\w+)\}',
                    lambda match: f'(?P<{match.group(1)}>.+?)',
                    el["Log"]
                ), # converter json em regex pra busca
                el["Replay"] if "Replay" in el else None
            ))
    
    def ParseLine(self, line:str):
        print(line.rstrip("\n"))
        for pat in self.Lang:
            match = re.match(pat.LogInput, line)
            if match is not None:
                for k, v in match.groupdict().items(): # dict com todas as informações
                    self.GameInfo[k] = v
                print(self.GameInfo)
                return re.sub(
                    r'\{(\w+)\}',
                    lambda match: self.GameInfo[match.group(1)],
                    pat.ReplayOutput
                ) if pat.ReplayOutput else None
        print(f"Couldn't find")

    def ConvertLog(self, path:str):
        with open(path, "r") as logFile:
            log = logFile.readlines()
        for line in log:
            if line == "\n": continue
            print(self.ParseLine(line), end="\n\n")

LTR = LogToReplayCoverter()
LTR.ConvertLog(r"examples/logs/BuRnXN0t.txt")