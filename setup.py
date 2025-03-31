import os
import sys
import subprocess
import platform
import importlib
from logger import logger

def check_package_installed(package_name, required_version):
    try:
        module = importlib.import_module(package_name.replace('-', '_'))
        if hasattr(module, '__version__'):
            installed = module.__version__ == required_version
            logger.info(f"Package {package_name} version check: {'✓' if installed else 'x'}")
            return installed
        return False
    except ImportError:
        logger.info(f"Package {package_name} not found")
        return False

def check_requirements():
    required_packages = {
        'python-telegram-bot': '20.8',
        'qrcode': '7.4.2',
        'pillow': '11.0.0',
        'python-dotenv': '1.0.1'
    }
    
    missing_packages = {}
    for package, version in required_packages.items():
        if not check_package_installed(package, version):
            missing_packages[package] = version
    
    return missing_packages

def create_venv():
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", ".venv"])

def install_requirements(missing_packages):
    logger.info("Installing missing requirements...")
    pip_cmd = os.path.join(".venv", "Scripts", "pip")  # Corrected path separator

    try:
        # Install wheel first
        logger.info("Installing wheel package...")
        subprocess.run([pip_cmd, "install", "wheel"], check=True)
        
        # Install each missing package
        for package, version in missing_packages.items():
            logger.info(f"Installing {package} version {version}...")
            subprocess.run([pip_cmd, "install", f"{package}=={version}"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing package: {str(e)}")
        raise

def main():
    try:
        logger.info("Starting setup process...")
        
        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        logger.info(f"Python version: {python_version}")
        
        if sys.version_info < (3, 8):
            logger.error("Python version 3.8 or higher is required")
            sys.exit(1)

        # Setup process
        venv_exists = os.path.exists(".venv")
        if not venv_exists:
            logger.info("Creating new virtual environment...")
            create_venv()
        else:
            logger.info("Virtual environment already exists")

        # Check and install requirements
        missing_packages = check_requirements()
        if missing_packages:
            logger.info("Installing missing packages...")
            install_requirements(missing_packages)
        else:
            logger.info("All requirements are satisfied")

        logger.info("Setup completed successfully!")
        
        # Start the bot
        logger.info("Starting the bot...")
        if platform.system() == "Windows":
            subprocess.run(["python", "bot.py"])
        else:
            subprocess.run(["python3", "bot.py"])

    except Exception as e:
        logger.error(f"Setup failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()