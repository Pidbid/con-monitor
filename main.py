import subprocess
import time

# 定义网络接口名称
INTERFACE = "wlan0"

# 定义Wi-Fi网络名称和密码
SSID = "SSID"
PASSWORD = "PASSWORD"

# 定义检测网络连接的间隔时间（秒）
INTERVAL = 300

def check_connection():
    """检测网络连接状态"""
    try:
        subprocess.check_output(["ping", "-c", "1", "8.8.8.8"], stderr=subprocess.STDOUT, timeout=5)
        print("Network is up.")
        return True
    except subprocess.CalledProcessError:
        print("Network connection lost. Reconnecting...")
        return False

def reconnect_wifi():
    """重新连接Wi-Fi"""
    # 关闭Wi-Fi接口
    subprocess.run(["sudo", "ifconfig", INTERFACE, "down"])
    time.sleep(2)

    # 重新启动Wi-Fi接口
    subprocess.run(["sudo", "ifconfig", INTERFACE, "up"])
    time.sleep(2)

    # 连接到Wi-Fi网络
    subprocess.run(["sudo", "nmcli", "device", "wifi", "connect", SSID, "password", PASSWORD])
    time.sleep(5)

def main():
    while True:
        if not check_connection():
            reconnect_wifi()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()