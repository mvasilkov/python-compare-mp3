import filecmp
from functools import lru_cache
from os import chmod
from pathlib import Path
import platform
from shutil import copy as copy_file, which
import stat
from subprocess import check_call, check_output
import sys
from tempfile import TemporaryDirectory

from mutagen import id3

DIFFERENT_MP3 = 0
SAME_FILE = 1
SAME_BITSTREAM = 2
SAME_WAV = 3

binary_dependencies = Path(__file__).parent / 'binary_dependencies'
system = platform.system()


def which_prog(prog_name: str, prog_binary: str):
    if system == 'Darwin':
        a = str(binary_dependencies / prog_binary)
        set_executable(a)  # package built on Windows won't have executable bits set
        return a

    if system == 'Windows':
        return str(binary_dependencies / f'{prog_binary}.exe')

    prog = which(prog_binary)
    if not prog:
        raise RuntimeError(f'{prog_name} is not installed')

    return prog


@lru_cache(1)
def which_lame():
    return which_prog('LAME', 'lame')


def test_requirements():
    assert sys.version_info.major == 3 and sys.version_info.minor >= 6

    version = check_output([which_lame(), '--version'], encoding='utf-8')
    assert (version.startswith('LAME 64bits version 3.100')
            or version.startswith('LAME 64bits version 3.99.5'))


def compare(a: str, b: str, check_tags: bool = True) -> int:
    if filecmp.cmp(a, b, False):
        return SAME_FILE

    if check_tags:
        with TemporaryDirectory('compare-mp3') as tempdir:
            tempdir = Path(tempdir)
            name_a = (tempdir / 'a.mp3').as_posix()
            name_b = (tempdir / 'b.mp3').as_posix()
            copy_file(a, name_a)
            copy_file(b, name_b)
            id3.delete(name_a)
            id3.delete(name_b)

            if filecmp.cmp(name_a, name_b, False):
                return SAME_BITSTREAM

    with TemporaryDirectory('.wav') as tempdir:
        name_a = tempdir + '/a.wav'
        name_b = tempdir + '/b.wav'

        check_call([which_lame(), '--decode', a, name_a])
        check_call([which_lame(), '--decode', b, name_b])
        set_writable(name_a)
        set_writable(name_b)

        if filecmp.cmp(name_a, name_b, False):
            return SAME_WAV

    return DIFFERENT_MP3


def compare_cli(a: str, b: str) -> int:
    result = compare(a, b)

    if result == SAME_FILE:
        print('This is literally the same file')
        return 0

    if result == SAME_BITSTREAM:
        print('Files have the same bitstream')
        return 0

    if result == SAME_WAV:
        print('Files contain the same audio (as decoded by LAME)')
        return 0

    if result == DIFFERENT_MP3:
        print('Completely different files')
        return 1

    raise RuntimeError('Catastrophic error')


def set_writable(a):
    if system == 'Windows':
        chmod(a, stat.S_IWRITE)


def noexcept(fun):
    def wrapped(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except:
            pass

    return wrapped


@noexcept
def set_executable(a):
    if system != 'Windows':
        chmod(a, 0o755)


def run():
    test_requirements()

    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} a.mp3 b.mp3')
    else:
        sys.exit(compare_cli(sys.argv[1], sys.argv[2]))


if __name__ == '__main__':
    run()
