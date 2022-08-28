In this age of open, accessible knowledge - be it OCW lectures from MIT, high school science from Khan Academy or guitar tutorials from Justin Guitar - youtube has become the defacto educational repository of the 21 century.
While the opportunities for a motivated learner are limitless, the duration and volume of many of these lectures are both daunting and time consuming - directly impacting productivity and increasing mental lethargy.

Consider your experience with video tutorials - you skip the introduction, aggressively fast-forward anything that looks like a sponsored message and skim through the prologue and outro at 2x speed. Watching the lectures at 2x speed actually presents more problems than it solves, requiring us to frequently rewind and slow it down at complex parts of the lecture.
(CHANGE) If only it were possible to jump right into the main parts of the lecture... 

*Some hype inducing background music*

Presenting Metrophon - an AI powered tool to speedrun your education. Built using state-of-the-art AI tech, and boasting of original research done by our team - Metrophon analyzes, highlights and summarizes any lecture, appropriately speeding up and slowing down the video throughout, to a pace you're comfortable with, so you only spend your time on whats important.
Reduces the time spent on each lecture by as much as 40%, allowing you to learn more in lesser amount of time.

*Demo*

This is accomplished by calculating the 'Information Density' of the transcript using both symblai and pretrained NLP models, which is then standardized using statistical models and other heuristics. The 'Information Density' can be described in informal terms as the amount of brain cells needed to process and understand the corresponding content.

A broad outline of its internals are as follows:
- First, the youtube video is accessed, along with its activity heatmap and transcript.
- Topic summarization functionality of `symblai` is then employed to determine the core topics.
- We then clean the transcript data, generating several features using both standard and custom NLP algorithms - Flesch-Kincaid readability, lexical diversity, topic frequency, cooccurence matrices, implication weights etc.
- Using the heatmap as our labels, we train a ML model using `Pytorch`, which determines the 'Information Density' graph.
- This data is then used to appropriately split, speeden and merge the video, giving it a normalized information density.

The power of this tech lies in its scalability - agnostic of the topic, it can be used on many forms of educational content like podcasts episodes, audio books, cooking and music videos, apart from the usual OCW lectures. Future plans of the software include extension to pinpoint core sections of articles and research papers, and the autogeneration of synopsis on Google Books and the likes, elimitating a lot of fluff noise.
