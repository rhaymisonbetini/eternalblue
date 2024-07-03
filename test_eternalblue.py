from eternalblue.eternalBlue import EternalBlue
import warnings

warnings.filterwarnings('ignore')


def test_eternalblue():
    hg_token = ''
    language = 'portuguese'
    audio_path = '/home/deathpirate/Downloads/tester.wav'

    eternal_blue = EternalBlue(hg_token, language)
    teste = eternal_blue.diarize(audio_path)
    print(teste)

if __name__ == '__main__':
    test_eternalblue()
