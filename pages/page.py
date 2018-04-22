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

    # before scripts of components on page
    def get_scripts_before(self):
        pass

    # after scripts of components on page
    def get_scripts_after(self):
        pass

    def render(self):
        page_template = self.loader.get_template(self.get_template())

        components_templates = {}
        scripts = {}
        scripts['scripts']=[]
        scripts['scripts']+=self.get_scripts_before()

        for component in self.components:
            id_ = component.get_id()
            if len(component.get_scripts()):
                scripts['scripts']+=component.get_scripts()

            component_template = self.loader.get_template(component.get_template())
            rendered = component_template.render(component.get_template_data())
            components_templates[id_]=rendered

        scripts['scripts'] += self.get_scripts_after()

        data = {}
        data.update(self.get_template_data())
        data.update(components_templates)
        data.update(scripts)
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