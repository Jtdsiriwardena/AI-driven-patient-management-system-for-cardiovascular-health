
//get response from chatbot
$(document).ready(function() {
    $('#send_btn').click(function() {
        var user_input = $('#user_input').val();
        $('#chat-container').append('<div class="user-container"><div class="user-msg">' + user_input + '</div></div>');
        $('#user_input').val('');

        $.ajax({
            url: '/get_response',
            type: 'POST',
            data: { user_input: user_input },
            success: function(response) {
                $('#chat-container').append('<div class="bot-container"><div class="bot-msg">' + response.response + '</div></div>');
                $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
            }
        });
    });
});
