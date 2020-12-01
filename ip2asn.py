#!/usr/bin/env python

import netaddr
import os
import requests
import gzip
import SubnetTree

library = "ip2asn-v4.tsv.gz"

class ip2asn(object):
    
    """Ip2ASN Data based on https://iptoasn.com/"""

    cache = SubnetTree.SubnetTree()
    
    
    def __init__(self,reload=False, library=library ):
        """Initialize class, optionally refetch the mapping data."""
        self.library = library
        if reload:
            self.reload()
        else:
            self._load()
            
    def _load(self):
        """Load the data into the cache. This may take some time."""
        with gzip.open( os.path.expanduser( self.library ) ) as fp:
            for line in fp:
                tmp = line.decode().strip().split("\t")
                cidrs = netaddr.iprange_to_cidrs(tmp[0],tmp[1])
                for cidr in cidrs:
                    ip2asn.cache[str(cidr)] = tmp[2:]
                    
    def reload(self):
        """Fetch latest ip2asn map and relaod the cache"""
        try:
            r = requests.get( "https://iptoasn.com/data/ip2asn-v4.tsv.gz" )
            with open( os.path.expanduser( self.library ) , "wb" ) as fp:
                fp.write( r.content )
            self._load()
        except:
            print( "Could not download new version")
            
    def lookup(self, ip):
        """Retun the ASN of the given ip"""
        try:
            return ip2asn.cache[ip]
        except:
            return None
            
            
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2 :
        print( "Usage: {} ip".format( sys.argv[0] ) )
        exit(1)
    
    i2a = ip2asn()
    print( "{}: AS{}".format( sys.argv[1], i2a.lookup( sys.argv[1] )))