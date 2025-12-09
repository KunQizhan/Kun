# Kali Linux 攻击机虚拟机配置指南

## 1. 概述

本文档指导如何在 VirtualBox 中创建和配置 Kali Linux 虚拟机，作为渗透测试攻击机使用。

## 2. 下载 Kali Linux

### 2.1 官方下载
访问 [Kali Linux 官方下载页面](https://www.kali.org/get-kali/)

### 2.2 镜像选择

推荐下载预构建的 VirtualBox 镜像（最简单）:
```
文件类型: VirtualBox (64-bit)
文件名: kali-linux-YYYY.X-virtualbox-amd64.7z
大小: 约 3-4GB (压缩后)
```

或下载 ISO 镜像（自定义安装）:
```
文件类型: Installer Images
文件名: kali-linux-YYYY.X-installer-amd64.iso
大小: 约 4GB
```

**镜像版本**:
- **Installer**: 标准安装镜像
- **Live**: 可以直接运行，无需安装
- **NetInstaller**: 网络安装镜像（最小）

### 2.3 解压 VirtualBox 镜像（如果下载的是预构建版）

```bash
# Windows: 使用 7-Zip
# macOS/Linux:
7z x kali-linux-YYYY.X-virtualbox-amd64.7z
```

## 3. 方法一：导入预构建的 VirtualBox 镜像 (推荐)

### 3.1 导入虚拟机

1. **打开 VirtualBox**
2. **文件** > **导入虚拟电脑**
3. **选择文件**: 浏览到解压后的 `.vbox` 或 `.ova` 文件
4. **设置**:
   ```
   名称: Kali-Attack
   RAM: 2048 MB (推荐 4096 MB)
   CPU: 2 核心
   ```
5. **导入**

### 3.2 配置导入的虚拟机

右键点击 "Kali-Attack" > "设置"

#### 3.2.1 系统设置
**主板**:
```
基本内存: 2048 MB (最低)
          4096 MB (推荐)
          
启动顺序:
  ☑ 硬盘
  ☑ 光驱
  ☐ 软驱
```

**处理器**:
```
处理器数量: 2 (推荐)
执行上限: 100%
```

#### 3.2.2 显示设置
```
显存大小: 128 MB
监视器数量: 1
缩放因子: 100%
显卡控制器: VMSVGA

扩展特性:
  ☑ 启用 3D 加速 (推荐，提升桌面性能)
```

#### 3.2.3 网络设置

**网卡 1** (NAT - 互联网访问):
```
启用网络连接: ☑
连接方式: NAT
控制芯片: Intel PRO/1000 MT Desktop
```

**网卡 2** (Host-only - 实验室内部):
```
启用网络连接: ☑
连接方式: 仅主机(Host-Only)适配器
界面名称: vboxnet0
控制芯片: Intel PRO/1000 MT Desktop
```

### 3.3 启动虚拟机

默认凭据:
```
用户名: kali
密码: kali
```

**首次登录后立即修改密码**:
```bash
passwd
```

## 4. 方法二：从 ISO 全新安装

### 4.1 创建虚拟机

1. **新建虚拟机**
   ```
   名称: Kali-Attack
   类型: Linux
   版本: Debian (64-bit)
   ```

2. **内存**
   ```
   推荐: 2048 MB
   理想: 4096 MB
   ```

3. **虚拟硬盘**
   ```
   类型: VDI
   存储: 动态分配
   大小: 30 GB (推荐 40GB)
   ```

### 4.2 配置虚拟机设置

#### 4.2.1 系统
**主板**:
```
启动顺序: 光驱、硬盘
启用 I/O APIC: ☑
硬件时钟 UTC: ☑
```

**处理器**:
```
处理器: 2
启用 PAE/NX: ☑
```

#### 4.2.2 存储
挂载 Kali Linux ISO:
```
控制器: IDE
  └─ [选择 Kali ISO 文件]
  
控制器: SATA
  └─ Kali-Attack.vdi (30GB)
```

#### 4.2.3 网络
配置双网卡（同上述预构建版本）

### 4.3 安装 Kali Linux

#### 4.3.1 启动安装
1. 启动虚拟机
2. 选择 "Graphical Install"

#### 4.3.2 安装步骤

**语言选择**:
```
Language: English (或中文简体)
Location: [您的国家]
Keymap: American English
```

**网络配置**:
```
Hostname: kali-attack
Domain name: [留空]
```

**用户设置**:
```
Full name: Kali User
Username: kali
Password: [设置强密码]
```

**分区**:
```
方法: Guided - use entire disk
分区方案: All files in one partition (推荐新手)

或高级分区:
  - /boot: 500 MB
  - /: 25 GB
  - swap: 2 GB
  - /home: 剩余
```

**软件选择**:
```
Desktop Environment: Xfce (推荐，轻量)
                    或 KDE / GNOME

工具集: 
  ☑ default
  ☑ large (如果磁盘空间充足)
  或
  ☐ top10 (最常用的工具)
```

**GRUB 引导**:
```
Install GRUB: Yes
Device: /dev/sda
```

**完成**:
```
Installation complete
Remove installation media
Reboot
```

## 5. 初始配置

### 5.1 首次登录

登录桌面环境:
```
用户名: kali
密码: [你设置的密码]
```

### 5.2 更新系统

打开终端:
```bash
# 更新软件源
sudo apt update

# 升级所有包
sudo apt upgrade -y

# 更新 Kali 工具集
sudo apt dist-upgrade -y

# 清理
sudo apt autoremove -y
sudo apt autoclean
```

### 5.3 配置静态 IP

#### 5.3.1 通过图形界面

1. 点击右上角网络图标
2. 选择 "Edit Connections"
3. 选择 "Wired connection 2" (eth1/enp0s8)
4. 点击编辑图标

**IPv4 Settings**:
```
Method: Manual

Address: 192.168.56.20
Netmask: 255.255.255.0 (或 /24)
Gateway: [留空]

DNS servers: 8.8.8.8, 8.8.4.4
```

5. 保存并重新连接

#### 5.3.2 通过命令行

编辑网络接口配置:
```bash
sudo vim /etc/network/interfaces
```

添加配置:
```bash
# Host-only 网络
auto eth1
iface eth1 inet static
    address 192.168.56.20
    netmask 255.255.255.0
```

重启网络:
```bash
sudo systemctl restart networking
```

或使用 NetworkManager:
```bash
sudo nmcli con mod "Wired connection 2" ipv4.addresses 192.168.56.20/24
sudo nmcli con mod "Wired connection 2" ipv4.method manual
sudo nmcli con up "Wired connection 2"
```

### 5.4 验证网络配置

```bash
# 查看 IP 地址
ip addr show

# 测试互联网连接 (eth0/NAT)
ping -c 4 8.8.8.8

# 测试 Host-only 网络
ping -c 4 192.168.56.1  # 宿主机
ping -c 4 192.168.56.10 # SOC 服务器
```

### 5.5 配置主机名解析

```bash
sudo vim /etc/hosts
```

添加:
```
192.168.56.10   soc-server
192.168.56.20   kali-attack
192.168.56.1    host-machine
```

### 5.6 安装额外工具

```bash
# 常用工具
sudo apt install -y \
  terminator \
  tmux \
  vim \
  git \
  curl \
  wget

# 网络工具
sudo apt install -y \
  netcat-traditional \
  socat \
  proxychains4 \
  openvpn

# 渗透测试工具 (如果未预装)
sudo apt install -y \
  metasploit-framework \
  sqlmap \
  hydra \
  john \
  aircrack-ng \
  wireshark \
  burpsuite \
  zaproxy

# Web 应用测试
sudo apt install -y \
  nikto \
  dirb \
  gobuster \
  wfuzz

# 漏洞扫描
sudo apt install -y \
  nmap \
  masscan \
  openvas
```

### 5.7 安装 VirtualBox Guest Additions

增强虚拟机性能和功能:

```bash
# 安装必要的包
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r)

# 在 VirtualBox 菜单栏: 设备 > 安装增强功能
# 然后在终端执行:
sudo mkdir -p /mnt/cdrom
sudo mount /dev/cdrom /mnt/cdrom
sudo /mnt/cdrom/VBoxLinuxAdditions.run

# 重启虚拟机
sudo reboot
```

功能:
- 共享剪贴板
- 拖放文件
- 自动调整分辨率
- 共享文件夹

### 5.8 配置 Metasploit

```bash
# 启动 PostgreSQL 数据库
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 初始化 Metasploit 数据库
sudo msfdb init

# 测试 Metasploit
msfconsole -q
```

在 msfconsole 中:
```
msf6 > db_status
[*] Connected to msf. Connection type: postgresql.
msf6 > exit
```

## 6. 创建快照

保存配置完成的状态:

1. 关闭虚拟机: `sudo poweroff`
2. VirtualBox > 右键 "Kali-Attack" > "快照" > "生成快照"
3. 名称: "Initial Configuration - Tools Ready"
4. 描述: "Kali Linux 基础配置完成，工具已更新"

## 7. 常用操作

### 7.1 启动常用服务

```bash
# SSH 服务 (用于远程访问)
sudo systemctl start ssh
sudo systemctl enable ssh

# Apache Web 服务器
sudo systemctl start apache2

# MySQL/MariaDB
sudo systemctl start mysql
```

### 7.2 配置代理（可选）

编辑 ProxyChains 配置:
```bash
sudo vim /etc/proxychains4.conf
```

在文件末尾添加代理:
```
[ProxyList]
socks5  127.0.0.1 9050
# 或
http    proxy.example.com 8080
```

使用:
```bash
proxychains4 nmap -sT target.com
```

### 7.3 共享文件夹（与宿主机）

在 VirtualBox 中配置:
1. 设置 > 共享文件夹 > 添加共享文件夹
   ```
   文件夹路径: [宿主机路径]
   文件夹名称: shared
   自动挂载: ☑
   固定分配: ☑
   ```

在 Kali 中挂载:
```bash
sudo mkdir -p /mnt/shared
sudo mount -t vboxsf shared /mnt/shared

# 或添加到 /etc/fstab 自动挂载
echo "shared /mnt/shared vboxsf defaults 0 0" | sudo tee -a /etc/fstab
```

## 8. 安全最佳实践

### 8.1 修改默认密码
```bash
# 修改用户密码
passwd

# 修改 root 密码
sudo passwd root
```

### 8.2 启用防火墙
```bash
sudo apt install -y ufw
sudo ufw enable
sudo ufw allow from 192.168.56.0/24  # 允许实验室网络
```

### 8.3 禁用不必要的服务
```bash
# 列出所有服务
sudo systemctl list-unit-files --type=service

# 禁用不需要的服务
sudo systemctl disable bluetooth.service
sudo systemctl stop bluetooth.service
```

## 9. 故障排除

### 9.1 网络问题

**问题**: 无法访问互联网
```bash
# 检查路由
ip route show

# 添加默认路由
sudo ip route add default via 10.0.2.2 dev eth0
```

**问题**: Host-only 网络无法通信
```bash
# 检查接口状态
ip link show eth1

# 启用接口
sudo ip link set eth1 up

# 重新配置 IP
sudo dhclient eth1
```

### 9.2 图形界面问题

**问题**: 分辨率无法自动调整
```bash
# 重新安装 Guest Additions
sudo apt install --reinstall virtualbox-guest-x11
sudo reboot
```

### 9.3 工具问题

**问题**: Metasploit 数据库连接失败
```bash
# 重新初始化数据库
sudo msfdb delete
sudo msfdb init
```

## 10. 验证配置

运行以下命令验证配置:

```bash
# 系统信息
echo "=== System Info ==="
uname -a
cat /etc/os-release

# 网络配置
echo "=== Network Config ==="
ip addr show
ip route show

# 测试连通性
echo "=== Connectivity Tests ==="
ping -c 2 8.8.8.8
ping -c 2 192.168.56.10

# 已安装工具
echo "=== Installed Tools ==="
which nmap metasploit-framework sqlmap hydra
```

## 11. 下一步

Kali Linux 配置完成后:
- 继续 [网络配置指南](./04-network-configuration.md)
- 进行 [验证与测试](./05-verification.md)

## 12. 参考资源

- [Kali Linux 官方文档](https://www.kali.org/docs/)
- [Kali Tools 列表](https://www.kali.org/tools/)
- [Metasploit Unleashed](https://www.metasploitunleashed.com/)
- [渗透测试执行标准](http://www.pentest-standard.org/)
