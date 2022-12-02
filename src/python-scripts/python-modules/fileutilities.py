import json

class fileutilities:
    def __init__(self):
        self.data_path = "../../../data/"

    def getbarefootoutput(self, startsegment: int) -> json:
        filepath: str = self.data_path + 'barefoot-response-' + str(startsegment) + '.txt'
        try:

            with open(filepath, 'r') as f:
                barefootresponse = json.load(f)
                f.close()
                return barefootresponse
        except FileNotFoundError:
            print('The file -: ', filepath, " does not exist")

    def getdecoderoutput(self, startsegment: int) -> json:
        filepath: str = self.data_path + 'decoder_out_' + str(startsegment) + '.txt'

        try:
            with open(filepath, 'r') as f:
                decoderresponse = json.load(f)
                f.close()
                return decoderresponse
        except FileNotFoundError:
            print('The file -: ', filepath, " does not exist")
