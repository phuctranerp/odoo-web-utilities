odoo.define('website.get_fshare_link', function (require) {
    'use strict';
    
    var Dialog = require('web.Dialog');
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.GetFsharePage = publicWidget.Widget.extend({
        selector: '#wrapwrap',
    
        events: {
            'click .btn-get-link-fshare': '_action_get_fshare_link'
        },
    
        start: function () {
            return this._super.apply(this, arguments);
        },
        
        _action_get_fshare_link: function() {
            console.log("OK");
            var fshare_link = $("#txt_source_fshare_link").val();
            $(".btn-get-link-fshare").attr("disabled", true);

            if (!!fshare_link) {
                $("#txt_dest_fshare_link").val("Getting link. Please wait.....");

                $.ajax(
                   {
                      type:'GET',
                      url:'/get_fshare_direct_link',
                      data:"url=" + fshare_link,
                      success: function(data){
                            $("#txt_dest_fshare_link").val(data);
                      },
                      error: function(error) {
                            Dialog.alert(this, "Unable to get the link");
                      },
                      timeout: 60000
                   }
                ).always(function(){
                    console.log("done");
                    $('.btn-get-link-fshare').removeAttr("disabled");
                });
            } else {
                Dialog.alert(this, "Enter fshare link to get direct link");
            }
        }
        
    })
    });
    
    