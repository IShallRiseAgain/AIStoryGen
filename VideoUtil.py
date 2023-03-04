import subprocess
import os, random

def combine_videos(path, imagefiles, audiofiles, config):

    folder_path = "." + path
    output_filename = path + "\\" + "final.mp4"
    count = len(imagefiles)
    concat_command= "[0][1][2][3][4][5]concat=n=" + str(count) + ":v=1:a=1[vv][a];[vv]format=yuv420p[v]"
    ffmpeg_command = ["ffmpeg"] + generate_source_list(imagefiles, audiofiles) + ["-filter_complex"] + [concat_command] + ["-map", "[v]", "-map", "[a]", output_filename]
    print (" ".join(ffmpeg_command))
    # Run the FFmpeg command
    subprocess.run(ffmpeg_command, check=True, shell=True)
    
def generate_source_list(imagefiles, audiofiles):
    image_index=0
    sourceList = []
    for i in imagefiles:
        sourceList.append("-i")
        sourceList.append(i)
        sourceList.append("-i")
        sourceList.append(audiofiles[image_index])
        image_index=image_index + 1
    image_index=image_index+1
    return sourceList

def retrieve_music(config):
    path = "music\\" + config["music_genre"] + "\\" + random.choice(os.listdir("music\\" + config["music_genre"]))
    return ["-i", path]
