import mutagen


separator = " --> "

def convertToSrtTimestamp(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = round((seconds % 1) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{milliseconds:03d}"

def updateSubtitle(subtitle, path, text, ind):
    subtitletxt =  subtitle[0] + str(ind) + "\n\n"
    duration = mutagen.File(path).info.length
    currentlength = subtitle[1] + duration 
    subtitletxt = subtitletxt + convertToSrtTimestamp(subtitle[1]) + separator + convertToSrtTimestamp(currentlength) + "\n\n"   
    subtitletxt = subtitletxt + text + "\n\n"
    return [subtitletxt, currentlength]  
