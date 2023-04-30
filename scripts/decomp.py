from struct import unpack
import zlib
import os

OUT_DIR = f"sectors"

def u32(i):
    return unpack(">I", i)[0]

def u16(i):
    return unpack(">H", i)[0]

def slicer(d, s, l):
    return d[s:s+l]

if __name__ == '__main__':

    with open(f"../artifacts/spa50x-30x-7-6-2f.bin", "rb") as f:
        data = f.read()

    # Firmware Header
    total_sectors = u32(slicer(data, 0x7c, 0x4))

    offset = 0x40
    for sector in range(total_sectors - 1):

        sector_header   = slicer(data, offset + 0x80, 0x40)

        sector_id       = u16(slicer(sector_header, 0x0, 0x2))
        sector_flag     = u16(slicer(sector_header, 0x2, 0x2))
        sector_size     = u32(slicer(sector_header, 0x4, 0x4))
        sector_offset   = u32(slicer(sector_header, 0x8, 0x4))

        # Grab our data from sector
        sector_data = slicer(data, sector_offset, sector_size)

        print(f"Decompressing sector {sector_id}")

        os.makedirs(OUT_DIR, exist_ok=True)

        with open(f"./{OUT_DIR}/sector_{hex(sector_id)}.bin", "wb") as f:
            if sector_flag & 0x1 == 0x1:
                # Sector is not compressed
                f.write(sector_data)
            else:
                sector_data_decomp = zlib.decompress(sector_data, 0xf)
                f.write(sector_data)

        offset += 0x40
