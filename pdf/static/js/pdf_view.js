/* Javascript for pdfXBlock. */
// eslint-disable-next-line no-unused-vars
function pdfXBlockInitView(runtime, element) {
    /* Weird behaviour :
     * In the LMS, element is the DOM container.
     * In the CMS, element is the jQuery object associated*
     * So here I make sure element is the jQuery object */
    if (element.innerHTML) {
        element = $(element);
    }

    $(function () {
        element.find('.pdf-download-button').on('click', function () {
            const handlerUrl = runtime.handlerUrl(element, 'on_download');
            $.post(handlerUrl, '{}');
        });
    });
}
