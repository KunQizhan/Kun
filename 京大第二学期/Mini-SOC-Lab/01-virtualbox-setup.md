# VirtualBox 环境搭建指南

## 1. VirtualBox 简介

VirtualBox 是 Oracle 提供的免费开源虚拟化软件，支持 Windows、macOS 和 Linux 平台，非常适合初学者搭建实验环境。

## 2. 系统要求

### 2.1 硬件要求
- **CPU**: 64位处理器，支持硬件虚拟化
  - Intel: VT-x
  - AMD: AMD-V
- **内存**: 至少 8GB（推荐 16GB）
  - SOC虚拟机: 2-4GB
  - Kali虚拟机: 2-4GB
  - 宿主机预留: 4-8GB
- **硬盘**: 至少 60GB 可用空间
  - Ubuntu Server: 20-25GB
  - Kali Linux: 25-30GB
  - 预留空间: 10-15GB

### 2.2 软件要求
- **操作系统**: 
  - Windows 10/11 (64位)
  - macOS 10.13+ 
  - Linux (kernel 2.6.13+)
- **VirtualBox**: 7.0 或更高版本

## 3. 下载 VirtualBox

### 3.1 官方下载
访问 [VirtualBox 官网](https://www.virtualbox.org/wiki/Downloads)

根据你的操作系统选择对应的安装包：
- Windows hosts
- macOS hosts (Intel / Apple Silicon)
- Linux distributions

### 3.2 Extension Pack（可选但推荐）
下载 **VirtualBox Extension Pack** 以获得以下功能：
- USB 2.0/3.0 设备支持
- VirtualBox RDP (远程桌面协议)
- 磁盘加密
- NVMe 和 PXE 引导支持

## 4. 安装 VirtualBox

### 4.1 Windows 安装步骤

1. **运行安装程序**
   ```
   双击下载的 VirtualBox-x.x.x-xxxxxx-Win.exe
   ```

2. **安装向导**
   - 点击 "Next"
   - 选择安装位置（默认即可）
   - 选择功能组件（全选推荐）
   - 警告：网络接口会短暂断开，点击 "Yes"
   - 点击 "Install" 开始安装

3. **完成安装**
   - 勾选 "Start Oracle VM VirtualBox after installation"
   - 点击 "Finish"

### 4.2 macOS 安装步骤

1. **打开 DMG 文件**
   ```
   双击下载的 VirtualBox-x.x.x-xxxxxx-OSX.dmg
   ```

2. **安装**
   - 双击 VirtualBox.pkg
   - 按照提示完成安装
   - 可能需要在 "系统偏好设置" > "安全性与隐私" 中允许

3. **配置权限**
   - 授予 VirtualBox 完全磁盘访问权限
   - 系统偏好设置 > 安全性与隐私 > 隐私 > 完全磁盘访问权限

### 4.3 Linux 安装步骤（Ubuntu/Debian）

```bash
# 更新包列表
sudo apt update

# 安装依赖
sudo apt install -y wget software-properties-common

# 添加 VirtualBox 仓库
wget -O- https://www.virtualbox.org/download/oracle_vbox_2016.asc | sudo gpg --dearmor --yes --output /usr/share/keyrings/oracle-virtualbox-2016.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-2016.gpg] https://download.virtualbox.org/virtualbox/debian $(lsb_release -cs) contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list

# 安装 VirtualBox
sudo apt update
sudo apt install -y virtualbox-7.0

# 添加用户到 vboxusers 组
sudo usermod -aG vboxusers $USER
```

## 5. 安装 Extension Pack

### 5.1 下载 Extension Pack
从 [VirtualBox 下载页面](https://www.virtualbox.org/wiki/Downloads) 下载 Extension Pack

### 5.2 安装步骤

**方法一：通过 VirtualBox Manager**
1. 打开 VirtualBox
2. 点击 "文件" > "工具" > "扩展包管理器"
3. 点击 "安装" 按钮
4. 选择下载的 Extension Pack 文件
5. 阅读许可协议并接受
6. 输入管理员密码（如需要）

**方法二：双击安装**
1. 确保 VirtualBox 已运行
2. 双击下载的 .vbox-extpack 文件
3. 点击 "安装"
4. 接受许可协议

## 6. 启用硬件虚拟化

### 6.1 检查是否启用

**Windows:**
```powershell
# 使用 PowerShell
systeminfo | findstr /C:"Virtualization"
```

**Linux:**
```bash
# 检查 CPU 虚拟化支持
egrep -c '(vmx|svm)' /proc/cpuinfo
# 输出大于 0 表示支持
```

**macOS:**
```bash
sysctl -a | grep machdep.cpu.features | grep VMX
```

### 6.2 在 BIOS/UEFI 中启用

如果虚拟化未启用，需要在 BIOS 中开启：

1. **重启电脑进入 BIOS/UEFI**
   - 常见按键：F2, F10, F12, Del, Esc
   - 具体按键取决于主板品牌

2. **找到虚拟化选项**
   - Intel: "Intel Virtualization Technology" 或 "VT-x"
   - AMD: "AMD-V" 或 "SVM Mode"
   - 通常在 "Advanced" > "CPU Configuration" 中

3. **启用并保存**
   - 将选项设为 "Enabled"
   - 保存并退出（F10）

## 7. 配置 VirtualBox 全局设置

### 7.1 默认虚拟机位置
1. 打开 VirtualBox
2. "文件" > "偏好设置" > "常规"
3. 设置 "默认虚拟电脑位置"（选择有足够空间的磁盘）

### 7.2 网络设置
1. "文件" > "偏好设置" > "网络"
2. 查看 "仅主机(Host-only)网络" 选项卡
3. 如果没有网络，点击添加 (绿色+图标)
4. 记录网络名称（如 vboxnet0）

**配置 Host-only 网络:**
- 点击编辑图标
- **适配器** 选项卡:
  - IPv4 地址: 192.168.56.1
  - IPv4 网络掩码: 255.255.255.0
  - IPv6: 可选
- **DHCP 服务器** 选项卡:
  - 启用服务器: ☑
  - 服务器地址: 192.168.56.100
  - 服务器掩码: 255.255.255.0
  - 地址下限: 192.168.56.101
  - 地址上限: 192.168.56.254

### 7.3 输入设置（可选）
1. "文件" > "偏好设置" > "输入"
2. 取消勾选 "自动捕获键盘"（避免意外锁定）
3. 设置虚拟机热键（建议使用右 Ctrl）

## 8. 验证安装

### 8.1 检查版本
打开 VirtualBox，点击 "帮助" > "关于 VirtualBox"
确认版本为 7.0 或更高

### 8.2 检查 Extension Pack
"文件" > "工具" > "扩展包管理器"
确认 Extension Pack 已安装

### 8.3 检查网络
"文件" > "偏好设置" > "网络"
确认至少有一个 Host-only 网络适配器

## 9. 常见问题

### 9.1 VT-x/AMD-V 未启用
**错误信息**: "VT-x is not available"

**解决方法**:
1. 在 BIOS 中启用虚拟化
2. 禁用 Hyper-V (Windows):
   ```powershell
   # 以管理员身份运行
   bcdedit /set hypervisorlaunchtype off
   # 重启电脑
   ```

### 9.2 网络适配器创建失败
**解决方法**:
- 以管理员身份运行 VirtualBox
- 检查防火墙设置
- 重新安装 VirtualBox 网络驱动

### 9.3 安装 Extension Pack 失败
**解决方法**:
- 确保 Extension Pack 版本与 VirtualBox 版本匹配
- 以管理员/root 权限运行
- 卸载旧版本后重新安装

### 9.4 虚拟机无法启动
**可能原因**:
- 内存分配过高
- 虚拟化未启用
- 磁盘空间不足

**解决方法**:
- 降低虚拟机内存分配
- 确保虚拟化已启用
- 清理磁盘空间

## 10. 下一步

VirtualBox 安装完成后，继续：
- [Ubuntu Server SOC 配置](./02-ubuntu-soc-setup.md)
- [Kali Linux 攻击机配置](./03-kali-setup.md)

## 11. 参考资源

- [VirtualBox 用户手册](https://www.virtualbox.org/manual/UserManual.html)
- [VirtualBox 论坛](https://forums.virtualbox.org/)
- [VirtualBox 网络配置指南](https://www.virtualbox.org/manual/ch06.html)
