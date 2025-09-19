"""
Extraction Module
Handles extraction of server files from downloaded archives
"""
import tempfile
import shutil
import zipfile
import os


def extract_server_files(zip_path, requirements):
    print("Extracting server files...")
    
    try:
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
            server_found = False
            dll_count = 0
            
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    if (file.lower() == requirements["server_name"].lower() or 
                        file.lower() == "llama-server.exe" or
                        file.lower() == "llama-server"):
                        
                        shutil.copy2(file_path, requirements["local_name"])
                        print(f"Copied server: {file} -> {requirements['local_name']}")
                        server_found = True

                        if requirements["needs_chmod"]:
                            os.chmod(requirements["local_name"], 0o755)
                            print("Made server executable")
                    
                    elif (file.endswith('.dll') or 
                          file.endswith('.so') or 
                          file.endswith('.dylib')):
                        
                        shutil.copy2(file_path, file)
                        dll_count += 1
                        print(f"Copied library: {file}")
            
            if not server_found:
                print("Server executable not found in archive")
                print("Archive contents:")
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        print(f"   - {file}")
                return False, temp_dir

            print(f"Extracted server + {dll_count} libraries")
            return True, temp_dir

    except Exception as e:
        print(f"Extraction failed: {e}")
        return False, None
