import whisper

model = whisper.load_model('medium')


def get_timestamps(filepath: str) -> list[dict]:
    """
    Use whisper to get timestamps of spoken segments of an
    audio file
    :param filepath: the path to the audio file
    :return: a list containing timestamp information about each
             spoken segment
    """
    print("Reading timestamps from audio")

    result = model.transcribe(filepath, language='en', verbose=False)

    return [{'text': segment['text'], 'start_time': segment['start'], 'end_time': segment['end']} for segment in
            result['segments']]
