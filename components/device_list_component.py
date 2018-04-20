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
        return {}