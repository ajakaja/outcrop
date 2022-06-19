A script for adding space around photos in order to make them have a desired aspect ratio.

I made this because it's very annoying that photo printing websites will crop your images to a certain aspect ratio, but won't _expand_ your images and add space around them to do the same thing.

Usage:

```
./outcrop.py <filename> <aspect ratio> [-c <color>] [-p <padding>]
```

* `aspect ratio` should be a string like '8x10'. 
* `color` should be the name of a color, as recognized by ImageMagick. Defaults to `white`.
* `padding` is a value in pixels that it will make sure surrounds the whole image. Defaults to none.

Requires python3, at least 3.6 I think for f-strings? I dunno.
Requires `wand` (Python bindings for ImageMagick) to be available for import:

```
pip3 install wand
```

If you want to run this on all the files in a folder, or something, you can probably use something like:

```
find . -name "*.png" -exec ./outcrop.py {} 8x10 \;
```

Anyway, enjoy!
