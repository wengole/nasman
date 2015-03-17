jQuery(document).ready(function ($) {
    var ws4redis = WS4Redis({
        uri: '{{ WEBSOCKET_URI }}foobar?subscribe-broadcast&publish-broadcast&echo',
        receive_message: receiveMessage,
        heartbeat_msg: "{{ WS4REDIS_HEARTBEAT }}"
    });

// attach this function to an event handler on your site
    function sendMessage() {
        ws4redis.send_message('A message');
    }

// receive a message though the websocket from the server
    function receiveMessage(msg) {
        alert('Message from Websocket: ' + msg);
    }
});
