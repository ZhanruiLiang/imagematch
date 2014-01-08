$(function() {
function getProgress() {
    $.ajax({
        url: '../teststatus/',
        type: 'get',
        success: function(data) {
            $('#progress .value').html(data['progress']);
            $('#state .value').html(data['state']);
            state = data['state']
            if(state === 'finished' || state === 'error') {
                clearInterval(handle);
            }
            if(state === 'finished') {
                $('#final-info').html(
                    data['groupAverageRates'] 
                    + '<br/>' 
                    + data['averageRate']);
            }
        }
    });
}

handle = setInterval(getProgress, 1000);

});
