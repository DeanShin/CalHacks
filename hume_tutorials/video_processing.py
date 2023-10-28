# Preliminary Steps
# 1. Import Video with Audio
# 2. Split into 5 second increments 
# 3. Detach audio from these 5 second clips
#    1. result would be 5 second video and audio clips that we can leverage both apis
# 4. Create a map of the timestamps using these clips
# 5. For every 5 second clip
#    1. Send audio and video to hume
#       1. Can we send a zip file of all 5 second clips to hume?
#    2. return result
#    3. map results to time-span (ex: 0:00 - 0:05)
# 6. Deduce "spikes" in emotions
