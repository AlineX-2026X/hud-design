#!/usr/bin/env python3
# 由 hero.html（英文版）生成 hero-zh.html（中文版）。
# 单一源文件 + 文案映射，避免两份布局各自漂移。
import sys

SRC = 'hero.html'
DST = 'hero-zh.html'

MAP = [
    # 顶栏
    ('>RECON&#8209;3<', '>侦察&#8209;3<'),
    ('COMBINED ARMS &nbsp;/&nbsp; SECTOR 07', '合成部队 &nbsp;/&nbsp; 第07区域'),
    ('OP <b>IRON VEIL</b><br>DAY <b>02</b> &nbsp;&#183;&nbsp; WX CLR<br>RULES <b>ROE-2</b>',
     '行动 <b>铁幕</b><br>第 <b>02</b> 天 &nbsp;&#183;&nbsp; 天气晴朗<br>规则 <b>ROE-2</b>'),
    ('MAG 037&#176; &nbsp;&nbsp;&#183;&nbsp;&nbsp; TRUE 041&#176;', '磁方位 037&#176; &nbsp;&nbsp;&#183;&nbsp;&nbsp; 真方位 041&#176;'),
    ("<span>BRG<b>041&#176;14'</b></span>", "<span>方位<b>041&#176;14'</b></span>"),
    ('<span>GRID<b>34.2N 118.6E</b></span>', '<span>网格<b>34.2N 118.6E</b></span>'),
    ('<span>ALT<b>420 M</b></span>', '<span>高度<b>420 米</b></span>'),
    ('<span>SPD<b>18 KM/H</b></span>', '<span>速度<b>18 公里/时</b></span>'),
    ('LINK 98.2% &nbsp;/&nbsp; AES-256 &nbsp;/&nbsp; NODE 06-A', '链路 98.2% &nbsp;/&nbsp; AES-256 &nbsp;/&nbsp; 节点 06-A'),

    # 左轨
    ('<span class="t9">Formation</span><em>6 ASSETS</em>', '<span class="t9">编队</span><em>共 6 架</em>'),
    ('SCOUT LEAD', '侦察长机'), ('SCOUT LEFT', '侦察左翼'), ('SCOUT RIGHT', '侦察右翼'),
    ('RELAY</span>', '中继</span>'), ('THERMAL</span>', '红外</span>'), ('STANDBY', '待命'),
    ('<span class="t9">Spectrum 2.4&#8211;5.8 GHz</span><em>SNR 21 dB</em>',
     '<span class="t9">频谱 2.4&#8211;5.8 GHz</span><em>信噪比 21 dB</em>'),
    ('<span class="t9">Mission clock</span><em>T+03:41</em>', '<span class="t9">任务时钟</span><em>T+03:41</em>'),
    ('<span>UAV-02 handover &#8594; 01</span>', '<span>02&#8594;01 链路交接</span>'),
    ('<span>Mesh rebuild &#183; 1.2 M pts</span>', '<span>地形网格重建 &#183; 120 万点</span>'),
    ('<span>Route corridor widened</span>', '<span>航线走廊加宽</span>'),
    ('<span>HOSTILE &#183; TGT-04</span>', '<span>敌情 &#183; 目标04</span>'),
    ('<span>ROE-2 acknowledged</span>', '<span>交战规则 ROE-2 确认</span>'),

    # 中央
    ('ALERT &nbsp;HOSTILE CONTACT', '告警 &nbsp;敌方接触'),
    ('<em>TGT-04 &nbsp;/&nbsp; 2.4 KM &nbsp;/&nbsp; CONF 0.64</em>', '<em>目标04 &nbsp;/&nbsp; 2.4 公里 &nbsp;/&nbsp; 置信 0.64</em>'),
    ('SECTOR 07 &nbsp;//&nbsp; <b>VALLEY APPROACH</b> &nbsp;&#183;&nbsp; MESH 1.2 M',
     '第07区域 &nbsp;//&nbsp; <b>谷地接近路线</b> &nbsp;&#183;&nbsp; 网格 1.2 米'),
    ('>MESH / 41.2K TRI<', '>网格 / 4.12 万面<'),
    ('>TRACK VECTOR / INBOUND<', '>航迹矢量 / 接近<'),
    ('>THERMAL 34.6&#176;C<', '>红外 34.6&#176;C<'),
    ('>CONVOY / 4 VEH<', '>车队 / 4 车<'),
    ('>RANGE 1.1 KM<', '>距离 1.1 公里<'),
    ('>RELAY HOP / 12 MS<', '>中继 / 12 毫秒<'),
    ('<span class="n">TGT-02</span><span class="m">VEHICLE / TRUCK</span>', '<span class="n">目标02</span><span class="m">车辆 / 卡车</span>'),
    ('<span class="n">TGT-03</span><span class="m">STRUCTURE</span>', '<span class="n">目标03</span><span class="m">建筑</span>'),
    ('<span class="n">TGT-04</span><span class="m">HOSTILE / 2 CREW</span>', '<span class="n">目标04</span><span class="m">敌方 / 2 人</span>'),
    ('<span class="n">TGT-01</span><span class="m">CONVOY LEAD / WHEELED</span>', '<span class="n">目标01</span><span class="m">车队前导 / 轮式</span>'),
    ('>PRIORITY<', '>最高优先<'),
    ('<span>CONF<b>0.91</b></span><span>1.8 KM</span>', '<span>置信 <b>0.91</b></span><span>1.8 公里</span>'),
    ('<span>CONF<b>0.78</b></span><span>1.1 KM</span>', '<span>置信 <b>0.78</b></span><span>1.1 公里</span>'),
    ('<span>CONF<b>0.64</b></span><span>2.4 KM</span>', '<span>置信 <b>0.64</b></span><span>2.4 公里</span>'),
    ('<div class="k">RANGE</div><div class="v">0.8<small>KM</small></div>', '<div class="k">距离</div><div class="v">0.8<small>公里</small></div>'),
    ('<div class="k">BEARING</div><div class="v">037<small>DEG</small></div>', '<div class="k">方位</div><div class="v">037<small>度</small></div>'),
    ('<div class="k">SPEED</div><div class="v">22<small>KM/H</small></div>', '<div class="k">速度</div><div class="v">22<small>公里/时</small></div>'),
    ('<div class="k">CONF</div><div class="v">0.94</div>', '<div class="k">置信</div><div class="v">0.94</div>'),
    ('<span>TRACKS <b>05</b></span>', '<span>航迹 <b>05</b></span>'),
    ('<span>FRAME <b>1080 / 60</b></span>', '<span>帧率 <b>1080 / 60</b></span>'),
    ('<span>DRAW CALLS <b>212</b></span>', '<span>绘制调用 <b>212</b></span>'),
    ('<span>OVERDRAW <b>&lt; 3.6x</b></span>', '<span>过绘制 <b>&lt; 3.6x</b></span>'),
    ('<span>ALERT PIXELS <b>4.1%</b></span>', '<span>告警像素 <b>4.1%</b></span>'),

    # 右轨
    ('<span class="t9">Track queue</span><em>5 &#183; SORT THREAT</em>', '<span class="t9">目标队列</span><em>5 个 &#183; 按威胁排序</em>'),
    ('<span>ID</span><span>CLASS / CONF</span><span>AGE</span>', '<span>编号</span><span>类型 / 置信</span><span>更新</span>'),
    ('<div class="id">TGT-01</div><div class="st"><i class="sq"></i>TRACKING</div>', '<div class="id">目标01</div><div class="st"><i class="sq"></i>跟踪中</div>'),
    ('<div class="id">TGT-02</div><div class="st"><i class="sq"></i>TRACKING</div>', '<div class="id">目标02</div><div class="st"><i class="sq"></i>跟踪中</div>'),
    ('<div class="id">TGT-03</div><div class="st"><i class="sq"></i>OBSERVED</div>', '<div class="id">目标03</div><div class="st"><i class="sq"></i>已观察</div>'),
    ('<div class="id" style="color:var(--alert)">TGT-04</div><div class="st hostile"><i class="tri"></i>HOSTILE</div>',
     '<div class="id" style="color:var(--alert)">目标04</div><div class="st hostile"><i class="tri"></i>敌方</div>'),
    ('<div class="id">TGT-05</div><div class="st"><i class="sq"></i>STALE</div>', '<div class="id">目标05</div><div class="st"><i class="sq"></i>过期</div>'),
    ('<div class="mid">CONVOY LEAD<br><b>0.94</b></div>', '<div class="mid">车队前导<br><b>0.94</b></div>'),
    ('<div class="mid">VEHICLE / TRUCK<br><b>0.91</b></div>', '<div class="mid">车辆 / 卡车<br><b>0.91</b></div>'),
    ('<div class="mid">STRUCTURE<br><b>0.78</b></div>', '<div class="mid">建筑<br><b>0.78</b></div>'),
    ('<div class="mid" style="color:rgba(255,59,48,.72)">CREW / SMALL ARMS', '<div class="mid" style="color:rgba(255,59,48,.72)">人员 / 轻武器'),
    ('<div class="mid" style="opacity:.55">UNKNOWN', '<div class="mid" style="opacity:.55">未知'),
    ('<span class="t9">Event stream</span><em>WINDOW 60 S</em>', '<span class="t9">事件流</span><em>60 秒窗口</em>'),
    ('<span>Priority re-rank &#8594; TGT-01</span>', '<span>优先级重排 &#8594; 目标01</span>'),
    ('<span>CONF &lt; 0.70 &#183; TGT-04</span>', '<span>置信 &lt; 0.70 &#183; 目标04</span>'),
    ('<span>UAV-05 thermal lock</span>', '<span>UAV-05 红外锁定</span>'),
    ('<span>LOD 0&#8594;1 &#183; draw &#8722;38%</span>', '<span>网格层级 0&#8594;1 &#183; 绘制 &#8722;38%</span>'),
    ('<span>Relay handshake OK</span>', '<span>中继握手正常</span>'),
    ('<span>Corridor deconflicted</span>', '<span>走廊冲突解除</span>'),

    # 底栏
    ('>Payload<', '>载荷<'), ('>Power<', '>电量<'), ('>Bandwidth<', '>带宽<'), ('>Latency<', '>时延<'),
    ('<small>MS</small>', '<small>毫秒</small>'),
    ('<div>HOLD</div><div class="on">ENGAGE</div><div>RTB</div>', '<div>保持</div><div class="on">交战</div><div>返航</div>'),
    ('<div class="age">12 S</div>', '<div class="age">12 秒</div>'),
    ('<div class="age">18 S</div>', '<div class="age">18 秒</div>'),
    ('<div class="age">41 S</div>', '<div class="age">41 秒</div>'),
    ('<div class="age" style="color:rgba(255,59,48,.8)">06 S</div>', '<div class="age" style="color:rgba(255,59,48,.8)">06 秒</div>'),
    ('<div class="age" style="opacity:.55">142 S</div>', '<div class="age" style="opacity:.55">142 秒</div>'),
]

