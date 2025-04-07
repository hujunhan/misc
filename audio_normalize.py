from pydub import AudioSegment
import pathlib


def normalize_audio(input_file, output_file, target_dBFS=-20.0):
    # Load the audio file (supports multiple formats)
    audio = AudioSegment.from_file(input_file)
    # Calculate the gain adjustment needed (in dB)
    change_in_dBFS = target_dBFS - audio.dBFS
    # Apply the gain adjustment
    normalized_audio = audio.apply_gain(change_in_dBFS)
    # Export the normalized audio in mp3 format
    normalized_audio.export(output_file, bitrate="256k")
    print(f"Normalized audio saved to: {output_file}")
    return normalized_audio


if __name__ == "__main__":
    # Define the root and train paths
    root_path = pathlib.Path(r"/Users/hu/Downloads")
    train_path = root_path / "train"
    output_dir = root_path / "train_normalize"

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Variable to store total duration in milliseconds
    total_duration_ms = 0

    # Iterate over files in the train folder
    for file in train_path.iterdir():
        if file.suffix.lower() == ".m4a":
            input_file = file
            # Construct output file name with .mp3 extension
            output_file = output_dir / f"{file.stem}.mp3"
            # Normalize the audio and capture the returned AudioSegment
            audio = normalize_audio(input_file, output_file)
            # Add the duration of this audio (in ms) to the total duration
            total_duration_ms += len(audio)

    # Convert total duration to seconds
    total_duration_sec = total_duration_ms / 1000
    print(
        f"Total duration of audio files in 'train' folder: {total_duration_sec:.2f} seconds"
    )
