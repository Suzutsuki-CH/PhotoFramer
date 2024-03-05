# Suzutsuki's PhotoFramer :camera:

My photo-framer helps you automatically frame your photo and embed camera parameters to output photo.

## Dependency

You will need to install `PIL`, `numpy`, `tqdm`, and `os` to run this program. 

**Important**: Your photo must have **exif data** for this program to function properly.

## How to use?

You are supposed to run the `main.py` file in your terminal. You will be asked to provide values for the following parameters:
* `shrink_factor`: float between 0-1 (actually anything works), meaning your photo will be resized during the framing process. A prompt of `"Enter shrink factor (between 0 to 1)"` will pop up when you execute the program.
* `all_export`: y/n, if you want to export all photos in the source folder, a prompt of `Do you want to export all photos? (y/n)` will pop up in the terminal after entering shrink factor.
* `idx`: if you answered n/N to the previous question, you will be prompted to enter the index of the photo you want to process, whe range will be given.

**By Defalut**, the program will only read photos one put in the `./source` folder, and output will be places in the `./output` folder, but feel free to modify the code to fit your preference! 

Ideally, you should move your photo compilation to the `./source` folder, and execute the `main.py` file. After everything finishes, you will be able to see the output in the `./output/` folder. It takes a bit time to run if the shrink factor (or your original photo) is large. I have not yet tested it with raw files, but I assume it works. 

Make sure to clean your `./source` folder every time you finish framing a batch of photos!

##  Miscellaneous
I tested this program with photos taken with my Panasonic LUMIX DC-G9, a camera Panasonic released in 2018. Please test on other models and let me know if there are bugs!
