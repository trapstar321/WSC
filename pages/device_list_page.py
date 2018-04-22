from pages.page import Page
from components.device_list_component import DevListComponent

class DeviceListPage(Page):
    def __init__(self, loader):
        super(DeviceListPage, self).__init__(loader)
        dev_list_comp = DevListComponent()
        dev_list_comp.set_id(1)
        super(DeviceListPage, self).add_component(dev_list_comp)

    def get_template_data(self):
        return {'title':'Device list'}

    def get_url_segment(self):
        return 'dev_list'

    def get_template(self):
        return 'device_list.html'

    def get_scripts_before(self):
        return ['js/protocol.js', 'js/client.js', 'js/components/component.js']

    def get_scripts_after(self):
        return ['js/pages/device_list_page.js']