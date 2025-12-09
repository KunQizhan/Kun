# 网络配置指南

## 1. 概述

本文档详细说明如何配置 Mini-SOC Lab 的网络拓扑，确保虚拟机之间能够正常通信，同时保持与外部网络的连接。

## 2. 网络架构设计

### 2.1 网络拓扑图

```
                         互联网
                            ↑
                            │
                    ┌───────┴────────┐
                    │  NAT Network   │
                    │  10.0.2.0/24   │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───┴────┐         ┌────┴─────┐       ┌────┴─────┐
    │ NAT 1  │         │  NAT 2   │       │  宿主机  │
    └───┬────┘         └────┬─────┘       └────┬─────┘
        │                   │                   │
    ┌───┴──────┐       ┌────┴──────┐           │
    │ SOC VM   │       │ Kali VM   │           │
    │ eth0     │       │ eth0      │           │
    │10.0.2.15 │       │10.0.2.15  │           │
    └───┬──────┘       └────┬──────┘           │
        │                   │                   │
        │ eth1              │ eth1              │
        │                   │                   │
    ┌───┴───────────────────┴───────────────────┴───┐
    │         Host-only Network (vboxnet0)          │
    │              192.168.56.0/24                  │
    │                                               │
    │  192.168.56.1    192.168.56.10    192.168.56.20
    │   (宿主机)        (SOC Server)      (Kali)     │
    └───────────────────────────────────────────────┘
```

### 2.2 IP 地址分配

| 设备 | 接口 | 网络类型 | IP 地址 | 用途 |
|------|------|----------|---------|------|
| 宿主机 | vboxnet0 | Host-only | 192.168.56.1 | 实验室管理 |
| SOC Server | enp0s3 (eth0) | NAT | 10.0.2.15 (DHCP) | 互联网访问 |
| SOC Server | enp0s8 (eth1) | Host-only | 192.168.56.10 | 实验室通信 |
| Kali Attack | eth0 | NAT | 10.0.2.15 (DHCP) | 互联网访问 |
| Kali Attack | eth1 | Host-only | 192.168.56.20 | 实验室通信 |

## 3. VirtualBox 网络配置

### 3.1 配置 Host-only 网络

#### 3.1.1 创建 Host-only 网络

1. **打开 VirtualBox**
2. **文件** > **工具** > **网络管理器**
3. 选择 **Host-only Networks** 选项卡
4. 点击 **创建** 按钮

#### 3.1.2 配置网络参数

**适配器** 选项卡:
```
IPv4 地址: 192.168.56.1
IPv4 网络掩码: 255.255.255.0
IPv6 地址: [可选，留空]
```

**DHCP 服务器** 选项卡:
```
☑ 启用服务器

服务器地址: 192.168.56.100
服务器掩码: 255.255.255.0
地址下限: 192.168.56.101
地址上限: 192.168.56.254
```

#### 3.1.3 验证配置

在宿主机上:

**Windows:**
```cmd
ipconfig | findstr "192.168.56"
```

**Linux/macOS:**
```bash
ip addr show vboxnet0
# 或
ifconfig vboxnet0
```

预期输出:
```
inet 192.168.56.1 netmask 255.255.255.0
```

### 3.2 配置虚拟机网络

#### 3.2.1 SOC Server 网络配置

**网卡 1 (NAT)**:
```
启用网络连接: ☑
连接方式: NAT
高级:
  控制芯片: Intel PRO/1000 MT Desktop (82540EM)
  混杂模式: 拒绝
  MAC 地址: [自动生成]
  接入网线: ☑
```

**网卡 2 (Host-only)**:
```
启用网络连接: ☑
连接方式: 仅主机(Host-Only)适配器
界面名称: vboxnet0
高级:
  控制芯片: Intel PRO/1000 MT Desktop (82540EM)
  混杂模式: 拒绝
  MAC 地址: [自动生成]
  接入网线: ☑
```

#### 3.2.2 Kali Attack 网络配置

