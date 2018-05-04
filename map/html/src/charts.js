var echarts = require('echarts');
require('echarts/extension/bmap/bmap');

// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));


var option = {
    // 加载 bmap 组件
    bmap: {
        // 百度地图中心经纬度
        center: [120.13066322374, 30.240018034923],
        // 百度地图缩放
        zoom: 14,
        // 是否开启拖拽缩放，可以只设置 'scale' 或者 'move'
        roam: true,
        // 百度地图的自定义样式，见 http://developer.baidu.com/map/jsdevelop-11.htm
        mapStyle: {}
    },
    series: [{
        type: 'scatter',
        // 使用百度地图坐标系
        coordinateSystem: 'bmap',
        // 数据格式跟在 geo 坐标系上一样，每一项都是 [经度，纬度，数值大小，其它维度...]
        data: [ [120, 30, 1] ]
    }]
}

// 获取百度地图实例，使用百度地图自带的控件
var bmap = myChart.getModel().getComponent('bmap').getBMap();
bmap.addControl(new BMap.MapTypeControl());

myChart.setOption(option)