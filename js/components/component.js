class Component{
    constructor(){
        this.protocol=null;
    }

    on_message(message){
        console.log("components.js Component on_message: message="+JSON.stringify(message));
    }

    send(message){
         console.log("components.js Component send: message="+JSON.stringify(message));
        this.protocol.send(message);
    }

    setProtocol(){
        this.protocol = protocol;
    }
}