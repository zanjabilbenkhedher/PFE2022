# -*- coding: utf-8 -*-
from odoo import api, fields, models
import js2py
from PIL import Image
import pytesseract
import base64
from io import BytesIO
from deep_translator import GoogleTranslator
import pdftables_api
import xml.etree.cElementTree as ET
import os
from odoo.modules import get_module_resource
import xml.etree.ElementTree as ET
import json
from xml.etree.ElementTree import XML, fromstring
import re

class FactureFact(models.Model):
    _name = 'facture.fact'
    fournisseur = fields.Char("Name")
    date = fields.Date("Date")
    montantT = fields.Float("MT")
    reference = fields.Char("Reference")
    tranText = fields.Text("Text")
    SELECTION_LIST = [
        ('fr', 'français'),
        ('en', 'anglais'),
        ('ar', 'arabe')
    ]
    lang = fields.Selection(SELECTION_LIST, default=SELECTION_LIST[1][0], string="langue")
    Facture_image = fields.Image(string="Upload Facture Image", max_widh=2000, max_height=2000)
    prescription = fields.Text(string="Prescription")
    OtherInfo = fields.Text(string="info")

    def displayFacture(self):
        for i in self:
            i.display_facture_image = i.Facture_image
            # Create file which has the image code
            #byte = i.display_facture_image
            #  f = open('output.bin', 'wb')
            # f.write(byte)
            # Convert the code to image
            # file = open('output.bin', 'rb')
            # byteform = file.read()
            #  file.close()
            # fh = open('images/verification.png', 'wb')
            #  fh.write(base64.b64decode(byteform))
            #  fh.close()
            # Convert image to text
            # image = 'images/verification.png'
            # Convert pdf to xml
            #c = pdftables_api.Client('d3zqhuckvngq')
            #c.xml('File/modele_de_facture.pdf', 'output')


            #tree = ET.ElementTree(file='output.xml')
            #root = tree.getroot()
            #for chld in root:
                #if(chld.tag=='page'):
                    #for table in chld:
                        #for tr in table:
                            #for td in tr:
                                #if(td.tag=='td' and td.text!=None):
                                    #x = re.findall("\d\d[-/]\d\d[-/]\d{2,4}",td.text)
                                    #print(x)


    display_facture_image = fields.Image(compute=displayFacture)


    @api.onchange('Facture_image')
    def _onchange_field(self):
        for i in self:
            i.display_facture_image = i.Facture_image

    def translate(self, text, langue='en'):
        # translate text to english
        translated = GoogleTranslator(source='auto', target=langue).translate(text)
        return translated

    def readText(self):
        text = pytesseract.image_to_string(Image.open(BytesIO(base64.b64decode(self.display_facture_image))),
                                           lang="eng")
        self.write({"tranText": self.translate(text, self.lang)})


    @api.model
    def testjs(self , num , ref):
        #a=self.env['facture.fact'].browse(num)
        b=self.env['facture.fact'].search([], limit=1)
        return{
            'name': num,
            'name2': b.reference
        }






