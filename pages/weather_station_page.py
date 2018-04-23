from pages.page import Page
from components.weather_station_component import WeatherStationComponent


class WeatherStationPage(Page):
    def __init__(self, loader):
        super(WeatherStationPage, self).__init__(loader)
        component = WeatherStationComponent()
        component.set_id(1)
        super(WeatherStationPage, self).add_component(component)

    def get_template_data(self, args=None):
        return {'title':'Weather station {}'.format(args['id'])}

    def get_url_segment(self):
        return 'weather_station/{id}'

    def get_template(self):
        return 'weather_station_page.html'

    def get_scripts_before(self):
        return ['js/protocol.js', 'js/client.js', 'js/components/component.js', 'js/pages/jquery-3.3.1.min.js']

    def get_scripts_after(self):
        return ['js/pages/weather_station_page.js']

    def get_css_before(self):
        return {'css/pages/weather_station_page.css'}

    def get_css_after(self):
        return {}