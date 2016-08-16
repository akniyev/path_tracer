from PIL import Image, ImageFilter

im = Image.open("image.jpg")

im.show()

im_sharp = im.filter(ImageFilter.SHARPEN)

im_sharp.save('image_sharpened.jpg', 'JPEG')

im_sharp.show()

r,g,b = im_sharp.split()

exif_data = im._getexif()

exif_data