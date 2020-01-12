from bookworm.helper import provision_database
import os

if __name__ == "__main__":
    y = os.environ['APP_CONFIG_FILE']
    print(y)
    provision_database()
