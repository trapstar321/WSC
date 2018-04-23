from components.component import Component

class DevListComponent(Component):
    def __init__(self):
        self.id=None

    def set_id(self, id):
        self.id=id

    def get_id(self):
        return 'DevListComponent_{}'.format(self.id)

    def get_template(self):
        return "device_list_component.html"

    def get_template_data(self):
        return {'device_list_component_id':'device_list_component_'+str(self.id)}

    def get_scripts(self):
        return ['js/components/device_list_component.js']

    def get_css(self):
        return {'css/components/device_list_component.css'}