from struct import unpack
import zlib
import os
import argparse

def u32(i):
    return unpack(">I", i)[0]

def u16(i):
    return unpack(">H", i)[0]

def slicer(d, s, l):
    return d[s:s+l]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SPA504G Toolkit')
    parser.add_argument("--file", "-f", help="File path for the firmware .bin file (The script supports bash's wildcard to specify a number of firmware files)", type=str, nargs="+", required=True)
    parser.add_argument("--unpack", "-u", help="Flag used to specify if the firmware should be unpacked and decompressed", action="store_true")
    parser.add_argument("--out", "-o", help="If unpack mode is specified this will defined the location that will contain the unpacked sections", default="sectors")
    args = parser.parse_args()

    for file_path in args.file:

        fmr_path = args.file[0]

        print()
        print(f"### Processing firmware file at: \"{fmr_path}\"")

        with open(fmr_path, "rb") as f:
            data = f.read()

        # Firmware Header
        total_sectors = u32(slicer(data, 0x7c, 0x4))

        print(f"Firmware has {total_sectors} sectors")

        all_data = b""

        offset = 0x40
        for sector in range(total_sectors - 1):

            sector_header   = slicer(data, offset + 0x80, 0x40)

            sector_id       = u16(slicer(sector_header, 0x0, 0x2))
            sector_flag     = u16(slicer(sector_header, 0x2, 0x2))
            sector_size     = u32(slicer(sector_header, 0x4, 0x4))
            sector_offset   = u32(slicer(sector_header, 0x8, 0x4))

            print(f"\t[Sector] ID: {sector_id} -- Size: {hex(sector_size)} -- Offset: {hex(sector_offset)}")

            # Grab our data from sector
            sector_data = slicer(data, sector_offset, sector_size)

            if args.unpack:

                print(f"\tDecompressing sector {sector_id}")

                os.makedirs(args.out, exist_ok=True)

                with open(f"./{args.out}/sector_{hex(sector_id)}.bin", "wb") as f:
                    if sector_flag & 0x1 == 0x1:
                        # Sector is not compressed
                        write_data = sector_data
                    else:
                        sector_data_decomp = zlib.decompress(sector_data, 0xf)
                        write_data = sector_data_decomp

                    all_data += write_data
                    f.write(write_data)

            offset += 0x40

        # Writes all the data to a single file with a guaranteed order
        if all_data != b"":
            with open(f"./{args.out}/all.bin", "wb") as f:
                f.write(all_data)
