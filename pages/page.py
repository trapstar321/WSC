class Page:
    def __init__(self, loader):
        self.loader = loader
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def get_template_data(self):
        pass

    def get_template(self):
        pass

    def get_url_segment(self):
        pass

    def get_scripts(self):
        pass

    def render(self):
        page_template = self.loader.get_template(self.get_template())

        components_templates = {}

        for component in self.components:
            id_ = component.get_id()
            component_template = self.loader.get_template(component.get_template())
            rendered = component_template.render(component.get_template_data())
            components_templates[id_]=rendered


        data = {}
        data.update(self.get_template_data())
        data.update(components_templates)
        data.update({'scripts':self.get_scripts()})
        return page_template.render(data)

if __name__=="__main__":
    from pages.device_list_page import DeviceListPage
    from components.device_list_component import DevListComponent

    page = DeviceListPage()
    dev_list_comp = DevListComponent()
    dev_list_comp.set_id(1)
    id_=dev_list_comp.get_id()
    page.add_component(dev_list_comp)

    template = page.render()
    print(template)