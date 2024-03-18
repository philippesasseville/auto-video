from video_downloader import download_youtube_video
from reddit_thread_extractor import get_reddit_thread
from asset_generator import generate_title_card_from_template, render_html_to_image
from video_composer import compose_video_parts

def create_tiktok_video(youtube_url, reddit_url, output_name):
    download_youtube_video(youtube_url, output_name)
    title, selftext, comments = get_reddit_thread(reddit_url)
    generate_title_card_from_template('assets/title_card/template.html', 'assets/title_card/output.html', title)
    render_html_to_image('assets/title_card/output.html', 'bin/title_card')
    compose_video_parts(output_name,title,selftext)

