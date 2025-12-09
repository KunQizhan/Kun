# Ubuntu Server SOC 虚拟机配置指南

## 1. 概述

本文档指导如何在 VirtualBox 中创建和配置 Ubuntu Server 虚拟机，作为 SOC（安全运营中心）服务器使用。

## 2. 下载 Ubuntu Server ISO

### 2.1 官方下载
访问 [Ubuntu Server 下载页面](https://ubuntu.com/download/server)

推荐版本：
- **Ubuntu Server 22.04 LTS** (长期支持版本)
- **Ubuntu Server 24.04 LTS** (最新 LTS)

### 2.2 镜像选择
```
文件名示例: ubuntu-22.04.3-live-server-amd64.iso
大小: 约 2GB
```

## 3. 创建虚拟机

### 3.1 新建虚拟机

1. **启动创建向导**
   - 打开 VirtualBox
   - 点击 "新建" 或 "Machine" > "New"

2. **基本信息**
   ```
   名称: SOC-Ubuntu-Server
   文件夹: [选择虚拟机存储位置]
   类型: Linux
   版本: Ubuntu (64-bit)
   ```

3. **内存大小**
   ```
   推荐: 2048 MB (2GB)
   最低: 1024 MB (1GB)
   可选: 4096 MB (4GB) - 如果要运行更多服务
   ```

4. **虚拟硬盘**
   - 选择 "现在创建虚拟硬盘"
   - 硬盘文件类型: VDI (VirtualBox 磁盘映像)
   - 存储方式: 动态分配
   - 大小: 20 GB (推荐 25GB)

5. **完成创建**
   - 点击 "创建"

### 3.2 配置虚拟机设置

右键点击创建的虚拟机 > "设置"

#### 3.2.1 系统设置
**主板** 选项卡:
```
启动顺序:
  ☑ 光驱
  ☑ 硬盘
  ☐ 软驱
  ☐ 网络

扩展特性:
  ☑ 启用 I/O APIC
  ☐ 硬件时钟使用 UTC 时间
  ☑ 启用 EFI (可选)
```

**处理器** 选项卡:
```
处理器数量: 2 (推荐)
执行上限: 100%

扩展特性:
  ☑ 启用 PAE/NX
  ☑ 启用嵌套 VT-x/AMD-V (如果需要嵌套虚拟化)
```

**加速** 选项卡:
```
准虚拟化接口: 默认
硬件虚拟化:
  ☑ 启用 VT-x/AMD-V
  ☑ 启用嵌套分页
```

#### 3.2.2 显示设置
```
显存大小: 16 MB (最小值)
监视器数量: 1
缩放因子: 100%
显卡控制器: VMSVGA

扩展特性:
  ☐ 启用 3D 加速 (不需要)
```

#### 3.2.3 存储设置
1. **IDE 控制器** > 点击空的光驱图标
   - 点击右侧光盘图标
   - 选择 "选择虚拟盘..." 
   - 选择下载的 Ubuntu Server ISO 文件

2. **验证配置**
   ```
   控制器: IDE
   └─ ubuntu-22.04.3-live-server-amd64.iso
   
   控制器: SATA
   └─ SOC-Ubuntu-Server.vdi (20GB)
   ```

#### 3.2.4 网络设置

**网卡 1** (NAT - 用于互联网访问):
```
启用网络连接: ☑
连接方式: NAT
高级设置:
  控制芯片: Intel PRO/1000 MT Desktop (82540EM)
  混杂模式: 拒绝
  接入网线: ☑
```

**网卡 2** (Host-only - 用于实验室内部通信):
```
启用网络连接: ☑
连接方式: 仅主机(Host-Only)适配器
界面名称: vboxnet0 (或创建的 Host-only 网络)
高级设置:
  控制芯片: Intel PRO/1000 MT Desktop (82540EM)
  混杂模式: 拒绝
  接入网线: ☑
```

## 4. 安装 Ubuntu Server

### 4.1 启动虚拟机
1. 选择虚拟机
2. 点击 "启动"
3. 虚拟机将从 ISO 启动

### 4.2 安装步骤

#### 4.2.1 语言选择
```
选择: English (或中文简体，如果需要)
```

#### 4.2.2 键盘布局
```
Layout: English (US)
Variant: English (US)
```

#### 4.2.3 安装类型
```
选择: Ubuntu Server (default)
```

#### 4.2.4 网络配置
```
自动配置 (DHCP):
  enp0s3 (NAT): 自动获取 IP
  enp0s8 (Host-only): 待稍后配置
  
继续不配置也可以，安装后再设置
```

#### 4.2.5 代理配置
```
Proxy address: [留空，如果不需要]
或输入: http://proxy.example.com:8080
```

#### 4.2.6 Ubuntu Archive 镜像
```
使用默认镜像或选择更快的镜像:
中国用户推荐:
  - https://mirrors.tuna.tsinghua.edu.cn/ubuntu
  - https://mirrors.aliyun.com/ubuntu
```

#### 4.2.7 存储配置
```
选择: Use an entire disk
  
磁盘: VBOX HARDDISK (20GB)
  
分区方案: 使用默认 LVM (推荐)
  或自定义分区:
    - /boot: 1GB
    - /: 15GB
    - swap: 2GB
    - /var: 剩余空间
```

#### 4.2.8 配置文件和服务器信息
```
Your name: SOC Administrator
Your server's name: soc-server
Pick a username: socadmin
Choose a password: [设置强密码]
Confirm your password: [重复密码]
```

**重要**: 记住这些凭据！

#### 4.2.9 SSH 设置
```
☑ Install OpenSSH server
```

**Import SSH identity**: 
```
选择: No (或从 GitHub/Launchpad 导入公钥)
```

#### 4.2.10 Featured Server Snaps
```
可选安装 (建议跳过，后续手动安装):
  ☐ docker
  ☐ microk8s
  ☐ ...
```

#### 4.2.11 安装进度
等待安装完成（约 5-10 分钟）

#### 4.2.12 完成安装
```
提示: Installation complete!
操作: Remove the installation medium, then reboot
```

1. 按 Enter 或点击 "Reboot Now"
2. 虚拟机会自动弹出 ISO
3. 等待系统重启

## 5. 初始配置

### 5.1 首次登录
```
soc-server login: socadmin
Password: [输入密码]
```

### 5.2 更新系统
```bash
# 更新包列表
sudo apt update

# 升级所有包
sudo apt upgrade -y

# 安装常用工具
sudo apt install -y net-tools curl wget vim git htop
```

### 5.3 配置静态 IP (Host-only 网络)

#### 5.3.1 查看网络接口
```bash
ip addr show
```

输出示例:
```
1: lo: <LOOPBACK,UP,LOWER_UP>
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> inet 10.0.2.15/24
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> inet 192.168.56.101/24
```

#### 5.3.2 编辑 Netplan 配置
```bash
sudo vim /etc/netplan/00-installer-config.yaml
```

配置内容:
```yaml
network:
  version: 2
  ethernets:
    enp0s3:  # NAT 网络 (自动获取)
      dhcp4: true
    enp0s8:  # Host-only 网络 (静态 IP)
      dhcp4: no
      addresses:
        - 192.168.56.10/24
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

#### 5.3.3 应用配置
```bash
# 测试配置
sudo netplan try

# 如果测试成功，应用配置
sudo netplan apply

# 验证 IP 地址
ip addr show enp0s8
```

### 5.4 配置防火墙

```bash
# 启用 UFW 防火墙
sudo ufw enable

# 允许 SSH (从 Host-only 网络)
sudo ufw allow from 192.168.56.0/24 to any port 22

# 查看状态
sudo ufw status verbose
```

### 5.5 配置主机名解析

```bash
# 编辑 hosts 文件
sudo vim /etc/hosts
```

添加:
```
192.168.56.10   soc-server
192.168.56.20   kali-attack
```

### 5.6 安装安全工具

```bash
# 安装基础安全工具
sudo apt install -y \
  fail2ban \
  ufw \
  aide \
  rkhunter \
  lynis

# 安装监控工具
sudo apt install -y \
  tcpdump \
  wireshark-common \
  nmap \
  netcat

# 安装日志分析工具
sudo apt install -y \
  logwatch \
  rsyslog
```

### 5.7 创建快照 (重要!)

在 VirtualBox 中创建快照以保存当前状态:
1. 关闭虚拟机: `sudo poweroff`
2. 在 VirtualBox 中右键虚拟机 > "快照" > "生成快照"
3. 名称: "Initial Configuration Complete"
4. 描述: "Ubuntu Server 基础配置完成"

## 6. 验证配置

### 6.1 检查网络连通性

```bash
# 检查互联网连接 (通过 NAT)
ping -c 4 8.8.8.8

# 检查 DNS 解析
ping -c 4 google.com

# 检查 Host-only 网络
ip addr show enp0s8 | grep inet
```

### 6.2 检查服务状态

```bash
# SSH 服务
sudo systemctl status ssh

# 防火墙状态
sudo ufw status

# 查看监听端口
sudo netstat -tulpn | grep LISTEN
```

## 7. 可选高级配置

### 7.1 启用 SSH 密钥认证

在宿主机上:
```bash
# 生成 SSH 密钥 (如果还没有)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥到 SOC 服务器
ssh-copy-id socadmin@192.168.56.10
```

在 SOC 服务器上禁用密码登录:
```bash
sudo vim /etc/ssh/sshd_config
```

修改:
```
PasswordAuthentication no
PubkeyAuthentication yes
```

重启 SSH:
```bash
sudo systemctl restart ssh
```

### 7.2 配置自动更新

```bash
# 安装 unattended-upgrades
sudo apt install -y unattended-upgrades

# 配置自动更新
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 7.3 安装 Docker (可选)

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 添加用户到 docker 组
sudo usermod -aG docker $USER

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker
```

## 8. 故障排除

### 8.1 网络问题

**问题**: Host-only 网络无法通信
```bash
# 检查网络接口状态
ip link show enp0s8

# 如果接口是 DOWN
sudo ip link set enp0s8 up

# 重新应用 netplan
sudo netplan apply
```

### 8.2 SSH 连接问题

**问题**: 无法从宿主机 SSH 到虚拟机
```bash
# 检查 SSH 服务
sudo systemctl status ssh

# 检查防火墙
sudo ufw status

# 检查监听端口
sudo netstat -tulpn | grep :22
```

### 8.3 性能问题

**问题**: 虚拟机运行缓慢
- 增加分配的 CPU 核心数
- 增加内存分配
- 在 VirtualBox 中安装 Guest Additions

```bash
# 安装 VirtualBox Guest Additions
sudo apt install -y virtualbox-guest-utils virtualbox-guest-x11
```

## 9. 下一步

SOC 服务器配置完成后:
- 继续 [Kali Linux 攻击机配置](./03-kali-setup.md)
- 配置 [网络连通性](./04-network-configuration.md)

## 10. 参考资源

- [Ubuntu Server 官方文档](https://ubuntu.com/server/docs)
- [Netplan 配置参考](https://netplan.io/reference/)
- [UFW 防火墙指南](https://help.ubuntu.com/community/UFW)
