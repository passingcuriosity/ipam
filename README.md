IPAM
====

This is a utility to help maintain IP network address mappings.

Describe your IP address space (including networks with multiple,
disjoint address spaces) in plain text files and store them in a
repository managed by your favorite version control system. Then use
a CI/CD solution to run the included the Python script to validate
changes to your described configuration.

A solution like GitHub, BitBucket, or GitLab makes it easy to set up
your own repository and configure it to ensure that changes are valid.

Usage
-----

Run the script, passing one or more text files are command-line
arguments. The script will load the network map, validate it, and
print any errors.

```
$ python3 -m ipam example/*.ipam
```

File Format
-----------

The file format is simple:

- Lines begining with `#` are comments.

- Lines beginning with `host` describe a single address allocated to
  a host. It might not be worth 

- Lines beginning with `subnet` describe an address space which might
  be allocated. E.g. to a cloud VPC, or a branch office network.

- Lines begining with `network` describe an address space which must
  be broken up into `subnet`s.

- Addresses are given in CIDR notation: `1.2.0.0/16`, `1.2.3.0/24`,
  etc.

- All statements can contain arbitrary text after the address. This
  should be used to describe the status of each address space (e.g.
  whether it is allocated or free, what it is being used for, contact
  details for the managers, hostnames, etc.)

Example
-------

An organisation has a `/24` public IP allocation and uses an RFC 1918
address range for their internal network.

See the example in `example/`.

To see an example with errors, see the [Example error pull request][3].

[3]: https://github.com/passingcuriosity/ipam/pull/2
