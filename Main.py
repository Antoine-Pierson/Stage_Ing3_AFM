from PIL import Image
import numpy as np
from PIL.TiffTags import TAGS

im = Image.open('Si__010.tiff')
im.show()
print(np.size(im))

imarray = np.array(im)
print(np.shape(imarray))

with Image.open('Si__010.tiff') as img:
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.iterkeys()}

