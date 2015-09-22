$(document).ready(function() {
            $( "#edit_photo" ).change(function() {
                var new_photo = window.URL.createObjectURL(this.files[0])
                $('#photo_preview').attr('src', new_photo)
            });
            function block_form() {
                $("#loading").show();
                $('textarea').attr('disabled', 'disabled');
                $('input').attr('disabled', 'disabled');
            }
            function unblock_form() {
                $('#loading').hide();
                $('textarea').removeAttr('disabled');
                $('input').removeAttr('disabled');
                $('.errorlist').remove();
            }
            var options = {
                beforeSubmit: function(form, options) {
                    block_form();
                },
                success: function() {
                    unblock_form();
                    $("#form_edit_success").show();
                    setTimeout(function() {
                        $("#form_edit_success").hide();
                    }, 5000);
                },
                error:  function(resp) {
                    unblock_form();
                    $("#form_edit_error").show();
                    // render errors in form fields
                    var errors = JSON.parse(resp.responseText);
                    for (error in errors) {
                        var id = '#id_' + error;
                        $(id).parent('p').prepend(errors[error]);
                     }
                        setTimeout(function() {
                        $("#form_edit_error").hide();
                    }, 5000);
                }
            };
            $('#form_edit').ajaxForm(options);
        });
