
from moviepy.editor import VideoFileClip, TextClip, AudioFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from gtts import gTTS
from moviepy.video.fx.all import crop
import re
import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')

def compose_video_parts(output_name, title, selftext):
    video_clip = VideoFileClip(f'bin/{output_name}.mp4').subclip(10)

    # Crop video to 9:16 aspect ratio (for TikTok)
    video_clip = crop(video_clip, width=600, height=5000, x_center=video_clip.size[0] / 2, y_center=video_clip.size[1] / 2)
    audio_clips = []
    text_clips = []

    # Add original post as text clip
    sentences = split_sentences(f'{title} {selftext}')
    print(sentences)
    for sentence in sentences:
        if sentence and sentence.strip():  # Check if sentence is not empty or just whitespace
            # Remove special characters from the sentence
            sentence_clean = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)

            # Generate audio clip with text-to-speech
            tts = gTTS(text=sentence_clean, lang='en')
            audio_file = f'{output_name}_audio_{len(audio_clips)}.mp3'
            tts.save(f'bin/{audio_file}')
            audio_clip = AudioFileClip(f'bin/{audio_file}')
            audio_clips.append(audio_clip)

            # Split text into lines without breaking words
            lines = wrap_text(sentence, 30)  # Adjust the number of characters per line as needed
            wrapped_text = '\n'.join(lines)
            print(wrapped_text)
            # Create a text clip with the same duration as the audio clip
            text_clip = TextClip(wrapped_text, fontsize=36, color='yellow', font='Helvetica-Bold').set_duration(
                audio_clip.duration)
            text_clip = text_clip.set_position(('center', 'center'))  # Set position to center
            text_clips.append(text_clip)

    # Split the video into clips corresponding to the audio clips
    total_duration = 0
    video_clips = []
    for audio_clip in audio_clips:
        video_clip_part = video_clip.subclip(total_duration, total_duration + audio_clip.duration)
        video_clip_part = video_clip_part.set_audio(audio_clip)
        video_clips.append(video_clip_part)
        total_duration += audio_clip.duration

    # Arrange video clips and text clips in CompositeVideoClip objects
    composite_clips = []
    for video_clip_part, text_clip in zip(video_clips, text_clips):
        composite_clip = CompositeVideoClip([video_clip_part, text_clip])
        composite_clips.append(composite_clip)

    # Create clips with the composite clips, each approximately 60 seconds long
    target_length = 60  # Target length for each clip in seconds
    current_clip_duration = 0
    current_clip_index = 1
    current_clips = []
    for clip in composite_clips:
        if current_clip_duration + clip.duration <= target_length:
            current_clips.append(clip)
            current_clip_duration += clip.duration
        else:
            final_clip = concatenate_videoclips(current_clips)
            # Load the cropped image and use it as a mask for the text clip
            cropped_image_path = 'bin/title_card__cropped.png'
            cropped_clip = ImageClip(cropped_image_path).set_duration(final_clip.duration)
            # Position the cropped image at the top of the final clip
            cropped_clip = cropped_clip.set_position(('center', 20))
            # Composite the cropped image on top of the final clip
            final_clip = CompositeVideoClip([final_clip, cropped_clip])
            final_clip.write_videofile(f'output/{output_name}_part{current_clip_index}.mp4')
            current_clips = [clip]
            current_clip_duration = clip.duration
            current_clip_index += 1

    # Write the last clip
    if current_clips:
        final_clip = concatenate_videoclips(current_clips)
        # Load the cropped image and use it as a mask for the text clip
        cropped_image_path = 'bin/title_card__cropped.png'
        cropped_clip = ImageClip(cropped_image_path).set_duration(final_clip.duration)
        # Position the cropped image at the top of the final clip
        cropped_clip = cropped_clip.set_position(('center', 20))
        # Composite the cropped image on top of the final clip
        final_clip = CompositeVideoClip([final_clip, cropped_clip])
        final_clip.write_videofile(f'output/{output_name}_part{current_clip_index}.mp4')

# Function to split text into sentences using spaCy
def split_sentences(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

# Function to split text into lines without breaking words
def wrap_text(text, width):
    lines = []
    words = re.findall(r'\S+|\n', text)
    current_line = ''
    for word in words:
        if '\n' in word:
            lines.append(current_line.strip())
            current_line = ''
        elif len(current_line) + len(word) <= width:
            current_line += word + ' '
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    if current_line:
        lines.append(current_line.strip())
    return lines
