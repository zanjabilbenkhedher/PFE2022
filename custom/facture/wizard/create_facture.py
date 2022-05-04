from odoo import api, fields, models, _
from io import BytesIO
import base64
from PIL import Image,ImageChops,ImageDraw
import cv2
from pytesseract import pytesseract
from pytesseract import Output
from io import BytesIO
import io

class CreateFactureWiz(models.TransientModel):
    _name = 'create.facture.wizard'
    _description = "Create invoice  wizard"
    uploadedFacture = fields.Image(string='Upload Your File')
    invoice_id = fields.Many2one('facture.fact', string="invoice" )
    model = fields.Many2one('facture.fact', string="Model", )
    # i1 = Image.open(BytesIO(base64.b64decode(self.uploadedFacture)))
    imageCode = fields.Text('imageCode')
    activity_id = fields.Many2one('facture.model.activity', string="invoice")

    def displayFacture(self):
        for i in self:
            i.display_facture_image = i.uploadedFacture

    display_facture_image = fields.Image(compute=displayFacture)

    @api.onchange('Facture_image')
    def _onchange_field(self):
        for i in self:
            i.display_facture_image = i.uploadedFacture

    display_facture_image = fields.Image(compute=displayFacture)


    @api.onchange('uploadedFacture')
    def _onchange_field(self):
        for i in self:
            i.display_facture_image = i.uploadedFacture

    def action_create_invoice(self):
        vals = {
            'fournisseur': self.invoice_id.fournisseur,
            'fournisseur' : self.fournisseur,
            'imageCode': self.invoice_id.imageCode,
            'imageCode': self.uploadedFacture


        }
        facture_rec = self.env['facture.fact'].create(vals)
        print("facture", facture_rec.id)
        # return {
        #     'name': _('facture'),
        #     'type' : 'ir.action.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'facture.fact',
        #     'res_id': facture_rec.id
        # }

    def compare(self, img1 , img2):
        if img1 and img2:
            i1 = Image.open(BytesIO(base64.b64decode(img1)))
            i1 = i1.resize((500, 500), Image.ANTIALIAS)
            i2 = Image.open(BytesIO(base64.b64decode(img2)))
            i2 = i2.resize((500, 500), Image.ANTIALIAS)
            # print(self.uploadedFacture)
            # assert i1.mode == i2.mode, "Different kinds of images."
            # assert i1.size == i2.size, "Different sizes."

            pairs = zip(i1.getdata(), i2.getdata())
            if len(i1.getbands()) == 1:
                # for gray-scale jpegs
                dif=0
                for p1,p2 in pairs:
                    if not p1 is list and not p1 is tuple:
                        p1=[p1]
                    val=zip(p1,p2)
                    if val :
                        for c1,c2 in val:
                            dif+=abs(c1-c2)
                # dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))
            else:
                dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

            ncomponents = i1.size[0] * i1.size[1] * 3
            print("Difference (percentage):", (dif / 255.0 * 100) / ncomponents)
            return (dif / 255.0 * 100) / ncomponents

        return False


    def comparaison(self):
        if self.uploadedFacture and self.uploadedFacture2:
            self.compare(self.uploadedFacture, self.uploadedFacture2)


    def draw_rectangle(self , w , h , img , x , y):
        shape = [(x, y), (w+x, h+y)]
        draw = ImageDraw.Draw(img)
        draw.rectangle(shape, fill=200)
        return img

    def model_zoning(self , model , image):
        if image:
            img = Image.open(BytesIO(base64.b64decode(image)))
            if model.detail_ids:
                for d in model.detail_ids:
                    img = self.draw_rectangle(d.width, d.height, img, d.x, d.y)

            output = io.BytesIO()
            if img.mode == "RGB":
                img.save(output, format='JPEG')
            elif img.mode in ["RGBA", "P"]:
                img.save(output, format='PNG')

            model.write({"codeZoning": base64.b64encode(output.getvalue())})

            return base64.b64encode(output.getvalue())

        return False

    def zoning(self):
        self.model_zoning(self.model , self.model.imageCode)

    def find_model(self, img):
        model = self.env['facture.fact'].search([])
        min = -1
        model_min = False
        ICPSudo = self.env['ir.config_parameter'].sudo()
        pourcentages = ICPSudo.get_param('facture.pourcentage')
        for m in model:
            im1 = self.model_zoning(m, m.imageCode)
            im2 = self.model_zoning(m, img)
            if im1 and im2:


                valeur = self.compare(im1, im2)
                if float(pourcentages)> valeur:
                    if min == -1:
                        min = valeur
                        model_min = m
                    elif valeur < min:
                        min = valeur
                        model_min = m


        print(model_min)
        print(min)
        return  model_min,min

    def read_model(self):
        liste = {

        }
        res = False
        model,compareValue = self.find_model(self.uploadedFacture)

        if model:
            for i in model.detail_ids:
                liste[i.field_id.name] = i.readText(self.uploadedFacture)

            res=self.env[model.model_id.model].create(liste)
        self.env['facture.model.activity'].create({
                'invoicemodel_id':model.id if model else False,
                'model_id': model.model_id.id if model else False,
                'res_id': res.id if model else False,
                'compare': compareValue if model else False,
                'showImage':self.uploadedFacture,
                'state':'validate' if model else 'progress'

        })

        print(liste)
    def zoning2(self):
        # i1 = Image.open(BytesIO(base64.b64encode(self.uploadedFacture)))
        img = cv2.imread("images/facture.png")
        print(img)
        image_data = pytesseract.image_to_data(img, output_type=Output.DICT)
        for i, word in enumerate(image_data['text']):
            if word != "":
                x, y, w, h = image_data['left'][i], image_data['top'][i], image_data['width'][i], image_data['height'][
                    i]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
                # print(word)
                # cv2.putText(img,word,(x,y-16), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
        cv2.imshow("window", img)
        cv2.waitKey(0)


    def action_create_facture(self):
        print("button is created")
        i1 = Image.open(BytesIO(base64.b64decode(self.uploadedFacture)))

        i1 = i1.resize((500, 500), Image.ANTIALIAS)

        i2 = Image.open(BytesIO(base64.b64decode(self.uploadedFacture2)))

        i2 = i2.resize((500, 500), Image.ANTIALIAS)

        # assert i1.mode == i2.mode, "Different kinds of images."
        # assert i1.size == i2.size, "Different sizes."
        #
        # pairs = zip(i1.getdata(), i2.getdata())
        # if len(i1.getbands()) == 1:
        #     # for gray-scale jpegs
        #     dif = sum(abs(p1 - p2) for p1, p2 in pairs)
        # else:
        #     dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))
        #
        # ncomponents = i1.size[0] * i1.size[1] * 3
        # print("Difference (percentage):", (dif / 255.0 * 100) / ncomponents)


        # def comparaison2(self):
        #     i1 = Image.open(BytesIO(base64.b64decode(self.uploadedFacture)))
        #
        #     i1 = i1.resize((500, 500), Image.ANTIALIAS)
        #
        #     i2 = Image.open(BytesIO(base64.b64decode(self.uploadedFacture2)))
        #
        #     i2 = i2.resize((500, 500), Image.ANTIALIAS)
        #     diff = ImageChops.difference(i1, i2)
        #     if diff.getbbox():
        #         diff.show()





    # @api.onchange('uploadedFacture')
    # def action_create_facture(self,tab):
    #     if self.uploadedFacture:
    #         tab = []
    #         tab.append([
    #             0, 0, {
    #                 'fournisseur': 'uploadedFacture',
    #             }
    #         ])
    #
    #     self.invoice_id = tab

        # self.uploadedFacture=self.uploadedFacture
        # self.invoice_id = self.uploadedFacture