odoo.define('facture.loadView', function (require) {
'use strict';

var actionMag=require('web.actionManager')


actionMag.include({
_handleAction: function (action, options) {
            if (action.type === 'ir.actions.reload') {
                return this.reloadController();
            }
            return this._super(action, options);
        },
        reloadController: function (action, options) {
            this.getCurrentController().widget.reload();
            return $.when();
        },
});

})