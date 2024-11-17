import subprocess
import time

# 定义网络接口名称
INTERFACE = "wlan0"

# 定义Wi-Fi网络名称和密码
SSID = "SSID"
PASSWORD = "PASSWORD"

# 定义失败几次重新连接
TIMES = 3

# 定义检测网络连接的间隔时间（秒）
INTERVAL = 60

def check_connection():
    """检测网络连接状态"""
    try:
        subprocess.check_output(["ping", "-c", "1", "baidu.com"], stderr=subprocess.STDOUT, timeout=5)
        print("Network is up.")
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print("Network connection lost. Reconnecting...")
        return False

def reconnect_wifi():
    """重新连接Wi-Fi"""
    # 关闭Wi-Fi接口
    subprocess.run(["sudo", "ifconfig", INTERFACE, "down"], check=True)
    time.sleep(2)

    # 重新启动Wi-Fi接口
    subprocess.run(["sudo", "ifconfig", INTERFACE, "up"], check=True)
    time.sleep(2)

    # 连接到Wi-Fi网络
    subprocess.run(["sudo", "nmcli", "device", "wifi", "connect", SSID, "password", PASSWORD], check=True)
    time.sleep(5)

def main():
    count = 0
    while True:
        if not check_connection():
            count += 1
            if count >= TIMES:
                reconnect_wifi()
                count = 0  # 重置计数器
        else:
            count = 0  # 如果网络连接正常，重置计数器
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()