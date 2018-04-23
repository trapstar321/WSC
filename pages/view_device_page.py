from pages.page import Page

class ViewDevicePage(Page):
    def __init__(self, loader):
        super(ViewDevicePage, self).__init__(loader)

    def get_template_data(self, args=None):
        return {'title':'View device {}'.format(args['id'])}

    def get_url_segment(self):
        return 'view_device/{id}'

    def get_template(self):
        return 'view_device_page.html'

    def get_scripts_before(self):
        return ['js/protocol.js', 'js/client.js', 'js/components/component.js', 'js/pages/jquery-3.3.1.min.js']

    def get_scripts_after(self):
        return ['js/pages/view_device_page.js']

    def get_css_before(self):
        return {'css/pages/view_device_page.css'}

    def get_css_after(self):
        return {}