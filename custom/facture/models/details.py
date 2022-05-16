from odoo import api, fields, models
from PIL import Image  # import pillow library (can install with "pip install pillow")
import pytesseract
from io import BytesIO
import io
import base64
import numpy as gfg
class FactureDetails(models.Model):
    _name = 'facture.details'
    facture_id = fields.Many2one(comodel_name='facture.fact')
    tableModel_id = fields.Many2one(comodel_name='facture.fact')
    model_id = fields.Many2one(comodel_name='ir.model')
    field_id = fields.Many2one(comodel_name='ir.model.fields')
    x = fields.Float("X")
    y = fields.Float("Y")
    height = fields.Float("Height")
    width = fields.Float("Width")
    champ1= fields.Text('champ1')
    champ2=fields.Text("champ2")
    isTable = fields.Boolean(default=False)
    cropimg = fields.Image("Crop Image ")
    last_date = fields.Date(string='last_create', default=fields.Date.today(), required=True, copy=False)

    # cropper l'image selon data(x,y,height,width) et extraction de text avec pytesseract
    def cropImage(self, base64Image, data):

        im = Image.open(BytesIO(base64.b64decode(base64Image)))
        im = im.crop(data)
        # if self.isTable:
        #     return str(gfg.asarray(im))
        result=False
        try:
            result = pytesseract.image_to_string(im, lang="eng")
            if self.champ2 and "result" in self.champ2:
                result=eval(self.champ2)
            if self.champ1:
                result=repr(result).split(self.champ1)
            if self.champ2 and "item" in self.champ2 and type(result) is list:
                for i in range(0,len(result)):
                    item=result[i]
                    result[i]=eval(self.champ2)
        except:
            result = False
        return result

    def get_cropped_image(self, base64Image, data):
        im = Image.open(BytesIO(base64.b64decode(base64Image)))
        im = im.crop(data)
        return im

    # faire une boucle pour chaque image cropper
    def newTest(self):
        for i in self:
            if i.facture_id.imageCode:
                text = i.cropImage(i.facture_id.imageCode, (i.x, i.y, i.width+i.x,i.height+i.y))
                i.extraction_text = text

    extraction_text = fields.Text(compute=newTest, string="Text Extraction")

    def readText(self , img):
        if not self.isTable:
            text = self.cropImage(img, (self.x, self.y, self.width + self.x, self.height + self.y))
        else:
            self.env['create.facture.wizard'].create({
                'uploadedFacture':self.get_cropped_image(img, (self.x, self.y, self.width + self.x, self.height + self.y))

            }).read_by_model(self.tableModel_id)

        return text



    # display de l'image cropper (decoder le base64)
    def solvedPictureSize(self, binaryImg, data):
        if binaryImg:
            image = Image.open(BytesIO(base64.b64decode(binaryImg)))
            new_image = image.crop(data)
            output = io.BytesIO()
            if new_image.mode == "RGB":
                new_image.save(output, format='JPEG')
            elif new_image.mode in ["RGBA", "P"]:
                new_image.save(output, format='PNG')

            return base64.b64encode(output.getvalue())

        return False





    # faire une boucle pour chaque image cropper
    def dataImage(self):
        for i in self:
            i.display_image = i.solvedPictureSize(i.facture_id.imageCode, (i.x, i.y, i.width+i.x,i.height+i.y))

    display_image = fields.Image("Image", compute=dataImage )

    @api.model
    def displayDetails(self,facture_id):
        liste = []
        if facture_id:
            search = self.env['facture.details'].search([('facture_id', '=', facture_id)])
            for i in search:
                liste.append({
                    'x': i.x,
                    'y': i.y,
                    'width': i.width,
                    'height': i.height,
                    'champ1': i.champ1,
                    'champ2': i.champ2,
                    'isTable':i.isTable,
                    'id': i.id,
                    'field_id':i.field_id.id,
                })

        return liste

    def _cropImage(self ,base64Image,data):
        if base64Image:
            img = Image.open(BytesIO(base64.b64decode(base64Image)))
            img = img.crop(data)
            output = io.BytesIO()
            if img.mode == "RGB":
                img.save(output, format='JPEG')
            elif img.mode in ["RGBA", "P"]:
                img.save(output, format='PNG')

            return base64.b64encode(output.getvalue())

        return False