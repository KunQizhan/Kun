# 环境验证与测试指南

## 1. 概述

本文档提供完整的验证步骤，确保 Mini-SOC Lab 环境配置正确，所有组件正常工作。

## 2. 验证前准备

### 2.1 确认虚拟机状态

在 VirtualBox 中检查:
- ✅ SOC-Ubuntu-Server: 运行中
- ✅ Kali-Attack: 运行中
- ✅ 两台虚拟机都已配置双网卡

### 2.2 确认网络配置

**SOC Server**:
```bash
ip addr show | grep "192.168.56.10"
```

**Kali Attack**:
```bash
ip addr show | grep "192.168.56.20"
```

## 3. 基础网络验证

### 3.1 测试互联网连接

#### 3.1.1 SOC Server

```bash
# 测试 DNS 解析
nslookup google.com

# 测试网络连通性
ping -c 4 8.8.8.8
ping -c 4 www.google.com

# 测试 HTTP 连接
curl -I https://www.google.com

# 更新软件包 (最终测试)
sudo apt update
```

#### 3.1.2 Kali Attack

```bash
# 测试 DNS
nslookup kali.org

# 测试连通性
ping -c 4 8.8.8.8
ping -c 4 www.kali.org

# 测试 HTTP
curl -I https://www.kali.org

# 更新工具
sudo apt update
```

### 3.2 测试 Host-only 网络连通性

#### 3.2.1 从 SOC 到 Kali

在 SOC Server 上:
```bash
# ICMP (ping)
ping -c 4 192.168.56.20
ping -c 4 kali-attack

# 追踪路由
traceroute 192.168.56.20

# ARP 表
arp -a | grep 192.168.56.20
```

#### 3.2.2 从 Kali 到 SOC

在 Kali Attack 上:
```bash
# ICMP (ping)
ping -c 4 192.168.56.10
ping -c 4 soc-server

# 追踪路由
traceroute 192.168.56.10

# ARP 表
arp -a | grep 192.168.56.10
```

#### 3.2.3 从宿主机到虚拟机

在宿主机上:

**Windows**:
```cmd
ping 192.168.56.10
ping 192.168.56.20
```

**Linux/macOS**:
```bash
ping -c 4 192.168.56.10
ping -c 4 192.168.56.20
```

### 3.3 测试主机名解析

#### 3.3.1 SOC Server

```bash
# 解析 Kali 主机名
ping -c 2 kali-attack
ping -c 2 kali

# 查看 hosts 文件
cat /etc/hosts | grep kali
```

#### 3.3.2 Kali Attack

```bash
# 解析 SOC 主机名
ping -c 2 soc-server
ping -c 2 soc

# 查看 hosts 文件
cat /etc/hosts | grep soc
```

## 4. 服务验证

### 4.1 SSH 服务测试

#### 4.1.1 SOC Server SSH

在 SOC 上启动 SSH:
```bash
sudo systemctl start ssh
sudo systemctl enable ssh
sudo systemctl status ssh
```

从 Kali 连接:
```bash
# 测试 SSH 连接
ssh socadmin@192.168.56.10

# 或使用主机名
ssh socadmin@soc-server
```

从宿主机连接:
```bash
ssh socadmin@192.168.56.10
```

#### 4.1.2 Kali SSH

在 Kali 上启动 SSH:
```bash
sudo systemctl start ssh
sudo systemctl enable ssh
sudo systemctl status ssh
```

从 SOC 连接:
```bash
ssh kali@192.168.56.20
```

从宿主机连接:
```bash
ssh kali@192.168.56.20
```

### 4.2 Web 服务测试

#### 4.2.1 在 SOC 上部署测试 Web 服务

```bash
# 安装 nginx
sudo apt install -y nginx

# 启动服务
sudo systemctl start nginx
sudo systemctl enable nginx

# 创建测试页面
echo "<h1>SOC Server - Web Test</h1>" | sudo tee /var/www/html/index.html

# 检查服务
sudo systemctl status nginx
sudo netstat -tulpn | grep :80
```

#### 4.2.2 从 Kali 访问

