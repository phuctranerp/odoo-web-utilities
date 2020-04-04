odoo.define('website.fshare_giveaway', function (require) {
    'use strict';
    
    var Dialog = require('web.Dialog');
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.FshareGiveAway = publicWidget.Widget.extend({
        selector: '#wrapwrap',
    
        events: {
            'click .btn-submit-give-away': '_action_submit_giveaway'
        },
    
        start: function () {
            return this._super.apply(this, arguments);
        },
        
        _action_submit_giveaway: function() {
            var email = $("#txt_email").val();

            if (!!email) {
                $(".btn-submit-give-away").attr("disabled", true);
                $.ajax(
                   {
                      type:'GET',
                      url:'/submit_giveaway_email',
                      data:"email=" + email,
                      success: function(data){
                          if (data == "accepted") {
                            Dialog.alert(this, "Cảm ơn bạn, chờ mình thông báo kết quả nhé :)");
                          } else {
                            Dialog.alert(this, "Huhu, hết lượt rồi, chờ lần sau nhé");
                          }
                          $("#txt_email").attr("disabled", true);
                      },
                      error: function(error) {
                        Dialog.alert(this, "Huhu, có lỗi gì đó, mình chưa nhận được, bạn refresh rồi submit lại nhen");
                      },
                      timeout: 60000
                   }
                )
            } else {
                Dialog.alert(this, "Bạn chưa nhập email fshare kìa");
            }
        }
        
    })
    });
    
    