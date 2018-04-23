var MESSAGE_TYPE = {
        DEV_LIST: 1,
        DEV_STATUS: 2,
        IGNORE: 3
    };

class DeviceListComponent extends Component{
    constructor(id_){
        super(id_);
        this.accessor='#device_list_component_'+this.get_id()+" ul";
    }

    get_message_type(message){
        if(message.hasOwnProperty('dev_list')){     
            return MESSAGE_TYPE.DEV_LIST;
        }else if(message.hasOwnProperty('dev_id') && (message.hasOwnProperty('connected') || message.hasOwnProperty('disconnected'))){
            return MESSAGE_TYPE.DEV_STATUS;
        }else{
            return MESSAGE_TYPE.IGNORE;
        }
    }

    gen_device_record(dev_id, connected, address){
        return "<li class='"+(connected?"connected":"disconnected")+"' id='dev_"+dev_id+"'>Dev "+dev_id+" ["+address[0]+":"+address[1]+"]</li>";
    }

    on_message(message){
        super.on_message(message);        
        var accessor=this.accessor;
        var gen_device_record=this.gen_device_record;
        var msg_type=this.get_message_type(message);
        if(msg_type==MESSAGE_TYPE.DEV_LIST){           
            message['dev_list'].forEach(function(device){     
                $(accessor).empty();           
                $(accessor).append(gen_device_record(device.dev, device.connected, device.address));
            });            
        }else if(msg_type==MESSAGE_TYPE.DEV_STATUS){
            if($("#dev_"+message.dev_id).length==0){
                $(accessor).append(gen_device_record(message.dev_id, message.connected, message.address));
            }else{
                if(message.hasOwnProperty('connected')){
                    $("#dev_"+message.dev_id).prop('class', 'connected');
                }else if(message.hasOwnProperty('disconnected')){
                    $("#dev_"+message.dev_id).prop('class', 'disconnected');
                }
            }
        }
    }

    onload(){
        console.log('device_list_component.js DeviceListComponent onload()');
        var message = {'query':1, 'params':{'dev_list':1}}
        this.send(message);
    }
}