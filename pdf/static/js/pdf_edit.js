/* Javascript for pdfXBlock. */
// eslint-disable-next-line no-unused-vars
function pdfXBlockInitEdit(runtime, element) {
    $(element).find('.action-cancel').bind('click', function () {
        runtime.notify('cancel', {});
    });

    $(element).find('.action-save').bind('click', function () {
        const data = {
            'display_name': $('#pdf_edit_display_name').val(),
            'url': $('#pdf_edit_url').val(),
            'allow_download': $('#pdf_edit_allow_download').val() || '',
            'source_text': $('#pdf_edit_source_text').val() || '',
            'source_url': $('#pdf_edit_source_url').val() || ''
        };

        runtime.notify('save', { state: 'start' });

        const handlerUrl = runtime.handlerUrl(element, 'save_pdf');
        $.post(handlerUrl, JSON.stringify(data)).done(function (response) {
            if (response.result === 'success') {
                runtime.notify('save', { state: 'end' });
            }
            else {
                runtime.notify('error', { msg: response.message });
            }
        });
    });
}
