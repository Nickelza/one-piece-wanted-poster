# one-piece-wanted-poster

[![Python](https://img.shields.io/pypi/pyversions/one-piece-wanted-poster)](https://img.shields.io/pypi/pyversions/one-piece-wanted-poster)
[![Pypi](https://img.shields.io/pypi/v/one-piece-wanted-poster)](https://pypi.org/project/one-piece-wanted-poster/)
[![LOC](https://sloc.xyz/github/nickelza/one-piece-wanted-poster/?category=code)](https://github.com/nickelza/one-piece-wanted-poster/)
[![Downloads](https://static.pepy.tech/personalized-badge/one-piece-wanted-poster?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month)](https://pepy.tech/project/one-piece-wanted-poster)
[![Downloads](https://static.pepy.tech/personalized-badge/one-piece-wanted-poster?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/one-piece-wanted-poster)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/nickelza/one-piece-wanted-poster/blob/master/LICENSE)
[![Forks](https://img.shields.io/github/forks/nickelza/one-piece-wanted-poster.svg)](https://github.com/nickelza/one-piece-wanted-poster/network)
[![Issues](https://img.shields.io/github/issues/nickelza/one-piece-wanted-poster.svg)](https://github.com/nickelza/one-piece-wanted-poster/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)

---------

### Install one-piece-wanted-poster from PyPi.
```bash
pip install one-piece-wanted-poster
```

#### Example

```
import os
from wantedposter.wantedposter import WantedPoster
from PIL import Image


def main():
    # Set "Luffy" as first name and "D. Monkey" as last name
    first_name = 'Luffy'
    last_name = 'Monkey D.'

    # Set bounty amount to 3.000.000.000
    bounty_amount = 3_000_000_000

    # Create WantedPoster object
    wanted_poster = WantedPoster(None, first_name, last_name, bounty_amount)

    # Generate poster
    path = wanted_poster.generate()

    # Show image
    Image.open(path).show()


if __name__ == '__main__':
    main()
```

### Credits

[AlleCosti95](https://github.com/allecosti95?tab=repositories)

Thanks to ClayStage for providing the original [template](https://claystage.com/one-piece-wanted-poster-template).