```bash
# 使用 curl
curl http://192.168.56.10
curl http://soc-server

# 使用 wget
wget -O - http://192.168.56.10

# 使用浏览器
firefox http://192.168.56.10 &
```

#### 4.2.3 在 Kali 上部署测试 Web 服务

```bash
# 启动 Apache
sudo systemctl start apache2
sudo systemctl enable apache2

# 创建测试页面
echo "<h1>Kali Attack - Web Test</h1>" | sudo tee /var/www/html/index.html

# 检查服务
sudo systemctl status apache2
```

从 SOC 访问:
```bash
curl http://192.168.56.20
```

## 5. 安全工具验证

### 5.1 Nmap 扫描测试

#### 5.1.1 从 Kali 扫描 SOC

```bash
# 基础扫描
nmap 192.168.56.10

# 详细扫描
nmap -sV -O 192.168.56.10

# 全端口扫描
nmap -p- 192.168.56.10

# 服务版本检测
nmap -sV --version-intensity 5 192.168.56.10
```

预期结果示例:
```
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 8.9p1 Ubuntu
80/tcp  open  http    nginx 1.18.0
```

#### 5.1.2 从 SOC 扫描 Kali

```bash
# 安装 nmap (如果未安装)
sudo apt install -y nmap

# 基础扫描
nmap 192.168.56.20

# 服务扫描
nmap -sV 192.168.56.20
```

### 5.2 Netcat 连接测试

#### 5.2.1 在 SOC 上启动监听

```bash
# 监听 TCP 端口 9999
nc -lvnp 9999
```

#### 5.2.2 从 Kali 连接

```bash
# 连接到 SOC
nc 192.168.56.10 9999

# 输入消息并按 Enter
# 消息应该在 SOC 端显示
```

#### 5.2.3 反向测试

在 Kali 上监听:
```bash
nc -lvnp 8888
```

从 SOC 连接:
```bash
nc 192.168.56.20 8888
```

### 5.3 Wireshark/tcpdump 流量捕获

#### 5.3.1 在 SOC 上捕获流量

```bash
# 捕获 Host-only 网络流量
sudo tcpdump -i enp0s8 -w /tmp/capture.pcap

# 在另一个终端，从 Kali 发送流量
# Ctrl+C 停止捕获

# 分析捕获的包
sudo tcpdump -r /tmp/capture.pcap | head -20
```

#### 5.3.2 在 Kali 上使用 Wireshark

```bash
# 启动 Wireshark (GUI)
sudo wireshark &

# 选择 eth1 接口
# 开始捕获
# 从 SOC 发送流量
# 观察捕获的包
```

### 5.4 Metasploit 测试

#### 5.4.1 在 Kali 上启动 Metasploit

```bash
# 启动 PostgreSQL
sudo systemctl start postgresql

# 初始化数据库 (首次)
sudo msfdb init

# 启动 Metasploit
msfconsole -q
```

#### 5.4.2 扫描 SOC 服务器

在 msfconsole 中:
```ruby
# 使用辅助扫描模块
use auxiliary/scanner/portscan/tcp
set RHOSTS 192.168.56.10
set PORTS 1-1000
run

# 检查 SSH 版本
use auxiliary/scanner/ssh/ssh_version
set RHOSTS 192.168.56.10
run

# 退出
exit
```

## 6. 性能验证

### 6.1 网络带宽测试

#### 6.1.1 安装 iperf3

SOC Server:
```bash
sudo apt install -y iperf3
```

Kali Attack:
```bash
sudo apt install -y iperf3
```

#### 6.1.2 运行带宽测试

在 SOC 上启动服务器:
```bash
iperf3 -s
```

在 Kali 上运行客户端:
```bash
# TCP 测试
iperf3 -c 192.168.56.10 -t 10

# UDP 测试
iperf3 -c 192.168.56.10 -u -b 100M
```

预期结果: 通常应该能达到 1 Gbps 或更高（取决于虚拟化性能）

### 6.2 延迟测试

