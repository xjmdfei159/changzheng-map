<!DOCTYPE html>
<html>
<head>
    <title>中国红军长征路线图 - 响应式布局、可折叠详情页与部署指南</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            overflow: hidden;
        }
        #map-container {
            position: absolute;
            top: 0;
            bottom: 150px; /* 留出时间轴空间 */
            left: 0;
            width: 100%; /* 初始宽度为100%，当详情页展开时会覆盖 */
            transition: width 0.3s ease; /* 添加过渡动画 */
        }
        #map-container.details-open {
            width: 70%; /* 当详情页展开时，地图宽度为70% */
        }
        #timeline-container {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%; /* 初始宽度为100% */
            height: 150px;
            background: white;
            border-top: 1px solid #ccc;
            overflow-x: auto;
            white-space: nowrap;
            padding: 10px 0;
            transition: width 0.3s ease; /* 添加过渡动画 */
        }
        #timeline-container.details-open {
            width: 70%; /* 当详情页展开时，时间轴宽度为70% */
        }
        .timeline-event {
            display: inline-block;
            margin: 0 10px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: #f9f9f9;
            cursor: pointer;
            transition: all 0.3s;
            vertical-align: top;
        }
        .timeline-event:hover {
            background: #e9e9e9;
            transform: translateY(-3px);
        }
        .timeline-event.active {
            background: #d4edda;
            border-color: #28a745;
            box-shadow: 0 0 8px rgba(40, 167, 69, 0.3);
        }
        .timeline-date {
            font-weight: bold;
            color: #333;
            font-size: 12px;
        }
        .timeline-keyword {
            color: #6c757d;
            font-size: 14px;
            margin-top: 5px;
        }
        #details-panel {
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            width: 30%;
            background: white;
            padding: 0;
            box-shadow: -5px 0 10px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s ease; /* 添加滑动过渡动画 */
            transform: translateX(0); /* 初始位置在视图内 */
        }
        #details-panel.hidden {
            transform: translateX(100%); /* 当隐藏时，完全滑出视图 */
            width: 0; /* 隐藏时宽度为0，避免占据空间 */
        }
        #details-header {
            background: #007bff;
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        #details-header h3 {
            margin: 0;
            font-size: 16px;
        }
        #toggle-details {
            background: none;
            border: none;
            color: white;
            font-size: 18px;
            cursor: pointer;
        }
        #details-content {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }
        .info-header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }
        .event-item {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 5px;
            background: #f9f9f9;
            cursor: pointer;
            transition: background 0.3s;
        }
        .event-item:hover {
            background: #e9e9e9;
        }
        .event-item.active {
            background: #d4edda;
            border-left: 4px solid #28a745;
        }
        .event-title {
            font-weight: bold;
            color: #333;
        }
        .event-date {
            color: #6c757d;
            font-size: 0.9em;
        }
        .event-description {
            margin-top: 8px;
            color: #555;
            line-height: 1.4;
        }
        .navigation-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
        }
        .nav-button {
            padding: 8px 16px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            flex: 1;
            margin: 0 5px;
        }
        .nav-button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        .nav-button.prev {
            background-color: #6c757d;
        }
        .nav-button.next {
            background-color: #28a745;
        }
        .legend {
            text-align: left;
            line-height: 18px;
            color: #555;
            margin-top: 15px;
        }
        .legend i {
            width: 18px;
            height: 18px;
            float: left;
            margin-right: 8px;
            opacity: 0.7;
        }
        /* 地图上的导航按钮 */
        .map-nav-container {
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .map-nav-button {
            padding: 10px 15px;
            background-color: rgba(0, 123, 255, 0.8);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            min-width: 100px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .map-nav-button:disabled {
            background-color: rgba(108, 117, 125, 0.6);
            cursor: not-allowed;
        }
        .map-nav-button.prev {
            background-color: rgba(108, 117, 125, 0.8);
        }
        .map-nav-button.next {
            background-color: rgba(40, 167, 69, 0.8);
        }
    </style>
</head>
<body>
    <div id="map-container">
        <div class="map-nav-container">
            <button id="map-prev-btn" class="map-nav-button prev">上一个事件</button>
            <button id="map-next-btn" class="map-nav-button next">下一个事件</button>
        </div>
    </div>
    <div id="timeline-container"></div>
    <div id="details-panel">
        <div id="details-header">
            <h3>长征详情</h3>
            <button id="toggle-details">[-]</button>
        </div>
        <div id="details-content">
            <div class="info-header">
                <h3>中国工农红军长征</h3>
                <p>1934年10月 - 1936年10月</p>
                <p>江西瑞金 → 陕北吴起镇</p>
            </div>
            <div id="events-list"></div>
            <div class="navigation-buttons">
                <button id="prev-btn" class="nav-button prev">上一个事件</button>
                <button id="next-btn" class="nav-button next">下一个事件</button>
            </div>
            <div class="legend">
                <div><i style="background: #e74c3c;"></i>起点：瑞金</div>
                <div><i style="background: #f39c12;"></i>重要地点</div>
                <div><i style="background: #e74c3c;"></i>重要战役</div>
                <div><i style="background: #3498db;"></i>渡河</div>
                <div><i style="background: #95a5a6;"></i>翻山</div>
                <div><i style="background: #27ae60;"></i>终点：吴起镇</div>
            </div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        // 初始化地图
        var map = L.map('map-container').setView([30.0, 105.0], 5);

        // 添加OpenStreetMap瓦片图层
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(map);

        // 长征路线上的重要地点和事件
        var routePoints = [
            {
                id: 1,
                name: "瑞金",
                latlng: [25.8789, 116.0269],
                type: "start",
                date: "1934年10月",
                event: "中央红军主力从江西瑞金出发，开始长征",
                description: "中共中央和中央红军（红一方面军）主力约8.6万人，由于第五次反围剿失败，被迫撤离中央苏区，踏上战略转移的征途。",
                keyword: "长征开始"
            },
            {
                id: 2,
                name: "雩都",
                latlng: [25.9327, 115.4097],
                type: "stop",
                date: "1934年10月17日",
                event: "于都河渡河",
                description: "中央红军主力从于都县渡过于都河，正式踏上长征路。于都河是中央苏区的最后一条河流，过河标志着中央苏区的结束。",
                keyword: "于都河渡河"
            },
            {
                id: 3,
                name: "湘江",
                latlng: [26.2320, 111.3000],
                type: "battle",
                date: "1934年11月27日-12月1日",
                event: "湘江战役",
                description: "长征途中最惨烈的战役之一，红军与桂军、湘军血战五昼夜，最终突破第四道封锁线，但付出了惨重代价，兵力从出发时的8.6万人锐减到3万余人。",
                keyword: "湘江战役"
            },
            {
                id: 4,
                name: "遵义",
                latlng: [27.7286, 106.9083],
                type: "important",
                date: "1935年1月15日-17日",
                event: "遵义会议",
                description: "中共中央政治局在遵义召开扩大会议，确立了毛泽东在中共中央和红军的领导地位，挽救了党、挽救了红军、挽救了中国革命。",
                keyword: "遵义会议"
            },
            {
                id: 5,
                name: "四渡赤水",
                latlng: [28.0000, 105.5000],
                type: "battle",
                date: "1935年1月19日-3月22日",
                event: "四渡赤水",
                description: "毛泽东指挥红军在赤水河流域进行的运动战，通过四次渡河，灵活机动地摆脱了敌人的围追堵截，是红军长征史上以少胜多、变被动为主动的光辉战例。",
                keyword: "四渡赤水"
            },
            {
                id: 6,
                name: "巧渡金沙江",
                latlng: [26.5417, 101.0000],
                type: "crossing",
                date: "1935年5月3日-9日",
                event: "巧渡金沙江",
                description: "红军利用缴获的几条小船，在7天7夜内将3万多人的部队全部渡过金沙江，摆脱了几十万国民党军队的围追堵截，取得了战略转移中具有决定意义的胜利。",
                keyword: "巧渡金沙江"
            },
            {
                id: 7,
                name: "强渡大渡河",
                latlng: [29.0000, 103.0000],
                type: "crossing",
                date: "1935年5月25日",
                event: "强渡大渡河",
                description: "红军先头部队在安顺场强渡大渡河，但由于此处渡口船只少，大部队无法迅速过河，于是决定沿河而上，飞夺泸定桥。",
                keyword: "强渡大渡河"
            },
            {
                id: 8,
                name: "飞夺泸定桥",
                latlng: [29.5833, 102.2333],
                type: "battle",
                date: "1935年5月29日",
                event: "飞夺泸定桥",
                description: "红四团22名勇士冒着枪林弹雨，攀着光溜溜的铁索，冲过泸定桥，打开了红军北上的道路，是中国革命史上的著名战例。",
                keyword: "飞夺泸定桥"
            },
            {
                id: 9,
                name: "翻越夹金山",
                latlng: [30.5000, 102.5000],
                type: "mountain",
                date: "1935年6月12日",
                event: "翻越夹金山",
                description: "红军翻越长征路上第一座大雪山——夹金山，海拔4114米。山上空气稀薄，气候恶劣，许多战士因高原反应和严寒牺牲。",
                keyword: "翻越夹金山"
            },
            {
                id: 10,
                name: "懋功",
                latlng: [30.9833, 102.3667],
                type: "meeting",
                date: "1935年6月18日",
                event: "一四方面军会师",
                description: "中央红军（红一方面军）与红四方面军在懋功（今小金县）会师，红军力量得到增强，但同时也为后来的分裂埋下伏笔。",
                keyword: "一四方面军会师"
            },
            {
                id: 11,
                name: "松潘",
                latlng: [32.6333, 103.5833],
                type: "stop",
                date: "1935年7月-8月",
                event: "通过松潘草地",
                description: "红军穿越松潘草地，这是一片海拔3500米以上的沼泽地，气候恶劣，缺乏食物，许多战士牺牲在草地中。",
                keyword: "穿越松潘草地"
            },
            {
                id: 12,
                name: "腊子口",
                latlng: [34.0000, 103.5000],
                type: "battle",
                date: "1935年9月17日",
                event: "腊子口战役",
                description: "红军攻克天险腊子口，打通了北上抗日的道路。腊子口是四川进入甘肃的唯一通道，地势险要，一夫当关万夫莫开。",
                keyword: "腊子口战役"
            },
            {
                id: 13,
                name: "哈达铺",
                latlng: [34.3500, 104.2000],
                type: "stop",
                date: "1935年9月20日",
                event: "哈达铺决策",
                description: "毛泽东在哈达铺从报纸上得知陕北有红军和根据地的消息，决定前往陕北。",
                keyword: "哈达铺决策"
            },
            {
                id: 14,
                name: "吴起镇",
                latlng: [36.8167, 108.1667],
                type: "end",
                date: "1935年10月19日",
                event: "长征胜利结束",
                description: "中央红军（红一方面军）到达陕北吴起镇，与陕北红军会师，标志着中央红军长征胜利结束。",
                keyword: "长征胜利结束"
            }
        ];

        // 定义不同类型的图标
        var iconTemplates = {
            start: '<div style="background-color: #e74c3c; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{id}</div>',
            stop: '<div style="background-color: #f39c12; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{id}</div>',
            important: '<div style="background-color: #f39c12; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{id}</div>',
            battle: '<div style="background-color: #e74c3c; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{id}</div>',
            crossing: '<div style="background-color: #3498db; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{id}</div>',
            mountain: '<div style="background-color: #95a5a6; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{id}</div>',
            meeting: '<div style="background-color: #9b59b6; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{id}</div>',
            end: '<div style="background-color: #27ae60; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">{id}</div>'
        };

        // 创建路线点的经纬度数组
        var routeCoordinates = routePoints.map(point => point.latlng);

        // 绘制长征路线
        var routeLine = L.polyline(routeCoordinates, {
            color: '#8B0000',
            weight: 4,
            opacity: 0.7
        }).addTo(map);

        // 标记所有重要地点
        var markers = {};
        routePoints.forEach(function(point) {
            // 为每个点创建独立的图标，确保ID正确
            var customIcon = L.divIcon({
                className: 'custom-icon',
                html: iconTemplates[point.type].replace('{id}', point.id),
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            });
            
            var marker = L.marker(point.latlng, {icon: customIcon}).addTo(map);
            marker.bindPopup(`<b>${point.name}</b><br>${point.event}`);
            
            // 为标记添加点击事件
            marker.on('click', function() {
                showEventDetails(point.id);
            });
            
            markers[point.id] = marker;
        });

        // 在右侧显示事件列表
        var eventsList = document.getElementById('events-list');
        routePoints.forEach(function(point) {
            var eventItem = document.createElement('div');
            eventItem.className = 'event-item';
            eventItem.innerHTML = `
                <div class="event-title">${point.id}. ${point.name}</div>
                <div class="event-date">${point.date}</div>
                <div class="event-description">${point.event}</div>
            `;
            eventItem.onclick = function() {
                showEventDetails(point.id);
            };
            eventsList.appendChild(eventItem);
        });

        // 创建时间轴
        var timelineContainer = document.getElementById('timeline-container');
        routePoints.forEach(function(point) {
            var timelineEvent = document.createElement('div');
            timelineEvent.className = 'timeline-event';
            timelineEvent.innerHTML = `
                <div class="timeline-date">${point.date}</div>
                <div class="timeline-keyword">${point.keyword}</div>
            `;
            timelineEvent.onclick = function() {
                showEventDetails(point.id);
            };
            timelineContainer.appendChild(timelineEvent);
        });

        // 导航按钮
        var currentIndex = 0; // 当前显示的事件索引

        function updateNavigationButtons() {
            var prevBtn = document.getElementById('prev-btn');
            var nextBtn = document.getElementById('next-btn');
            var mapPrevBtn = document.getElementById('map-prev-btn');
            var mapNextBtn = document.getElementById('map-next-btn');
            
            // 禁用或启用按钮
            prevBtn.disabled = (currentIndex <= 0);
            nextBtn.disabled = (currentIndex >= routePoints.length - 1);
            mapPrevBtn.disabled = (currentIndex <= 0);
            mapNextBtn.disabled = (currentIndex >= routePoints.length - 1);
            
            // 更新时间轴选中状态
            var timelineEvents = document.querySelectorAll('.timeline-event');
            timelineEvents.forEach((event, index) => {
                if (index === currentIndex) {
                    event.classList.add('active');
                } else {
                    event.classList.remove('active');
                }
            });
        }

        function showEventDetails(id) {
            // 清除之前选中的样式
            document.querySelectorAll('.event-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // 为当前事件添加选中样式
            var eventItems = document.querySelectorAll('.event-item');
            routePoints.forEach((point, index) => {
                if (point.id === id) {
                    currentIndex = index; // 更新当前索引
                    eventItems[index].classList.add('active');
                    
                    // 高亮地图上的标记
                    Object.keys(markers).forEach(key => {
                        if (key == id) {
                            // 可以添加额外的高亮效果
                            markers[key].openPopup();
                            // 移动地图到该点
                            map.setView(point.latlng, 8);
                        }
                    });
                }
            });
            
            // 更新选中事件的弹窗内容
            var selectedPoint = routePoints.find(p => p.id === id);
            if (selectedPoint) {
                var popupContent = `
                    <div style="max-width: 300px;">
                        <h3>${selectedPoint.id}. ${selectedPoint.name}</h3>
                        <p><strong>时间：</strong>${selectedPoint.date}</p>
                        <p><strong>事件：</strong>${selectedPoint.event}</p>
                        <p><strong>详情：</strong>${selectedPoint.description}</p>
                    </div>
                `;
                // 重新绑定弹窗内容
                markers[id].unbindPopup().bindPopup(popupContent).openPopup();
            }
            
            updateNavigationButtons();
        }

        // 导航按钮事件
        document.getElementById('prev-btn').addEventListener('click', function() {
            if (currentIndex > 0) {
                currentIndex--;
                showEventDetails(routePoints[currentIndex].id);
            }
        });

        document.getElementById('next-btn').addEventListener('click', function() {
            if (currentIndex < routePoints.length - 1) {
                currentIndex++;
                showEventDetails(routePoints[currentIndex].id);
            }
        });

        // 地图上的导航按钮事件
        document.getElementById('map-prev-btn').addEventListener('click', function() {
            if (currentIndex > 0) {
                currentIndex--;
                showEventDetails(routePoints[currentIndex].id);
            }
        });

        document.getElementById('map-next-btn').addEventListener('click', function() {
            if (currentIndex < routePoints.length - 1) {
                currentIndex++;
                showEventDetails(routePoints[currentIndex].id);
            }
        });

        // 详情页折叠功能
        var isDetailsVisible = true;
        var toggleButton = document.getElementById('toggle-details');
        var detailsPanel = document.getElementById('details-panel');
        var mapContainer = document.getElementById('map-container');
        var timelineContainerEl = document.getElementById('timeline-container');

        toggleButton.addEventListener('click', function() {
            isDetailsVisible = !isDetailsVisible;
            
            if (isDetailsVisible) {
                detailsPanel.classList.remove('hidden');
                mapContainer.classList.add('details-open');
                timelineContainerEl.classList.add('details-open');
                toggleButton.textContent = '[-]';
            } else {
                detailsPanel.classList.add('hidden');
                mapContainer.classList.remove('details-open');
                timelineContainerEl.classList.remove('details-open');
                toggleButton.textContent = '[+]';
            }
        });

        // 初始化显示第一个事件的详情
        if (routePoints.length > 0) {
            showEventDetails(1);
        }

        // 调整地图视野以适应路线
        var group = new L.featureGroup([routeLine]);
        routePoints.forEach(function(point) {
            group.addLayer(L.marker(point.latlng));
        });
        map.fitBounds(group.getBounds().pad(0.1));
        
        // 初始更新按钮状态
        updateNavigationButtons();
    </script>
</body>
</html>



