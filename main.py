from PIL import ImageFilter,ImageEnhance,ExifTags,Image
from PIL import ImageDraw, ImageFont
from pillow_heif import register_heif_opener
from PIL.ExifTags import TAGS
import numpy as np
import os
from tqdm import tqdm

def processPhoto(im_name, shrink_f=0.6514, sourceFolder="./source/", outputFolder="./output/", suffix="_o"):
    # Path to the image or video
    imagename = im_name
    # Read the image data using PIL
    image = Image.open(sourceFolder + imagename)

    width = image.size[0]
    height = image.size[1]

    shrink_factor = shrink_f
    # Creating Shrinked New Image
    new_image = image.resize(np.array([int(width*shrink_factor),
                                    int(height*shrink_factor)]))
    new_size = new_image.size

    # Getting Photo Metadata
    img_exif = image.getexif()
    # Loop all exif and save to a dictionary
    exif_dict = {}
    for ifd_key, ifd_value in img_exif.get_ifd(ExifTags.Base.ExifOffset).items():

        ifd_tag_name = ExifTags.TAGS.get(ifd_key, ifd_key)
        exif_dict.update({f"{ifd_tag_name}": ifd_value})
    # Iterating over all EXIF data fields
    for tag_id in img_exif:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = img_exif.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        exif_dict.update({f"{tag}": data})
    
    # Creating New Canvas
    ## Scale relative to the shrinked image, I set it to be fixed
    ## Feel Free to change if needed
    # Creating New Canvas
    scale = np.array([1.15,1.35])
    portrait_factor = 1
    
    if width < height: 
        portrait_factor = 1.1
        scale = [1.15,1.30]

    canvas_size = [int(width*shrink_factor*scale[0]), int(height*shrink_factor*scale[1])]

    max_edge = max(canvas_size)

    canvas = Image.new('RGB', (canvas_size[0], canvas_size[1]), (255,255,219))

    # Creating background
    enlarged_image = image.resize((int(max_edge/height*width), max_edge))
    # Blurring background
    enlarged_image_blurred = enlarged_image.filter(ImageFilter.GaussianBlur(25))
    # Dimming Background
    enhancer = ImageEnhance.Brightness(enlarged_image_blurred)
    enlarged_image_blurred = enhancer.enhance(0.44)
    # crop image - (left, top, right, bottom)
    enlarged_size = enlarged_image_blurred.size

    left = 0
    right = canvas_size[0]
    top = (enlarged_size[1] - canvas_size[0])/2
    bottom = top + canvas_size[1]


    cropped = enlarged_image_blurred.crop((left, top, right, bottom))

    # Checking if the cropped background fits the canvas
    # print(list(cropped.size), canvas_size)
    if not list(cropped.size) == canvas_size: 
        pass
        # raise("False")

    # Pasting background
    canvas.paste(cropped)
    # Pasting image to wrap
    position = [int(canvas_size[0]/2 - new_size[0]/2),int((canvas_size[1]/2 - new_size[1]/2)*0.5)]
    canvas.paste(new_image, (position[0], position[1]))

    # Custom font style and font size
    # Custom font style and font size
    size1 = int(max(width*shrink_factor,height*shrink_factor)*(75/3376)*portrait_factor+0.5)
    size2 = int(60/75*size1*portrait_factor+0.5)
    size3 = int(260/75*size1*portrait_factor+0.5)

    # Fonts
    cmu_serif = ImageFont.truetype('./cmunui.ttf', size1)
    # cmu_bold = ImageFont.truetype('./cmunbx.ttf', 60)
    cmu_bold = ImageFont.truetype('./cmunsx.ttf', size2)
    cmu_tt = ImageFont.truetype('./cmuntt.ttf', size1)
    cmu_bold2 = ImageFont.truetype('./cmunbx.ttf',size3)
    charlottes = ImageFont.truetype('./Charlotte.otf',int(size3*0.75))

    # Setting Splitting
    split1 = int(80/75*size1*portrait_factor+0.5)
    split2 = int(100/75*size1*portrait_factor+0.5)
    split3 = int(split2*0.6*portrait_factor)

    text_top = np.array(position.copy()) + np.array([0,new_size[1]])

    # canvas.save(f"./output/{imagename[:-4]}_o_NO.png")

    # Adding texts
    canvas_draw = ImageDraw.Draw(canvas)
    # print(exif_dict["LensModel"])

    # Lens Model
    canvas_draw.text((text_top[0], text_top[1]+split3+split1), text = exif_dict["Make"] + " " + exif_dict["Model"], font=cmu_bold, fill =(255, 255, 255))
    # Camera Make
    canvas_draw.text((text_top[0], text_top[1]+split3+split1*2), text = exif_dict["LensModel"], font=cmu_bold, fill=(255, 255, 255))
    # Date & Time
    canvas_draw.text((text_top[0], text_top[1]+split3+split1*3), text = exif_dict["DateTimeOriginal"].replace(":", "-"), font=cmu_bold, fill=(255, 255, 255))

    w = int(split1/15+0.5)

    # Splitting Line
    canvas_draw.line(xy=[(text_top[0], text_top[1]+split3+split1*3+1.4*split2), 
                        (text_top[0]+int(13.5*split2), text_top[1]+split3+split1*3+1.4*split2)], 
                    width=w,
                    fill=(255, 255, 255))

    # Photo Parameters
    exposure_t = "1/"

    if float(exif_dict["ExposureTime"]) >= 1: 
        exposure_t = str(exif_dict["ExposureTime"])[:-2]
    else:
        exposure_t += str(int(1/exif_dict["ExposureTime"]))


    canvas_draw.text((text_top[0], text_top[1]+split3+split1*3+1.4*split2), 
                    text = "ISO " + str(exif_dict["ISOSpeedRatings"]) + " | " 
                    + "F" + str(exif_dict["FNumber"]) + " | " 
                    + exposure_t + " s" + " | "
                    + str(exif_dict["FocalLength"])[:-2] + " mm",
                    font=cmu_tt, fill =(255, 255, 255))

    # Logo Placeholder
    c_box = [(text_top[0] + width*shrink_factor, text_top[1] + int(1.5*split2)),
                (text_top[0] + width*shrink_factor, text_top[1] + int(5.5*split2)),
                (text_top[0] + width*shrink_factor - int(9*split2), text_top[1] + int(5.5*split2)),
                (text_top[0] + width*shrink_factor - int(9*split2), text_top[1] + int(1.5*split2))]

    placeholder = False
    sign = False

    if placeholder:
        canvas_draw.line(xy=[c_box[0], c_box[1]], width=w, fill=(255, 255, 255))
        canvas_draw.line(xy=[c_box[1], c_box[2]], width=w, fill=(255, 255, 255))
        canvas_draw.line(xy=[c_box[2], c_box[3]], width=w, fill=(255, 255, 255))
        canvas_draw.line(xy=[c_box[3], c_box[0]], width=w, fill=(255, 255, 255))

        canvas_draw.text(np.array(c_box[3]) + np.array([24,40]) , 
                        text = "LOGO",
                        font=cmu_bold2, fill =(255, 255, 255))
    elif sign:
        canvas_draw.text((np.array(c_box[2])[0] - 250, text_top[1]+200), 
                        text = "Suzutsuki-CH",
                        font=charlottes, fill =(255, 255, 255))
    # Saving the photo
    canvas.save(f"./output/{imagename[:-4]}_o.png")


def main():

    """    
    # Setting Source Directory
    print("Please enter the local path to your photos:")
    sourceFolder = input() + "/"

    # Setting Source Directory
    print("Please enter the local path to your desired output folder:")
    outputFolder = input() + "/"
    """

    register_heif_opener()

    sourceFolder="./source/"
    PhotoList = os.listdir(sourceFolder)
    PhotoList.remove('.DS_Store')

    print("Enter shrink factor (between 0 to 1): ")
    sf = float(input())

    print("Do you want to export all photos? (y/n)")
    all_export = input()

    if all_export.capitalize() == "Y":
        for im_name in tqdm(PhotoList):
            try:
                processPhoto(im_name, shrink_f=sf, sourceFolder="./source/", outputFolder="./output/", suffix="_o")
            except: 
                print(f"Unable to process: {im_name}")
                continue
            

    elif all_export.capitalize() == "N":
        print(f"Enter the index of number you want to process (0 to {str(len(PhotoList)-1)}):")
        idx = int(input())
        processPhoto(PhotoList[idx], shrink_f=sf, sourceFolder="./source/", outputFolder="./output/", suffix="_o")



if __name__ ==  '__main__':
    main()