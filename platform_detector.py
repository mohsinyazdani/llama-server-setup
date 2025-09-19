"""
Platform Detection Module
Detects platform requirements for LLama server setup
"""
import platform


def detect_platform_requirements():
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return {
            "system": system,
            "pattern": "bin-win-cpu-x64.zip",
            "server_name": "llama-server.exe",
            "local_name": "server.exe",
            "startup_script": "start.bat",
            "needs_chmod": False,
            "description": "Windows x64 CPU"
        }
    elif system == "linux":
        if "x86_64" in machine or "amd64" in machine:
            return {
                "system": system,
                "pattern": "bin-ubuntu-x64.zip",
                "server_name": "llama-server",
                "local_name": "server",
                "startup_script": "start.sh",
                "needs_chmod": True,
                "description": "Linux x64"
            }
        elif "aarch64" in machine or "arm64" in machine:
            return {
                "system": system,
                "pattern": "bin-ubuntu-arm64.zip",
                "server_name": "llama-server",
                "local_name": "server",
                "startup_script": "start.sh",
                "needs_chmod": True,
                "description": "Linux ARM64"
            }
    elif system == "darwin":
        if "arm64" in machine:
            return {
                "system": system,
                "pattern": "bin-macos-arm64.zip",
                "server_name": "llama-server",
                "local_name": "server",
                "startup_script": "start.sh",
                "needs_chmod": True,
                "description": "macOS ARM64 (Apple Silicon)"
            }
        else:
            return {
                "system": system,
                "pattern": "bin-macos-x64.zip",
                "server_name": "llama-server",
                "local_name": "server",
                "startup_script": "start.sh",
                "needs_chmod": True,
                "description": "macOS x64 (Intel)"
            }
    
    return None
