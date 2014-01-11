$(document).ready(function() {
    function getProgress() {
        $.ajax({
            url: '../teststatus/',
            type: 'get',
            dataType: 'json',
            success: function(data) {
                $('#state .value').html(data['state']);
                if (data['state'] == 'finished') {
                    $('.progress-pie-chart').remove();
                    var state = data['state'];
                    if (state == 'finished' || state == 'error') {
                        clearInterval(handle);
                    }
                    if (state == 'finished') {
                        $('#averageRate span.value').html(data['averageRate']);
                        var groupAverageRates = data['groupAverageRates'];
                        barChart(groupAverageRates);
                    }
                } else {
                    progressPieChart(data['progress']);
                }
            },
            error: function() {
                alert('error');
            }
        });
    }

    handle = setInterval(getProgress, 100);

    function progressPieChart(progress) {
        var $ppc = $('.progress-pie-chart'),
            percent = parseInt(progress * 100),
            deg = 360 * percent / 100;
        if (percent > 50) {
            $ppc.addClass('gt-50');
        }
        $('.ppc-progress-fill').css('transform', 'rotate(' + deg + 'deg)');
        $('.ppc-percents span').html(percent + '%');
    }

    function barChart(groupAverageRates) {
        var myData = new Array();
        var length = groupAverageRates.length;
        for (var i = 0; i < length; i++) {
            myData.push(['Group ' + groupAverageRates[i].group.toString(), groupAverageRates[i].rate]);
        };
        var colors = ['#F4B300', '#78BA00', '#2673EC', '#AE113D', '#FF7D23', '#FF1D77', '#1FAEFF', '#AA40FF', '#FF2E12', '#00AAAA'];
        var myColors = colors.slice(0, length);
        var myChart = new JSChart('graph', 'bar');
        myChart.setDataArray(myData);
        myChart.colorizeBars(myColors);
        myChart.setTitle('Average Rate per Group');
        myChart.setTitleColor('#8E8E8E');
        myChart.setAxisNameX('Groups');
        myChart.setAxisNameY('Average Rate');
        myChart.setAxisColor('#c6c6c6');
        myChart.setAxisWidth(1);
        myChart.setAxisNameColor('#9a9a9a');
        myChart.setAxisValuesColor('#939393');
        myChart.setAxisPaddingTop(60);
        myChart.setAxisPaddingLeft(50);
        myChart.setAxisPaddingBottom(60);
        myChart.setTextPaddingBottom(20);
        myChart.setTextPaddingLeft(15);
        myChart.setTitleFontSize(11);
        myChart.setBarBorderWidth(0);
        myChart.setBarSpacingRatio(50);
        myChart.setBarValuesColor('#737373');
        myChart.setGrid(false);
        myChart.setSize(700, 350);
        myChart.draw();
    }
});
