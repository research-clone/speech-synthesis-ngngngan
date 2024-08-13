import os
import json
import re
import unicodedata
from yt_dlp import YoutubeDL

from _constants import INFO_DATA_PATH
import argparse


os.makedirs(INFO_DATA_PATH, exist_ok=True)

def get_info(args):
	if args.colab_dir_base != None:
		INFO_DATA_PATH = INFO_DATA_PATH.replace("data", args.colab_dir_base)

	with open("scripts/youtube_links.txt") as ytl:
		channel_list = ytl.readlines()
		print(channel_list)


	for channel in channel_list:
		channel = channel.strip()
		channel_video = f"{channel}/videos"

		channel_name = channel.split("@")[-1]
		info_path = os.path.join(INFO_DATA_PATH, f"{channel_name}.json")
		# TODO do same with podcast 

		# get info from all audio
		with YoutubeDL({}) as ydl:
			info = ydl.extract_info(channel_video, download=False)
		raw_list_vid = {
			el["id"]: {
				# "url": el["webpage_url"],
				"title": el["title"],
				# "upload_date": el["upload_date"],  # already sorted by upload date
				"description": el["description"],
				"is_downloaded": 0
			}
			for el in ydl.sanitize_info(info)["entries"]
		}


		with open(info_path, "w", encoding="utf-8") as f_i:
			json.dump(raw_list_vid, f_i, ensure_ascii=False, indent="\t")
	# see file draft.json to understand how below regex is written


if __name__=="__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('--colab_dir_base', type=str, default=None)
	
	args = parser.parse_args()

	get_info(args)
