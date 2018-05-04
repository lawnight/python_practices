var echarts = require('echarts');
require('echarts/extension/bmap/bmap');
import $ from 'jquery'

// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));

// $.get('data/asset/data/lines-bus.json', function(data) {
//     var busLines = [].concat.apply([], data.map(function (busLine, idx) {
//         var prevPt;
//         var points = [];
//         for (var i = 0; i < busLine.length; i += 2) {
//             var pt = [busLine[i], busLine[i + 1]];
//             if (i > 0) {
//                 pt = [
//                     prevPt[0] + pt[0],
//                     prevPt[1] + pt[1]
//                 ];
//             }
//             prevPt = pt;

//             points.push([pt[0] / 1e4, pt[1] / 1e4]);
//         }
//         return {
//             coords: points
//         };
//     }));



$.get('bus_station_location.json', function (data) {
    // console.log(data)
    var bus_stations = data
    // console.log(bus_stations)
    var a = [].concat(1)



    var points = [
        [104.078156, 30.554803],
        [104.102806, 30.563821],
        [104.095332, 30.57115]
    ]

    var busLines = [
        {
            coords: points
        }
    ]



    var option = {
        // 加载 bmap 组件
        bmap: {
            // 百度地图中心经纬度
            center: [104.078156, 30.554803],
            // 百度地图缩放
            zoom: 12,
            // 是否开启拖拽缩放，可以只设置 'scale' 或者 'move'
            roam: true,
            // 百度地图的自定义样式，见 http://developer.baidu.com/map/jsdevelop-11.htm
            mapStyle: {

            }
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                return params.name + ' : ' + params.value[2];
            }
        },
        series: [
            {
                name: 'pm2.5',
                type: 'scatter',
                coordinateSystem: 'bmap',
                data: bus_stations,
                symbolSize: value => value[2],
                label: {
                    normal: {
                        show: false
                    },
                    emphasis: {
                        show: false
                    }
                },
                itemStyle: {
                    emphasis: {
                        borderColor: '#fff',
                        borderWidth: 1
                    }
                }
            },
            {
                type: 'lines',
                coordinateSystem: 'bmap',
                polyline: true,
                data: busLines,
                silent: true,
                lineStyle: {
                    normal: {
                        color: '#c23531',
                        color: 'rgb(200, 35, 45)',
                        opacity: 0.2,
                        width: 1
                    }
                },
                progressiveThreshold: 500,
                progressive: 200
            }
        ]
    }

    // 获取百度地图实例，使用百度地图自带的控件
    // var bmap = myChart.getModel().getComponent('bmap').getBMap();
    // bmap.addControl(new BMap.MapTypeControl());

    myChart.setOption(option);
});


