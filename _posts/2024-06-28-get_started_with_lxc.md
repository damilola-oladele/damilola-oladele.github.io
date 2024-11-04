---
title: "Get started with LXC: Explained with installation guide"
description: Linux containers (LXC) have revolutionized the way applications are packaged and deployed across different environments, offering lightweight virtualization and efficient resource utilization.
date: 2024-06-28 00:00:00 +0100
categories: [Software Engineering, Linux]
tags: [lxc, lxd, ubuntu]
pin: false
image: false
published: true
---

Containers have been around for a while, but their recent broad adoption has transformed modern application development and deployment.

You can see containers as separate environments used for running different applications or software systems on a single computer while keeping them isolated from one another. Containers are different from virtual machines because they share the same operating system kernel as the host machine they operate on. This makes containers more lightweight and efficient. Each container has a separate view of the operating system, its processes, network, and storage. So applications running in different containers don't interfere with each other. 

There are two broad categories of containers—Linux containers (LXC) and Windows containers. While LXC run on the Linux kernel, Windows containers run on the Windows operating system.

This article explains LXC, its installation on Ubuntu, the creation of privileged and unprivileged LXC containers, and management using LXC commands. Also, we'll compare LXC with LXD (Linux Daemon), a similar container solution.

## What is LXC?

> _LXC was initially developed by [IBM](https://en.wikipedia.org/wiki/IBM). It's a tool used for operating-system virtualization. LXC is used to run multiple isolated Linux systems (containers) on a control host using a single Linux kernel. [Source: [Wikipedia](https://en.wikipedia.org/wiki/LXC)]_

Each LXC container has its files, processes, network interfaces, and other resources isolated from the other containers and the host system. LXC uses Linux [namespaces](https://en.wikipedia.org/wiki/Linux_namespaces), a kernel feature that allows the partitioning of global system resources into isolated instances. LXC also uses [cgroups](https://en.wikipedia.org/wiki/Cgroups), another Linux kernel feature, to limit, measure, and control resource usage for processes.

By combining resource isolation through `namespaces` and resource control through `cgroups`, LXC provides a secure and efficient way to run multiple isolated Linux environments on a single host system.

## How to Install LXC

Most Linux distributions offer recent versions of LXC either directly in their package repositories or through backport channels. For your first LXC experience, it is advisable to use a recent supported release for a smoother experience. If you're using Ubuntu, **Ubuntu 18.04 LTS** is the recommended choice as a container host.

Now let's go through the steps of installing LXC on Ubuntu, one of the most popular Linux distributions.

First, update your package lists by running the following command:

```sh
sudo apt update
```

Then install LXC and its dependencies by running the command:

```sh
sudo apt install lxc
```

After running the preceding command, your system will have all the LXC commands available, all its templates as well as the python3 binding should you want to script LXC.

_On some Linux distributions, installing LXC may not automatically install all its dependencies and templates. So, you have to download the LXC dependencies and templates after installing the LXC package._

Once the installation is complete, you can verify that LXC is correctly installed by running:

```sh
lxc-checkconfig
```

You should get an output similar to this in your terminal:

```
LXC version 5.0.0
Kernel configuration not found at /proc/config.gz; searching...
Kernel configuration found at /boot/config-6.5.0-28-generic
--- Namespaces ---
Namespaces: enabled
Utsname namespace: enabled
Ipc namespace: enabled
Pid namespace: enabled
User namespace: enabled
Network namespace: enabled

--- Control groups ---
Cgroups: enabled
Cgroup namespace: enabled

Cgroup v1 mount points: 


Cgroup v2 mount points: 
/sys/fs/cgroup

Cgroup v1 systemd controller: missing
Cgroup v1 freezer controller: missing
Cgroup ns_cgroup: required
Cgroup device: enabled
Cgroup sched: enabled
Cgroup cpu account: enabled
Cgroup memory controller: enabled
Cgroup cpuset: enabled

--- Misc ---
Veth pair device: enabled, not loaded
Macvlan: enabled, not loaded
Vlan: enabled, not loaded
Bridges: enabled, loaded
Advanced netfilter: enabled, loaded
CONFIG_IP_NF_TARGET_MASQUERADE: enabled, not loaded
CONFIG_IP6_NF_TARGET_MASQUERADE: enabled, not loaded
CONFIG_NETFILTER_XT_TARGET_CHECKSUM: enabled, not loaded
CONFIG_NETFILTER_XT_MATCH_COMMENT: enabled, not loaded
FUSE (for use with lxcfs): enabled, not loaded

--- Checkpoint/Restore ---
checkpoint restore: enabled
CONFIG_FHANDLE: enabled
CONFIG_EVENTFD: enabled
CONFIG_EPOLL: enabled
CONFIG_UNIX_DIAG: enabled
CONFIG_INET_DIAG: enabled
CONFIG_PACKET_DIAG: enabled
CONFIG_NETLINK_DIAG: enabled
File capabilities: 

Note : Before booting a new kernel, you can check its configuration
usage : CONFIG=/path/to/config /usr/bin/lxc-checkconfig
```

## Privileged and Unprivileged LXC Containers

There are two methods of using LXC—privileged and unprivileged. These methods determine the level of access and permissions granted to the container processes, affecting their isolation, security, and functionality.

### How to Create Privileged LXC Containers 

Privileged containers are containers created by root and run with root privileges on the host system. This grants them unrestricted access to system resources and the ability to perform operations reserved for the root user. This mode offers greater flexibility and control over system configurations, making it suitable for applications that require direct access to hardware resources or kernel modifications. However, privileged containers pose security risks. Due to their elevated privileges, any actions performed within a privileged container can affect the stability and security of the host system.

To create a privileged LXC container interactively, run the following command:

```sh
sudo lxc-create --template download --name privileged-container
```

The preceding command will interactively ask for the container root filesystem type to download, including the distribution, release, and architecture. The download template shows you a list of available container images and their details.

```Note
You can replace the name, `privileged-container` with any container name that will be memorable for you.
```

If you want to create a container non-interactively, specify the values of the root filesystem type, the distribution, release, and architecture in your command. For example, if you want to create a container, named `privileged-container`, using the Ubuntu Linux distribution version 20.04 (Focal Fossa) on the AMD64 architecture, run the command:

```sh
sudo lxc-create --template download --name privileged-container -- --dist ubuntu --release focal --arch amd64
```

See [Linux Containers - Image server](https://images.linuxcontainers.org/) for the list of available container images and their details.

To start your `privileged-container` container, run the command:

```sh
sudo lxc-start --name privileged-container
```

After running the preceding command, use the following command to check if your container is now running:

```sh
sudo lxc-info --name privileged-container
```

Running the preceding command should give you an output similar to this:

```
Name:           privileged-container
State:          RUNNING
PID:            7615
IP:             10.0.3.190
Link:           veth4LHNrz
 TX bytes:      1.57 KiB
 RX bytes:      4.16 KiB
 Total bytes:   5.74 KiB
```

You can follow the preceding steps to create as many privileged containers as you want. For a detailed list of all LXC (Linux Containers) on your system in a more readable format, run:

```sh
sudo lxc-ls --fancy
```

To remove a container, you have to first stop it using the `lxc-stop` command like this:

```sh
sudo lxc-stop privileged-container
```

Then remove the container and it's configuration files using the `lxc-destroy` command:

```sh
sudo lxc-destroy privileged-container
```

See [LXC / Manpages](https://linuxcontainers.org/lxc/manpages/) for the complete list of LXC commands and their usage.

### How to Create Unprivileged LXC Containers

Unprivileged LXC containers have limited access and enhanced isolation compared to privileged LXC containers. They are launched without root privileges using features like user namespaces and resource limitations. This improves security and minimizes the risk of breaching the host system.

To create an unprivileged LXC container, you need to start by creating a default container configuration file. This file should specify your preferred ID mappings and network setup. Also, you will need to configure the host to allow the unprivileged user to connect to the host network.

Now, let's go through the steps of creating unprivileged LXC Containers.

First, run the following commands to check if your user has user and group id ranges:

```sh
grep $USER /etc/subuid
grep $USER /etc/subgid
```

If your user has no ranges assigned, add them with the following command:

```sh
sudo usermod -v 100000-200000 -w 100000-200000 user1
```

Now create an LXC config directory and default config file by running:

```sh
mkdir -p ~/.config/lxc
echo "lxc.idmap = u 0 100000 65536" > ~/.config/lxc/default.conf
echo "lxc.idmap = g 0 100000 65536" >> ~/.config/lxc/default.conf
echo "lxc.net.0.type = veth" >> ~/.config/lxc/default.conf
echo "lxc.net.0.link = lxcbr0" >> ~/.config/lxc/default.conf
echo "$USER veth lxcbr0 2" | sudo tee -a /etc/lxc/lxc-usernet
```

> The preceding command assumes that your user and group id ranges are `100000 65536`. Ensure you replace the values with the values you got from running `grep $USER /etc/subuid` and `grep $USER /etc/subgid`.
{: .prompt-tip }

Now create an unprivileged container named `unprivileged-container`, using the Ubuntu Linux distribution version 20.04 (Focal Fossa) on the AMD64 architecture by running the command:

```sh
lxc-create -t download -n unprivileged-container -- --dist ubuntu --release focal --arch amd64
```

Once you have created your unprivileged container, check if your working directory has execute permission by running the command:

```sh
ls -ld /<current working directory>
```

If your working directory has the execute permission, you will get an output similar to this:

```sh
drwxr-x--x 21 <username> 4096 May 13 12:34 /<working directory>
```

If it doesn't, you can grant it the execute permission by running the command:

```sh
chmod +x /<current working directory>
```

Now, start the container by running the following command:

```sh
lxc-start -n unprivileged-container
```

## LXC vs LXD

Both LXC (Linux Containers) and LXD (Linux Daemon) are tools used for virtualization and container management on Linux systems. While LXC provides the core functionality for creating and running containers, LXD is an extension that improves LXC with additional features and capabilities. To get started with LXD, see [First steps with LXD](https://documentation.ubuntu.com/lxd/en/latest/tutorial/first_steps/).

The following table shows the differences between LXC and LXD:

| LXC | LXD |
| --- | --- |
| Tool for virtualization of operating systems | Extension of LXC with advanced features |
| Requires multiple processes for containers | Provides a single process for managing multiple containers. |
| Limited built-in security features | Host-level security features to enhance container security |
| Lacks support for snapshots, live migration, and storage pooling | Supports snapshots, live migration, and storage pooling |
| Basic security and integration capabilities | Offers a wide range of security features |
| Limited scalability capabilities | Enables scalability within LXC |
| Less user-friendly and requires expertise | LXD is more user-friendly |
| No data retrieval feature after processing | Provides data retrieval feature |
| Uses C API | Uses REST API |

## Conclusion

LXC have revolutionized the way applications are packaged and deployed across different environments, offering lightweight virtualization and efficient resource utilization.

While LXC pioneered operating system-level virtualization on Linux, providing the core functionality for creating and managing containers, LXD has emerged as a powerful extension that enhances the container management experience. By introducing a single system daemon for managing multiple containers, host-level security features, live migration support, snapshots, and storage pooling capabilities, LXD addresses many of the shortcomings of LXC.

As the adoption of containerization continues to grow, container solutions like LXD that streamline and simplify container management will become increasingly valuable.

## References and Further Reading

1. [https://en.wikipedia.org/wiki/LXC](https://en.wikipedia.org/wiki/LXC)
2. [https://linuxcontainers.org/lxc/getting-started/](https://linuxcontainers.org/lxc/getting-started/)
3. [https://ubuntu.com/server/docs/lxc-containers](https://ubuntu.com/server/docs/lxc-containers)
4. [https://askubuntu.com/questions/293275/what-is-lxc-and-how-to-get-started](https://askubuntu.com/questions/293275/what-is-lxc-and-how-to-get-started)
5. [https://documentation.ubuntu.com/lxd/en/latest/explanation/lxd_lxc/](https://documentation.ubuntu.com/lxd/en/latest/explanation/lxd_lxc/)