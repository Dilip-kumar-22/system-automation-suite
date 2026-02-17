# System Automation Suite 

Startups and high-frequency trading environments require optimized workflows. This repository contains custom automation daemons tailored for Windows/Linux environments.

## Module 1: File Sentinel
An autonomous background daemon that utilizes the `watchdog` library to monitor file system events in real-time. It enforces organization protocols on the `Downloads` directory, sorting incoming data streams into designated silos (Images, Code, Archives, etc.) with duplicate handling and robust logging.

### Tech Stack
- Python 3.12
- Watchdog (Observer Pattern)
- Shutil & OS modules

### Usage
Run `file_sentinel.py` in the background to activate the monitoring agent.
