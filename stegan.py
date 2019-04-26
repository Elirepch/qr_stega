import numpy as np
import qrcode
from PIL import Image, ImageDraw


class Stega:
    def __init__(self, im_address, qr_text = "", mode = ""):
        """
        Initiallizes the variables and encodes,decodes or both
        with the corresponding codes(non case sensetive){e,d,b}.
        """
        self.im_address = im_address
        self.qr_text = qr_text
        if self.qr_text is not None and mode == "E" or mode == "e":
            self.encode()
        elif self.qr_text is None and mode == "E" or mode == "e":
            raise Exception('"qr_text" argument has to be filled.')
        elif mode == "D" or mode == "d":
            self.decode()
        
    def create_qr(self):
        """
        creates the qr data and image, further research needs
        to be done on if the image is needed at all. will need refactoring.
        """
        self.qr_data = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=2,
                border=2
            )
        self.qr_data.add_data(self.qr_text)
        self.qr_data.make(fit=True)
        self.qr_img = self.qr_data.make_image(fill_color="black", back_color="white")
    
    def encode(self):
        """
        Embeds qr code inside of image using the following logic:
        For each of the pixels in qr, if the pixel in qr is black
        make sure the corresponding r,g,b sum of the pixel in the image is odd
        otherwise make sure it's even.
        For example if we stumble upon a black pixel in the qr code
        and the image's rgb sum is 300, then add one.
        If the pixel were white we would move to the next pixel.
        """
        # Load the data
        self.create_qr()
        self.img = Image.open(self.im_address)
        self.img_arr = np.array(self.img.getdata(),dtype = "uint8").reshape(self.img.size[0],self.img.size[1],4)
        self.qr_arr = np.array(self.qr_img.getdata()).reshape(self.qr_img.size[0],self.qr_img.size[1])

        # Apply logic
        
        # Iterate over the x,y coordinates of the qr image
        for y in range(self.qr_arr.shape[1]):
            for x in range(self.qr_arr.shape[0]):
                # If the current coordinate in the qr code array
                # is black (False) then make sure the sum of the
                # current image cell is odd.
                # Otherwise make sure its even.
                if self.qr_arr[x][y] == 0:
                    if sum(self.img_arr[x][y]) % 2 == 0:
                        self.img_arr[x][y][0] += 1
                elif self.qr_arr[x][y] == 255:
                    if sum(self.img_arr[x][y]) % 2 == 1:
                        self.img_arr[x][y][0] -= 1

        # Create a new image from the mutated array
        self.img = Image.fromarray(self.img_arr)
        # Save the file
        self.img.save('stega.png',"PNG")

    def decode(self):
        # Load data
        self.img = Image.open(self.im_address)
        self.img_arr = np.array(self.img.getdata(),dtype = "uint8").reshape(self.img.size[0],self.img.size[1],4)
        # Prepare to draw
        self.new = Image.new("L", self.img.size,(255))
        self.draw = ImageDraw.Draw(self.new)
        
        for x in range(self.img_arr.shape[1]):
            for y in range(self.img_arr.shape[0]):
                if sum(self.img_arr[x][y]) % 2 == 1:
                    self.draw.point((x,y),(0))
                else:
                    pass
        self.new.save("decoded.png","PNG")

x = Stega("flower.png", "Steganography","E")
y = Stega("stega.png", mode = "D")
