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

    def write_data_file_for_vehicle_client(self, coordinates: list):
        filepath: str = self.data_path + 'slinga_with_e45.data'

        try:
            with open(filepath, 'a') as f:
                for point in coordinates:
                    f.write(str(round(point[0], 5)) + "," + str(round(point[1], 5)) + '\n')
                f.close()
        except FileNotFoundError:
            print('error writing to file -: ', filepath)

