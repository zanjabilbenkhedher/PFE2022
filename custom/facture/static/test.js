odoo.define('facture.test', function (require) {
'use strict';

var X,Y,HEIGHT,WIDTH,D;
var base64;
var saveElement=null;
let myGreatImage = null;
var Widget = require('web.Widget');
var rpc = require('web.rpc');
var core = require('web.core');
var imageDisplay; //la grande image
var imageCropDisplay; // image cropped
var tableauDisplay;
var lienDisplay
var QWeb = core.qweb;
var test= Widget.extend({
    template: 'template_testjs',
    lastElement:[],
    monTableau:null,
    cropper :null,
    activeIndex:-1,
    events: {
        'change .imageodoo':'testimage',
        'click #cropButton':'cropImage',
         'click #btn-edit':'editRow',
         'click #btn-delete':'deleteRow',
        'click #myGreatImage':'processImage',

    },

    init: function (parent, options) {
        imageDisplay=arguments[1].data.imageCode;
        imageCropDisplay= arguments[1].data.test
             saveElement=null;

        this._super.apply(this, arguments);
    },

    start: function () {
        var self = this;
        this.monTableau=new Array();
        this.lastElement=new Array();


         //save invoice (Display invoice in the widget)
         if(imageDisplay){
        this.renderImage(imageDisplay);
        }
        if(imageCropDisplay){
        this.renderCrop(imageCropDisplay)
        }


    var res = this._super.apply(this, arguments);
    return res;
    },

// upload and display invoice
getImage:function() {
     var self=this;
     var files=document.getElementById('imageodoo');
     console.log("images", files);
     const imageToProcess = files;
     var reader = new FileReader();
     reader.readAsDataURL(files.files[0]);
     reader.onload = function () {
     const base64String = reader.result
     .replace('data:', '')
     .replace(/^.+,/, '');

    $('textarea[name=imageCode]').val(base64String).change()
	// display uploaded image
    let newImg = new Image(200, 200);
    newImg.src = reader.result;
    newImg.id = "myGreatImage";
    self.renderImage(base64String);
    $('#uploadedImage').css({"border":"4px solid #7C7BAD"});
    self.processImage();
};
    reader.onerror = function (error) {
	console.log('Error: ', error);
};
},

// invoice widget
renderImage: function(data){
    this.$el.find('#uploadedImage').html(QWeb.render("template_imageRender", {widget: {image:data}}));
 },

 generateHash:function(str, asString, seed) {
    /*jshint bitwise:false */
    var i, l,
        hval = (seed === undefined) ? 0x811c9dc5 : seed;

    for (i = 0, l = str.length; i < l; i++) {
        hval ^= str.charCodeAt(i);
        hval += (hval << 1) + (hval << 4) + (hval << 7) + (hval << 8) + (hval << 24);
    }
    if( asString ){
        // Convert to 8 digit hex string
        return ("0000000" + (hval >>> 0).toString(16)).substr(-8);
    }
    return hval >>> 0;
},

getIndex:function(liste, key,value){
for(let i=0;i<liste.length;i++){
if(liste[i][key]==value){
return i
}
}
return -1
},

// selectioner les zones , crop image , detailles dans un tableau
 processImage: function() {
    var self=this;
    $('#cropButton').css({"display":"block"});
    this.cropper = new Cropper(document.getElementById('myGreatImage'), {
    crop(event ) {
       var detaille = event.detail
       detaille["id"]=null
       detaille["index"]=self.generateHash(event.detail.toString()).toString()
        self.monTableau.push(event.detail)
        D=event.detail
        X=event.detail.x
        Y=event.detail.y
        HEIGHT=event.detail.height
        WIDTH=event.detail.width
        const canvas = self.cropper.getCroppedCanvas();
        return (self.monTableau,X,Y,HEIGHT,WIDTH , D)
    }
  }
  )
},

//
cropImage: function() {
    const imgurl = this.cropper.getCroppedCanvas().toDataURL();
    const img = document.createElement("img");
   console.log(this.cropper.getCropBoxData())
    if (this.activeIndex>=0){
     this.lastElement[this.activeIndex]=this.monTableau[this.monTableau.length-1] ;
     this.activeIndex=-1
    }
    else{
     this.lastElement.push(this.monTableau[this.monTableau.length-1]) ;
    }
    saveElement=this.lastElement
    console.table(this.lastElement);
    var index =this.lastElement.indexOf(D)
    $('textarea[name=detaille]').val(JSON.stringify(this.lastElement)).change();
    img.src = imgurl;
    img.id="myGreatCropImage"
     var base64 = img.src
     .replace('data:', '')
     .replace(/^.+,/, '');
      $('textarea[name=test]').val(base64).change();
    document.getElementById("cropResult").appendChild(img);
    this.$el.find('#cropTable').html(QWeb.render("template_cropTableData", this));
},

 editRow: function(ev) {
    var self=this;
    var id=$(ev.currentTarget).parent().parent().attr('id')
    var index=this.getIndex(this.lastElement,"index" , id)
    var data={
    left:(this.lastElement[index].x*this.getEchelleWidth())+this.cropper.canvasData.left,
    top:(this.lastElement[index].y*this.getEchelleHeight())+this.cropper.canvasData.top,
    width:this.lastElement[index].width*this.getEchelleWidth(),
    height:this.lastElement[index].height*this.getEchelleHeight(),
    }
   console.log(data)
    this.cropper.setCropBoxData(
    data
    )
    this.activeIndex=index
},

getEchelleWidth:function(){
return this.cropper.canvasData.width/this.cropper.canvasData.naturalWidth
},

getEchelleHeight:function(){
return this.cropper.canvasData.height/this.cropper.canvasData.naturalHeight
},


deleteRow: function (ev) {
  var id=$(ev.currentTarget).parent().parent().attr('id')
  var index=this.getIndex(this.lastElement,"index" , id)
 this.deleteFromListe(this.lastElement,parseInt(index))
  $(ev.currentTarget).parent().parent().remove()
    console.table(this.lastElement);
},

deleteFromListe: function(liste, index){
for( var i = 0; i < liste.length; i++){

        if ( i == index) {
            liste.splice(i, 1);
            i--;
        }
    }
    return liste
},
// invoice widget
renderCrop: function(data){
    this.$el.find('#cropResult').html(QWeb.render("template_imageCropRender", {widget: {image:data}}));

 },

testimage: function(e) {
//     console.log(e);
     this.getImage();
    }
});

require('web.widget_registry').add("template_testjs", test);



var core = require('web.core');
var FormController = require('web.FormController');
FormController.include({
    init: function () {
        this._super.apply(this, arguments);
    },

    _barcodeRecordFilter: function (candidate, barcode, activeBarcode) {
        return candidate.data.product_barcode === barcode;
    },

   _onSave: function (ev) {
          console.log(this)
          console.log("on save")
          this._super.apply(this, arguments);

    },
    _confirmSave: function (id) {
    console.log("on confirme save")
    var record = this.model.get(this.handle);
    console.log(record)
    if(record.model=="facture.fact"){
       rpc.query({ async: false,
                                    model: "facture.fact",
                                    method: "createDetails",
                                    args: [saveElement,record.res_id] }).then(function(responce){console.log(responce)})
                                    saveElement=null;
    }

    return this._super.apply(this, arguments)

    },
_onCreate: function () {
        this.createRecord();
        console.log("create")
    },

    _onButtonClicked: function (ev) {
     console.log(ev)
     return this._super.apply(this, arguments)
    }
});
});


