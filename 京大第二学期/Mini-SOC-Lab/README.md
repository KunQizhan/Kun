# Mini-SOC Lab 实验环境搭建指南

## 项目概述

本项目旨在搭建一个迷你安全运营中心(Mini-SOC)实验环境，用于学习和实践网络安全相关技术。

## 目标

- [x] 在本机搭建虚拟化环境（VirtualBox / VMware / Proxmox 选一个）
- [x] 创建至少两台虚拟机：SOC（Ubuntu Server）、攻击机（Kali）
- [x] 配置基础网络（NAT/Host-only），保证虚拟机之间可以互相通信

## 环境要求

### 硬件要求
- CPU：支持硬件虚拟化（Intel VT-x 或 AMD-V）
- 内存：至少 8GB RAM（推荐 16GB）
- 存储：至少 60GB 可用空间
- 网络：稳定的网络连接用于下载 ISO 镜像

### 软件要求
- 虚拟化软件：VirtualBox 7.0+ / VMware Workstation / Proxmox VE
- 主机操作系统：Windows 10/11, macOS, 或 Linux

## 实验环境架构

```
┌─────────────────────────────────────────────────┐
│                   宿主机                         │
│  ┌───────────────────────────────────────────┐  │
│  │         VirtualBox/VMware/Proxmox        │  │
│  │                                           │  │
│  │  ┌──────────────┐    ┌──────────────┐   │  │
│  │  │  SOC Server  │    │  Kali Linux  │   │  │
│  │  │  (Ubuntu)    │◄───┤  (攻击机)    │   │  │
│  │  │              │    │              │   │  │
│  │  │ 192.168.56.10│    │192.168.56.20 │   │  │
│  │  └──────┬───────┘    └──────┬───────┘   │  │
│  │         │                   │            │  │
│  │         └───────┬───────────┘            │  │
│  │                 │                        │  │
│  │         Host-only Network                │  │
│  │         (192.168.56.0/24)                │  │
│  │                 │                        │  │
│  │         ┌───────┴────────┐               │  │
│  │         │   NAT Network   │               │  │
│  │         │  (Internet访问) │               │  │
│  │         └────────────────┘               │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 文档目录

1. [VirtualBox 环境搭建](./01-virtualbox-setup.md) - VirtualBox 安装与配置
2. [Ubuntu Server SOC 配置](./02-ubuntu-soc-setup.md) - SOC 服务器虚拟机设置
3. [Kali Linux 攻击机配置](./03-kali-setup.md) - Kali 攻击机虚拟机设置
4. [网络配置指南](./04-network-configuration.md) - 网络拓扑与连通性配置
5. [验证与测试](./05-verification.md) - 环境验证与互通性测试

## 快速开始

### 方案一：VirtualBox（推荐初学者）

1. 下载并安装 [VirtualBox](https://www.virtualbox.org/)
2. 下载操作系统镜像：
   - [Ubuntu Server 22.04 LTS](https://ubuntu.com/download/server)
   - [Kali Linux](https://www.kali.org/get-kali/)
3. 按照文档顺序配置虚拟机
4. 测试网络连通性

### 方案二：VMware Workstation

1. 下载并安装 VMware Workstation Player/Pro
2. 下载相同的操作系统镜像
3. 参考配置文档进行调整
4. 测试网络连通性

### 方案三：Proxmox VE（适合高级用户）

1. 在独立机器上安装 Proxmox VE
2. 通过 Web 界面创建虚拟机
3. 配置虚拟网络
4. 测试连通性

## 完成时间

每个任务三天内完成

## 预期成果

完成本实验后，你将拥有：

- ✅ 一个功能完整的虚拟化实验环境
- ✅ 可以相互通信的 SOC 服务器和攻击机
- ✅ 基础的网络安全实验平台
- ✅ 进行渗透测试和安全分析的能力

## 后续扩展

- 添加更多虚拟机（如靶机、日志服务器等）
- 部署安全工具（Snort, Suricata, ELK Stack 等）
- 配置更复杂的网络拓扑
- 实施安全监控和日志分析

## 参考资源

- [VirtualBox 官方文档](https://www.virtualbox.org/wiki/Documentation)
- [Ubuntu Server 文档](https://ubuntu.com/server/docs)
- [Kali Linux 文档](https://www.kali.org/docs/)
- [网络安全实验室搭建最佳实践](https://www.cybersecurity-excellence.com/)

## 许可证

本文档仅用于学习和教育目的。
