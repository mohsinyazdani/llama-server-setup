"""
Setup Module
Core LlamaServerSetup class and orchestration logic
"""
import os
from platform_detector import detect_platform_requirements
from downloader import get_latest_release, find_matching_asset, download_with_progress
from extractor import extract_server_files
from file_creator import create_startup_script, create_test_script, create_models_directory


class LlamaServerSetup:
    def __init__(self):
        self.github_api_url = "https://api.github.com/repos/ggml-org/llama.cpp/releases/latest"
        self.temp_dir = None
        
    def print_header(self):
        import platform
        print("LLama Server Auto-Setup")
        print("=" * 50)
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Python: {platform.python_version()}")
        print("=" * 50)
        print()

    def run_setup(self):
        self.print_header()

        requirements = detect_platform_requirements()
        if not requirements:
            print("Unsupported platform")
            print("Supported: Windows x64, Linux x64/ARM64, macOS x64/ARM64")
            return False

        print(f"Platform: {requirements['description']}")
        print(f"Looking for: {requirements['pattern']}")
        print()

        release = get_latest_release(self.github_api_url)
        if not release:
            return False

        asset = find_matching_asset(release, requirements['pattern'])
        if not asset:
            return False

        if os.path.exists(requirements['local_name']):
            response = input(f"\nWarning: {requirements['local_name']} already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Setup cancelled.")
                return False

        print()

        zip_filename = f"llama-server-{release['tag_name']}.zip"
        if not download_with_progress(asset['browser_download_url'], zip_filename):
            return False

        success, self.temp_dir = extract_server_files(zip_filename, requirements)
        if not success:
            self.cleanup_temp_files(zip_filename)
            return False

        create_startup_script(requirements)
        create_test_script()
        create_models_directory()

        self.cleanup_temp_files(zip_filename)

        self.print_success_summary(requirements)
        return True

    def cleanup_temp_files(self, zip_path):
        print("Cleaning up temporary files...")
        
        try:
            if os.path.exists(zip_path):
                os.unlink(zip_path)
            
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
            
            print("Cleanup complete")
        except Exception as e:
            print(f"Warning: Cleanup warning: {e}")

    def print_success_summary(self, requirements):
        print("\n" + "=" * 20)
        print("SETUP COMPLETE!")
        print("=" * 20)
        print()
        print("What was installed:")
        print(f"   - LLama server for {requirements['description']}")
        print("   - All required libraries/DLLs")
        print(f"   - Startup script ({requirements['startup_script']})")
        print("   - API test script (test_api.py)")
        print("   - Models directory")
        print()
        print("Next Steps:")
        print("   1. Place a GGUF model in the models/ directory")
        print(f"   2. Run: {requirements['startup_script']}")
        print("   3. Test: python test_api.py")
        print("   4. Open browser: http://localhost:8080")
        print()
        print("Need models? Check models/README.md for download links")