配置与 SOC Server 相同（双网卡：NAT + Host-only）

## 4. 操作系统网络配置

### 4.1 Ubuntu Server (SOC) 配置

#### 4.1.1 查看网络接口

```bash
# 列出所有网络接口
ip link show

# 查看 IP 地址
ip addr show
```

#### 4.1.2 配置 Netplan

编辑配置文件:
```bash
sudo vim /etc/netplan/00-installer-config.yaml
```

完整配置:
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:  # NAT 接口
      dhcp4: true
      dhcp6: false
      optional: true
      
    enp0s8:  # Host-only 接口
      dhcp4: false
      dhcp6: false
      addresses:
        - 192.168.56.10/24
      routes:
        - to: 192.168.56.0/24
          via: 0.0.0.0
          metric: 100
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
        search: []
```

#### 4.1.3 应用配置

```bash
# 测试配置 (30秒超时，如有问题自动回滚)
sudo netplan try

# 按 Enter 确认配置正确

# 或直接应用
sudo netplan apply

# 验证
ip addr show enp0s8
```

#### 4.1.4 验证路由表

```bash
# 查看路由表
ip route show

# 预期输出:
# default via 10.0.2.2 dev enp0s3 proto dhcp src 10.0.2.15 metric 100
# 10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100
# 192.168.56.0/24 dev enp0s8 proto kernel scope link src 192.168.56.10
```

### 4.2 Kali Linux 配置

#### 4.2.1 方法一：使用 NetworkManager (GUI)

1. 点击系统托盘的网络图标
2. **Network Settings** > **Wired**
3. 选择 **Wired connection 2** (eth1)
4. 点击齿轮图标 ⚙️

**IPv4 配置**:
```
Method: Manual

Addresses:
  Address: 192.168.56.20
  Netmask: 255.255.255.0 (或写成 /24)
  Gateway: (留空)

DNS: 8.8.8.8, 8.8.4.4

Routes: (自动)
```

5. 点击 **Apply** 保存
6. 关闭并重新打开连接

#### 4.2.2 方法二：使用 nmcli (命令行)

```bash
# 查看所有连接
nmcli connection show

# 配置 Host-only 接口
nmcli connection modify "Wired connection 2" \
  ipv4.method manual \
  ipv4.addresses 192.168.56.20/24 \
  ipv4.dns "8.8.8.8,8.8.4.4"

# 激活连接
nmcli connection up "Wired connection 2"

# 验证
ip addr show eth1
```

#### 4.2.3 方法三：编辑 /etc/network/interfaces

```bash
sudo vim /etc/network/interfaces
```

添加配置:
```bash
# NAT 接口 (自动配置)
auto eth0
iface eth0 inet dhcp

# Host-only 接口 (静态 IP)
auto eth1
iface eth1 inet static
    address 192.168.56.20
    netmask 255.255.255.0
    # 不需要 gateway，这是内部网络
```

重启网络:
```bash
sudo systemctl restart networking
# 或
sudo ifdown eth1 && sudo ifup eth1
```

#### 4.2.4 验证配置

```bash
# 查看 IP
ip addr show eth1

# 查看路由
ip route show

# 测试连通性
ping -c 4 192.168.56.1  # 宿主机
ping -c 4 192.168.56.10 # SOC Server
```

## 5. 配置主机名解析

### 5.1 在所有虚拟机上配置

#### 5.1.1 SOC Server

```bash
sudo vim /etc/hosts
```

添加:
```
127.0.0.1       localhost
127.0.1.1       soc-server

# 实验室网络
192.168.56.1    host-machine
192.168.56.10   soc-server
192.168.56.20   kali-attack kali
```

#### 5.1.2 Kali Attack

```bash
sudo vim /etc/hosts
```

添加:
```
127.0.0.1       localhost
127.0.1.1       kali-attack

