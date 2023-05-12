# Session 4

A session full of frustration. Running `binwalk` on the sector files was giving corrupted and uninteresting elf files. We spent most of time faffing about with getting that sorted.

## Investigation

I tried the same thing on my device at home, and some chunky `elf` files appeared. What??

After comparing hashes and making sure everything going into `binwalk` was correct I've narrowed it down to different shell programs

### `fish` vs `bash`

During the session I was running:

```
cat *.bin > ALL.bin
```

This would give me one file `binwalk` could work with.

If we compare the output from both shells:

```
bash$ cat *.bin | md5sum
c171188feff17e5771d43633b98ec341  -
```

```
fish$ cat *.bin | md5sum
0015effed24d09c088cf4d7b4c5e02df  -
```

Something is going on here, I was under the assumption that a shell wouldn't effect the output of basic tools like `cat`. How wrong I was....

It comes down to how each shell handles the expansion of the wildcard (`*.bin`)

We can see immediately they're in a different order...

`fish`:
```
sector_0x1.bin
sector_0x3.bin
sector_0x3a.bin
sector_0x3b.bin
sector_0x3c.bin
sector_0x3d.bin
sector_0x3e.bin
sector_0x3f.bin
[...]
```

`bash`:
```
sector_0x1.bin
sector_0x3.bin
sector_0x35.bin
sector_0x36.bin
sector_0x37.bin
sector_0x38.bin
sector_0x39.bin
sector_0x3a.bin
[...]
```

There is a lesson here somewhere...

This also shows us that the order of the sectors is important. I will update the script to just create us an `all.bin` file with a guaranteed order. 

## Investigation #2

So even the order that `bash` produces is not correct. If we compare the output of `binwalk` on the `all.bin` provided by the updates to the script:

`bash`
```
-rwxrwxrwx 1 user user 3309964 May 12 13:19 1A7FBA
-rwxrwxrwx 1 user user 3272202 May 12 13:19 1A7FBA.zlib
-rwxrwxrwx 1 user user 2103504 May 12 13:19 2AAC70
-rwxrwxrwx 1 user user 2212180 May 12 13:19 2AAC70.zlib
-rwxrwxrwx 1 user user  523660 May 12 13:19 363D67
-rwxrwxrwx 1 user user 1454173 May 12 13:19 363D67.zlib
-rwxrwxrwx 1 user user 4886400 May 12 13:19 kosmos_ipp.st.gz
-rwxrwxrwx 1 user user  142444 May 12 13:19 psbl.elf
```

Script output:
```
-rwxrwxrwx 1 user user 3309964 May 12 13:18 1A7FBA
-rwxrwxrwx 1 user user 3272202 May 12 13:18 1A7FBA.zlib
-rwxrwxrwx 1 user user 2103504 May 12 13:18 2AAC70
-rwxrwxrwx 1 user user 2212180 May 12 13:18 2AAC70.zlib
-rwxrwxrwx 1 user user  523660 May 12 13:18 363D67
-rwxrwxrwx 1 user user 1454173 May 12 13:18 363D67.zlib
-rwxrwxrwx 1 user user 4414461 May 12 13:18 kosmos_ipp.st
-rwxrwxrwx 1 user user  142444 May 12 13:18 psbl.elf
```

The main thing to notice is the is now successfully decompressed `kosmos_ipp.st`! 