class WebSocketClient{
    constructor(ip, port, protocol){
        this.url = "ws://"+ip+":"+port;
        this.client=null;
        this.protocol=protocol;
        this.protocol.setClient(this);
    }    

    disconnect(){
        this.client.close();
    }

    connect(){
        var protocol = this.protocol;
        this.client = new WebSocket(this.url);
        var client = this.client;
        this.client.onopen=function(){
            protocol.on_connected();
            client.onmessage=function(message){			
                protocol.on_message(message.data);
            }
            client .onclose=function(){                
                protocol.on_disconnected();
            }
        }

        /*CONNECTING	0	The connection is not yet open.
        OPEN	1	The connection is open and ready to communicate.
        CLOSING	2	The connection is in the process of closing.
        CLOSED	3	The connection is closed or couldn't be opened.*/
        client.onerror = function(evt){
            console.log("client.js connect(): WebSocket error occured");
            if(evt.target.readyState!=1){
                protocol.on_disconnected();
            }
        }
    }

    send(message){
        if(this.client.readyState!=1){
            return false;
        }else{
            this.client.send(message)
        }
    }
}