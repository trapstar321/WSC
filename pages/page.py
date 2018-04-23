class Page:
    def __init__(self, loader):
        self.loader = loader
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def get_template_data(self, args=None):
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

    def get_css_before(self):
        pass

    def get_css_after(self):
        pass

    def render(self, args=None):
        page_template = self.loader.get_template(self.get_template())

        components_templates = {}
        scripts = {}
        scripts['scripts']=[]
        scripts['scripts']+=self.get_scripts_before()

        css = {}
        css['css'] = []
        css['css'] += self.get_css_before()

        #render component template
        for component in self.components:
            id_ = component.get_id()

            component_template = self.loader.get_template(component.get_template())
            rendered = component_template.render(component.get_template_data())
            components_templates[id_]=rendered

        for component in self.components:
            if len(component.get_scripts()):
                scripts['scripts']+=component.get_scripts()

            if len(component.get_css()):
                css['css']+=component.get_css()

        scripts['scripts'] += self.get_scripts_after()
        css['css'] += self.get_css_after()

        data = {}
        data.update(self.get_template_data(args))
        data.update(components_templates)
        data.update(scripts)
        data.update(css)
        if args:
            data.update(args)

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