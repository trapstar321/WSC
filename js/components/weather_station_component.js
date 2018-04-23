var MESSAGE_TYPE = {        
        DEV_STATUS: 1,
        MESSAGE: 2
    };

class WeatherStationComponent extends Component{
    constructor(id_){
        super(id_);
        this.accessor='#weather_station_component_'+this.get_id()+" ul";
    }    

    get_message_type(message){
        if(message.hasOwnProperty('connected') || message.hasOwnProperty('not_connected') || message.hasOwnProperty('disconnected')){     
            return MESSAGE_TYPE.DEV_STATUS;
        }else{
            return MESSAGE_TYPE.MESSAGE
        }
    }

    on_message(message){
        super.on_message(message);   
        var msg_type = this.get_message_type(message);

        if(msg_type==MESSAGE_TYPE.DEV_STATUS){
            if(message.hasOwnProperty('connected')){
                $("#status").text("Connected");
            }else{
                $("#status").text("Not connected");
            }

            if(message.hasOwnProperty('address')){
                $("#address").text(message.address[0]+":"+message.address[1]);
            }
        }else if(msg_type==MESSAGE_TYPE.MESSAGE){
            $("#temperature").text(message.temperature);
            $("#humidity").text(message.humidity);
        }
    }

    onload(){
        console.log('weather_station_component.js WeatherStationComponent onload()');
        var message = {'choose':1, 'dev_id':Number.parseInt($("input[name=dev_id").val())}
        this.send(message);
    }
}