OVERLAY = """
  /* —— 中文版排版覆盖 —— */
  body{font-family:"PingFang SC","Hiragino Sans GB","Source Han Sans SC","Microsoft YaHei",-apple-system,sans-serif}
  .t9{font-size:10.5px;letter-spacing:.16em}
  .t10,.t11{letter-spacing:.12em}
  .asset .nm{font-size:10px;letter-spacing:.10em}
  .log{font-size:10.5px}
  .log b{letter-spacing:.04em}
  .tq .mid{font-size:9.5px;letter-spacing:.10em}
  .st{letter-spacing:.10em}
  .phase{letter-spacing:.02em}
  .phase-sub{letter-spacing:.14em}
  .opbox{letter-spacing:.10em}
  .compass .deg,.bearings{letter-spacing:.08em}
  .link{letter-spacing:.10em}
  .alertbar{letter-spacing:.16em}
  .alertbar em{letter-spacing:.08em}
  .sector{letter-spacing:.14em}
  .foot{letter-spacing:.10em}
  .lock .tag .n{letter-spacing:.06em}
  .lock .tag .m{letter-spacing:.10em}
  .lock .meta{letter-spacing:.08em}
  .primary .prio{letter-spacing:.18em}
  .primary .kpi .k{letter-spacing:.12em}
  .cmd div{letter-spacing:.18em}
  .ph em{letter-spacing:.10em}
  .spec-axis{letter-spacing:.06em}
"""


def main():
    s = open(SRC, encoding='utf-8').read()
    miss = []
    for a, b in MAP:
        if a in s:
            s = s.replace(a, b, 1)
        else:
            miss.append(a[:60])
    s = s.replace('</style>', OVERLAY + '</style>', 1)
    s = s.replace('<html lang="en">', '<html lang="zh-CN">', 1)
    s = s.replace('<title>TACTICAL SITUATION HUD</title>', '<title>战术态势 HUD</title>', 1)
    open(DST, 'w', encoding='utf-8').write(s)
    print(f'wrote {DST}; unmatched={len(miss)}')
    for m in miss:
        print('  MISS', m)
    return 1 if miss else 0


if __name__ == '__main__':
    sys.exit(main())
