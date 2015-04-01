Developer Documentation
=======================

This covers code style, planned features, and architectural decisions for
reference

Code Style
----------

* PEP8 always

File recovery feature
---------------------

The primary function of this project,
is to allow convenient recovery of files from ZFS snapshots.

* Search for files across "live" filesystem(s) and snapshots

  - Done for live filesystem
* Browse filesystems and snapshot

  - Done for live filesystem
* Recover files from snapshots to live filesystem

.. todo::

    * `Indexing snapshots`_

Indexing snapshots
++++++++++++++++++

* WiZFS will eventually handle snapshot creation and rotation.
  A call to a view will create a snapshot, optionally recursively
  and rotate old ones.

* When a snapshot is created, we fire a task to index it.
  Likewise when one is deleted, remove it from the index.

* Indexing doesn't have to do anything fancy like hash files.

Planned Features
----------------

As the primary use case is for ZFS based storage servers
there are many other useful possibilities that could be developed later:

* Disk space usage analyser - find large files/folders
* `Duplicate Finder`_
* `System health dashboard`_
* `Backup to multiple locations`_

Duplicate Finder
----------------

A good way to free up space is to find duplicate files.
There are numerous ways to do this; hashing, filesize comparison, filename comparison etc.

I intend to do something a little unique.
My use case is remove duplicate HD video files (left over from transcoding etc)
These are likely to have different filesizes and hashes (as the content will differ).
But they should have at least similar metadata.

The plan therefore is to do the following:

* Extract metadata from files whilst indexing them
* Store the metadata in Xapian faceted
* Use facets to determine duplicates

System health dashboard
-----------------------

As ZFS storage servers tend to be tucked away
they're often forgotten about
until something breaks.

There aren't many (any?) good, simple monitoring tools "that just work" out the box

* Monitor hardware - temp, disk health etc
* Monitor pool(s) - disk space, faulted disks
* Notifications
 
Backup to multiple locations
----------------------------

Using zfs send and receive commands pools can be easily backed up whilst online.
There are other tools that do this, but as wizfs will manage snapshots it makes 
sense for it to manage backups.

Possible backup options include:
 
* Mirroring pool to local or remote pool
* Incremental backup
* A customisable history of snapshots
* Backups piped to xz/tar for compression
* Backups piped to GnuPG or OpenSSL for encryption
* Backup to a file to be stored on non-zfs filesystem

  - Cloud, DVD, Bluray, dumb hard drive, etc.
* Combinations of the above
 
Perhaps even having access to cloud providers within the app to do this automatically.
