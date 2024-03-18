import argparse
from tiktok_video_creator import create_tiktok_video
from bin_cleaner import clear_folder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a TikTok-style video from a YouTube video and a Reddit thread.')
    parser.add_argument('youtube_url', type=str, help='YouTube video URL')
    parser.add_argument('reddit_url', type=str, help='Reddit thread URL')
    parser.add_argument('output_name', type=str, help='Output video name')
    args = parser.parse_args()
    clear_folder('bin/')
    clear_folder('output/')
    create_tiktok_video(args.youtube_url, args.reddit_url, args.output_name)