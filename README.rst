

=================================
⚡ EternalBlue 🔊
=================================

**EternalBlue** is a project for audio diarization and transcription. It separates speakers in a `.wav` audio file and returns the diarized and transcribed audio.

Description
===========

EternalBlue is a powerful tool for audio analysis, capable of identifying and separating different speakers in a `.wav` audio file. Additionally, it performs complete transcription of the spoken content, facilitating the analysis and interpretation of conversations.

Installation
============

Requirements
------------

- Python 3.8 or higher

Installation Steps
------------------

You can install EternalBlue via pip:

.. code-block:: shell

    pip install eternalblue

Usage
=====

.. code-block:: python

    from eternalblue import EternalBlue
    eternal_blue = EternalBlue('', 'portuguese')
    eternalresponse = eternal_blue.diarize(audio, 2)

Here's an example of how to use the `EternalBlue` class in a Flask application:

.. code-block:: python

    from eternalblue import EternalBlue

    @app.route('/diarization', methods=['POST'])
    def diarization():
        try:
            eternalresponse = {}
            if 'audio' in request.files:
                audio_file = request.files['audio']
                if audio_file.filename != '':
                    save_path = os.path.join(AUDIO_PATH, audio_file.filename)
                    audio_file.save(save_path)
                    eternal_blue = EternalBlue('', 'portuguese')
                    eternalresponse = eternal_blue.diarize(save_path, 2)
            return eternalresponse, 200
        except Exception as e:
            print(f"Error: {e}")
            return str(e), 500


For empty trash in failed jobs

.. code-block:: python

    from eternalblue import EternalBlue
    EternalBlue.clear_cache()

Description
-----------

The `EternalBlue` class requires a Hugging Face API key, the language, and optionally the Whisper model in its constructor. The `diarize` method expects the path to the `.wav` audio file and the number of speakers.

Constructor Parameters
----------------------
- **api_key**: The Hugging Face API key as a string.
- **language**: The language of the audio as a string.
- **whisper_model** (optional): The Whisper model to use.

Method `diarize`
----------------
- **audio_file_path**: The path to the `.wav` audio file as a string.
- **num_speakers**: The number of speakers as an integer.

Expected Return
===============

The `diarize` method returns a list of dictionaries containing metadata and transcriptions, formatted as follows:

.. code-block:: json

    [
        {
            "metadata": [
                {
                    "audioname": "tester.wav",
                    "time_type": "seconds"
                }
            ]
        },
        {
            "end": 5.984999999999999,
            "speaker_id": "SPEAKER_01",
            "start": 1.299,
            "text": " Is your name Bento Ferreira, then? Are you Brazilian? Yes, sir."
        },
        {
            "end": 5.934,
            "speaker_id": "SPEAKER_00",
            "start": 5.323,
            "text": " Yes, sir."
        },
        {
            "end": 8.498,
            "speaker_id": "SPEAKER_01",
            "start": 6.851,
            "text": " military police officer, That's it ?."
        },
        {
            "end": 13.829,
            "speaker_id": "SPEAKER_00",
            "start": 9.856,
            "text": " Thank God, after 35 years in the reserve."
        },
        {
            "end": 16.613,
            "speaker_id": "SPEAKER_00",
            "start": 15.645,
            "text": " Mr. Miguel. Miguel! "
        },
        {
            "end": 19.618000000000002,
            "speaker_id": "SPEAKER_00",
            "start": 16.969,
            "text": " Any relation to  James ?"
        },

    ]

This JSON structure contains the following information for each segment:
- **metadata**: General information about the audio file.
- **speaker_id**: The identifier for the speaker.
- **start**: The start time of the speech segment in seconds.
- **end**: The end time of the speech segment in seconds.
- **text**: The transcribed text of the speech segment.