```bash
# 从 Kali 到 SOC
ping -c 100 192.168.56.10 | tail -5

# 计算平均延迟
ping -c 100 192.168.56.10 | grep avg
```

预期结果: 延迟应该小于 1ms（本地虚拟网络）

### 6.3 系统资源监控

#### 6.3.1 SOC Server

```bash
# 安装监控工具
sudo apt install -y htop iotop nethogs

# 查看资源使用
htop

# 网络带宽监控
sudo nethogs enp0s8
```

#### 6.3.2 Kali Attack

```bash
# 系统资源
htop

# 网络连接
ss -tuln

# 实时网络流量
sudo iftop -i eth1
```

## 7. 防火墙验证

### 7.1 SOC 防火墙测试

```bash
# 查看规则
sudo ufw status verbose

# 测试阻止的端口
# 在 SOC 上监听一个端口
nc -lvnp 12345

# 从 Kali 尝试连接（应该被阻止）
# 然后添加规则允许
sudo ufw allow from 192.168.56.20 to any port 12345

# 重新测试（应该成功）
```

### 7.2 Kali 防火墙测试

```bash
# 查看规则
sudo ufw status verbose

# 测试连接过滤
```

## 8. 创建验证脚本

### 8.1 完整验证脚本

创建 `/tmp/lab-verification.sh`:

```bash
#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "   Mini-SOC Lab Verification Script"
echo "========================================"
echo ""

# Function to test command
test_cmd() {
    local description=$1
    local command=$2
    
    echo -n "Testing: $description... "
    if eval $command &>/dev/null; then
        echo -e "${GREEN}✓ PASS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        return 1
    fi
}

# Network Interface Tests
echo "=== Network Interface Tests ==="
test_cmd "NAT interface (eth0/enp0s3)" "ip addr show eth0 2>/dev/null || ip addr show enp0s3"
test_cmd "Host-only interface (eth1/enp0s8)" "ip addr show eth1 2>/dev/null || ip addr show enp0s8"
echo ""

# Internet Connectivity
echo "=== Internet Connectivity ==="
test_cmd "DNS resolution" "nslookup google.com"
test_cmd "Ping gateway" "ping -c 2 10.0.2.2"
test_cmd "Ping internet (8.8.8.8)" "ping -c 2 8.8.8.8"
test_cmd "HTTPS connectivity" "curl -Is https://www.google.com"
echo ""

# Lab Network Connectivity
echo "=== Lab Network Connectivity ==="
test_cmd "Ping host machine (192.168.56.1)" "ping -c 2 192.168.56.1"
test_cmd "Ping SOC server (192.168.56.10)" "ping -c 2 192.168.56.10"
test_cmd "Ping Kali attack (192.168.56.20)" "ping -c 2 192.168.56.20"
echo ""

# Hostname Resolution
echo "=== Hostname Resolution ==="
test_cmd "Resolve soc-server" "ping -c 1 soc-server"
test_cmd "Resolve kali-attack" "ping -c 1 kali-attack"
echo ""

# Service Tests
echo "=== Service Tests ==="
test_cmd "SSH service running" "systemctl is-active ssh || systemctl is-active sshd"
test_cmd "SSH port listening" "netstat -tulpn | grep ':22 '"
echo ""

# Tool Tests
echo "=== Security Tools ==="
test_cmd "nmap installed" "which nmap"
test_cmd "netcat installed" "which nc"
test_cmd "tcpdump installed" "which tcpdump"
echo ""

echo "========================================"
echo "   Verification Complete"
echo "========================================"
```

运行脚本:
```bash
chmod +x /tmp/lab-verification.sh
/tmp/lab-verification.sh
```

### 8.2 在两台虚拟机上运行

**SOC Server**:
```bash
bash /tmp/lab-verification.sh
```

**Kali Attack**:
```bash
bash /tmp/lab-verification.sh
```

## 9. 常见问题验证

### 9.1 检查清单

- [ ] 两台虚拟机都能访问互联网
- [ ] 两台虚拟机之间可以互相 ping 通
- [ ] SSH 服务可以正常连接
- [ ] 主机名解析正常工作
- [ ] 防火墙规则配置正确
- [ ] 可以从 Kali 扫描 SOC
- [ ] 网络工具正常运行
- [ ] 没有 IP 地址冲突

