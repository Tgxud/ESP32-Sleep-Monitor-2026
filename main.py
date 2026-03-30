from machine import Pin
import time

# 引脚定义
trig = Pin(25, Pin.OUT)
echo = Pin(33, Pin.IN)

# 上一次有效距离（用于滤波）
last_distance = 0

# 最大允许变化幅度（超过这个值视为突变，过滤掉）
MAX_CHANGE = 15

# 有效距离范围（已修改为 2cm 起步）
MIN_DISTANCE = 2   # 小于2cm：过近，无效
MAX_DISTANCE = 300 # 大于300cm：无人，无效

while True:
    # 发送触发信号
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # 计时
    while echo.value() == 0:
        start = time.ticks_us()
    while echo.value() == 1:
        end = time.ticks_us()

    # 计算距离
    duration = time.ticks_diff(end, start)
    dist = duration * 0.034 / 2

    # ===================== 过滤开始 =====================
    # 1. 过滤过近 / 过远的无效数据
    if dist < MIN_DISTANCE or dist > MAX_DISTANCE:
        print("无效数据：距离异常")
        time.sleep(0.5)
        continue

    # 2. 过滤大幅度突变（防止干扰）
    if last_distance != 0:
        change = abs(dist - last_distance)
        if change > MAX_CHANGE:
            print("无效数据：距离突变")
            time.sleep(0.5)
            continue

    # 3. 只有有效数据才更新并输出
    last_distance = dist
    print(f"有效距离：{last_distance:.2f} cm")

    # ===================== 过滤结束 =====================
    time.sleep(0.5)