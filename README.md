python-compare-mp3
===

Compare <img src="https://cdn.rawgit.com/mvasilkov/python-compare-mp3/6ce037d0/pictures/mp3.svg" width="48" valign="bottom" alt="mp3" title="mp3"> files using Python.

Installation
---

```sh
pip install -U compare-mp3
```

Command-line usage
---

```sh
compare-mp3 a.mp3 b.mp3
```

Programmatic usage
---

```python
from compare_mp3 import compare

if compare('a.mp3', 'b.mp3'):
    print('Files contain the same audio')
```

**Return values**

- `compare_mp3.SAME_FILE` Literally the same file
- `compare_mp3.SAME_BITSTREAM` Files have the same bitstream (but may have different metadata)
- `compare_mp3.SAME_WAV` Files contain the same audio (as decoded by LAME)
- `compare_mp3.DIFFERENT_MP3` Completely different files