### 9.2 验证报告模板

创建验证报告 `/tmp/verification-report.txt`:

```
Mini-SOC Lab 验证报告
====================================

日期: [填写日期]
测试人: [填写姓名]

环境信息:
- VirtualBox 版本: [版本号]
- 宿主机 OS: [操作系统]
- SOC Server OS: Ubuntu Server 22.04 LTS
- Kali Version: [版本号]

网络配置:
- Host-only 网络: 192.168.56.0/24
- SOC IP: 192.168.56.10
- Kali IP: 192.168.56.20

测试结果:
1. 互联网连接: ✓ 通过 / ✗ 失败
2. 虚拟机互通: ✓ 通过 / ✗ 失败
3. SSH 连接: ✓ 通过 / ✗ 失败
4. 主机名解析: ✓ 通过 / ✗ 失败
5. 工具验证: ✓ 通过 / ✗ 失败

性能指标:
- 网络延迟: [X] ms
- 带宽: [X] Mbps
- SOC CPU: [X]%
- SOC Memory: [X]%
- Kali CPU: [X]%
- Kali Memory: [X]%

问题记录:
[记录遇到的问题和解决方法]

备注:
[其他说明]
```

## 10. 最终确认

### 10.1 完整功能测试场景

执行以下完整测试场景:

1. **场景 1: 端口扫描**
   ```bash
   # 从 Kali
   nmap -sV -p- 192.168.56.10
   ```

2. **场景 2: 文件传输**
   ```bash
   # 在 SOC 上创建测试文件
   echo "Test file from SOC" > /tmp/test.txt
   
   # 使用 SCP 传输到 Kali
   scp /tmp/test.txt kali@192.168.56.20:/tmp/
   
   # 在 Kali 上验证
   cat /tmp/test.txt
   ```

3. **场景 3: 网络监控**
   ```bash
   # 在 SOC 上启动 tcpdump
   sudo tcpdump -i enp0s8 -w /tmp/traffic.pcap
   
   # 从 Kali 生成流量
   curl http://192.168.56.10
   
   # 停止捕获并分析
   sudo tcpdump -r /tmp/traffic.pcap
   ```

4. **场景 4: Metasploit 侦察**
   ```bash
   # 在 Kali 上使用 Metasploit
   msfconsole -q -x "use auxiliary/scanner/portscan/tcp; set RHOSTS 192.168.56.10; run; exit"
   ```

### 10.2 创建最终快照

所有测试通过后，为两台虚拟机创建快照:

1. 关闭虚拟机
2. VirtualBox > 虚拟机 > 快照 > 生成快照
3. 名称: "Lab Verified - Ready for Use"
4. 描述: "所有功能验证通过，可以开始实验"

## 11. 下一步

环境验证完成后，你可以:

1. **开始安全实验**
   - 漏洞扫描练习
   - 渗透测试实验
   - 网络流量分析

2. **扩展环境**
   - 添加更多虚拟机（靶机、日志服务器）
   - 部署安全工具（SIEM, IDS/IPS）
   - 配置更复杂的网络拓扑

3. **学习资源**
   - 练习 CTF 挑战
   - 学习 OWASP Top 10
   - 研究实际安全事件

## 12. 维护建议

- 定期更新系统和工具
- 定期创建快照备份
- 记录所有实验和配置更改
- 保持虚拟机资源充足
- 定期清理不需要的文件

## 13. 参考资源

- [VirtualBox 故障排除](https://www.virtualbox.org/wiki/Troubleshooting)
- [Ubuntu Server 网络配置](https://ubuntu.com/server/docs/network-configuration)
- [Kali Linux 网络配置](https://www.kali.org/docs/general-use/network-configuration/)
- [Nmap 参考指南](https://nmap.org/book/man.html)
- [Metasploit Unleashed](https://www.metasploitunleashed.com/)

---

**恭喜！Mini-SOC Lab 环境已经完全配置并验证完成！** 🎉
