from src.EternalBlue import EternalBlue

def test_eternalblue():
    hg_token = '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'
    language = 'portuguese'
    audio_path = '/home/deathpirate/Downloads/tester.wav'

    eternal_blue = EternalBlue(hg_token, language)
    eternal_blue.diarize(audio_path)


if __name__ == '__main__':
    test_eternalblue()
