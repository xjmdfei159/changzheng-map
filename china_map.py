import folium
import json

# 创建中国地图对象，设置中心点和初始缩放级别
# 中国的大致中心点坐标：北纬35.86166度，东经104.195397度
# 初始放大到50km级别（zoom_start=8）
china_map = folium.Map(location=[25.8856, 116.0270], zoom_start=8,  # 初始位置设置为瑞金（第一个节点），已更新为更准确的坐标
                        tiles='OpenStreetMap',  # 使用OpenStreetMap图层
                        control_scale=True)    # 显示比例尺

# 为地图添加唯一ID，用于JavaScript控制
china_map.get_root().header.add_child(folium.Element('<div id="map-id" style="display: none;">map</div>'))

# 定义红军长征主要节点的经纬度坐标（从江西瑞金到陕北吴起镇）
# 重构数据结构，包含地点简介、主要事件、详细故事和相关图片
long_march_waypoints = [
    {        
        'name': '瑞金', 
        'location': [25.8856, 116.0270],  # 更新为更准确的坐标
        'description': '长征出发地',
        'introduction': '瑞金是中华苏维埃共和国临时中央政府所在地，被誉为红色故都、共和国摇篮。',
        'events': '1934年10月10日，中共中央、中革军委率中央红军主力从瑞金等地出发，开始长征。',
        'story': '1934年10月，由于第五次反"围剿"失败，中央红军被迫实行战略性转移。在瑞金，红军进行了充分的准备，包括人员、物资的集结和政治动员。红军将士们怀着对革命事业的坚定信念，踏上了艰苦卓绝的长征之路。',
        'image': 'https://pic.rmb.bdstatic.com/bjh/news/e3b61520c2e4f516b1c4651f4691815d.jpeg'
    },
    {
        'name': '雩都', 
        'location': [25.9811, 115.4442],
        'description': '于都河渡河',
        'introduction': '雩都（今于都）是中央红军长征的第一渡，是红军离开中央苏区的最后一站。',
        'events': '1934年10月16日至19日，中央红军主力8.6万余人从于都河的8个渡口渡河，开始了著名的二万五千里长征。',
        'story': '在于都，当地群众积极支持红军，他们不仅提供了大量的船只，还帮助红军搭建浮桥。许多群众自发为红军战士送茶送水，甚至把自己的口粮拿出来支援红军。在群众的帮助下，红军成功渡过了于都河，开始了艰苦的长征历程。',
        'image': 'https://img.zcool.cn/community/01b4d45d383265a8012193a3696d2e.jpg@1280w_1l_2o_100sh.jpg'
    },
    {
        'name': '遵义', 
        'location': [27.7172, 106.9271],
        'description': '遵义会议召开地',
        'introduction': '遵义是中国革命历史上的重要转折点，遵义会议确立了毛泽东在党中央和红军的领导地位。',
        'events': '1935年1月15日至17日，中共中央在遵义召开政治局扩大会议，确立了毛泽东在党中央和红军的领导地位。',
        'story': '遵义会议是中国共产党历史上一个生死攸关的转折点。会议集中解决了当时具有决定意义的军事和组织问题，结束了王明"左"倾教条主义在党中央的统治，确立了毛泽东在党中央和红军的领导地位。这次会议挽救了党、挽救了红军、挽救了中国革命，是党的历史上一个伟大的转折点。',
        'image': 'https://pic.rmb.bdstatic.com/bjh/news/b3bd8b8d9bceb918e1421e11b91a8d83.jpeg'
    },
    {
        'name': '赤水', 
        'location': [28.5081, 105.7975],
        'description': '四渡赤水',
        'introduction': '赤水是红军长征中著名的四渡赤水战役发生地，是毛泽东军事指挥艺术的得意之笔。',
        'events': '1935年1月19日至3月22日，中央红军在毛泽东等指挥下，四渡赤水，巧妙地跳出了国民党军的包围圈。',
        'story': '四渡赤水战役是红军长征中最精彩的军事行动之一，也是毛泽东军事指挥艺术的得意之笔。在毛泽东的指挥下，红军采取灵活机动的战略战术，声东击西，迷惑敌人，成功地摆脱了国民党军的围追堵截，实现了战略转移的目标。',
        'image': 'https://img.zcool.cn/community/01f02858a471e7a801219c77d2e322.jpg@1280w_1l_2o_100sh.jpg'
    },
    {
        'name': '金沙江', 
        'location': [27.1564, 100.2562],
        'description': '巧渡金沙江',
        'introduction': '金沙江是长江的上游，水流湍急，是红军长征中的一道天险。',
        'events': '1935年5月3日至9日，中央红军干部团在后有追兵的情况下，仅凭7只小船，用6天6夜时间巧渡金沙江。',
        'story': '金沙江战役是红军长征中的一次重要战役。红军先头部队化装成国民党军，智取了皎平渡，并控制了渡口。当地群众帮助红军仅用7只小船，在6天6夜时间里，将中央红军主力全部渡过了金沙江，成功地摆脱了国民党军的围追堵截。',
        'image': 'https://pic.rmb.bdstatic.com/bjh/news/a6a3b39b0bbd5f2f1ce3d1b1f8e28d8e.jpeg'
    },
    {
        'name': '大渡河', 
        'location': [29.4333, 102.2167],
        'description': '强渡大渡河',
        'introduction': '大渡河是红军长征中的又一道天险，水流湍急，两岸悬崖峭壁。',
        'events': '1935年5月24日至25日，中央红军在安顺场强渡大渡河，十八勇士冒着敌人的枪林弹雨，成功突破天险。',
        'story': '强渡大渡河是红军长征中的一次勇敢壮举。在敌人的严密防守下，红军十八勇士在火力掩护下，乘坐木船强行渡河，成功地突破了敌人的防线。这次战役展现了红军战士不怕牺牲、英勇无畏的革命精神。',
        'image': 'https://pic.rmb.bdstatic.com/bjh/news/a40e6c959663850777e278d9cf295be2.jpeg'
    },
    {
        'name': '泸定桥', 
        'location': [29.9428, 102.2956],
        'description': '飞夺泸定桥',
        'introduction': '泸定桥是一座铁索桥，横跨大渡河，是红军长征中的关键节点。',
        'events': '1935年5月29日，22名红军战士在火力掩护下，攀着铁索向对岸冲锋，最终夺下泸定桥。',
        'story': '飞夺泸定桥是红军长征中最惊险、最悲壮的战役之一。在敌人拆除了桥上的木板，只剩下13根铁索的情况下，22名红军战士手持冲锋枪，身背马刀，腰缠手榴弹，冒着敌人的枪林弹雨，攀着铁索向对岸冲锋。最终，红军成功地夺下了泸定桥，为中央红军北上打开了通道。',
        'image': 'https://pic.rmb.bdstatic.com/bjh/news/35e4fbd5b33c4307160c507a8133afb1.jpeg'
    },
    {
        'name': '夹金山', 
        'location': [30.6853, 102.8677],
        'description': '翻越夹金山',
        'introduction': '夹金山是红军长征中翻越的第一座大雪山，海拔4000多米，山上终年积雪，空气稀薄。',
        'events': '1935年6月12日，中央红军先头部队翻越长征途中第一座大雪山——夹金山，山上终年积雪，空气稀薄。',
        'story': '翻越夹金山是红军长征中的一次艰苦卓绝的考验。山上终年积雪，空气稀薄，气温极低，许多红军战士因为严寒、缺氧而牺牲。但红军战士们发扬了不怕苦、不怕死的革命精神，互相帮助，互相鼓励，最终成功地翻越了夹金山。',
        'image': 'https://img.zcool.cn/community/01611d58a471e9a801219c77557881.jpg@1280w_1l_2o_100sh.jpg'
    },
    {
        'name': '懋功', 
        'location': [31.5543, 102.4531],
        'description': '与红四方面军会师',
        'introduction': '懋功是中央红军与红四方面军会师的地点，标志着红军力量的壮大。',
        'events': '1935年6月18日，中央红军与红四方面军在懋功会师，两军将士欢欣鼓舞，庆祝胜利会师。',
        'story': '懋功会师是红军长征中的一个重要里程碑。中央红军与红四方面军的胜利会师，壮大了红军的力量，增强了红军的信心。两军将士互相学习，互相帮助，结下了深深的革命友谊。',
        'image': 'https://img.zcool.cn/community/015c5558a471e8a801219c779f01fc.jpg@1280w_1l_2o_100sh.jpg'
    },
    {
        'name': '松潘草地', 
        'location': [32.6000, 103.8000],
        'description': '过草地',
        'introduction': '松潘草地是红军长征中最艰苦的路段之一，到处是沼泽泥潭，一不小心就会陷进去。',
        'events': '1935年8月21日至26日，中央红军过松潘草地，草地茫茫无边，到处是沼泽泥潭，不少红军战士陷入泥潭牺牲。',
        'story': '过草地是红军长征中最艰苦的历程之一。草地茫茫无边，到处是沼泽泥潭，一不小心就会陷进去，而且没有食物，没有水，许多红军战士因为饥饿、寒冷、疾病而牺牲。但红军战士们发扬了革命乐观主义精神，互相帮助，互相鼓励，最终成功地走出了草地。',
        'image': 'https://pic.rmb.bdstatic.com/bjh/news/ce287241f06b1665e6b1fc778a7fb59d.jpeg'
    },
    {
        'name': '吴起镇', 
        'location': [36.92785, 108.17611],
        'description': '长征终点',
        'introduction': '吴起镇是中央红军长征的终点，标志着长征的胜利结束。',
        'events': '1935年10月19日，中央红军到达陕北吴起镇，与陕北红军会师，胜利完成了二万五千里长征。',
        'story': '吴起镇会师是红军长征胜利的标志。经过一年多的艰苦跋涉，中央红军终于到达了陕北，与陕北红军胜利会师。长征的胜利，保存了党和红军的基干力量，打开了中国革命的新局面。',
        'image': 'https://pic.rmb.bdstatic.com/bjh/news/18afdc74229304940c6cf7756957d376.jpeg'
    }
]

