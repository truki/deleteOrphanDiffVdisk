deleteOrphanDiffVdisk.py
===

Context
---
XenServer version 6.1 (build number 59235p)XenDesktop 5.6.0.35

XenDesktop can create two types of desktops, "Pooled desktops" and "Dedicated Desktops", the main difference between them is whats happen to the Difference vDisk when a user log out.
In a dedicated desktop the differencing disk is retained after a user log out, while in a pooled desktop the differencing disk is deleted.
Sometime (perhaps a bug in XenDesktop, i don't find any information about it), differencing disks in pooled desktop are not released, and we have to release them manually.

We have to locate them in XenServer and delete manually, but previously we have to identified which differentials disk are in used (THIS CAN NOT BE DELETED!!!)

This script, parse the return of XenApi request, thus is very important to know, because it has been tested with XenServer (build number 59235p), XenDesktop 5.6.0.3.5. Any changes on this technologies must be tested again with carefully.

## Software versions




Installation
---

Put this script in some folder inside XenServer Operating System, and scheduled in using cron as you want.

Example:
```
# delete orphan diff at 08:30
30 8 * * * root /root/deleteOrphanDiffVdisk.py

# delete orphan diff at 15:30
30 15 * * * root /root/deleteOrphanDiffVdisk.py
```

Only install in one server of every XenServer's Pool, don't install it on everyone.