# 实验室网络
192.168.56.1    host-machine
192.168.56.10   soc-server soc
192.168.56.20   kali-attack
```

### 5.2 在宿主机上配置（可选）

#### Windows (需要管理员权限)

编辑 `C:\Windows\System32\drivers\etc\hosts`:
```
192.168.56.10   soc-server
192.168.56.20   kali-attack
```

#### Linux/macOS

```bash
sudo vim /etc/hosts
```

添加:
```
192.168.56.10   soc-server
192.168.56.20   kali-attack
```

## 6. 防火墙配置

### 6.1 SOC Server 防火墙

```bash
# 启用 UFW
sudo ufw enable

# 允许来自实验室网络的所有流量
sudo ufw allow from 192.168.56.0/24

# 允许来自 NAT 网络的特定服务 (如 SSH)
sudo ufw allow from 10.0.2.0/24 to any port 22

# 查看规则
sudo ufw status verbose

# 查看编号规则
sudo ufw status numbered
```

示例输出:
```
Status: active

To                         Action      From
--                         ------      ----
Anywhere                   ALLOW       192.168.56.0/24
22                         ALLOW       10.0.2.0/24
```

### 6.2 Kali Attack 防火墙

```bash
# 安装 UFW (如果未安装)
sudo apt install -y ufw

# 启用防火墙
sudo ufw enable

# 允许实验室网络
sudo ufw allow from 192.168.56.0/24

# 允许特定端口 (如 SSH, HTTP)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 查看状态
sudo ufw status verbose
```

## 7. 高级网络配置

### 7.1 端口转发（NAT 端口映射）

如果需要从宿主机直接访问虚拟机服务:

#### 7.1.1 配置 SSH 端口转发

**SOC Server**:
1. VirtualBox > SOC-Ubuntu-Server > 设置 > 网络 > 网卡 1 (NAT)
2. 高级 > 端口转发
3. 添加规则:
   ```
   名称: SSH-SOC
   协议: TCP
   主机 IP: 127.0.0.1
   主机端口: 2222
   子系统 IP: 10.0.2.15
   子系统端口: 22
   ```

**Kali Attack**:
```
名称: SSH-Kali
协议: TCP
主机 IP: 127.0.0.1
主机端口: 2223
子系统 IP: 10.0.2.15
子系统端口: 22
```

从宿主机连接:
```bash
# 连接到 SOC
ssh socadmin@127.0.0.1 -p 2222

# 连接到 Kali
ssh kali@127.0.0.1 -p 2223
```

### 7.2 桥接网络（可选）

如果需要虚拟机在物理网络中可见:

1. VirtualBox > 虚拟机 > 设置 > 网络 > 网卡 3
2. 连接方式: 桥接网卡
3. 界面名称: [选择物理网卡]

**注意**: 桥接模式会使虚拟机暴露在物理网络中，注意安全。

### 7.3 内部网络（可选）

创建完全隔离的内部网络:

1. VirtualBox > 虚拟机 > 设置 > 网络 > 网卡 3
2. 连接方式: 内部网络
3. 网络名称: intnet (自定义)

所有连接到 "intnet" 的虚拟机可以互相通信，但与外界隔离。

## 8. 网络性能优化

### 8.1 调整 MTU

```bash
# 查看当前 MTU
ip link show eth1 | grep mtu

# 临时修改 MTU
sudo ip link set eth1 mtu 9000

# 永久修改 (Netplan)
# 在 netplan 配置中添加:
# mtu: 1500
```

### 8.2 启用巨型帧（可选）

在 VirtualBox 虚拟机设置中:
```bash
VBoxManage modifyvm "SOC-Ubuntu-Server" --nictype2 82545EM
VBoxManage modifyvm "SOC-Ubuntu-Server" --nicpromisc2 allow-all
```

### 8.3 禁用不需要的网络服务

```bash
# 禁用 IPv6 (如果不需要)
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1

