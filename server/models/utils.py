def chunk_transcript(input: dict, duration: int):
    """
    Breaks the array of transcripts into subarrays arrays,
    each no more than 'duration' seconds in length.

    The input transcript looks as follows:
    [
        {
            "text": "Welcome to my youtube channel",
            "start": 1.23,
            "duration": 3.45
        },
        ...
    ]
    """

    output = []

    curr_l = 0.0
    curr_arr = []

    for st in input:
        # Transcript belongs to next segment.
        while curr_l+duration < st["start"]:
            output.append(curr_arr)
            curr_arr = []
            curr_l += duration
        
        curr_arr.append(st)
    # This is required as 'curr_arr' is not guarenteed to be empty.
    output.append(curr_arr)

    return output