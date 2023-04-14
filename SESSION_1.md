# Session 1

After unpacking the firmware zip we now have:

- `spa50x-30x-7-6-2f.bin`
- `spa50x-30x-7-6-2f.exe`
- `spa50x-30x-7-6-2f-recovery.exe`

Lets look at the `.bin` file.

### spa50x-30x-7-6-2f.bin

After running:

```
binwalk -M -e ./spa50x-30x-7-6-2f.bin
```

We now have the following:

### `kosmos_ipp.st.gz`

A `gzip` file that seems to be corrupted.

We get the following when `gunzip`ing:

```
gzip: kosmos_ipp.st.gz: unexpected end of file
```

The `kosmos` string seems to match the string at the start of the `.bin` firmware:

```
00000000  53 6b 4f 73 4d 6f 35 20  66 49 72 4d 77 41 72 45  |SkOsMo5 fIrMwArE|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000030  90 2d f5 21 17 f8 1f e7  8b 4d 68 27 cc b1 87 a4  |.-.!.....Mh'....|
00000040  8c 6c d4 ed 19 b2 74 e9  3e 49 ad eb f6 55 01 a3  |.l....t.>I...U..|
00000050  00 00 00 80 00 00 00 40  00 43 15 3d 37 2e 36 2e  |.......@.C.=7.6.|
00000060  32 66 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |2f..............|
00000070  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 4f  |...............O|
00000080  00 00 00 00 00 00 77 8b  00 00 14 40 16 16 e6 d2  |......w....@....|
00000090  1e a2 87 c2 7a a1 db 0b  37 8f dd fb 00 00 00 00  |....z...7.......|
````

*Not sure how this helpful?*

### `psbl.elf`

This is the most promising artefact. It's a MIPS binary with **symbols**

```
psbl.elf: ELF 32-bit MSB executable, MIPS, MIPS-II version 1 (SYSV), statically linked, not stripped
```

## Teardown 

After cracking the case open and having a look at the board we can tell the the chip is manafactured by Texas Instruments and has the text `TNETVI057ZDW` written on it. 