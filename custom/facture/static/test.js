odoo.define('facture.test', function (require) {
'use strict';

var X,Y,HEIGHT,WIDTH,D;
var d;
var base64;
var saveElement=null;
var saveModel=null;
var deleteListe=[];
var basicController=require('web.BasicController')
var canLoad=true;
var saveTab=null;
let myGreatImage = null;
var refId;
var Widget = require('web.Widget');
var rpc = require('web.rpc');
var core = require('web.core');
var imageDisplay; //la grande image
var tableauDisplay;
var imageCropDisplay; // image cropped
var lienDisplay
var QWeb = core.qweb;
var test= Widget.extend({
    template: 'template_testjs',
    monTableau:null,
    cropper :null,
    listeFields:[],
    activeIndex:-1,
    events: {
        'change .imageodoo':'testimage',
        'change .inv_fildsListeSave':'saveFields',
        'change .inv_fildsChamp1':'saveChamp1',
        'change .inv_fildsChamp2':'saveChamp2',
        'click #cropButton':'cropImage',
        'click #cropTableButton':'cropTable',
         'click #btn-edit':'editRow',
         'click #btn-delete':'deleteRow',
        'click #myGreatImage':'processImage',
        'change #mySelect':'getField',
        'click #btn':'getField',

//        'click .selectFiled':'selectField'

    },

    init: function (parent, options) {
        imageDisplay=arguments[1].data.imageCode;
        imageCropDisplay= arguments[1].data.test;
        saveElement=null;
        deleteListe=[];
        refId=options.data.id

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

        this.loadDetail()




    var res = this._super.apply(this, arguments);
    return res;
    },

loadDetail:function(){
var self=this
        setTimeout(function(){
        if (canLoad){
              rpc.query({ async: false,
                                    model: "facture.fact",
                                    method: "getModelId",
                                    args: [refId] }).then(function(responce) {
                                    saveModel=responce
                                    self.getModel()
                                           if (saveModel){
                                  self._getField(saveModel).then(function(res){
                                  self.getDetails()
                                  })
//        }
}else
          self.getDetails()
                                    })
        }
        else{
         self.loadDetail()
        }

}, 1000);
},
selectField:function(event){
console.log(event)
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
    $('#uploadedImage').css({"border":"4px solid white"});
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
    str=JSON.stringify(str).toString()
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
    $('#cropButton').css({"display":"inline"});
    $('#cropTableButton').css({"display":"inline"});
    $('#uploadedImage').css({"border":"4px solid white "});
    this.cropper = new Cropper(document.getElementById('myGreatImage'), {
    crop(event ) {
       var detaille = event.detail
       detaille['field_id']=null
       detaille["id"]=null
       detaille["champ1"]=null
       detaille["champ2"]=null
       detaille["index"]=self.generateHash(detaille).toString()
       detaille.x= detaille.x.toFixed(2)
       detaille.y= detaille.y.toFixed(2)
       detaille.width=detaille.width.toFixed(2)
       detaille.height= detaille.height.toFixed(2)
        self.monTableau.push(detaille)
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

initCropper: async function(){
  return true
},

updateMap:function(map,mapValue){
var key=Object.keys(mapValue)
for(let i=0;i<key.length;i++){
if (!(map[key[i]] && key[i]=='id'))
map[key[i]]=mapValue[key[i]]
}
return map
},
//
cropTable:function(){
this._cropImage(1)
},

cropImage:function(){
this._cropImage(0)
},

_cropImage: function(isTable) {
    const imgurl = this.cropper.getCroppedCanvas().toDataURL();
    const img = document.createElement("img");
   console.log(this.cropper.getCropBoxData())
    if (this.activeIndex>=0){
    this.lastElement[this.activeIndex]=this.updateMap(this.lastElement[this.activeIndex],this.monTableau[this.monTableau.length-1])
//     this.lastElement[this.activeIndex]=this.monTableau[this.monTableau.length-1] ;
     this.activeIndex=-1
    }
    else{
    this.monTableau[this.monTableau.length-1]["isTable"]=isTable;
     this.lastElement.push(this.monTableau[this.monTableau.length-1]) ;
    }
    saveElement=this.lastElement
    console.table(this.lastElement);
    var index =this.lastElement.indexOf(D)
//    $('textarea[name=detaille]').val(JSON.stringify(this.lastElement)).change();
    img.src = imgurl;
    img.id="myGreatCropImage"
     var base64 = img.src
     .replace('data:', '')
     .replace(/^.+,/, '');
      $('textarea[name=test]').val(base64).change();
    document.getElementById("cropResult").appendChild(img);
    this.$el.find('#cropTable').html(QWeb.render("template_cropTableData",{lastElement: this.lastElement , fields:this.listeFields}));

},

renderField:function(){
this.$el.find('.inv_fieldListeSelect').html(QWeb.render("template_field",{fields: this.listeFields}));
},

_edit:function(ev){
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

 editRow: async function(ev) {
    var self=this;
    if(!this.cropper)
  {

    this.cropper = await new Cropper(document.getElementById('myGreatImage'), {
     crop(event ) {
       var detaille = event.detail
       detaille['field_id']=null
       detaille["id"]=null
       detaille["index"]=self.generateHash(detaille).toString()
        self.monTableau.push(detaille)
        D=event.detail
       event.detail.x= event.detail.x.toFixed(2)
       event.detail.y= event.detail.y.toFixed(2)
       event.detail.width=event.detail.width.toFixed(2)
       event.detail.height= event.detail.height.toFixed(2)
        X=event.detail.x
        Y=event.detail.y
        HEIGHT=event.detail.height
        WIDTH=event.detail.width
        const canvas = self.cropper.getCroppedCanvas();
        return (self.monTableau,X,Y,HEIGHT,WIDTH , D)
    },
  ready() {
     $('#cropButton').css({"display":"inline"});
     $('#cropTableButton').css({"display":"inline"});
     self._edit(ev)
  }
  })
  }
  else {
  this._edit(ev)
  }
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
  if (this.lastElement[index]['id'])
      deleteListe.push(this.lastElement[index]['id'])

this.lastElement= this.deleteFromListe(this.lastElement,parseInt(index))

  $(ev.currentTarget).parent().parent().remove()
    console.table(this.lastElement);
//        $('textarea[name=detaille]').val(JSON.stringify(this.lastElement)).change();
         saveElement=this.lastElement
         console.log(this.lastElement)
},

deleteFromListe: function(liste, index){
var newListe=[]
for( var i = 0; i < liste.length; i++){

        if ( i != index) {
          newListe.push(liste[i])

        }
    }
    return newListe
},
// invoice widget
renderCrop: function(data){
    this.$el.find('#cropResult').html(QWeb.render("template_imageCropRender", {widget: {image:data}}));

 },

testimage: function(e) {
//     console.log(e);
     this.getImage();
    },

HashData:function(data){
for (let i=0;i<data.length;i++){
 data[i]["index"]=this.generateHash(data[i]).toString()
}
return data
},
getDetails:function(){
       var self=this
       rpc.query({ async: false,
                                    model: "facture.details",
                                    method: "displayDetails",
                                    args: [refId] }).then(function(responce) {
                                    self.lastElement=self.HashData(responce)
                                    self.$el.find('#cropTable').html(QWeb.render("template_cropTableData",{lastElement: self.lastElement , fields:self.listeFields}));
                                    console.log(responce)
                                    })
},

getModel:function(){
    var self=this
      rpc.query({ async: false,
                                    model: "facture.fact",
                                    method: "getModel",
                                    args: [] }).then(function(responce) {
                                    self.$el.find('#modelData').html(QWeb.render("tamplate_model",{model: responce , model_id:saveModel}));
                                    console.log("save",saveModel)

                                    })
},


getField:function(){
      saveModel=parseInt(document.getElementById("mySelect").value)
      this._getField(saveModel)
},

_getField:async function(model_id){
    var self=this

      await rpc.query({ async: false,
                                    model: "facture.fact",
                                    method: "getField",
                                    args: [model_id] }).then(function(responce) {
                                    self.$el.find('#fieldsData').html(QWeb.render("template_field",{fields: responce}));
                                    console.log(responce)
                                    self.listeFields=responce
                                    self.renderField()
                                    })

                                    return true
},

saveFields:function(ev){
  var id=$(ev.currentTarget).parent().parent().parent().attr('id')
    var index=this.getIndex(this.lastElement,"index" , id)
    this.lastElement[index]['field_id']=parseInt($(ev.currentTarget).val())
//     $('textarea[name=detaille]').val(JSON.stringify(this.lastElement)).change();
     saveElement=this.lastElement

},

saveChamp1:function(ev){
  var id=$(ev.currentTarget).parent().parent().attr('id')
    var index=this.getIndex(this.lastElement,"index" , id)
    this.lastElement[index]['champ1']=$(ev.currentTarget).val()
//     $('textarea[name=detaille]').val(JSON.stringify(this.lastElement)).change();
     saveElement=this.lastElement
     console.log(saveElement)
},

saveChamp2:function(ev){
  var id=$(ev.currentTarget).parent().parent().attr('id')
    var index=this.getIndex(this.lastElement,"index" , id)
    this.lastElement[index]['champ2']=$(ev.currentTarget).val()
//     $('textarea[name=detaille]').val(JSON.stringify(this.lastElement)).change();
     saveElement=this.lastElement
     console.log(saveElement)

},


});

require('web.widget_registry').add("template_testjs", test);


basicController.include({
 _saveRecord: function(recordID, options) {
 console.log("save record")
            if (this.modelName=='facture.fact'){

            recordID = recordID || this.handle;
            options = _.defaults(options || {}, {
                stayInEdit: false,
                reload: true,
                savePoint: false,
            });
            if (this.canBeSaved(recordID)) {
                var self = this;
                var saveDef = this.model.save(recordID, {
                    reload: options.reload,
                    savePoint: options.savePoint,
                    viewType: options.viewType,
                });
                if (!options.stayInEdit) {
                    saveDef = saveDef.then(function(fieldNames) {
                        var def =  self._confirmSave(recordID);
                        return def.then(function() {
                            return fieldNames;
                        });
                    });
                }
                return saveDef;
            } else {
                return Promise.reject("SaveRecord: this.canBeSave is false");
            }
            }
            else{
            return  this._super.apply(this, arguments);
            }
        },

});

var core = require('web.core');
var FormController = require('web.FormController');
FormController.include({
// renderTab: function(data){
//    this.$el.find('#cropTable').html(QWeb.render("template_cropTableData", data));
// },
    init: function () {
        this._super.apply(this, arguments);
    },

    _barcodeRecordFilter: function (candidate, barcode, activeBarcode) {
        return candidate.data.product_barcode === barcode;
    },

   _onSave: function (ev) {
//            console.log("onsave ")
//            console.log("helo" ,saveElement)
//     console.log(d.__parentedParent.state.id)
//console.log(lastElement)
         return this._super.apply(this, arguments);

    },
    _confirmSave: function (id) {
    console.log("on confirme save")
    var record = this.model.get(this.handle);
//      console.log(record)
//   var p=document.getElementById("cropTable")
    if(record.model=="facture.fact"){
    canLoad=false
       var _saveModel=saveModel
       rpc.query({ async: false,
                                    model: "facture.fact",
                                    method: "createDetails",
                                    args: [saveElement,saveModel,deleteListe,record.res_id] }).then(function(responce) {console.log(responce)
                                      canLoad=true
                                    saveModel=_saveModel

                                    })

                                    saveElement=null;
                                    deleteListe=[];


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


