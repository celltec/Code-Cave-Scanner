import os
import argparse
from itertools import count

def find_code_caves(exe_bytes: bytes, min_size: int):
    data = enumerate(exe_bytes, 1)

    QUOTIENT = 100 / len(exe_bytes)
    prev_percent = 0
    total_found = 0

    for pos, byte in data:
        percent = int(QUOTIENT * pos)
        if percent > prev_percent:
            print(f'\rScanning file: {percent} %{f" ({total_found} found)" if total_found else ""}', end='')
            prev_percent = percent

        if byte:
            continue

        address = pos - 1
        for size in count(1):
            try:
                byte = next(data)[1]
                if byte != 0x0:
                    break
            except StopIteration:
                break

        if size >= min_size:
            total_found += 1
            yield hex(address), size

def main():
    parser = argparse.ArgumentParser(description='Find code caves in executables')
    parser.add_argument('file', type=str, help='Path to executable file')
    parser.add_argument('size', nargs='?', type=int, default=100, help='Minimum size in bytes')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f'{args.file} is not a file')

    if args.size < 10:
        parser.error('A code cave must be at least 10 bytes')

    with open(args.file, 'rb') as file:
        code_caves = []
        try:
            for code_cave in find_code_caves(file.read(), args.size):
                code_caves.append(code_cave)
        except KeyboardInterrupt:
            pass

        print(f'\r{" " * 40}\rFound {len(code_caves)} code cave{"s" if len(code_caves) > 1 else ""}:\n')
        print('Address      Size\n')

        code_caves.sort(key=lambda x: x[1], reverse=True)
        for address, size in code_caves:
            print(str(address).ljust(12), size)

if __name__ == '__main__':
    main()