# 提取长征路线的坐标点用于绘制路线 - 基础节点
long_march_coordinates = [point['location'] for point in long_march_waypoints]

# 增强版长征路线 - 确保节点都在线段上
enhanced_march_coordinates = [
    # 瑞金到雩都段
    [25.8856, 116.0270],  # 瑞金
    [25.9250, 115.8700],  # 于都河渡口附近
    [25.9811, 115.4442],  # 雩都
    
    # 雩都到遵义段
    [25.9000, 114.9000],  # 向湘江方向
    [25.6000, 113.9000],  # 湘江战役附近
    [26.0000, 113.0000],  # 贵州边界
    [26.5000, 111.8000],  # 贵州境内
    [27.1000, 109.8000],  # 接近遵义
    [27.7172, 106.9271],  # 遵义
    
    # 遵义到赤水段
    [27.8000, 106.5000],  # 遵义附近
    [28.0000, 106.2000],  # 四渡赤水路线点1
    [28.2000, 105.9000],  # 四渡赤水路线点2
    [28.4000, 105.8000],  # 四渡赤水路线点3
    [28.5081, 105.7975],  # 赤水
    
    # 赤水到金沙江段
    [28.3000, 105.2000],  # 向金沙江方向
    [27.9000, 104.5000],  # 云南境内
    [27.5000, 103.2000],  # 接近金沙江
    [27.1564, 100.2562],  # 金沙江
    
    # 金沙江到大渡河段
    [27.5000, 100.0000],  # 继续北上
    [28.0000, 101.0000],  # 四川境内
    [28.8000, 101.8000],  # 接近大渡河
    [29.4333, 102.2167],  # 大渡河
    
    # 大渡河到泸定桥段
    [29.6000, 102.2500],  # 向泸定桥方向
    [29.9428, 102.2956],  # 泸定桥
    
    # 泸定桥到懋功段（简化，不再显示具体雪山位置）
    [30.1000, 102.4000],  # 向西北方向
    [30.5000, 102.6000],  # 继续北上
    [31.0000, 102.5000],  # 继续北上
    [31.3000, 102.4500],  # 接近懋功
    [31.5543, 102.4531],  # 懋功（与红四方面军会师）
    
    # 懋功到吴起镇段（简化松潘草地路线）
    [31.8000, 102.8000],  # 向松潘草地方向
    [32.0000, 103.0000],  # 松潘草地附近
    [32.3000, 103.4000],  # 松潘草地北部
    [32.6047, 103.6553],  # 松潘草地（更精确的坐标）
    [33.0000, 104.0000],  # 离开草地
    [33.5000, 104.5000],  # 甘肃境内
    [34.0000, 105.0000],  # 继续北上
    [34.5000, 105.5000],  # 陕西边界
    [35.0000, 106.0000],  # 陕西境内
    [35.5000, 106.5000],  # 接近吴起镇
    [36.0000, 107.0000],  # 继续向吴起镇
    [36.5000, 107.5000],  # 陕北境内
    [36.92785, 108.17611]  # 吴起镇（长征终点）
]