# 永久禁用
echo "net.ipv6.conf.all.disable_ipv6 = 1" | sudo tee -a /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" | sudo tee -a /etc/sysctl.conf
```

## 9. 故障排除

### 9.1 无法 ping 通其他虚拟机

**检查清单**:
1. 确认网卡已启用
   ```bash
   ip link show eth1
   # 应该看到 "UP" 状态
   ```

2. 确认 IP 地址正确
   ```bash
   ip addr show eth1
   ```

3. 确认防火墙允许 ICMP
   ```bash
   # 临时允许 ping
   sudo ufw allow from 192.168.56.0/24 to any proto icmp
   ```

4. 检查路由表
   ```bash
   ip route show
   ```

5. 尝试手动添加路由
   ```bash
   sudo ip route add 192.168.56.0/24 dev eth1
   ```

### 9.2 虚拟机无法访问互联网

**检查 NAT 网卡**:
```bash
# 查看 NAT 网卡状态
ip addr show eth0

# 查看默认路由
ip route show | grep default

# 测试 DNS
nslookup google.com

# 测试网关
ping -c 4 10.0.2.2
```

**添加默认路由**:
```bash
sudo ip route add default via 10.0.2.2 dev eth0
```

### 9.3 DNS 解析失败

**检查 DNS 配置**:
```bash
cat /etc/resolv.conf
```

**手动设置 DNS**:
```bash
# 临时设置
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# 永久设置 (Netplan)
# 在 netplan 配置中的 nameservers 部分添加
```

### 9.4 网络配置未生效

**重启网络服务**:

Ubuntu:
```bash
sudo netplan apply
# 或
sudo systemctl restart systemd-networkd
```

Kali:
```bash
sudo systemctl restart NetworkManager
# 或
sudo systemctl restart networking
```

### 9.5 VirtualBox Host-only 网络不存在

**手动创建**:
```bash
# Linux/macOS
VBoxManage hostonlyif create
VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0

# Windows (PowerShell)
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" hostonlyif create
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" hostonlyif ipconfig "VirtualBox Host-Only Ethernet Adapter" --ip 192.168.56.1 --netmask 255.255.255.0
```

## 10. 验证网络配置

创建验证脚本 `/tmp/network-test.sh`:

```bash
#!/bin/bash

echo "=== Network Configuration Test ==="
echo ""

echo "1. Network Interfaces:"
ip -br addr show
echo ""

echo "2. Routing Table:"
ip route show
echo ""

echo "3. DNS Configuration:"
cat /etc/resolv.conf
echo ""

echo "4. Connectivity Tests:"
echo "   - Gateway:"
ping -c 2 10.0.2.2 2>/dev/null && echo "     ✓ Gateway reachable" || echo "     ✗ Gateway unreachable"

echo "   - Internet (DNS):"
ping -c 2 8.8.8.8 2>/dev/null && echo "     ✓ Internet reachable" || echo "     ✗ Internet unreachable"

echo "   - Host Machine:"
ping -c 2 192.168.56.1 2>/dev/null && echo "     ✓ Host reachable" || echo "     ✗ Host unreachable"

echo "   - SOC Server:"
ping -c 2 192.168.56.10 2>/dev/null && echo "     ✓ SOC reachable" || echo "     ✗ SOC unreachable"

echo "   - Kali Attack:"
ping -c 2 192.168.56.20 2>/dev/null && echo "     ✓ Kali reachable" || echo "     ✗ Kali unreachable"

echo ""
echo "5. Open Ports:"
sudo netstat -tulpn | grep LISTEN
```

运行测试:
```bash
chmod +x /tmp/network-test.sh
/tmp/network-test.sh
```

## 11. 下一步

网络配置完成后:
- 进行 [验证与测试](./05-verification.md)
- 开始使用 Mini-SOC Lab 进行安全实验

## 12. 参考资源

- [VirtualBox 网络模式详解](https://www.virtualbox.org/manual/ch06.html)
- [Ubuntu Netplan 配置](https://netplan.io/)
- [NetworkManager 命令行工具](https://networkmanager.dev/docs/api/latest/nmcli.html)
