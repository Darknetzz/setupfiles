import subprocess
import os

# ─────────────────────────────────────────────────────────────────────── #
#                             check_connection                            #
# ─────────────────────────────────────────────────────────────────────── #
def check_connection(ip_address):
    try:
        subprocess.check_output(["ping", "-c", "1", ip_address])
        return True
    except subprocess.CalledProcessError:
        return False

# ─────────────────────────────────────────────────────────────────────── #
#                                is_mounted                               #
# ─────────────────────────────────────────────────────────────────────── #
def is_mounted(mount_path):
    check_cmd  = f"mount | grep {mount_path}"
    
    # Check if the share is mounted
    result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return True
    return False
    
# ─────────────────────────────────────────────────────────────────────── #
#                                mount_nfs                                #
# ─────────────────────────────────────────────────────────────────────── #
def mount_nfs(name, ip_address, volume, folder):
    mount_path = f"/{name}/{folder}"
    nfs_path   = f"{ip_address}:/{volume}/{folder}/"
    create_cmd = f"sudo mkdir -p {mount_path}"
    mount_cmd  = f"mount -t nfs {nfs_path} {mount_path}"
    
    # Check if already mounted
    if is_mounted(mount_path):
        print(f"{name} is already mounted: {mount_path}")
        return
    
    # Create the mount point if it doesn't exist
    if not os.path.exists(mount_path):
        subprocess.run(create_cmd, shell=True)
        
    # Mount the share
    subprocess.run(mount_cmd, shell=True)
    

# ─────────────────────────────────────────────────────────────────────── #
#                     Check that we can reach DARK.NET                    #
# ─────────────────────────────────────────────────────────────────────── #
if __name__ == "__main__":
    ip_address = "10.0.0.1"
    if check_connection(ip_address):
        print(f"OK: Successfully reached {ip_address}")
    else:
        exit(f"Error: Failed to reach {ip_address}")

# Mount options
mountOptions = "rw,sync,hard,_netdev"

# ─────────────────────────────────────────────────────────────────────── #
#                               Shares dict                               #
# ─────────────────────────────────────────────────────────────────────── #
shares = {
    "NAS1": {
        "ip": "10.0.1.25",
            "video": {
                "volume": "volume1",
                "folder": "video",
            },
            "music": {
                "volume": "volume1",
                "folder": "music",
            },
            "Data": {
                "volume": "volume1",
                "folder": "Data",
            },
    },
    
    "NAS2": {
        "ip": "10.0.1.30",
            "video": {
                "volume": "volume1",
                "folder": "video",
            },
            "Data": {
                "volume": "volume1",
                "folder": "Data",
            }
    },
    
    "NAS3": {
        "ip": "10.0.1.23",
            "Share": {
                "volume": "volume1",
                "folder": "Share",
            }
    }
}

# ─────────────────────────────────────────────────────────────────────── #
#                                  Mount                                  #
# ─────────────────────────────────────────────────────────────────────── #
for share_name, share_data in shares.items():
    ip_address = share_data.pop("ip")          # remove the ip address from the dictionary
    for share, details in share_data.items():  # now we're looping over the remaining items
        volume = details["volume"]
        folder = details["folder"]
        if not check_connection(ip_address):
            print(f"Failed to reach {share_name}@{ip_address}. Skipping...")
            continue
        
        print(f"Mounting {share_name} ({ip_address}) -> {folder}")
        mount_nfs(share_name, ip_address, volume, folder)