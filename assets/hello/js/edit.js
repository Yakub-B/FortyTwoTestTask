$(function () {
    let options = {
        target: $('#success'),
        dataType: 'json',
        beforeSubmit: function(arr, $form, options) {
            for (let i in $form[0].elements) {
                options.target.html('<h3>Loading...</h3>')
                if ('INPUT' !== $form[0].elements[i].nodeName &&
                    'TEXTAREA' !== $form[0].elements[i].nodeName)
                    continue;
                $($form[0].elements[i]).attr('disabled', true);
            }
            return true;
        },
        success: function (data, textStatus, jqXHR, $form) {
            for (let i in $form[0].elements) {
                if ('INPUT' !== $form[0].elements[i].nodeName &&
                    'TEXTAREA' !== $form[0].elements[i].nodeName)
                    continue;
                $($form[0].elements[i]).attr('disabled', false);
            }
            if (data.success) {
                $('#fail').attr('hidden', true)
                $('#success').html("Ok. Form saved.").attr('hidden', false)
            } else {
                $('#success').attr('hidden', true)
                $('#fail').text("Form does not saved. Please fix errors above:").attr('hidden', false)
                    .append('<ul></ul>')
                for (let key in data.errors) {
                    $('#fail > ul').append(`<li>Field: ${key}, error - ${data.errors[key][0]}</li>`)
                }
            }
        }
    }

    $('#profile_edit').ajaxForm(options)
})
