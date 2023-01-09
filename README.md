Example code:

```
import os
from WantedPoster import WantedPoster
from PIL import Image


def main():
    # Open test portrait
    portrait_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test', 'luffy.jpg')

    # Set "Luffy" as first name and "D. Monkey" as last name
    first_name = 'Luffy'
    last_name = 'Monkey D.'

    # Set bounty amount to 3.000.000.000
    bounty_amount = 3_000_000_000

    # Create WantedPoster object
    wanted_poster = WantedPoster(portrait_path, first_name, last_name, bounty_amount)

    # Generate poster
    path = wanted_poster.generate()

    # Show image
    Image.open(path).show()


if __name__ == '__main__':
    main()
```
