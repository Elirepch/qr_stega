import numpy as np
import qrcode
from PIL import Image, ImageDraw
'''
TODO:
complication of the encoding algorithm (specifically the summing of the rgba values)
to  
variable placing of the qr code on the image
'''

class Stega:
    def __init__(self, im_address, qr_text = "", mode="", output="output.png",x_pos = 0, y_pos = 0):
        """
        Initiallizes the variables and encodes,decodes or both
        with the corresponding codes(non case sensetive){e,d,b}.
        """
        self.output = output      
        self.im_address = im_address
        self.qr_text = qr_text
        self.mode = mode
        self.x_pos = x_pos
        self.y_pos = y_pos
  
        if self.qr_text is not None and self.mode == "E" or self.mode == "e":
            self.encode()
        elif self.qr_text is None and self.mode == "E" or self.mode == "e":
            raise Exception('"qr_text" argument has to be filled.')
        elif mode == "D" or mode == "d":
            self.decode()
        
    def create_qr(self):
        """
        creates the qr data and image, further research needs
        to be done on if the image is needed at all. will need refactoring.
        """
        self.qr_data = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=2,
                border=2
            )
        self.qr_data.add_data(self.qr_text)
        self.qr_data.make(fit=True)
        self.qr_img = self.qr_data.make_image(fill_color="black", back_color="white")
    
    def encode(self):
        """
        Embeds the qr code into the image using the following logic:
        If the current pixel in the qr code is black; then make sure
        the RGB sum of the image at that pixel is odd.
        else make sure its even.
        """
        # Load the data
        self.create_qr()
        self.img = Image.open(self.im_address)
        self.img_arr = np.array(self.img.getdata(),dtype = "uint8").reshape(self.img.size[0],self.img.size[1],4)
        
        self.qr_arr = np.array(self.qr_img.getdata()).reshape(self.qr_img.size[0],self.qr_img.size[1])

        img_proc = self.img_arr[self.x_pos: ,self.y_pos:]
        # Apply logic
         
        # Iterate over the x,y coordinates of the qr image
        for y in range(self.qr_arr.shape[1]):
            for x in range(self.qr_arr.shape[1]):
                # If the current coordinate in the qr code array
                # is black (False) then make sure the sum of the
                # current image cell is odd.
                # Otherwise make sure its even.
                if self.qr_arr[x][y] == 0:
                    if sum(img_proc[x][y]) % 2 == 0:
                        img_proc[x][y][0] += 1
                elif self.qr_arr[x][y] == 255:
                    if sum(img_proc[x][y]) % 2 == 1:
                        img_proc[x][y][0] -= 1 

        # Create a new image from the mutated array
        self.img = Image.fromarray(self.img_arr)
        # Save the file
        self.img.save(self.output,"PNG")


    def decode(self):
        """
	Decodes an image with that has a qr code embedded in it
        using the technique used in this program.
        for each pixel in the image it checks if its
	odd or even and draws a black or white pixel accordingly
	"""
        # Load data
        self.img = Image.open(self.im_address)
        self.img_arr = np.array(self.img.getdata(),dtype = "uint8").reshape(self.img.size[0],self.img.size[1],4)
        # Prepare to draw
        self.new = Image.new("L", self.img.size,(255))
        self.draw = ImageDraw.Draw(self.new)
        # Draw the decoded image
        for y in range(self.img_arr.shape[1]):
            for x in range(self.img_arr.shape[0]):
                if sum(self.img_arr[x][y]) % 2 == 1:
                    self.draw.point((x,y),(0))
                else:
                    pass
        self.new.save(self.output,"PNG")