# 绘制红军长征真实路线 - 粉色实线显示实际走过的路径
folium.PolyLine(
    locations=enhanced_march_coordinates,
    color='#FFB6C1',  # 粉色
    weight=4,  # 较粗的线宽
    opacity=0.9,
    tooltip='红军长征真实路线',
    popup='红军长征（1934-1935）：从瑞金到吴起镇，翻雪山过草地的真实路径'
).add_to(china_map)

# 确保所有节点都在路线上
# 1. 首先检查enhanced_march_coordinates中是否包含所有long_march_waypoints的位置
for i, waypoint in enumerate(long_march_waypoints):
    # 检查当前waypoint的location是否在enhanced_march_coordinates中
    is_on_path = False
    for coord in enhanced_march_coordinates:
        # 提高精度要求，确保节点准确位于路线上
        if abs(coord[0] - waypoint['location'][0]) < 0.00001 and abs(coord[1] - waypoint['location'][1]) < 0.00001:
            is_on_path = True
            break
    
    # 如果不在路线上，则更新为最近的路线点
    if not is_on_path:
        # 找到最接近的点
        closest_point = None
        min_distance = float('inf')
        
        # 遍历所有路线点，计算距离
        for coord in enhanced_march_coordinates:
            distance = ((coord[0] - waypoint['location'][0])**2 + (coord[1] - waypoint['location'][1])** 2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest_point = coord
        
        # 更新waypoint的location为最近的路线点
        if closest_point:
            long_march_waypoints[i]['location'] = closest_point.copy()
            print(f"已调整节点'{waypoint['name']}'的位置，使其位于路线上")

# 为每个长征节点添加数字标记
for i, waypoint in enumerate(long_march_waypoints):
    # 创建包含图标和名称的HTML
    marker_html = f"""
    <div style="text-align: center;">
        <div style="
            position: relative;
            width: 40px;
            height: 40px;
            margin: 0 auto;
        ">
            <!-- 自定义图标 -->
            <div style="
                background-color: #d32f2f;
                color: white;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                box-shadow: 0 0 10px rgba(211, 47, 47, 0.7);
            ">🏮</div>
            <!-- 右上角数字 -->
            <div style="
                position: absolute;
                top: -5px;
                right: -5px;
                background-color: #ffd700;
                color: #d32f2f;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 12px;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
            ">{i+1}</div>
        </div>
        <!-- 删除图标下方的名称文本 -->
    </div>"""
    
    # 使用自定义Popup设置宽度，添加"查看更多"按钮
    popup_content = folium.Popup(
        f"<div style='font-size: 14px;'><strong>{waypoint['name']}</strong><br>{waypoint['description']}<br><button onclick='openDetailsForNode({i})' style='margin-top: 10px; padding: 5px 10px; background-color: #d32f2f; color: white; border: none; border-radius: 4px; cursor: pointer;'>查看更多</button></div>",
        max_width=300,  # 设置最大宽度
        min_width=200   # 设置最小宽度
    )
    
    folium.Marker(
        location=waypoint['location'],
        popup=popup_content,
        tooltip=f"{i+1}. {waypoint['name']}",
        icon=folium.DivIcon(html=marker_html)
    ).add_to(china_map)

# 添加图层控制器，允许用户切换不同的地图图层
folium.LayerControl().add_to(china_map)

# 添加自定义CSS和JavaScript来实现界面增强
custom_css = '''
<style>
    /* 左侧悬浮窗样式 */
    #progress-panel {
        position: fixed;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
        width: 150px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        font-family: 'Microsoft YaHei', Arial, sans-serif;
    }
    
    #progress-panel h3 {
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 16px;
        color: #d32f2f;
        text-align: center;
    }
    
    #progress-info {
        margin-bottom: 15px;
        text-align: center;
    }
    
    #progress-bar {
        width: 100%;
        height: 8px;
        background: #e0e0e0;
        border-radius: 4px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    #progress-fill {
        height: 100%;
        background: #d32f2f;
        width: 0%;
        transition: width 0.3s ease;
    }
    
    .control-btn {
        width: 100%;
        padding: 8px;
        margin: 5px 0;
        background: #d32f2f;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }
    
    .control-btn:hover {
        background: #b71c1c;
    }
    
    /* 顶部标志样式 */
    #header-banner {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1001;
        font-family: 'Microsoft YaHei', Arial, sans-serif;
    }
    
    #header-banner h1 {
        margin: 0;
        font-size: 24px;
        font-weight: bold;
    }
    
    /* 右侧详情页样式 */
    #details-panel {
        position: fixed;
        right: -400px;
        top: 60px;
        bottom: 0;
        width: 400px;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        transition: right 0.3s ease;
        padding: 20px;
        overflow-y: auto;
        font-family: 'Microsoft YaHei', Arial, sans-serif;
    }
    
    #details-panel.show {
        right: 0;
    }
    
    #details-panel h2 {
        margin-top: 0;
        color: #d32f2f;
        font-size: 20px;
    }
    
    #details-panel h3 {
        color: #757575;
        font-size: 16px;
        margin-top: 5px;
    }
    
    .detail-section {
        margin-bottom: 20px;
    }
    
    .detail-section h4 {
        color: #333;
        font-size: 14px;
        margin-bottom: 8px;
        padding-bottom: 5px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .detail-section p {
        line-height: 1.6;
        color: #555;
        margin: 0;
    }
    
    .close-btn {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        width: 30px;
        height: 30px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1002;
        color: #333;
        font-size: 20px;
        line-height: 1;
        padding: 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .close-btn:hover {
        opacity: 0.8;
    }
    
    /* 确保地图容器有足够的空间显示所有内容 */
    .map-container {
        position: relative;
        width: 100%;
        height: 100vh;
    }
    
    /* 音效控制样式 */
    #audio-control {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #e0e0e0;
    }
    
    #audio-btn {
        width: 100%;
        padding: 8px;
        background: #2196f3;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }
    
    #audio-btn:hover {
        background: #1976d2;
    }
    
    /* 调整地图容器位置，避免被UI元素遮挡 */
    .folium-map {
        top: 60px !important;
        height: calc(100% - 60px) !important;
    }
    
    /* 选中点发光效果 */
    .selected-marker {
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.8));
        }
        to {
            filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.8)) drop-shadow(0 0 20px rgba(255, 0, 0, 0.6));
        }
    }
</style>
'''
custom_js = '''
<script>
    // 当前选中的节点索引
    let currentNodeIndex = 0;
    const totalNodes = %d;
    
    // 长征路线点数据
    const waypoints = %s;
    
    // 添加左侧悬浮窗
    const progressPanel = document.createElement('div');
    progressPanel.id = 'progress-panel';
    progressPanel.innerHTML = `
        <h3>长征进度</h3>
        <div id="progress-info">
            <div>第 <span id="current-step">1</span> / <span id="total-steps">${totalNodes}</span> 站</div>
            <div id="progress-bar"><div id="progress-fill"></div></div>
            <div id="current-location">${waypoints[0].name}</div>
        </div>
        <button id="prev-btn" class="control-btn" disabled>上一站</button>
        <button id="next-btn" class="control-btn">下一站</button>
        <div id="audio-control">
            <button id="audio-btn">🔊 播放音效</button>
        </div>
    `;
    document.body.appendChild(progressPanel);
    
    // 添加顶部标志
    const headerBanner = document.createElement('div');
    headerBanner.id = 'header-banner';
    headerBanner.innerHTML = '<h1>红军长征路线图</h1>';
    document.body.insertBefore(headerBanner, document.body.firstChild);
    
    // 添加右侧详情页
    const detailsPanel = document.createElement('div');
    detailsPanel.id = 'details-panel';
    detailsPanel.innerHTML = `
        <!-- 关闭按钮 - 确保样式正确 -->
        <button class="close-btn" onclick="closeDetails()" style="
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: 30px;
            height: 30px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1002;
            color: #333;
            font-size: 20px;
            line-height: 1;
            padding: 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        ">×</button>
        <h2 id="detail-name">${waypoints[0].name}</h2>
        <h3 id="detail-description">${waypoints[0].description}</h3>
        
        <!-- 地点简介 -->
        <div class="detail-section">
            <h4>地点简介</h4>
            <p id="detail-introduction">${waypoints[0].introduction}</p>
        </div>
        
        <!-- 主要事件 -->
        <div class="detail-section">
            <h4>主要事件</h4>
            <p id="detail-events">${waypoints[0].events}</p>
        </div>
        
        <!-- 详细故事 -->
        <div class="detail-section">
            <h4>详细故事</h4>
            <p id="detail-story">${waypoints[0].story}</p>
        </div>
    `;
    document.body.appendChild(detailsPanel);
    
    // 创建Web Audio API音效系统（完全不依赖外部资源）
    class MarchingSoundEffect {
        constructor() {
            this.audioContext = null;
            this.isPlaying = false;
            this.loopInterval = null;
        }
        
        // 初始化音频上下文
        init() {
            if (!this.audioContext) {
                try {
                    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    return true;
                } catch (e) {
                    console.log('无法初始化音频上下文:', e);
                    return false;
                }
            }
            return true;
        }
        
        // 播放行军风格的音效
        playMarchingSound() {
            if (!this.init()) return false;
            
            // 如果音频上下文被暂停，恢复它
            if (this.audioContext.state === 'suspended') {
                this.audioContext.resume();
            }
            
            // 创建鼓点音效
            this.createDrumBeat();
            return true;
        }
        
        // 创建鼓点音效
        createDrumBeat() {
            // 创建一个简单的两拍子鼓点
            const now = this.audioContext.currentTime;
            
            // 低音鼓
            this.playDrumSound(now, 40, 0.2, 0.15);
            this.playDrumSound(now + 0.5, 40, 0.2, 0.15);
            
            // 军鼓
            this.playSnareSound(now + 0.25, 150, 0.1, 0.1);
            this.playSnareSound(now + 0.75, 150, 0.1, 0.1);
        }
        
        // 播放鼓声
        playDrumSound(startTime, frequency, duration, volume) {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.type = 'sine';
            oscillator.frequency.value = frequency;
            
            gainNode.gain.setValueAtTime(0, startTime);
            gainNode.gain.linearRampToValueAtTime(volume, startTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
            
            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
        }
        
        // 播放军鼓声音
        playSnareSound(startTime, frequency, duration, volume) {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.type = 'square';
            oscillator.frequency.value = frequency;
            
            // 快速变化频率模拟军鼓声音
            oscillator.frequency.exponentialRampToValueAtTime(frequency * 0.5, startTime + duration * 0.3);
            
            gainNode.gain.setValueAtTime(0, startTime);
            gainNode.gain.linearRampToValueAtTime(volume, startTime + 0.005);
            gainNode.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
            
            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
        }
        
        // 播放胜利号角音效
        playFanfare() {
            if (!this.init()) return false;
            
            if (this.audioContext.state === 'suspended') {
                this.audioContext.resume();
            }
            
            const now = this.audioContext.currentTime;
            const notes = [261.63, 329.63, 392.00, 523.25]; // C4, E4, G4, C5
            const noteDuration = 0.3;
            
            notes.forEach((note, index) => {
                this.playTrumpetNote(now + index * noteDuration, note, noteDuration * 0.9);
            });
            
            return true;
        }
        
        // 播放小号音符
        playTrumpetNote(startTime, frequency, duration) {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.type = 'triangle';
            oscillator.frequency.value = frequency;
            
            // 颤音效果
            const vibrato = this.audioContext.createOscillator();
            const vibratoGain = this.audioContext.createGain();
            
            vibrato.type = 'sine';
            vibrato.frequency.value = 5;
            vibratoGain.gain.value = 2;
            
            vibrato.connect(vibratoGain);
            vibratoGain.connect(oscillator.frequency);
            
            gainNode.gain.setValueAtTime(0, startTime);
            gainNode.gain.linearRampToValueAtTime(0.1, startTime + 0.05);
            gainNode.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
            
            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
            vibrato.start(startTime);
            vibrato.stop(startTime + duration);
        }
    }
    
    // 创建音效实例
    const soundEffect = new MarchingSoundEffect();
    
    // 封装播放音效函数
    window.playSoundEffect = function() {
        // 随机播放行军鼓或胜利号角音效
        const success = Math.random() > 0.5 ? 
            soundEffect.playMarchingSound() : 
            soundEffect.playFanfare();
        
        // 提供视觉反馈
        const audioBtn = document.getElementById('audio-btn');
        const originalText = audioBtn.textContent;
        
        if (success) {
            audioBtn.textContent = '🎵 音效已播放';
        } else {
            audioBtn.textContent = '🔊 浏览器不支持音效';
        }
        
        setTimeout(() => {
            audioBtn.textContent = originalText;
        }, 1500);
        
        return success;
    };
    
    // 获取地图对象的辅助函数
    function getMap() {
        // 查找所有folium地图实例
        for (let key in window) {
            if (window.hasOwnProperty(key) && key.startsWith('map_') && window[key] instanceof L.Map) {
                return window[key];
            }
        }
        return null;
    }
    
    // 更新选中点的发光效果
    function updateMarkerGlow(index) {
        // 移除所有标记的发光效果
        const markers = document.querySelectorAll('.leaflet-marker-icon');
        markers.forEach(marker => marker.classList.remove('selected-marker'));
        
        // 为当前选中的标记添加发光效果
        if (markers.length > index && index >= 0) {
            markers[index].classList.add('selected-marker');
        }
    }
    
    // 更新进度显示
    function updateProgress(index) {
        currentNodeIndex = index;
        const progressPercent = ((index + 1) / totalNodes) * 100;
        
        document.getElementById('current-step').textContent = index + 1;
        document.getElementById('progress-fill').style.width = `${progressPercent}%`;
        document.getElementById('current-location').textContent = waypoints[index].name;
        
        // 更新按钮状态
        document.getElementById('prev-btn').disabled = index === 0;
        document.getElementById('next-btn').disabled = index === totalNodes - 1;
        
        // 定义需要高亮的关键词列表
        const keywords = ['红军', '长征', '毛泽东', '瑞金', '遵义', '赤水', '雪山', '草地', '吴起镇', '会师', '毛泽东', '周恩来', '朱德'];
        
        // 高亮关键词的函数
        function highlightKeywords(text) {
            let highlightedText = text;
            keywords.forEach(keyword => {
                const regex = new RegExp(`(${keyword})`, 'g');
                highlightedText = highlightedText.replace(regex, '<span style="color: #d32f2f; font-weight: bold;">$1</span>');
            });
            return highlightedText;
        }
        
        // 更新详情面板，对内容进行关键词高亮处理
        document.getElementById('detail-name').textContent = waypoints[index].name;
        document.getElementById('detail-description').textContent = waypoints[index].description;
        document.getElementById('detail-introduction').innerHTML = highlightKeywords(waypoints[index].introduction);
        document.getElementById('detail-events').innerHTML = highlightKeywords(waypoints[index].events);
        document.getElementById('detail-story').innerHTML = highlightKeywords(waypoints[index].story);
        
        // 居中显示当前点并设置缩放级别为10km视图（约12级）
        const map = getMap();
        if (map) {
            map.setView(waypoints[index].location, 11); // 从12调整为11，显示约20km视图范围
        }
        
        // 更新标记发光效果
        updateMarkerGlow(index);
        
        // 自动触发标记的弹出浮窗
        openMarkerPopup(index);
    }
    
    // 打开指定标记的弹出浮窗
    function openMarkerPopup(index) {
        const map = getMap();
        if (!map) return;
        
        // 查找对应索引的标记
        const markers = document.querySelectorAll('.leaflet-marker-icon');
        if (markers.length > index && index >= 0) {
            // 触发点击事件以打开浮窗
            markers[index].click();
        }
    }
    
    // 增强发光动效
    function updateMarkerGlow(index) {
        // 移除所有标记的发光效果
        const markers = document.querySelectorAll('.leaflet-marker-icon');
        markers.forEach(marker => marker.classList.remove('selected-marker'));
        
        // 为当前选中的标记添加发光效果
        if (markers.length > index && index >= 0) {
            markers[index].classList.add('selected-marker');
        }
    }
    
    // 添加CSS动画样式
    function addWalkingAnimation() {
        const style = document.createElement('style');
        style.textContent = `
            /* 线段动画样式 */
            .animated-path {
                stroke-dasharray: 15, 5;
                stroke-linecap: round;
                animation: dash 30s linear infinite;
            }
            
            @keyframes dash {
                to {
                    stroke-dashoffset: -1000;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // 打开详情面板
    function openDetails() {
        // 确保detailsPanel变量已正确初始化
        const detailsPanel = document.getElementById('details-panel');
        if (detailsPanel) {
            detailsPanel.classList.add('show');
        }
    }
    
    // 关闭详情面板
    function closeDetails() {
        const detailsPanel = document.getElementById('details-panel');
        if (detailsPanel) {
            detailsPanel.classList.remove('show');
        }
    }
    
    // 为线段添加动画效果
    function animatePaths() {
        // 查找地图上的所有PolyLine元素
        const pathElements = document.querySelectorAll('svg path.leaflet-interactive');
        pathElements.forEach(path => {
            path.classList.add('animated-path');
        });
    }
    
    // 确保closeDetails函数在全局作用域可用
    window.closeDetails = closeDetails;
    
    // 根据节点索引打开详情面板
    function openDetailsForNode(index) {
        updateProgress(index);
        openDetails();
    }
    
    // 添加按钮事件监听
    document.getElementById('prev-btn').addEventListener('click', function() {
        if (currentNodeIndex > 0) {
            updateProgress(currentNodeIndex - 1);
            // 不再自动打开详情面板
        }
    });
    
    document.getElementById('next-btn').addEventListener('click', function() {
        if (currentNodeIndex < totalNodes - 1) {
            updateProgress(currentNodeIndex + 1);
            // 不再自动打开详情面板
        }
    });
    
    // 音效控制 - 使用Web Audio API生成的内置音效
    document.getElementById('audio-btn').addEventListener('click', function() {
        // 播放音效（行军鼓或胜利号角随机选择）
        playSoundEffect();
    });
    
    // 为上一站/下一站按钮添加音效
    document.getElementById('prev-btn').addEventListener('click', function() {
        if (currentNodeIndex > 0) {
            // 播放短音效
            playSoundEffect();
        }
    });
    
    document.getElementById('next-btn').addEventListener('click', function() {
        if (currentNodeIndex < totalNodes - 1) {
            // 播放短音效
            playSoundEffect();
        }
    });
    
    // 添加行走动画样式
    addWalkingAnimation();
    
    // 为线段添加动画效果
    setTimeout(animatePaths, 2000);
    
    // 添加可拖拽的小士兵
    addSoldier();
    
    // 初始化进度
    updateProgress(0);
    
    // 为地图上的标记添加点击事件
    // 注意：这部分需要在地图完全加载后执行
    setTimeout(function() {
        const markers = document.querySelectorAll('.leaflet-marker-icon');
        markers.forEach((marker, index) => {
            marker.addEventListener('click', function(e) {
                // 阻止事件冒泡，避免循环调用
                e.stopPropagation();
                updateProgress(index);
                // 调用openDetails函数打开详情页
                openDetails();
                // 确保浮窗能正确弹出
                if (marker._icon && marker._icon.parentNode && marker._icon.parentNode._popup) {
                    marker._icon.parentNode.openPopup();
                }
            });
        });
    }, 1000);
    
    // 添加CSS样式使详情面板可见
    setTimeout(function() {
        const style = document.createElement('style');
        style.textContent = `
            #details-panel.show {
                right: 0;
            }
            
            /* 红军小人样式 */
            #soldier {
                position: absolute;
                width: 40px;
                height: 60px;
                cursor: move;
                z-index: 999;
                transform-origin: center bottom;
                pointer-events: all;
            }
            
            #soldier.dragging {
                opacity: 0.8;
                transform: scale(1.1);
            }
            
            /* 红军小人行走动画 */
            @keyframes walk {
                0%, 100% {
                    transform: translateY(0) rotate(0deg);
                }
                25% {
                    transform: translateY(-5px) rotate(-3deg);
                }
                50% {
                    transform: translateY(0) rotate(3deg);
                }
                75% {
                    transform: translateY(-5px) rotate(-2deg);
                }
            }
            
            #soldier.walking {
                animation: walk 0.6s infinite ease-in-out;
            }
            
            /* 红军小人组件 */
            .soldier-body {
                position: relative;
                width: 40px;
                height: 60px;
            }
            
            .soldier-head {
                position: absolute;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 24px;
                height: 24px;
                background-color: #f5d0c5;
                border-radius: 50%;
                border: 2px solid #000;
            }
            
            .soldier-uniform {
                position: absolute;
                top: 24px;
                left: 50%;
                transform: translateX(-50%);
                width: 30px;
                height: 20px;
                background-color: #d32f2f;
                border: 2px solid #000;
            }
            
            .soldier-legs {
                position: absolute;
                top: 44px;
                left: 50%;
                transform: translateX(-50%);
                width: 20px;
                height: 16px;
                display: flex;
                justify-content: space-between;
            }
            
            .soldier-left-leg,
            .soldier-right-leg {
                width: 6px;
                height: 16px;
                background-color: #212121;
                border: 1px solid #000;
                position: relative;
            }
            
            .soldier-arms {
                position: absolute;
                top: 28px;
                left: 50%;
                transform: translateX(-50%);
                width: 40px;
                height: 8px;
                display: flex;
                justify-content: space-between;
            }
            
            .soldier-left-arm,
            .soldier-right-arm {
                width: 12px;
                height: 8px;
                background-color: #d32f2f;
                border: 1px solid #000;
            }
            
            /* 行走时的手脚动画 */
            #soldier.walking .soldier-left-leg {
                animation: leg-move 0.6s infinite ease-in-out;
            }
            
            #soldier.walking .soldier-right-leg {
                animation: leg-move 0.6s infinite ease-in-out 0.3s;
            }
            
            #soldier.walking .soldier-left-arm {
                animation: arm-move 0.6s infinite ease-in-out 0.3s;
            }
            
            #soldier.walking .soldier-right-arm {
                animation: arm-move 0.6s infinite ease-in-out;
            }
            
            @keyframes leg-move {
                0%, 100% {
                    transform: rotate(0deg);
                }
                50% {
                    transform: rotate(-20deg);
                }
            }
            
            @keyframes arm-move {
                0%, 100% {
                    transform: rotate(0deg);
                }
                50% {
                    transform: rotate(20deg);
                }
            }
        `;
        document.head.appendChild(style);
    }, 500);
    
    // 添加可拖拽的小人
    function addSoldier() {
        const soldier = document.createElement('div');
        soldier.id = 'soldier';
        
        // 创建带有手和脚的小人HTML结构
        soldier.innerHTML = `
            <div class="soldier-body">
                <div class="soldier-head"></div>
                <div class="soldier-uniform"></div>
                <div class="soldier-arms">
                    <div class="soldier-left-arm"></div>
                    <div class="soldier-right-arm"></div>
                </div>
                <div class="soldier-legs">
                    <div class="soldier-left-leg"></div>
                    <div class="soldier-right-leg"></div>
                </div>
            </div>
        `;
        
        // 设置初始位置
        soldier.style.left = '60px';
        soldier.style.bottom = '60px';
        
        document.body.appendChild(soldier);
        
        let isDragging = false;
        let currentX, currentY, initialX, initialY;
        let pathIndex = -1;
        let isWalking = false;
        
        // 获取所有路线元素
        function getPathElements() {
            return document.querySelectorAll('svg path.leaflet-interactive');
        }
        
        // 检查点是否在路径上
        function isPointOnPath(x, y, pathElement) {
            // 获取SVG元素
            const svgElement = pathElement.closest('svg');
            if (!svgElement) return false;
            
            const svgRect = svgElement.getBoundingClientRect();
            
            // 检查点击位置是否在SVG矩形内
            if (x < svgRect.left || x > svgRect.right || y < svgRect.top || y > svgRect.bottom) {
                return false;
            }
            
            // 获取SVG的CTM(Current Transformation Matrix)以将屏幕坐标转换为SVG坐标
            const point = svgElement.createSVGPoint();
            point.x = x;
            point.y = y;
            
            // 获取SVG元素的坐标系中的点
            const transformedPoint = point.matrixTransform(svgElement.getScreenCTM().inverse());
            
            // 使用isPointInStroke和isPointInFill来检测点是否在线上
            const isInStroke = pathElement.isPointInStroke(transformedPoint);
            const isInFill = pathElement.isPointInFill(transformedPoint);
            
            // 使用getPointAtLength进行更精确的检测
            const pathLength = pathElement.getTotalLength();
            
            // 增加采样密度以提高检测精度
            for (let i = 0; i <= pathLength; i += 1) {
                const pathPoint = pathElement.getPointAtLength(i);
                const distance = Math.sqrt(
                    Math.pow(transformedPoint.x - pathPoint.x, 2) + 
                    Math.pow(transformedPoint.y - pathPoint.y, 2)
                );
                
                // 扩大检测范围以提高成功率
                if (distance < 15) {
                    return true;
                }
            }
            
            return isInStroke || isInFill;
        }
        
        // 找到小士兵所在的路径索引
        function findPathIndex(x, y) {
            const paths = getPathElements();
            for (let i = 0; i < paths.length; i++) {
                // 直接传递绝对坐标给isPointOnPath
                if (isPointOnPath(x, y, paths[i])) {
                    console.log('找到路径索引:', i);
                    return i;
                }
            }
            console.log('未找到路径');
            return -1;
        }
        
        // 沿路径移动小人
    function moveAlongPath(pathIndex, duration = 20000) { // 减慢速度为20秒
        const paths = getPathElements();
        if (pathIndex < 0 || pathIndex >= paths.length) return;
        
        // 开始行走动画
        isWalking = true;
        soldier.classList.add('walking');
        
        const path = paths[pathIndex];
        const pathLength = path.getTotalLength();
        let startTime = null;
        let currentProgress = 0; // 保存当前行走进度
        
        function move(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = currentProgress + (timestamp - startTime) / duration;
            
            if (progress < 1 && isWalking) {
                const point = path.getPointAtLength(progress * pathLength);
                
                // 获取地图容器位置
                const mapContainer = document.querySelector('.map-container, .folium-map') || document.querySelector('.folium-map');
                if (!mapContainer) {
                    console.error('地图容器未找到');
                    return;
                }
                
                const mapRect = mapContainer.getBoundingClientRect();
                const svgElement = path.closest('svg');
                
                if (svgElement) {
                    const svgRect = svgElement.getBoundingClientRect();
                    
                    // 计算小人在地图中的绝对位置（不受地图拖拽影响）
                    const mapX = point.x + svgRect.left - mapRect.left - 20; // 减去小人宽度的一半使其居中
                    const mapY = point.y + svgRect.top - mapRect.top - 30; // 减去小人高度使其脚踩在线上
                    
                    // 设置小人位置（相对于地图容器）
                    soldier.style.position = 'absolute';
                    soldier.style.left = mapX + 'px';
                    soldier.style.top = mapY + 'px';
                    soldier.style.bottom = 'auto';
                    
                    // 确保小人始终显示在地图上方
                    soldier.style.zIndex = '999';
                }
                
                // 确保动画持续进行
                if (typeof window.requestAnimationFrame === 'function') {
                    requestAnimationFrame(move);
                } else {
                    // 降级方案 - 使用setTimeout作为后备
                    setTimeout(() => move(Date.now()), 16); // 约60fps
                }
            } else {
                // 移动结束
                isWalking = false;
                soldier.classList.remove('walking');
                
                // 移动到下一站
                currentNodeIndex = Math.min(currentNodeIndex + 1, totalNodes - 1);
                updateProgress(currentNodeIndex);
            }
        }
        
        // 确保动画开始，并重置startTime确保从路径起点开始
        startTime = null;
        if (typeof window.requestAnimationFrame === 'function') {
            requestAnimationFrame(move);
        } else {
            // 降级方案
            move(Date.now());
        }
        console.log('开始沿路径移动小人，路径索引:', pathIndex);
    }
        
        // 鼠标按下事件
        soldier.addEventListener('mousedown', function(e) {
            // 停止行走动画
            if (isWalking) {
                isWalking = false;
                soldier.classList.remove('walking');
            }
            
            initialX = e.clientX;
            initialY = e.clientY;
            isDragging = true;
            soldier.classList.add('dragging');
            
            // 改变为固定定位以便拖拽
            soldier.style.position = 'fixed';
        });
        
        // 鼠标移动事件
        document.addEventListener('mousemove', function(e) {
            if (isDragging) {
                e.preventDefault();
                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;
                initialX = e.clientX;
                initialY = e.clientY;
                
                const newLeft = parseInt(soldier.style.left || '60px') + currentX;
                const newBottom = parseInt(soldier.style.bottom || '60px') - currentY;
                
                // 限制在视口内
                if (newLeft > 0 && newLeft < window.innerWidth - 40) {
                    soldier.style.left = newLeft + 'px';
                }
                if (newBottom > 0 && newBottom < window.innerHeight - 40) {
                    soldier.style.bottom = newBottom + 'px';
                }
            }
        });
        
        // 鼠标释放事件
        document.addEventListener('mouseup', function() {
            if (isDragging) {
                isDragging = false;
                soldier.classList.remove('dragging');
                
                // 检查是否在路线上
                const rect = soldier.getBoundingClientRect();
                const x = rect.left + rect.width / 2;
                const y = rect.top + rect.height / 2;
                const newPathIndex = findPathIndex(x, y);
                
                if (newPathIndex !== -1 && newPathIndex !== pathIndex) {
                    pathIndex = newPathIndex;
                    // 沿路线移动
                    moveAlongPath(pathIndex);
                    playSoundEffect();
                }
            }
        });
        
        // 监听地图拖动事件，确保小人在行走时不受影响
        const map = getMap();
        if (map) {
            map.on('dragstart', function() {
                if (isWalking) {
                    // 保存当前位置
                    const rect = soldier.getBoundingClientRect();
                    const mapContainer = document.querySelector('.map-container, .folium-map');
                    const mapRect = mapContainer.getBoundingClientRect();
                    
                    // 保存当前进度
                    if (startTime) {
                        const elapsedTime = Date.now() - startTime;
                        currentProgress = Math.min(elapsedTime / duration, 1);
                    }
                    
                    // 转换为相对于地图的位置
                    soldier.style.position = 'absolute';
                    soldier.style.left = (rect.left - mapRect.left) + 'px';
                    soldier.style.top = (rect.top - mapRect.top) + 'px';
                    soldier.style.bottom = 'auto';
                }
            });
            
            map.on('dragend', function() {
                if (isWalking) {
                    // 继续行走动画，从保存的进度继续
                    if (pathIndex !== -1) {
                        // 重置startTime但保留进度
                        startTime = null;
                        if (typeof window.requestAnimationFrame === 'function') {
                            requestAnimationFrame(move);
                        } else {
                            move(Date.now());
                        }
                    }
                }
            });
        }
    }
</script>
'''
# 将长征路线点数据转换为JSON字符串
waypoints_json = json.dumps(long_march_waypoints, ensure_ascii=False)

# 替换JS中的占位符 - 使用format方法避免格式冲突
custom_js = custom_js.replace('%d', str(len(long_march_waypoints))).replace('%s', waypoints_json)

# 将自定义CSS和JS添加到地图
china_map.get_root().html.add_child(folium.Element(custom_css))
china_map.get_root().html.add_child(folium.Element(custom_js))

# 保存地图为HTML文件
china_map.save('china_map.html')

print("中国地图（含红军长征路线）已成功生成并保存为 'china_map.html' 文件。")
print("请在浏览器中打开该文件查看增强版地图，包括长征路线、左右侧悬浮窗、顶部标志和详情页面。")