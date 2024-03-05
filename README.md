# Suzutsuki's PhotoFramer :camera:

My photo-framer helps you automatically frame your photos and embed camera parameters into the output photo.

## Dependency

You will need to install `PIL`, `numpy`, `tqdm`, and `os` to run this program.

**Important**: Your photo must have **EXIF data** for this program to function properly.

## How to Use?

To use the program, run the `main.py` file in your terminal. You will be asked to provide values for the following parameters:
* `shrink_factor`: A float between 0 and 1 (though, technically, any value works). This parameter determines how much your photo will be resized during the framing process. A prompt of `"Enter shrink factor (between 0 to 1)"` will appear when you execute the program.
* `all_export`: y/n. If you want to export all photos in the source folder, a prompt of `Do you want to export all photos? (y/n)` will appear in the terminal after entering the shrink factor.
* `idx`: If you answered 'n'/'N' to the previous question, you will be prompted to enter the index of the photo you want to process. The range will be given.

**By Default**, the program will only read photos placed in the `./source` folder, and the output will be placed in the `./output` folder. Feel free to modify the code to fit your preferences!

Ideally, you should move your photo compilation to the `./source` folder and execute the `main.py` file. After everything finishes, you will be able to see the output in the `./output/` folder. It takes a bit of time to run if the shrink factor (or your original photo) is large. I have not yet tested it with RAW files, but I assume it works.

Make sure to clean your `./source` folder every time you finish framing a batch of photos!

## Miscellaneous

I tested this program with photos taken with my Panasonic LUMIX DC-G9, a camera Panasonic released in 2018. Please test on other models and let me know if there are bugs! 

So far, the bug I have noticed is that when the image is in portrait orientation, you should make sure you have a large enough `shink_factor` otherwise error will raise.


## Example
![example](./output/example.png)
