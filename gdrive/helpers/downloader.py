"""downloader helper."""

import glob
import os
from urllib.error import HTTPError

import wget
import yt_dlp
from pySmartDL import SmartDL
from yt_dlp import DownloadError

from gdrive import DOWNLOAD_DIRECTORY, LOGGER


def download_file(url, dl_path):
    try:
        dl = SmartDL(url, dl_path, progress_bar=False)
        LOGGER.info(f"Downloading: {url} in {dl_path}")
        dl.start()
        return True, dl.get_dest()
    except HTTPError as error:
        return False, error
    except Exception as error:
        try:
            filename = wget.download(url, dl_path)
            return True, os.path.join(f"{DOWNLOAD_DIRECTORY}/{filename}")
        except HTTPError:
            return False, error


def utube_dl(link):
    ytdl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIRECTORY, "%(title)s"),
        "noplaylist": False,
        "logger": LOGGER,
        "format": "bestvideo+bestaudio/best",
        "geo_bypass_country": "IN",
    }
    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
        try:
            meta = ytdl.extract_info(link, download=True)
        except DownloadError as e:
            return False, str(e)
        return next(
            (
                (True, path)
                for path in glob.glob(os.path.join(DOWNLOAD_DIRECTORY, "*"))
                if path.endswith(
                    (
                        ".avi",
                        ".mov",
                        ".flv",
                        ".wmv",
                        ".3gp",
                        ".mpeg",
                        ".webm",
                        ".mp4",
                        ".mkv",
                    )
                )
                and path.startswith(ytdl.prepare_filename(meta))
            ),
            (False, "Something went wrong! No video file exists on server."),
        )
