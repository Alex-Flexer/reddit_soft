import os
from TikTokApi import TikTokApi
import instaloader
from pytube import YouTube


def get_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")




def download_tiktok_video(url):
    downloads_folder = get_downloads_folder()
    path_to_save = os.path.join(downloads_folder, "tiktok_video.mp4")

    api = TikTokApi()
    video_data = api.video(url=url).bytes()

    with open(path_to_save, 'wb') as file:
        file.write(video_data)





def download_instagram_video(url):
    downloads_folder = get_downloads_folder()

    loader = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
    path_to_save = os.path.join(downloads_folder, "instagram_video")

    loader.download_post(post, target=path_to_save)




def download_youtube_video(url):
    downloads_folder = get_downloads_folder()
    path_to_save = os.path.join(downloads_folder, "youtube_video.mp4")

    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()

    stream.download(output_path=downloads_folder, filename="youtube_video.mp4")
