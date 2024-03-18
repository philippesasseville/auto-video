from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend


def upload_videos(videos):
    auth = AuthBackend(cookies='cookies/cookies.txt')
    failed_videos = upload_videos(videos=videos, auth=auth)