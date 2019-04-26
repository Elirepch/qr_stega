from PIL import Image, ImageDraw

"""
TODO:ADD AUTOMATIC QR CODE DOWNLOADER
     ADD SUPPORT FOR PHOTOS BIGGER THAN 150x150
     ADD REGION SELECTION FOR PHOTOS BIGGER THAN 150x150
     ADD DOCUMENTATION
     REFACTOR FOR CLASSES

"""
class Stega:
    def __init__(self,address):
        self.imgqr = Image.open(address)
    def remove_bg(self):
        self.imgqr = self.imgqr.convert("RGBA")
        datas = self.imgqr.getdata()

        new_data = []

        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_data.append((255,255,255,0))
            else:
                new_data.append(item)
        self.imgqr.putdata(new_data)
        self.imgqr.save("qr.png","PNG")

    def encode(self,address_img,coords = (0,0,150,150)):
        img = Image.open(address_img)
        self.imgqr = self.imgqr.remove_bg()
        img = img.convert("RGBA")
        img_data = img.getdata()
        qr_data = self.imgqr.getdata()

        if img.size[0] < 150 or img.size[1] < 150:
            raise Exception("Photo is smaller than 150x150.\n Please use a photo with larger dimensions.") 
        lst = [list(elem) for elem in img_data]
        for i in range(len(img_data)):
            if qr_data[i][0] == 0:
                if sum(lst[i])%2 == 0:
                    lst[i][0] += 1
            if qr_data[i][0] != 0:
                if sum(lst[i])%2 == 1:
                    lst[i][0] += 1
        new_data = [tuple(elem) for elem in lst]
        img.putdata(new_data)
        try:
            if img_full is not None:
                img = img_full.paste(img,coords)
                img.save("stega.png","PNG")
        except NameError:
            img.save("stega.png","PNG")

    def decode(self,address_img):
        img = Image.open(address_img)
        img_data = img.getdata()
        x = 0
        y = 0
        new = Image.new("RGBA",(150,150),(255,255,255,255))
        draw = ImageDraw.Draw(new)
        lst = []
        for item in img_data:
            lst.append(sum(item))
        for item in lst:
            if item % 2 == 1:
                draw.point((x,y),(0,0,0,255))
            else:
                pass
            if x < 149:
                x += 1
            else:
                y += 1
                x = 0
        new.save("decoded.png","PNG")
x = Stega("qrcode.png")
x.remove_bg()
x.encode("ad.jpg")
x.decode("stega.png")