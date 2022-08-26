# pyrocury

## Motivation

If you've frequented learning from video lectures, youtube tutorials or any other prerecorded educational reference material, you'll be aware of the fluctuating 'Information Density'\* (in informal terms, the amount of brain cells required to process whats currently being discussed) throughout the content.

Almost everyone encounters this situtation without explicit knowledge of it - fast forwarding through the intro (BEFORE WE CONTINUE, WE THANK OUR SPONSORS RAID SHA-) and outro, skimming through the description of the tutorial (usually at 1.5x speed), and slowing down/pausing the video at the main sections that really matter, where you need time to process the information.

Infuriated by the bottleneck posed by this situation (instead resorting to audio transcripts to read), we've built `pyrocury`, an AI powered tool that smoothens the 'Information Density' for you by appropriately bifurcating and tweaking the speed of the lectures, so you spend your time on only whats important, while still watching the entire video.

Saves time, reduces mental lethargy, and empowers you to speedrun your education!

\*'Information Density' can be vaguely defined, in an academic sense, as the amount and complexity of new information imparted over time (or number of pages), considering you satisfy the course prerequisites.

## Client

The frontend take a youtube video link (bonus if uploading a video from the computer is allowed) as the input, along with a slider for the preferred 'information density rate'. And yes, a submit button.

This data is passed to the server, which returns the predicted information density graph (possibly bifurcated into sections) along with the normalized video. This is trivially sped up by the specified information density rate, and displayed using an embedded video player.

## Server

The core logic is based on the assumption that the activity heatmap (that can be found on popular youtube videos) has a degree of correlation to the 'information density' of the corresponding sections of the video.
