/etc/fstab should look as follows:

#proc            /proc               proc    defaults                    0   0
#/dev/mmcblk0p1  /boot               vfat    ro,noatime                  0   2
#/dev/mmcblk0p2  /                   ext4    defaults,noatime            0   1
# none            /var/run            tmpfs   size=1M,noatime             0   0
none            /var/log            tmpfs   size=1M,noatime             0   0
