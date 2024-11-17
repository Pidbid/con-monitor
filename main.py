import asyncio
import subprocess
import time
from datetime import datetime

# 定义网络接口名称
INTERFACE = "wlan0"

# 定义Wi-Fi网络名称和密码
SSID = "SSID"
PASSWORD = "PASSWORD"

# 定义失败几次重新连接
TIMES = 3

# 定义检测网络连接的间隔时间（秒）
INTERVAL = 60

async def run_command(command):
    """异步执行命令"""
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout, stderr, process.returncode

async def check_connection():
    """异步检测网络连接状态"""
    command = ["ping", "-c", "1", "baidu.com"]
    stdout, stderr, returncode = await run_command(command)
    
    if returncode == 0:
        output = stdout.decode("utf-8")
        if "1 packets received" in output:
            print(datetime.now(), "internet connection success")
            return True
        else:
            print(datetime.now(), "Network connection lost. Reconnecting...")
            return False
    else:
        print(datetime.now(), "Network connection lost. Reconnecting...")
        return False

async def reconnect_wifi():
    """异步重新连接Wi-Fi"""
    # 关闭Wi-Fi接口
    await run_command(["sudo", "ifconfig", INTERFACE, "down"])
    await asyncio.sleep(2)

    # 重新启动Wi-Fi接口
    await run_command(["sudo", "ifconfig", INTERFACE, "up"])
    await asyncio.sleep(2)

    # 连接到Wi-Fi网络
    await run_command(["sudo", "nmcli", "device", "wifi", "connect", SSID, "password", PASSWORD])
    await asyncio.sleep(5)

async def main():
    count = 0
    while True:
        if not await check_connection():
            count += 1
            if count >= TIMES:
                await reconnect_wifi()
                count = 0  # 重置计数器
        else:
            count = 0  # 如果网络连接正常，重置计数器
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())