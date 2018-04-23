from components.component import Component

class WeatherStationComponent(Component):
    def __init__(self):
        self.id=None

    def set_id(self, id):
        self.id=id

    def get_id(self):
        return 'WeatherStationComponent_{}'.format(self.id)

    def get_template(self):
        return "weather_station_component.html"

    def get_template_data(self):
        return {'weather_station_component_id':'weather_station_component_'+str(self.id)}

    def get_scripts(self):
        return ['js/components/weather_station_component.js']

    def get_css(self):
        return {'css/components/weather_station_component.css'}