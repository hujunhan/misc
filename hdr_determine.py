import exifread
import logging
import PIL.Image
import PIL.ExifTags
# logging.basicConfig(level=logging.DEBUG)
hdr_image_path='/Volumes/Untitled/DCIM/100OLYMP/P2182290.JPG'
nor_image_path='/Volumes/Untitled/DCIM/100OLYMP/P2182239.JPG'
img = PIL.Image.open(nor_image_path)
exif_data = img._getexif()
exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}
for key in exif.keys():
    if 'Gain' in key:
        print(key,exif[key])
    # print(key,exif[key])
## Read out the exif data of image file
# with open(hdr_image_path, 'rb') as f1:
#     hdr_tags = exifread.process_file(f1)
#     with open(nor_image_path, 'rb') as f2:
#         nor_tags = exifread.process_file(f2)
#         for tag in nor_tags.keys():
#             if str(hdr_tags[tag])!=str(nor_tags[tag]):
#                 print("Key: %s, value %s" % (tag, hdr_tags[tag]))
#                 print("Key: %s, value %s" % (tag, nor_tags[tag]))
import glob
image_list=glob.glob('/Volumes/Untitled/DCIM/100OLYMP/*.JPG')
for path in image_list:
    img = PIL.Image.open(nor_image_path)
    exif_data = img._getexif()
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    for key in exif.keys():
        if 'Gain' in key:
            print(key,exif[key])