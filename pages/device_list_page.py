from pages.page import Page
from components.device_list_component import DevListComponent

class DeviceListPage(Page):
    def __init__(self, loader):
        super(DeviceListPage, self).__init__(loader)
        dev_list_comp = DevListComponent()
        dev_list_comp.set_id(1)
        super(DeviceListPage, self).add_component(dev_list_comp)

    def get_template_data(self, args=None):
        return {'title':'Device list'}

    def get_url_segment(self):
        return 'dev_list'

    def get_template(self):
        return 'device_list_page.html'

    def get_scripts_before(self):
        return ['js/protocol.js', 'js/client.js', 'js/components/component.js', 'js/pages/jquery-3.3.1.min.js']

    def get_scripts_after(self):
        return ['js/pages/device_list_page.js']

    def get_css_before(self):
        return {'css/pages/device_list_page.css'}

    def get_css_after(self):
        return {}