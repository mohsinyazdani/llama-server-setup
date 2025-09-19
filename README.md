# Llama Server Auto-Setup

A modular Python-based setup tool for automatically downloading and configuring Llama server binaries for different platforms.

## Features

- **Automatic Platform Detection**: Detects Windows, Linux, and macOS platforms
- **Binary Download**: Downloads latest Llama server releases from GitHub
- **Modular Architecture**: Clean, organized code structure with separate modules
- **Startup Scripts**: Generates platform-specific startup scripts
- **API Testing**: Includes test utilities for server API endpoints
- **Docker Support**: Ready-to-use Docker configuration
- **Cross-Platform**: Supports Windows x64, Linux x64/ARM64, macOS x64/ARM64

## Project Structure

```
├── main.py                 # Main entry point
├── setup.py               # Core setup orchestration
├── platform_detector.py   # Platform detection logic
├── downloader.py          # GitHub release downloading
├── extractor.py           # Archive extraction utilities
├── file_creator.py        # Script and file generation
├── start.bat              # Windows startup script
├── test_api.py            # API testing utilities
├── models/                # Model storage directory
├── assets/                # Static assets
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
└── README.md              # This file
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/mohsinyazdani/llama-server-setup.git
   cd llama-server-setup
   ```

2. **Run the setup**
   ```bash
   python main.py
   ```

3. **Follow the prompts** to download and configure Llama server

4. **Start the server**
   ```bash
   # Windows
   start.bat

   # Linux/macOS
   ./start.sh
   ```

## Requirements

- Python 3.6+
- Internet connection for downloading binaries
- Git (for cloning)

## Supported Platforms

- **Windows**: x64 CPU
- **Linux**: x64 and ARM64
- **macOS**: x64 (Intel) and ARM64 (Apple Silicon)

## Usage

The setup tool will:
1. Detect your platform and architecture
2. Download the appropriate Llama server binary
3. Extract required libraries and dependencies
4. Generate startup scripts
5. Create necessary directories
6. Provide testing utilities

## Docker Usage

```bash
# Build and run with Docker
docker-compose up --build
```

## API Testing

After setup, test the server:

```bash
python test_api.py
```

This will test:
- Server health endpoint
- Models API
- Text completion functionality

## Configuration

Edit the generated startup script to customize:
- Model path
- Server host/port
- Context size
- Thread count
- GPU layers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check individual component licenses for Llama and related libraries.

## Disclaimer

This tool downloads and configures Llama server binaries. Ensure compliance with applicable licenses and terms of service.
