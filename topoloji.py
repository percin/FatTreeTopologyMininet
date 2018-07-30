#!/usr/bin/env python

from mininet.topo import Topo





class FatTreeTopo(Topo):

    
    cekirdek_seviyesi = 0
    yayilma_seviyesi = 1
    kenar_seviyesi = 2
    host_seviyesi = 3

    class FatTreeNodeID(object):
        

        def __init__(self, grup = 0, sw = 0, host = 0, dpid = None, isim = None):
            
            if isim:
                grup, sw, host = [int(s) for s in isim.split('_')]
                self.grup = grup
                self.sw = sw
                self.host = host
                self.dpid = (grup << 16) + (sw << 8) + host
            else:
                self.grup = grup
                self.sw = sw
                self.host = host
                self.dpid = (grup << 16) + (sw << 8) + host
        
		
	

        

        def isim_str(self):
            
            return "%i_%i_%i" % (self.grup, self.sw, self.host)

        
    
    def a(self, layer, isim = None):
        
        d = {}
        if isim:
            id = self.id_gen(isim = isim)
            
            d.update({'dpid': "%016x" % id.dpid})
        return d


    def __init__(self, k = 4):
        
        
		
		
        super(FatTreeTopo, self).__init__()
		
        

      

        self.k = k
        self.id_gen = FatTreeTopo.FatTreeNodeID
        self.numgrups = k
        self.aggPergrup = k / 2

        grups = range(0, k)
        cekirdek_sws = range(1, k / 2 + 1)
        yayilma_sws = range(k / 2, k)
        kenar_sws = range(0, k / 2)
        hosts = range(2, k / 2 + 2)

        for p in grups:
            for e in kenar_sws:
                kenar_id = self.id_gen(p, e, 1).isim_str()
                kenar_opts = self.a(self.kenar_seviyesi, kenar_id)
                self.addSwitch(kenar_id, **kenar_opts)

                for h in hosts:
                    host_id = self.id_gen(p, e, h).isim_str()
                    host_opts = self.a(self.host_seviyesi, host_id)
                    self.addHost(host_id, **host_opts)
                    self.addLink(host_id, kenar_id)

                for a in yayilma_sws:
                    yayilma_id = self.id_gen(p, a, 1).isim_str()
                    yayilma_opts = self.a(self.yayilma_seviyesi, yayilma_id)
                    self.addSwitch(yayilma_id, **yayilma_opts)
                    self.addLink(kenar_id, yayilma_id)

            for a in yayilma_sws:
                yayilma_id = self.id_gen(p, a, 1).isim_str()
                c_index = a - k / 2 + 1
                for c in cekirdek_sws:
                    cekirdek_id = self.id_gen(k, c_index, c).isim_str()
                    cekirdek_opts = self.a(self.cekirdek_seviyesi, cekirdek_id)
                    self.addSwitch(cekirdek_id, **cekirdek_opts)
                    self.addLink(cekirdek_id, yayilma_id)


    

    
		
		
		
topos = { 'ft': FatTreeTopo}