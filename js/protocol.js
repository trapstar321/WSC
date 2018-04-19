class Protocol{
	on_connected(){}
	on_disconnected(){}
	on_message(message){}
	send(message){}
}

class IdentityProtocol extends Protocol
{
	constructor(){
		super()
		this.client_id=null;
	}

	on_message(message){
		if(message.hasOwnProperty('unique_client_id')){
            if(this.client_id==null){
                this.client_id=message.unique_client_id;
            }
			return {'client_id':this.client_id};
    	}
		return null;
	}
}

class AckProtocol extends IdentityProtocol{
	constructor(client){
		super();
		this.queue={};
		this.acks=[];
		this.msg_id_counter=0;
		this.client=client;
	}	

	gen_msg_id(){
		if(this.msg_id_counter==Number.MAX_SAFE_INTEGER){
			this.msg_id_counter=0;			
		}
		this.msg_id_counter+=1;
		return this.msg_id_counter;
	}

	message_to_remove(msg_ids, key){
		msg_ids.forEach(function(id_){
			message = this.queue[id_];
			msg_keys = Object.keys(message);
			if(msg_keys.includes(key))
				return id_
		});
	}

	on_connected(){
		//check if something on queue and return all messages ordered by id
        //if next server message is ack, doesn't matter will be sent twice
		super.on_connected();

		this.acks.forEach(function(ack){
			this.send(ack);
		});
		
		//must ignore message with dev_id key
		var msg_ids = Object.keys(this.queue);		

		if(msg_ids.length>0){
			index = msg_ids.indexOf(this.message_to_remove(msg_ids, 'client_id'));
			msg_ids.splice(index,1);
		}

		msg_ids.forEach(function(id_){
			message = this.queue[id_];
			message['resend']=1;
			self.send(message);
		});
	}

	on_message(message){
		console.log('Received message '+message);
		message = JSON.parse(message);		
		var on_connect_msg = super.on_message(message);

		if(on_connect_msg){
			this.send(on_connect_msg);
		}

		this.acks=[];

		//acknowledge message
		if(message.hasOwnProperty('ack')){
			var msg_id = message['ack'];
			delete this.queue[msg_id];
			console.log("Got ack for message "+msg_id);
			return null;
		}else{
			// return ack and extract message
            // onyl if server signed the message
			if(message.hasOwnProperty('id')){
				var msg_id = message['id'];
				var ack = {'ack':msg_id};
				this.acks.push(ack);

				console.log("Return ack for message "+JSON.stringify(message));
				this.send(ack);
			}
		}
		return message;
	}

	send(message){
		console.log("Send message "+JSON.stringify(message));
		super.send(message);

		//add message_id to message so it can be acknowledged, only if not ack messag
		if(!message.hasOwnProperty('ack') && !message.hasOwnProperty('resend')){
			var id_ = this.gen_msg_id();
			this.queue[id_]=message;

			message['id']=id_
			console.log('Signed message '+JSON.stringify(message));
		}

		if(message.hasOwnProperty('resend')){
			console.log('Resend message '+JSON.stringify(message));
			delete message['resend'];
		}

		this.client.send(JSON.stringify(message));
	}
}


websocket = new WebSocket('ws://localhost:8888')
protocol = new AckProtocol(websocket);
websocket.onopen=function(){
	protocol.on_connected();
	websocket.onmessage=function(message){			
		protocol.on_message(message.data);
	}
}