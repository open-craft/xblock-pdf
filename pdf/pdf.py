""" pdfXBlock main Python class"""

from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Boolean, Scope, String
from xblock.fragment import Fragment
from xblock.utils.resources import ResourceLoader


from .utils import DummyTranslationService, _, bool_from_str, is_all_download_disabled, convert_to_pdf, GOTENBERG_HOST

try:
    import importlib_resources
except ImportError:
    import importlib.resources as importlib_resources

loader = ResourceLoader(__name__)


@XBlock.needs('i18n')
class PdfBlock(XBlock):
    """
    Icon of the XBlock. Values : [other (default), video, problem]
    """
    icon_class = "other"
    editable_fields = ('display_name', 'url', 'allow_download', 'source_text', 'source_url')

    # Fields
    display_name = String(
        display_name=_("Display Name"),
        default=_("PDF"),
        scope=Scope.settings,
        help=_("This name appears in the horizontal navigation at the top of the page.")
    )

    url = String(
        display_name=_("PDF URL"),
        default=_("https://tutorial.math.lamar.edu/pdf/Trig_Cheat_Sheet.pdf"),
        scope=Scope.content,
        help=_("The URL for your PDF.")
    )

    allow_download = Boolean(
        display_name=_("PDF Download Allowed"),
        default=True,
        scope=Scope.content,
        help=_("Display a download button for this PDF.")
    )

    source_text = String(
        display_name=_("Source document button text"),
        default="",
        scope=Scope.content,
        help=_(
            "Add a download link for the source file of your PDF. "
            "Use it for example to provide the PowerPoint file used to create this PDF."
        )
    )

    source_url = String(
        display_name=_("Source document URL"),
        default="",
        scope=Scope.content,
        help=_(
            "Add a download link for the source file of your PDF. "
            "Use it for example to provide the PowerPoint file used to create this PDF."
        )
    )

    # Util functions
    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource = importlib_resources.files("pdf").joinpath(resource_path)
        return resource.read_text("utf-8")

    def render_template(self, template_path, context=None):
        """
        Evaluate a template by resource path, applying the provided context
        """
        if context is None:
            context = {}
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    # Main functions
    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'disable_all_download': is_all_download_disabled(),
            'source_text': self.source_text,
            'source_url': self.source_url,
            '_i18n_service': self.i18n_service,
        }
        html = loader.render_django_template(
            'templates/html/pdf_view.html',
            context=context,
            i18n_service=self.i18n_service,
        )

        event_type = 'edx.pdf.loaded'
        event_data = {
            'url': self.url,
            'source_url': self.source_url,
        }
        self.runtime.publish(self, event_type, event_data)
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/pdf_view.js"))
        frag.initialize_js('pdfXBlockInitView')
        return frag


    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'disable_all_download': is_all_download_disabled(),
            'source_text': self.source_text,
            'source_url': self.source_url,
            'enable_conversion': GOTENBERG_HOST is not None,
        }
        html = loader.render_django_template(
            'templates/html/pdf_edit.html',
            context=context,
            i18n_service=self.i18n_service,
        )
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/pdf_edit.js"))
        frag.initialize_js('pdfXBlockInitEdit')
        return frag

    @XBlock.json_handler
    def on_download(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        The download file event handler
        """
        event_type = 'edx.pdf.downloaded'
        event_data = {
            'url': self.url,
            'source_url': self.source_url,
        }
        self.runtime.publish(self, event_type, event_data)

    def _generate_pdf_from_source(self):
        """
        Uses the Gotenberg API to convert the source document to a PDF.
        """
        output_path = "{loc.org}/{loc.course}/{loc.block_type}/{loc.block_id}.pdf".format(
            loc=self.location  # pylint: disable=no-member
        )
        return convert_to_pdf(
            self.source_url,
            output_path,
        )

    @XBlock.json_handler
    def save_pdf(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']

        if not is_all_download_disabled():
            self.allow_download = bool_from_str(data['allow_download'])
            self.source_text = data['source_text']
            self.source_url = data['source_url']
            if data['source_url'] and bool_from_str(data['pdf_auto_generate']):
                pdf_path = self._generate_pdf_from_source()
                self.url = pdf_path

        return {
            'result': 'success',
        }

    @property
    def i18n_service(self):
        """ Obtains translation service """
        i18n_service = self.runtime.service(self, "i18n")
        if i18n_service:
            return i18n_service
        return DummyTranslationService()
