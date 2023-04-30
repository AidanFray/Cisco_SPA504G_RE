# Session 3

Made a bit more progress with the the sector header reversing. We now know that the sector header has a length and a data offset.

We used this new information to make a decompression script. It slices out data from the firmware and sector headers to then grab data it can decompress.