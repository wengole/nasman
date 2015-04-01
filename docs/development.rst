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

We're only interested in the "history" of files in the ZFS filesystem.
As snapshots appear as an entire representation of the filesystem at a point in time,
we need to make sure we don't index files that are the same live filesystem.

To do this we determine the uniqueness of a file:

 * Filename + size + moditified time? Quite reliable and fast. Hash for good measure?
 * MD5 hash of file?

Planned Features
----------------

As the primary use case is for ZFS based storage servers
there are many other useful possibilities that could be developed later:

 * Disk space usage analyser - find large files/folders
 * `Duplicate Finder`_
 * `System health dashboard`_

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
